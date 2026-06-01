# Workflow Run Model

Use this reference when a task needs more than a simple checklist. The goal is to make the workflow behave like a small supervised engineering run: clear phases, bounded fan-out, explicit failures, and a final synthesis owned by the parent agent.

This is inspired by executable dynamic workflow systems, but this skill stays portable. Do not require a JavaScript runtime or claim a script runner exists unless the current environment provides one.

## Core Concepts

- Metadata: short name, description, when-to-use, success criteria, and budget.
- Phase: a named group of real work. Treat phases as active only when work starts.
- Label: a unique 2-5 word name for each packet or subagent.
- Parallel group: independent packets that can run together without shared write scope or result dependency.
- Pipeline group: repeated staged work where each target moves through the same ordered stages.
- Failure policy: rules for failed, skipped, blocked, and incomplete packets.
- Synthesis gate: final parent-agent review before conclusions become final.

## Phase Discipline

Planned phases are useful for orientation, but they are not progress evidence. Do not report a phase as done unless work actually ran for that phase.

Good phase names are short and concrete:

- Context bootstrap
- API review
- Implementation
- Verification
- Synthesis

Avoid speculative phase lists that imply skipped work happened.

## Parallel Versus Pipeline

Use parallel groups for independent work:

```text
Parallel group: review-risk
- security review
- reliability review
- docs review
```

Use pipeline groups when the same targets pass through ordered stages:

```text
Pipeline group: migrate-clients
Items: auth client, billing client, webhook client
Stages: inspect -> update -> verify
```

Do not use parallel groups when packets need each other's outputs. Do not use pipelines when there is only one target or when each target needs a different process.

## Packet Labels

Every packet needs a stable label so progress and failures are readable. Labels should be unique and short:

```text
Label: auth callers
Label: docs intent
Label: retry tests
```

## Packet Statuses

Every packet result must use one status:

- `complete`: expected output exists and has usable evidence.
- `failed`: the packet ran but errored or produced unusable output.
- `skipped`: the packet did not run because it no longer applied.
- `blocked`: the packet needs missing input, approval, tool access, credentials, or external state.
- `incomplete`: partial output exists but cannot support final claims alone.

The final synthesis must account for every non-complete status.

## Synthesis Gate

Before finalizing:

- Review every packet status.
- Read evidence, not just conclusions.
- Reject unsupported claims or mark them as assumptions.
- Resolve conflicts with authoritative sources.
- Keep unresolved conflicts in `Unknowns`.
- State whether failed, skipped, blocked, or incomplete packets reduce confidence.

The parent agent owns the final answer. Subagent output is input, not the final result.
