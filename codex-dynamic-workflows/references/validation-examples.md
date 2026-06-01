# Validation Examples

Use these examples to forward-test this skill.

## Small Task

Prompt:

```text
Use $codex-dynamic-workflows to fix a typo in README.md.
```

Expected behavior:

- Decide full orchestration is unnecessary.
- Make the edit directly.
- Verify the diff.
- Do not create a workflow directory unless the user insists.

## Risky Migration

Prompt:

```text
Use $codex-dynamic-workflows to migrate all API clients from REST to GraphQL and delete the old client.
```

Expected behavior:

- Draft plan and success criteria.
- Mark deletion and broad migration as approval-gated.
- Create packets for discovery, implementation, tests, docs, and verification.
- Ask before destructive edits.

## Parallel Research And Implementation

Prompt:

```text
Use $codex-dynamic-workflows to add SSO support. Research the provider docs, implement backend changes, update UI, and add tests.
```

Expected behavior:

- Create a workflow artifact.
- Enter goal mode if the user wants sustained execution.
- Split provider research, backend, frontend, tests, and docs into disjoint packets.
- Integrate results before final verification.

## Codebase Audit

Prompt:

```text
Use $codex-dynamic-workflows to audit this repo for slow startup and fix the biggest issue.
```

Expected behavior:

- Create audit packets for entrypoint tracing, dependency loading, test/build evidence, and fix candidates.
- Keep immediate blocking investigation local.
- Use subagents only for sidecar analysis.
- Implement one highest-confidence fix and verify it.

## No Subagent Runner

Prompt:

```text
Use $codex-dynamic-workflows to review this feature for security and reliability risks.
```

Expected behavior:

- Simulate subagents with isolated packet notes under `results/`.
- Keep security and reliability findings separate until integration.
- Produce a synthesized final report.

## Hallucination-Resistant Codebase Discovery

Prompt:

```text
Use $codex-dynamic-workflows to find how checkout sessions are created and update the retry behavior.
```

Expected behavior:

- Create a workflow artifact with `context-manifest.md`.
- Use CodeGraph or codebase-memory before packet planning to find the relevant symbols, callers, and impact.
- Use QMD if repo docs mention checkout, payments, retries, or provider behavior.
- Packet results separate facts, inferences, assumptions, and unknowns.
- Integration rejects or marks unsupported claims instead of treating them as facts.

## Docs-Heavy Repo With QMD

Prompt:

```text
Use $codex-dynamic-workflows to implement the behavior described in /docs for the new ingestion workflow.
```

Expected behavior:

- Use QMD as the primary `/docs` retrieval layer.
- Record QMD queries, selected docs, and unresolved doc conflicts in `context-manifest.md`.
- Use CodeGraph to validate runtime impact before implementation packets.
- Report stale or conflicting docs as unknowns if they cannot be resolved.

## External Library Documentation

Prompt:

```text
Use $codex-dynamic-workflows to upgrade the app to the latest auth SDK behavior.
```

Expected behavior:

- Check current external-library documentation through Context7 when available.
- If Context7 is unavailable, use official docs, the package repository, installed package source, or release notes.
- Record the source and date checked.
- Do not rely on model memory for library behavior when current docs are practical to inspect.

## Missing Context Tool

Prompt:

```text
Use $codex-dynamic-workflows to audit this repo with CodeGraph, QMD, DeepWiki, and Context7.
```

Expected behavior:

- Use available tools.
- Record unavailable tools in `context-manifest.md`.
- Continue with the best available sources.
- Report tool limitations in the final report.
- Do not fail only because a requested context MCP was unavailable.

## Parallel Review

Prompt:

```text
Use $codex-dynamic-workflows to review this payment feature for security, reliability, and docs risks.
```

Expected behavior:

- Create a run model with a context bootstrap phase, a parallel review group, and a synthesis phase.
- Give each packet a unique label.
- Keep security, reliability, and docs packets independent.
- Record failed, skipped, blocked, or incomplete packets instead of dropping them.
- Parent agent performs final synthesis and decides which findings are accepted.

## Pipeline Migration

Prompt:

```text
Use $codex-dynamic-workflows to migrate three API clients to the new SDK.
```

Expected behavior:

- Create a pipeline group when each client needs the same staged work.
- Use stages such as inspect, update, verify, and docs.
- Keep each target status visible.
- Do not treat one successful target as proof that all targets passed.

## Failed Packet Branch

Prompt:

```text
Use $codex-dynamic-workflows to audit startup performance with parallel packets.
```

Expected behavior:

- If one packet fails, record it as failed or incomplete.
- Continue safe independent work when possible.
- Final synthesis says whether the failed packet affects confidence.
- Unsupported claims from failed packets are rejected or marked uncertain.
