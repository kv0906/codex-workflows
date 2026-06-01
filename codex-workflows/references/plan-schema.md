# Plan Schema

Use this schema when a machine-readable workflow plan helps coordination. Keep `plan.md` as the human source of truth.

```json
{
  "goal": "string",
  "success_criteria": ["string"],
  "constraints": ["string"],
  "context": {
    "status": "not_started",
    "goal_terms": ["string"],
    "queries_run": [
      {
        "tool": "codegraph | qmd | deepwiki | context7 | official_docs | native_search",
        "query": "string",
        "result": "string",
        "source": "string or null"
      }
    ],
    "tools_available": ["string"],
    "tools_unavailable": ["string"],
    "sources": ["string"],
    "external_docs_checked": [
      {
        "library": "string",
        "source": "string",
        "checked_at": "ISO-8601 timestamp or date",
        "notes": "string"
      }
    ],
    "unknowns": ["string"]
  },
  "run_model": {
    "metadata": {
      "name": "short_snake_case",
      "description": "string",
      "when_to_use": "string"
    },
    "phases": [
      {
        "title": "string",
        "status": "planned | active | complete | skipped",
        "notes": "string"
      }
    ],
    "parallel_groups": [
      {
        "id": "string",
        "packet_ids": ["string"],
        "why_parallel": "string"
      }
    ],
    "pipeline_groups": [
      {
        "id": "string",
        "items": ["string"],
        "stages": ["string"],
        "why_pipeline": "string"
      }
    ],
    "budget": {
      "max_agents": "number or null",
      "max_parallel": "number or null",
      "notes": "string"
    },
    "failure_policy": "string"
  },
  "risks": [
    {
      "risk": "string",
      "approval_required": true,
      "mitigation": "string"
    }
  ],
  "max_concurrent_agents": 4,
  "max_total_agents": 12,
  "packets": [
    {
      "id": "01-discovery",
      "label": "repo inventory",
      "objective": "string",
      "context": "string",
      "files_or_sources": ["string"],
      "evidence_required": ["string"],
      "context_sources": ["string"],
      "tool_results_used": ["string"],
      "ownership": "string",
      "do": ["string"],
      "do_not": ["string"],
      "expected_output": "string",
      "status": "pending | in_progress | complete | failed | skipped | blocked | incomplete",
      "claims": ["string"],
      "unknowns": ["string"],
      "external_docs_checked": ["string"],
      "verification": ["string"]
    }
  ],
  "packet_statuses": {
    "complete": ["string"],
    "failed": ["string"],
    "skipped": ["string"],
    "blocked": ["string"],
    "incomplete": ["string"]
  },
  "synthesis": {
    "status": "not_started | in_progress | complete",
    "conflicts": ["string"],
    "unsupported_claims": ["string"],
    "unknowns": ["string"]
  },
  "integration_policy": {
    "owner": "parent",
    "conflict_resolution": "Inspect authoritative sources before choosing. Prefer codegraph for behavior, QMD/repo docs for project intent, and current external docs for library behavior.",
    "final_output": "string"
  },
  "verification": [
    {
      "check": "string",
      "command": "string or null",
      "required": true,
      "status": "pending"
    }
  ],
  "reusable_artifacts": ["string"]
}
```

Suggested defaults:

- `max_concurrent_agents`: 2-4 for normal work.
- `max_total_agents`: 6-12 unless the user approves a larger run.
- Packet IDs: prefix with two digits so files sort naturally.
- Status values: `pending`, `in_progress`, `complete`, `blocked`, `skipped`.
