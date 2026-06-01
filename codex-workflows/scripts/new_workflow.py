#!/usr/bin/env python3
"""Create an AI-agent dynamic workflow artifact directory."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:64].strip("-") or "workflow"


def write_new(path: Path, content: str) -> None:
    if path.exists():
        return
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("title", help="Workflow title or task summary")
    parser.add_argument(
        "--root",
        default=".workflow",
        help="Directory where workflow runs are stored (default: .workflow)",
    )
    parser.add_argument("--slug", help="Optional explicit workflow slug")
    args = parser.parse_args()

    slug = slugify(args.slug or args.title)
    run_dir = Path(args.root) / slug
    packets_dir = run_dir / "packets"
    results_dir = run_dir / "results"
    packets_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    state = {
        "title": args.title,
        "slug": slug,
        "created_at": now,
        "status": "planned",
        "context": {
            "status": "not_started",
            "tools_available": [],
            "tools_unavailable": [],
            "sources": [],
            "external_docs_checked": [],
            "unknowns": [],
        },
        "run_model": {
            "metadata": {"name": slug, "description": args.title, "when_to_use": ""},
            "phases": [],
            "active_phase": None,
            "parallel_groups": [],
            "pipeline_groups": [],
            "budget": {"max_agents": None, "max_parallel": None, "notes": ""},
            "failure_policy": "Record failed, skipped, blocked, and incomplete packets before synthesis.",
        },
        "approval": {"required": None, "granted": None, "notes": ""},
        "packets": [],
        "packet_statuses": {
            "complete": [],
            "failed": [],
            "skipped": [],
            "blocked": [],
            "incomplete": [],
        },
        "synthesis": {"status": "not_started", "conflicts": [], "unsupported_claims": [], "unknowns": []},
        "verification": {"status": "not_started", "checks": []},
    }

    write_new(
        run_dir / "plan.md",
        f"""# {args.title}

## Goal

## Success Criteria

## Current Context

## Context Bootstrap

## Workflow Run Model

## Phase Plan

## Parallel Groups

## Pipeline Groups

## Constraints

## Risks

## Approval Required

## Work Packets

## Evidence Policy

## Failure Policy

## Integration Policy

## Synthesis Gate

## Verification

## Reusable Artifacts
""",
    )
    write_new(
        run_dir / "context-manifest.md",
        f"""# Context Manifest: {args.title}

## Goal Terms

## Queries Run

## Tools Available

## Tools Unavailable

## Code Sources

## Repo Docs Sources

## External Docs Checked

## Selected Context For Packets

## Confidence

## Unknowns
""",
    )
    write_new(
        run_dir / "orchestration.md",
        f"""# Orchestration: {args.title}

## Execution Rules

- Keep the original objective intact.
- Ask for approval before risky, expensive, external, or destructive actions.
- Gather grounded context before packet planning.
- Define phases, parallel groups, pipelines, labels, budget, and failure policy before launching work.
- Keep immediate blocking work local.
- Delegate only bounded, disjoint, materially useful packets.
- Require evidence-backed packet outputs.
- Record failed, skipped, blocked, and incomplete packets.
- Integrate packet results before final verification.

## Branching Rules

## Context Bootstrap

## Phase Plan

## Parallel Groups

## Pipeline Groups

## Failure Policy

## Packet Prompts

Each packet prompt should include:

- Label
- Evidence required
- Context sources
- Tool results used
- Status
- Claims
- Unknowns
- External docs checked
- Verification needed

## Synthesis Gate

## Completion Audit
""",
    )
    write_new(run_dir / "state.json", json.dumps(state, indent=2) + "\n")
    write_new(
        run_dir / "final-report.md",
        f"""# Final Report: {args.title}

## Outcome

## Accepted Results

## Rejected Results

## Packet Statuses

## Conflicts Resolved

## Claims And Evidence

## Unknowns

## External Docs Checked

## Tool Limitations

## Synthesis Gate

## Verification Evidence

## Remaining Risks

## Reusable Follow-up
""",
    )

    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
