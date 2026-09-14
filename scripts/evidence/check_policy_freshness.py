#!/usr/bin/env python3
"""
Reusable T3-evidence check for any policy/RACI/register/minutes doc
that carries the shared frontmatter shape (control_id, last_reviewed,
review_cadence_months, next_review_due). Scans every *.md file under
docs/controls/<section>/ (one file per control, e.g.
docs/controls/governance/A.5.1-policies-for-information-security.md)
and docs/management-reviews/ (one file per review meeting, all tagged
with the same control_id -- see build_manifest's by-control grouping),
reads its frontmatter, and fails any whose `next_review_due` has
passed.

This is the "automated" half of a T3 control: it can't verify the
*content* of a review happened, but it can prove, on a schedule and
without a human remembering, that nobody let a document go silently
stale.

Three-state result, not just pass/fail, so there's an actual chance to
act before a document lapses instead of only finding out after:
  - PASS: more than `review_warning_days` days before next_review_due
  - WARN: within `review_warning_days` days of next_review_due (default 30)
  - FAIL: next_review_due has passed, or frontmatter is missing/invalid

Usage:
    python scripts/evidence/check_policy_freshness.py \
        [--dir docs/controls] [--file docs/some-other-doc.md]

One signed evidence manifest is written per distinct control_id found
(not one manifest for the whole scan), since each control_id is a
separate control in the Statement of Applicability and needs its own
evidence trail. Exit code 0 if every document is PASS, 2 if any is WARN
(not overdue yet, but flag it), 1 if any is FAIL.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from manifest import build_manifest, write_manifest, REPO_ROOT  # noqa: E402

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
REQUIRED_FIELDS = ("control_id", "last_reviewed", "review_cadence_months", "next_review_due")
DEFAULT_WARNING_DAYS = 30
STATUS_RANK = {"PASS": 0, "WARN": 1, "FAIL": 2}  # for picking the worst overall result


def parse_frontmatter(text: str) -> dict:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        fm[key.strip()] = value.strip().strip('"')
    return fm


def check_one(path: Path, today: date) -> dict:
    fm = parse_frontmatter(path.read_text(encoding="utf-8"))
    missing = [f for f in REQUIRED_FIELDS if f not in fm]
    if missing:
        return {
            "path": str(path.relative_to(REPO_ROOT)),
            "control_id": fm.get("control_id", "UNKNOWN"),
            "status": "FAIL",
            "reason": f"missing required frontmatter field(s): {missing}",
        }

    try:
        due = date.fromisoformat(fm["next_review_due"])
    except ValueError:
        return {
            "path": str(path.relative_to(REPO_ROOT)),
            "control_id": fm["control_id"],
            "status": "FAIL",
            "reason": f"next_review_due {fm['next_review_due']!r} is not a valid ISO date",
        }

    warning_days = int(fm.get("review_warning_days", DEFAULT_WARNING_DAYS))
    days_remaining = (due - today).days

    if days_remaining < 0:
        status, reason = "FAIL", f"overdue for review by {-days_remaining} day(s)"
    elif days_remaining <= warning_days:
        status, reason = "WARN", f"due in {days_remaining} day(s), within the {warning_days}-day warning window"
    else:
        status, reason = "PASS", f"due in {days_remaining} day(s), within review cadence"

    return {
        "path": str(path.relative_to(REPO_ROOT)),
        "control_id": fm["control_id"],
        "owner": fm.get("owner"),
        "last_reviewed": fm["last_reviewed"],
        "next_review_due": fm["next_review_due"],
        "status": status,
        "reason": reason,
    }


DEFAULT_DIRS = ["docs/controls", "docs/management-reviews"]
DEFAULT_FILES: list[str] = []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", action="append", default=None, help="directory to glob *.md from (repeatable)")
    parser.add_argument("--file", action="append", default=None, help="single file to check (repeatable)")
    args = parser.parse_args()

    dirs = args.dir if args.dir is not None else DEFAULT_DIRS
    extra_files = args.file if args.file is not None else DEFAULT_FILES

    files: list[Path] = []
    for d in dirs:
        policies_dir = REPO_ROOT / d
        if policies_dir.exists():
            files.extend(sorted(policies_dir.rglob("*.md")))
    for f in extra_files:
        file_path = REPO_ROOT / f
        if file_path.exists():
            files.append(file_path)

    if not files:
        print(f"no policy files found under {dirs} or {extra_files}", file=sys.stderr)
        return 1

    today = date.today()
    results = [check_one(p, today) for p in files]

    for r in results:
        marker = {"PASS": "OK  ", "WARN": "WARN", "FAIL": "FAIL"}[r["status"]]
        print(f"[{marker}] {r['control_id']:>6}  {r['path']}  ({r['reason']})")

    by_control: dict[str, list[dict]] = {}
    for r in results:
        by_control.setdefault(r["control_id"], []).append(r)

    worst_overall = "PASS"
    for control_id, control_results in sorted(by_control.items()):
        control_status = max((r["status"] for r in control_results), key=STATUS_RANK.get)
        worst_overall = max(worst_overall, control_status, key=STATUS_RANK.get)

        manifest = build_manifest(
            control_id=control_id,
            check_name="check_policy_freshness",
            result=control_status,
            evaluated_state_ref=", ".join(sorted({r["path"] for r in control_results})),
            freshness_sla_hours=24 * 7,  # checked weekly once scheduled
            details={"policies_checked": control_results, "default_warning_days": DEFAULT_WARNING_DAYS},
        )
        manifest_path = write_manifest(manifest)
        print(f"evidence written: {manifest_path.relative_to(REPO_ROOT)} (control {control_id}: {control_status})")

    return {"PASS": 0, "WARN": 2, "FAIL": 1}[worst_overall]


if __name__ == "__main__":
    raise SystemExit(main())
