---
title: "Citation Filtering Implementation Plan"
design_ref: "docs/maestro/plans/2026-04-05-reduce-citations-design.md"
created: "2026-04-05T02:05:00Z"
status: "draft"
total_phases: 2
estimated_files: 1
task_complexity: "medium"
---

# Citation Filtering Implementation Plan

## Plan Overview

- **Total phases**: 2
- **Agents involved**: `coder`, `debugger`
- **Estimated effort**: Medium refactor of the RAG engine's citation yielding logic.

## Dependency Graph

```
Phase 1 (Filter Logic in RAG Engine)
    |
Phase 2 (Validation and Testing)
```

## Execution Strategy

| Stage | Phases | Execution | Agent Count | Notes |
|-------|--------|-----------|-------------|-------|
| 1     | Phase 1 | Sequential | 1 | Modify engine.py |
| 2     | Phase 2 | Sequential | 1 | Test |

## Phase 1: Filter Logic in RAG Engine

### Objective
Update `backend/app/rag/engine.py` to filter `all_citations` based on the sources actually cited by the LLM in its response.

### Agent: `coder`
### Parallel: No

### Files to Modify
- `backend/app/rag/engine.py` — Accumulate the streamed response content into a `full_response` string. Use regex (e.g., `re.findall(r"\[Source (\d+)\]", full_response)`) to extract the used source IDs. Filter the `all_citations` list to only include citations with matching IDs before yielding the `"type": "citations"` message.

### Implementation Details
- Ensure the regex handles potential formatting variations if necessary.
- Only yield citations that were present in the LLM output.

### Validation
- `python3 -m py_compile backend/app/rag/engine.py`

### Dependencies
- Blocked by: None
- Blocks: 2

---

## Phase 2: Validation and Testing

### Objective
Verify that the citation filtering works correctly and only used citations are returned.

### Agent: `debugger`
### Parallel: No

### Files to Modify
- None

### Implementation Details
- Restart the backend container (`docker compose restart backend`).
- Run a test query (e.g., `pytest tests/legal_queries/test_constitutional.py`) and inspect the backend logs or test output to ensure the citations are filtered.

### Validation
- All existing tests should pass, and visually checking the output should confirm fewer citations are returned.

### Dependencies
- Blocked by: 1
- Blocks: None

---

## File Inventory

| # | File | Phase | Purpose |
|---|------|-------|---------|
| 1 | `backend/app/rag/engine.py` | 1 | Filtering citations before yielding |

## Risk Classification

| Phase | Risk | Rationale |
|-------|------|-----------|
| 1     | LOW | Simple regex filtering at the end of the generator. |
| 2     | LOW | Testing existing functionality. |

## Execution Profile

```
Execution Profile:
- Total phases: 2
- Parallelizable phases: 0 (in 0 batches)
- Sequential-only phases: 2
- Estimated parallel wall time: N/A
- Estimated sequential wall time: 2 agent turns

Note: Native subagents currently run without user approval gates.
All tool calls are auto-approved without user confirmation.
```
