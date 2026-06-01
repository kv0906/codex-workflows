---
name: codex-dynamic-workflows
description: Plan and run AI-agent dynamic workflows for complex tasks that benefit from explicit orchestration, goal mode, subagents or simulated work packets, approval gates, integration, verification, and reusable workflow artifacts. Use when the user invokes this skill, asks for a swarm, subagents, parallel agents, a dynamic workflow, a large migration or audit, multi-track research plus implementation, or Claude Code-style workflow orchestration.
---

# AI Agent Dynamic Workflows

Use this skill to turn a large task into a supervised AI-agent workflow: draft an orchestration artifact, gather grounded context, choose a clear run model, enter goal mode when sustained execution is requested, delegate disjoint work to subagents when available, integrate evidence-backed results, verify the outcome, and save reusable workflow artifacts.

This skill works in agents that support skills. Do not claim that a local script can call subagent tools unless the current environment exposes such a runner. When no programmable runner exists, create a human-readable orchestration script and operate it through the available agent tools.

## Decision Rule

Use dynamic orchestration when at least two are true:

- The task has independent research, coding, review, migration, QA, docs, or design tracks.
- The task is broad enough that an explicit success contract would reduce drift.
- The task has risk: destructive edits, external writes, deploys, secrets, production data, billing, user accounts, or large repo-wide changes.
- Verification benefits from a separate pass from implementation.
- The workflow could become a reusable recipe for future tasks.
- The user explicitly asks for a dynamic workflow, swarm, subagents, parallel agents, or Claude Code-style workflow.

If the task is small, do it directly and mention that full workflow orchestration was unnecessary.

## Operating Contract

When using this skill:

1. Restate the goal and success criteria.
2. Create or update a workflow artifact before delegating.
3. Run a context bootstrap before packet planning.
4. Define the workflow run model: phases, parallel groups, pipelines, labels, budget, and failure policy.
5. Ask for approval before risky, expensive, external, or destructive steps.
6. Enter goal mode when the user explicitly requests sustained execution or when the invoked task clearly requires multi-turn completion.
7. Split work into disjoint packets with clear ownership and explicit evidence requirements.
8. Spawn subagents only when the current environment allows it and the user has authorized delegated or parallel agent work.
9. Simulate subagents with isolated packet notes when no subagent runner is available.
10. Integrate results explicitly; do not paste raw subagent dumps as the final answer.
11. Verify with checks matched to the task's blast radius.
12. Save reusable artifacts only when they will help future work.

## Workflow Artifacts

Prefer creating a local run directory:

