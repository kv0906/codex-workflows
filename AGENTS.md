# AGENTS.md

Guidance for AI agents working in this repository.

## What this repo is

`codex-workflows` is a portable **agent skill** (not an application). It teaches a host
agent (Cursor, Claude Code, Codex, etc.) how to turn a large task into a supervised
multi-agent workflow: draft an orchestration artifact, gather grounded context, pick a
run model, delegate to subagents (or simulate them), integrate evidence-backed results,
verify, and save reusable recipes.

The skill is consumed by reading `SKILL.md` and its `references/`. The `scripts/` are
helper tools the skill invokes; there is no build step and no application to run.

## Layout

- `SKILL.md` — the skill entrypoint and operating contract. Source of truth for behavior.
- `agents/openai.yaml` — host interface metadata (display name, default prompt).
- `scripts/` — Python 3 stdlib-only CLIs:
  - `new_workflow.py "Title"` — scaffold `.workflow/<slug>/` (plan, state.json, manifests, packets/, results/).
  - `verify_workflow.py .workflow/<slug>` — assert a workflow artifact is complete enough to audit.
  - `collect_results.py .workflow/<slug>` — summarize `results/*.md` into an integration checklist.
- `references/` — deep-dive docs loaded on demand:
  - `context-gathering.md`, `plan-schema.md`, `risk-gates.md`, `workflow-run-model.md`, `validation-examples.md`.

## Commands

No package manager, no dependencies. Everything is Python 3 stdlib.

```bash
python3 scripts/new_workflow.py "Task title"        # scaffold a run dir
python3 scripts/verify_workflow.py .workflow/<slug> # check artifact completeness
python3 scripts/collect_results.py .workflow/<slug> # build integration checklist
```

There is no test suite, linter config, or CI in this repo. Validate changes by running
the scripts above. `verify_workflow.py` exits non-zero until `packets/` and `results/`
contain `.md` files — that's expected, not a bug.

## Conventions

- **Python**: 3.x, standard library only — do **not** add third-party deps. Keep
  `from __future__ import annotations`, type hints, `argparse` CLIs, and the
  `raise SystemExit(main())` entrypoint pattern used by existing scripts.
- **No runtime state in the repo**: `.workflow/` is generated output. Don't commit
  generated workflow runs, secrets, transcripts, or bulky logs.
- **Docs are the product**: changes to skill behavior live in `SKILL.md` /
  `references/`, not in code comments. Keep `SKILL.md` and the scripts in sync — if you
  add/rename a `state.json` key, update the `REQUIRED_*` tuples in `verify_workflow.py`.
- **Markdown**: keep headings and the artifact templates in `new_workflow.py` aligned
  with the schemas documented in `SKILL.md` and `references/plan-schema.md`.

## When acting as the skill

Follow the Operating Contract in `SKILL.md`: restate goal + success criteria, create the
workflow artifact before delegating, run a context bootstrap, define the run model, ask
for approval before risky/destructive/external actions, keep packets disjoint and
evidence-backed, integrate before verifying, and only save recipes that help future work.
Don't claim a tool (CodeGraph, QMD, Context7, subagent runner) was used if it wasn't
available — record gaps in the context manifest instead.
