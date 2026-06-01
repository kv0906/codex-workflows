# codex-workflows

A portable **agent skill** that turns a large task into a supervised multi-agent
workflow: draft an orchestration artifact, gather grounded context, pick a run model,
delegate to subagents (or simulate them), integrate evidence-backed results, verify, and
save reusable recipes.

It's not an application — there's nothing to build or deploy. A host agent (Cursor,
Claude Code, Codex, etc.) loads `SKILL.md` and drives the workflow, using the Python
helpers in `scripts/` to scaffold and check workflow artifacts.

## When to use it

Reach for it when at least two are true:

- The task has independent tracks (research, code, review, migration, QA, docs, design).
- An explicit success contract would reduce drift.
- There's real risk: destructive edits, external writes, deploys, secrets, prod data.
- Verification benefits from a separate pass than implementation.
- The work could become a reusable recipe.
- The user explicitly asks for a swarm, subagents, parallel agents, or a dynamic workflow.

If the task is small, do it directly — the skill says so itself.

## How to use it

Invoke the skill from a host agent that supports skills:

```text
Use $codex-workflows to plan and run a supervised multi-agent workflow for this task.
```

The agent then follows the Operating Contract in `SKILL.md`: restate goal + success
criteria, scaffold a workflow artifact, run a context bootstrap, define the run model,
gate risky steps for approval, run disjoint evidence-backed packets, integrate, and verify.

## Workflow lifecycle (scripts)

The helpers are Python 3 **stdlib only** — no install step.

```bash
# 1. Scaffold a run directory: .workflow/<slug>/ (plan, state.json, manifests, packets/, results/)
python3 scripts/new_workflow.py "Task title"

# 2. ...do the work: fill plan.md / context-manifest.md, write packets/*.md and results/*.md...

# 3. Summarize results into an integration checklist
python3 scripts/collect_results.py .workflow/<slug>

# 4. Verify the artifact is complete enough to audit
python3 scripts/verify_workflow.py .workflow/<slug>
```

`verify_workflow.py` exits non-zero until `packets/` and `results/` contain `.md`
files — that's expected early in a run, not a bug.

## Layout

| Path | Purpose |
|------|---------|
| `SKILL.md` | Skill entrypoint and operating contract (source of truth). |
| `agents/openai.yaml` | Host interface metadata (display name, default prompt). |
| `scripts/new_workflow.py` | Scaffold a `.workflow/<slug>/` run directory. |
| `scripts/collect_results.py` | Summarize `results/*.md` into an integration checklist. |
| `scripts/verify_workflow.py` | Check workflow-artifact completeness. |
| `references/context-gathering.md` | Context bootstrap and tool-priority guidance. |
| `references/plan-schema.md` | Machine-readable workflow plan schema. |
| `references/workflow-run-model.md` | Phases, parallel/pipeline groups, statuses, synthesis. |
| `references/risk-gates.md` | Approval gates for risky/destructive/external actions. |
| `references/validation-examples.md` | Forward-test scenarios for the skill. |

See `AGENTS.md` for conventions if you're modifying this repo.
