"""
Shared evidence-manifest builder, matching the schema defined in
docs/CONTINUOUS_EVIDENCE_ARCHITECTURE.md. Every control's check script
(check_policy_freshness.py and whatever comes next) imports this instead
of hand-rolling its own JSON/signing logic, so every manifest in
evidence/ is structurally identical no matter which control produced it.

Signing note: production signing is keyless Cosign via GitHub Actions
OIDC (no private key to manage or leak). There is no CI running this yet,
so this module signs locally with a throwaway key pair
(scripts/evidence/.keys/local-dev.key, gitignored) and stamps
`signing_mode: "local-key-dev"` on every manifest so it's never confused
with a real keyless-signed artifact. Swap `sign_manifest()` for a
keyless `cosign sign-blob` call (no --key) once this runs in real CI.
"""

from __future__ import annotations

import json
import hashlib
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from control_catalog import evidence_prefix  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = REPO_ROOT / "evidence"
LOCAL_KEY = Path(__file__).resolve().parent / ".keys" / "local-dev.key"
LOCAL_PUB = Path(__file__).resolve().parent / ".keys" / "local-dev.pub"


def _git_sha() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=REPO_ROOT, text=True
        ).strip()
    except Exception:
        return "uncommitted"


def _run_id() -> str:
    return os.environ.get("GITHUB_RUN_ID", f"local-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}")


def _trigger() -> str:
    if os.environ.get("GITHUB_EVENT_NAME") == "schedule":
        return "scheduled"
    if os.environ.get("GITHUB_ACTIONS"):
        return "event"
    return "manual"


def _previous_manifest(control_id: str) -> str | None:
    control_dir = EVIDENCE_DIR / evidence_prefix(control_id)
    if not control_dir.exists():
        return None
    existing = sorted(p for p in control_dir.glob("*_evidence-record.json"))
    if not existing:
        return None
    return str(existing[-1].relative_to(REPO_ROOT))


def build_manifest(
    control_id: str,
    check_name: str,
    result: str,
    evaluated_state_ref: str,
    freshness_sla_hours: int,
    details: dict | None = None,
) -> dict:
    assert result in ("PASS", "WARN", "FAIL"), "result must be PASS, WARN, or FAIL"
    return {
        "control_id": control_id,
        "framework": "ISO27001:2022-AnnexA",
        "check_name": check_name,
        "evaluated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "result": result,
        "evaluated_state_ref": evaluated_state_ref,
        "policy_ref": f"scripts/evidence/{check_name}.py@{_git_sha()}",
        "trigger": _trigger(),
        "run_id": _run_id(),
        "freshness_sla_hours": freshness_sla_hours,
        "previous_manifest": _previous_manifest(control_id),
        "signing_mode": "local-key-dev",
        "details": details or {},
    }


def write_manifest(manifest: dict) -> Path:
    """
    Writes three plainly-named files into
    evidence/controls/<section>/<control_id>-<slug>/, e.g.:
        evidence/controls/governance/5.1-policies-for-information-security/
            2026-09-12T12-06-47Z_evidence-record.json
            2026-09-12T12-06-47Z_fingerprint.sha256
            2026-09-12T12-06-47Z_signature.bundle.json
    matching the S3 key prefix this drops into once a real vault exists.
    Naming is deliberately spelled out (not just a bare timestamp or a
    cryptic extension) so a non-technical auditor opening this folder can
    tell what each file is without asking; see evidence/README.md.
    """
    control_dir = EVIDENCE_DIR / evidence_prefix(manifest["control_id"])
    control_dir.mkdir(parents=True, exist_ok=True)

    ts = manifest["evaluated_at"].replace(":", "-")
    manifest_path = control_dir / f"{ts}_evidence-record.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    digest = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    (control_dir / f"{ts}_fingerprint.sha256").write_text(digest + "\n", encoding="utf-8")

    sig_path = control_dir / f"{ts}_signature.bundle.json"
    _sign(manifest_path, sig_path)

    return manifest_path


def _sign(manifest_path: Path, sig_path: Path) -> None:
    if not LOCAL_KEY.exists():
        print(
            f"warning: no local signing key at {LOCAL_KEY}; manifest written unsigned",
            file=sys.stderr,
        )
        return

    env = dict(os.environ)
    env.setdefault("COSIGN_PASSWORD", "")
    subprocess.run(
        [
            "cosign",
            "sign-blob",
            "--key",
            str(LOCAL_KEY),
            "--yes",
            "--bundle",
            str(sig_path),
            str(manifest_path),
        ],
        check=True,
        env=env,
        capture_output=True,
    )