```text
.workflow/<slug>/
|-- plan.md
|-- state.json
|-- context-manifest.md
|-- orchestration.md
|-- packets/
|-- results/
`-- final-report.md
```

Use `scripts/new_workflow.py` to scaffold this structure:

```bash
python3 /path/to/codex-dynamic-workflows/scripts/new_workflow.py "Task title"
```

Keep `plan.md` human-readable. Use `state.json` for status, context status, run model, packet IDs, approval state, synthesis state, and verification state. Use `context-manifest.md` as the source handoff: goal terms, queries, tools used, unavailable tools, selected sources, external docs checked, confidence, and unknowns. Use `orchestration.md` as the executable mental model: the sequence the agent will follow, the branching rules, phase transitions, fan-out/fan-in groups, failure handling, and packet prompts.

## Orchestration Plan

Draft a concise plan with:

```text
Goal:
Success criteria:
Current context:
Context bootstrap:
Workflow run model:
Constraints:
Risks:
Approval required:
Workflow artifact path:
Work packets:
Evidence policy:
Integration policy:
Verification:
Reusable artifacts:
```

Do not over-plan obvious work. The plan should be detailed enough to guide delegation and verification, not a substitute for execution.

## Workflow Run Model

Before launching packets, define how the workflow will actually run. A reliable workflow is more than a list of tasks; it needs a visible execution shape.

Use these concepts:

- `metadata`: short workflow name, description, trigger, and success criteria.
- `phase`: a named group of work that starts only when real work begins. Do not report speculative phases as completed work.
- `label`: a unique 2-5 word name for each packet or subagent so status, failures, and logs are readable.
- `parallel group`: independent packets that can run at the same time because they do not depend on each other.
- `pipeline group`: repeated staged work where each item passes through the same ordered steps, such as inspect -> change -> verify.
- `budget`: rough limits for agent count, time, tokens, or review depth.
- `failure policy`: how to record failed, skipped, blocked, or incomplete packets before synthesis.
- `synthesis gate`: the parent agent reviews all packet statuses, evidence, conflicts, and unknowns before finalizing.

Prefer a small run model that matches the task. Do not add parallelism when the work is sequential. Do not create a pipeline when there is only one target.

## Context Bootstrap

Before creating work packets, gather enough context to prevent guesswork. Record the results in `context-manifest.md`.

Use the most authoritative available source for each kind of question:

- CodeGraph or codebase-memory MCP for code structure, symbols, routes, call paths, and impact.
- QMD for `/docs`, markdown-heavy repo knowledge, design notes, plans, and project documentation.
- DeepWiki for GitHub repository architecture and generated repo documentation when available.
- Context7 or current official docs for external libraries, APIs, SDKs, and framework behavior.
- Native search only for string literals, config values, logs, error text, or when structured tools are unavailable or insufficient.

Missing context tools are not automatic failures. If CodeGraph, QMD, DeepWiki, Context7, or another MCP is unavailable, say so in the manifest and continue with the best available source. Do not claim a tool was used if it was not available.

For external libraries, prefer current documentation over memory. If Context7 is unavailable, use official docs, the package repository, or installed package source where practical. Record the source and date checked.

## Approval Gates

Ask one clear approval question before:

- deleting, overwriting, mass-renaming, or force-pushing
- running migrations or broad codemods
- deploying, publishing, emailing, posting, or changing external systems
- touching credentials, secrets, production data, billing, or user accounts
- spawning many agents or long-running expensive jobs
- making irreversible Git or repository operations

If approval is denied or unavailable, continue only with safe read-only planning, local drafts, or non-destructive checks.

Read `references/risk-gates.md` when risk is unclear.

## Goal Mode

If goal mode tools are available and the user has asked this skill to run the workflow, call goal mode with the full objective. Keep the objective intact; do not shrink it to the next step.

Do not enter goal mode for a small one-shot task, a purely advisory discussion, or when the user asks only for a plan.

## Work Packets

Each packet must be self-contained:

```text
Packet ID:
Label:
Objective:
Context:
Files / sources:
Evidence required:
Context sources:
Tool results used:
Ownership:
Do:
Do not:
Expected output:
Status:
Claims:
Unknowns:
External docs checked:
Verification:
```

Prefer packets with disjoint ownership:

- codebase discovery
- dependency or API research
- implementation slice
- tests and fixtures
- docs and examples
- UX or product review
- security or risk review
- final verification

For code-edit packets, assign non-overlapping files or modules. Tell workers they are not alone in the codebase, must not revert others' edits, and must adapt to concurrent changes.

## Subagents

When a subagent runner is available:

- Spawn only concrete, bounded, materially useful subtasks.
- Keep immediate blocking work local.
- Delegate sidecar work that can run while the main agent makes progress.
- Avoid duplicate work across agents.
- Ask workers to edit directly only when their write scope is disjoint and clear.
- Wait for subagents only when their result is needed for the next critical-path step.
- Use unique labels for every worker.
- Use parallel groups only for independent work.
- Use pipeline groups only when multiple targets share the same ordered stages.
- Give each worker the relevant context manifest entries and require them to separate facts, inferences, assumptions, and unknowns.
- Require workers to cite the code, docs, command output, or external documentation behind important claims.

When no subagent runner is available:

- Simulate the swarm with isolated packet passes.
- Read only packet-relevant files during each pass.
- Write packet notes under `results/`.
- Integrate only after packet outputs are separate.
- Keep simulated packet notes evidence-backed in the same format expected from subagents.

## Packet Statuses

Every packet result must have one status:

- `complete`: packet produced the expected output with usable evidence.
- `failed`: packet ran but hit an error or produced unusable output.
- `skipped`: packet did not run because it was no longer needed or the branch did not apply.
- `blocked`: packet needs missing input, unavailable tools, approval, credentials, or external state.
- `incomplete`: packet produced partial output that may still be useful but cannot support final claims alone.

Failed, skipped, blocked, and incomplete packets do not disappear. Record them in `results/`, include them in integration, and say whether they affect confidence.

## Integration

After packets complete, synthesize:

```text
Accepted:
Rejected:
Conflicts:
Decisions:
Packet statuses:
Claims:
Evidence:
Unknowns:
External docs:
Tool limitations:
Final changes:
Remaining risks:
```

Resolve conflicts explicitly. If two packets disagree, inspect the authoritative source before choosing. Prefer CodeGraph or codebase-memory for behavior, QMD or repo docs for documented project intent, and current official documentation for external-library behavior.

Before the final answer, run a synthesis gate:

- Review every packet status.
- Reject unsupported claims or mark them as assumptions.
- Explain failed, skipped, blocked, or incomplete packets.
- Resolve conflicts or keep them in `Unknowns`.
- Confirm external-library claims were checked against current docs when practical.
- Confirm code behavior claims are tied to code evidence when practical.

Use `scripts/collect_results.py` to produce an integration checklist from result files:

```bash
python3 /path/to/codex-dynamic-workflows/scripts/collect_results.py .workflow/<slug>
```

## Verification

Run the narrowest reliable checks first, then broaden as risk warrants:

- unit tests for touched code
- typecheck or lint
- build
- browser or UI smoke test
- script dry run
- source citation check
- context manifest and evidence check
- packet status and synthesis gate check
- migration dry run
- manual checklist for non-code work

Use `scripts/verify_workflow.py` to check workflow artifact completeness:

```bash
python3 /path/to/codex-dynamic-workflows/scripts/verify_workflow.py .workflow/<slug>
```

Report skipped checks honestly. Do not treat a workflow as complete until the evidence proves the original success criteria.

## Reusable Recipes

When a run produces a useful pattern, save a concise recipe in a project-appropriate location, such as `.workflow/recipes/<name>.md` or a repo docs folder. Include:

- trigger
- plan shape
- packet list
- verification checklist
- known risks

Do not save transcripts, secrets, bulky logs, credentials, or sensitive personal details.

## References

- Read `references/plan-schema.md` when a machine-readable workflow plan is useful.
- Read `references/context-gathering.md` before context-heavy, external-library, or subagent workflows.
- Read `references/workflow-run-model.md` before designing parallel groups, pipelines, packet statuses, or synthesis gates.
- Read `references/risk-gates.md` before risky or ambiguous operations.
- Read `references/validation-examples.md` when forward-testing or improving this skill.
