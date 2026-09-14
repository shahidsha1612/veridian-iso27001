#!/usr/bin/env python3
"""
Control: 5.8 (Information security in project management).

Per ISO/IEC 27002:2022 guidance for this control, "integrated into
project management" means more than reviewing each code change: (a)
security objectives are included in project objectives, (b) a security
risk assessment happens early in the project, (c) security is
addressed throughout all phases, with responsibilities allocated to
defined roles. A PR checkbox alone only covers the delivery moment
(that's really control 8.32, Change management); this checks both
lifecycle points, since project management here genuinely happens in
GitHub:

1. Kickoff: every Issue opened with the "New project / feature" form
   (.github/ISSUE_TEMPLATE/project.yml) since it was adopted must have
   its security-considerations and security-reviewer fields actually
   filled in, not left blank.
2. Delivery: every PR opened since .github/PULL_REQUEST_TEMPLATE.md was
   adopted must have engaged with the security-review checkbox (either
   checked, or left unchecked with an explanation below it -- what's
   not acceptable is the template being silently deleted).

Both checks only apply from each template's adoption date forward
(determined from git history, or "now" if the template isn't committed
yet) -- PRs/issues that predate a control can't be evidence against it.

Usage:
    python scripts/evidence/check_project_management_security_review.py

Exit 0 on PASS, 1 on FAIL. Always writes one signed evidence manifest.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from manifest import build_manifest, write_manifest, REPO_ROOT  # noqa: E402

GITHUB_REPO = "shahidsha1612/veridian-iso27001"
ISSUE_TEMPLATE_PATH = ".github/ISSUE_TEMPLATE/project.yml"
PR_TEMPLATE_PATH = ".github/PULL_REQUEST_TEMPLATE.md"

# "N/A" / "None" are legitimate, template-instructed answers (means "assessed,
# doesn't apply") and must NOT be rejected -- only a genuinely empty response
# or an explicit deferral counts as not having engaged with the field.
PLACEHOLDER_VALUES = {"", "_no response_", "tbd", "todo"}


def _run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT)


def _parse_iso(ts: str) -> datetime:
    """
    Parses an ISO 8601 timestamp into an aware datetime, regardless of
    whether it uses a 'Z' suffix (GitHub API) or a numeric offset like
    '+01:00' (git log %aI, in the committer's local timezone). Comparing
    these as raw strings is wrong -- '13:34+01:00' sorts after
    '12:35Z' lexically even though the former is the earlier instant --
    so every comparison in this file goes through this first.
    """
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def _template_adoption_date(path: str) -> str:
    """ISO 8601 timestamp the given template was first added, via git history. Falls back to now if not yet committed."""
    proc = _run(["git", "log", "--diff-filter=A", "--format=%aI", "--", path])
    lines = [ln for ln in proc.stdout.strip().splitlines() if ln]
    if lines:
        return lines[-1]  # git log lists newest first; earliest add is last
    return datetime.now(timezone.utc).isoformat()


def _is_filled(value: str) -> bool:
    return value.strip().lower() not in PLACEHOLDER_VALUES


def _extract_field(body: str, heading: str) -> str:
    """Pulls the text under a '### <heading>' block from a GitHub issue-form-rendered body."""
    pattern = rf"###\s+{re.escape(heading)}\s*\n(.*?)(?=\n###\s|\Z)"
    m = re.search(pattern, body, re.DOTALL)
    return m.group(1).strip() if m else ""


def check_issues() -> dict:
    adoption = _template_adoption_date(ISSUE_TEMPLATE_PATH)
    proc = _run([
        "gh", "issue", "list", "--repo", GITHUB_REPO, "--label", "project", "--state", "all",
        "--json", "number,title,body,createdAt", "--limit", "200",
    ])
    if proc.returncode != 0:
        return {"check": "issues", "status": "FAIL", "reason": f"could not list issues: {proc.stderr.strip()}"}

    adoption_dt = _parse_iso(adoption)
    issues = [i for i in json.loads(proc.stdout) if _parse_iso(i["createdAt"]) >= adoption_dt]

    if not issues:
        return {
            "check": "issues",
            "status": "PASS",
            "reason": f"no project issues opened since template adoption ({adoption}); nothing to evaluate yet",
            "adoption_date": adoption,
        }

    problems = []
    for issue in issues:
        considerations = _extract_field(issue["body"], "Security considerations and planned controls")
        reviewer = _extract_field(issue["body"], "Security reviewer consulted")
        if not _is_filled(considerations) or not _is_filled(reviewer):
            problems.append(f"#{issue['number']} ({issue['title']}) missing security considerations and/or reviewer")

    status = "FAIL" if problems else "PASS"
    return {
        "check": "issues",
        "status": status,
        "reason": "; ".join(problems) if problems else f"all {len(issues)} project issue(s) since {adoption} have security considerations filled in",
        "adoption_date": adoption,
        "evaluated_count": len(issues),
    }


def check_prs() -> dict:
    adoption = _template_adoption_date(PR_TEMPLATE_PATH)
    proc = _run([
        "gh", "pr", "list", "--repo", GITHUB_REPO, "--state", "all",
        "--json", "number,title,body,createdAt", "--limit", "200",
    ])
    if proc.returncode != 0:
        return {"check": "pull_requests", "status": "FAIL", "reason": f"could not list PRs: {proc.stderr.strip()}"}

    adoption_dt = _parse_iso(adoption)
    prs = [p for p in json.loads(proc.stdout) if _parse_iso(p["createdAt"]) >= adoption_dt]

    if not prs:
        return {
            "check": "pull_requests",
            "status": "PASS",
            "reason": f"no PRs opened since template adoption ({adoption}); nothing to evaluate yet",
            "adoption_date": adoption,
        }

    problems = []
    checkbox_re = re.compile(r"-\s*\[[ xX]\]\s*I've considered the information security impact")
    for pr in prs:
        if not checkbox_re.search(pr["body"] or ""):
            problems.append(f"#{pr['number']} ({pr['title']}) missing the security-review checkbox entirely (template not used or removed)")

    status = "FAIL" if problems else "PASS"
    return {
        "check": "pull_requests",
        "status": status,
        "reason": "; ".join(problems) if problems else f"all {len(prs)} PR(s) since {adoption} engaged with the security-review checkbox",
        "adoption_date": adoption,
        "evaluated_count": len(prs),
    }


def main() -> int:
    checks = [check_issues(), check_prs()]

    for c in checks:
        marker = "OK  " if c["status"] == "PASS" else "FAIL"
        print(f"[{marker}] {c['check']}  ({c['reason']})")

    overall = "PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL"

    manifest = build_manifest(
        control_id="5.8",
        check_name="check_project_management_security_review",
        result=overall,
        evaluated_state_ref=f"github:{GITHUB_REPO} issues(label=project) + pull requests, since each template's adoption date",
        freshness_sla_hours=24 * 7,
        details={"checks": checks},
    )
    manifest_path = write_manifest(manifest)
    print(f"evidence written: {manifest_path.relative_to(REPO_ROOT)} (overall: {overall})")

    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
