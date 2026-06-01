#!/usr/bin/env python3
"""Check that an AI-agent dynamic workflow artifact is complete enough to audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_FILES = ("plan.md", "state.json", "context-manifest.md", "orchestration.md", "final-report.md")
REQUIRED_DIRS = ("packets", "results")
REQUIRED_STATE_KEYS = (
    "title",
    "slug",
    "status",
    "context",
    "run_model",
    "approval",
    "packets",
    "packet_statuses",
    "synthesis",
    "verification",
)
REQUIRED_CONTEXT_KEYS = (
    "status",
    "tools_available",
    "tools_unavailable",
    "sources",
    "external_docs_checked",
    "unknowns",
)
REQUIRED_RUN_MODEL_KEYS = (
    "metadata",
    "phases",
    "active_phase",
    "parallel_groups",
    "pipeline_groups",
    "budget",
    "failure_policy",
)
REQUIRED_PACKET_STATUS_KEYS = ("complete", "failed", "skipped", "blocked", "incomplete")
REQUIRED_SYNTHESIS_KEYS = ("status", "conflicts", "unsupported_claims", "unknowns")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workflow_dir", help="Path to .workflow/<slug>")
    args = parser.parse_args()

    workflow_dir = Path(args.workflow_dir)
    failures: list[str] = []

    if not workflow_dir.is_dir():
        failures.append(f"Missing workflow directory: {workflow_dir}")
    for name in REQUIRED_FILES:
        path = workflow_dir / name
        if not path.is_file():
            failures.append(f"Missing file: {path}")
        elif not path.read_text(encoding="utf-8").strip():
            failures.append(f"Empty file: {path}")
    for name in REQUIRED_DIRS:
        path = workflow_dir / name
        if not path.is_dir():
            failures.append(f"Missing directory: {path}")

    state_path = workflow_dir / "state.json"
    if state_path.is_file():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"Invalid JSON in {state_path}: {exc}")
        else:
            for key in REQUIRED_STATE_KEYS:
                if key not in state:
                    failures.append(f"Missing state key: {key}")
            context = state.get("context")
            if isinstance(context, dict):
                for key in REQUIRED_CONTEXT_KEYS:
                    if key not in context:
                        failures.append(f"Missing context state key: {key}")
            elif "context" in state:
                failures.append("State key is not an object: context")
            run_model = state.get("run_model")
            if isinstance(run_model, dict):
                for key in REQUIRED_RUN_MODEL_KEYS:
                    if key not in run_model:
                        failures.append(f"Missing run_model state key: {key}")
            elif "run_model" in state:
                failures.append("State key is not an object: run_model")
            packet_statuses = state.get("packet_statuses")
            if isinstance(packet_statuses, dict):
                for key in REQUIRED_PACKET_STATUS_KEYS:
                    if key not in packet_statuses:
                        failures.append(f"Missing packet_statuses state key: {key}")
            elif "packet_statuses" in state:
                failures.append("State key is not an object: packet_statuses")
            synthesis = state.get("synthesis")
            if isinstance(synthesis, dict):
                for key in REQUIRED_SYNTHESIS_KEYS:
                    if key not in synthesis:
                        failures.append(f"Missing synthesis state key: {key}")
            elif "synthesis" in state:
                failures.append("State key is not an object: synthesis")

    packet_files = sorted((workflow_dir / "packets").glob("*.md")) if (workflow_dir / "packets").is_dir() else []
    result_files = sorted((workflow_dir / "results").glob("*.md")) if (workflow_dir / "results").is_dir() else []
    if not packet_files:
        failures.append("No packet files found under packets/")
    if not result_files:
        failures.append("No result files found under results/")

    if failures:
        print("Workflow verification failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"Workflow verification passed: {workflow_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
