# Context Gathering

Use this reference before context-heavy workflows, external-library work, and subagent delegation.

## Purpose

The context bootstrap prevents hallucination by turning discovery into an explicit workflow stage. The agent should know which facts came from code, which came from docs, which came from external references, and which are still unknown before assigning work packets.

## Tool Priority

Use the most authoritative available source:

- CodeGraph or codebase-memory MCP: code structure, symbols, routes, call paths, and impact.
- QMD: `/docs`, markdown-heavy repo knowledge, requirements, plans, and design notes.
- DeepWiki: GitHub repository architecture and generated repo documentation.
- Context7: current external-library documentation.
- Official docs or source repository: external-library fallback when Context7 is unavailable.
- Native search: string literals, configs, logs, error text, or fallback when structured tools are unavailable.

Unavailable tools are not failures by themselves. Record them under `Tools Unavailable` in `context-manifest.md` and continue with the best available source. Never say a tool was used if it was not available.

## Context Manifest

Every serious workflow should keep `context-manifest.md` current:

```text
Goal Terms:
Queries Run:
Tools Available:
Tools Unavailable:
Code Sources:
Repo Docs Sources:
External Docs Checked:
Selected Context For Packets:
Confidence:
Unknowns:
```

Use the manifest as the handoff to subagents. Do not make workers rediscover the same baseline context unless their packet specifically requires deeper investigation.

## Packet Evidence Format

Packet results should separate:

- Facts: directly supported by code, docs, commands, or official external references.
- Inferences: reasoned conclusions from facts.
- Assumptions: choices made because evidence is incomplete.
- Unknowns: missing information that may affect correctness.

Important claims should include the source used. For code behavior, prefer symbol, file, function, route, or call-path evidence. For `/docs`, prefer QMD result file paths and headings. For external libraries, record the docs source and date checked.

## Conflict Resolution

When sources disagree:

- Behavior comes from current code and structural tools.
- Project intent comes from repo docs, plans, issues, or requirements.
- External API behavior comes from current official docs, Context7, package source, or release notes.

If the conflict cannot be resolved, keep it in `Unknowns` and report the risk clearly.

## Examples

Codebase change:

- Use CodeGraph to find symbols and callers.
- Use QMD to find repo docs that describe intended behavior.
- Assign implementation packets only after sources are recorded.

Docs-heavy repo:

- Use QMD as the primary `/docs` discovery layer.
- Use CodeGraph only to validate claims that affect runtime behavior.

External-library update:

- Use Context7 when available.
- If unavailable, use official docs or package source.
- Record missing Context7 as a tool limitation, not as a failed workflow.
