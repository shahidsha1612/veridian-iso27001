#!/usr/bin/env python3
"""
Control: 5.3 (Segregation of duties).

Two things get checked, both automatable without needing this
control's Terraform to actually be applied (there's no AWS account for
the workload yet -- see terraform/iam-segregation-of-duties/):

1. The Rego policy (policies/segregation_of_duties.rego) still passes,
   both its own unit test suite and a live evaluation against a JSON
   snapshot of the IAM roles that Terraform module defines. The
   snapshot is hand-mirrored from main.tf today; the moment this gets
   applied for real, swap `_iam_role_snapshot()` for `terraform show
   -json` parsing of the actual plan/state, so this checks live
   infrastructure instead of declared intent.
2. GitHub branch protection on `master` -- which IS live right now --
   actually requires an approving review, actually enforces that for
   admins too (no bypass), and actually requires this control's CI gate
   (.github/workflows/segregation-of-duties.yml's `required-checks`
   job) to pass before merge. This is what makes "approver != applier"
   real for a solo maintainer: the approving identity is
   github-actions[bot], never the human author, and its approval logic
   is itself gated behind the same required check.

Usage:
    python scripts/evidence/check_segregation_of_duties.py

Exit 0 on PASS, 1 on FAIL. Always writes one signed evidence manifest.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from manifest import build_manifest, write_manifest, REPO_ROOT  # noqa: E402

POLICY_DIR = REPO_ROOT / "policies"
GITHUB_REPO = "shahidsha1612/veridian-iso27001"
PROTECTED_BRANCH = "master"
REQUIRED_CHECK_CONTEXT = "required-checks"


def _iam_role_snapshot() -> dict:
    """
    Hand-mirrors terraform/iam-segregation-of-duties/main.tf. Replace
    with real `terraform show -json` parsing once this module is
    applied against a real AWS account.
    """
    return {
        "iam_roles": [
            {
                "name": "gha-terraform-plan",
                "assume_condition": {"ref": "*"},
                "actions": [
                    "ec2:DescribeInstances", "s3:GetObject", "s3:ListBucket",
                    "iam:GetRole", "iam:ListRoles", "kms:DescribeKey",
                ],
            },
            {
                "name": "gha-terraform-apply",
                "assume_condition": {"ref": "refs/heads/master"},
                "actions": [
                    "ec2:CreateTags", "s3:PutObject", "kms:CreateKey",
                    "kms:CreateAlias", "kms:TagResource", "budgets:CreateBudget",
                    "cloudtrail:CreateTrail", "guardduty:CreateDetector", "config:PutConfigRule",
                ],
            },
        ]
    }


def _run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT, **kwargs)


def check_opa_unit_tests() -> dict:
    proc = _run(["opa", "test", str(POLICY_DIR), "-v"])
    ok = proc.returncode == 0
    return {
        "check": "opa_unit_tests",
        "status": "PASS" if ok else "FAIL",
        "reason": (proc.stdout.strip().splitlines()[-1] if ok and proc.stdout else proc.stdout + proc.stderr).strip(),
    }


def check_opa_live_snapshot() -> dict:
    snapshot = _iam_role_snapshot()
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(snapshot, f)
        input_path = f.name

    try:
        proc = _run([
            "opa", "eval", "-d", str(POLICY_DIR), "--input", input_path,
            "data.segregation_of_duties.deny", "--format", "json",
        ])
    finally:
        Path(input_path).unlink(missing_ok=True)

    if proc.returncode != 0:
        return {"check": "opa_live_snapshot", "status": "FAIL", "reason": f"opa eval failed: {proc.stderr.strip()}"}

    result = json.loads(proc.stdout)
    denies = result["result"][0]["expressions"][0]["value"]
    if denies:
        return {"check": "opa_live_snapshot", "status": "FAIL", "reason": "; ".join(denies)}
    return {
        "check": "opa_live_snapshot",
        "status": "PASS",
        "reason": "no segregation-of-duties violations in the IAM role snapshot (2 distinct roles, plan role read-only, apply role cannot self-escalate)",
    }


def check_branch_protection() -> dict:
    proc = _run(["gh", "api", f"repos/{GITHUB_REPO}/branches/{PROTECTED_BRANCH}/protection"])
    if proc.returncode != 0:
        return {"check": "branch_protection", "status": "FAIL", "reason": f"could not read branch protection: {proc.stderr.strip()}"}

    data = json.loads(proc.stdout)
    problems = []

    review_count = data.get("required_pull_request_reviews", {}).get("required_approving_review_count", 0)
    if review_count < 1:
        problems.append(f"required_approving_review_count is {review_count}, need >= 1")

    if not data.get("enforce_admins", {}).get("enabled"):
        problems.append("enforce_admins is not enabled (admin could bypass required review)")

    contexts = data.get("required_status_checks", {}).get("contexts") or []
    if REQUIRED_CHECK_CONTEXT not in contexts:
        problems.append(f"required status check {REQUIRED_CHECK_CONTEXT!r} not in required contexts {contexts}")

    if data.get("allow_force_pushes", {}).get("enabled"):
        problems.append("force pushes to master are allowed")

    if data.get("allow_deletions", {}).get("enabled"):
        problems.append("branch deletion is allowed")

    if problems:
        return {"check": "branch_protection", "status": "FAIL", "reason": "; ".join(problems)}
    return {
        "check": "branch_protection",
        "status": "PASS",
        "reason": (
            f"master requires {review_count} approving review(s), enforced for admins, "
            f"gated on required check {REQUIRED_CHECK_CONTEXT!r}, no force-push/deletion allowed"
        ),
    }


def main() -> int:
    checks = [check_opa_unit_tests(), check_opa_live_snapshot(), check_branch_protection()]

    for c in checks:
        marker = "OK  " if c["status"] == "PASS" else "FAIL"
        print(f"[{marker}] {c['check']}  ({c['reason']})")

    overall = "PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL"

    manifest = build_manifest(
        control_id="5.3",
        check_name="check_segregation_of_duties",
        result=overall,
        evaluated_state_ref=f"policies/segregation_of_duties.rego, github:{GITHUB_REPO}@branch:{PROTECTED_BRANCH}/protection",
        freshness_sla_hours=24,  # branch protection can be changed by anyone with admin access at any time
        details={"checks": checks},
    )
    manifest_path = write_manifest(manifest)
    print(f"evidence written: {manifest_path.relative_to(REPO_ROOT)} (overall: {overall})")

    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
