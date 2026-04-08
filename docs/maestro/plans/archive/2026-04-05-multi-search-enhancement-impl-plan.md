---
title: "Iterative Search Loop Enhancement Implementation Plan"
design_ref: "docs/maestro/plans/2026-04-05-multi-search-enhancement-design.md"
created: "2026-04-05T10:15:00Z"
status: "draft"
total_phases: 2
estimated_files: 1
task_complexity: "medium"
---

# Iterative Search Loop Enhancement Implementation Plan

## Plan Overview

- **Total phases**: 2
- **Agents involved**: `coder`, `tester`
- **Estimated effort**: Refactoring the RAG engine's case analysis pipeline to support autonomous search iteration.

## Dependency Graph

```text
Phase 1 (Iterative Loop Logic)
    |
Phase 2 (E2E Validation)
```

## Execution Strategy

| Stage | Phases | Execution | Agent Count | Notes |
|-------|--------|-----------|-------------|-------|
| 1     | Phase 1 | Sequential | 1 | Core Logic |
| 2     | Phase 2 | Sequential | 1 | Testing |

---

## Phase 1: Iterative Loop Logic

### Objective
Refactor `RAGEngine.stream_case_analysis` to support up to 3 sequential search iterations driven by LLM evaluation.

### Agent: `coder`
### Parallel: false

### Files to Modify
- `backend/app/rag/engine.py`:
    - Introduce a `while` loop around the search and grading logic.
    - Update the `grading_prompt` to request a JSON object with `relevant_ids`, `needs_more_search`, and `next_search_query`.
    - Accumulate `relevant_results` and `all_citations` across loop iterations.
    - Yield a status update (e.g., "Refining search...") when a second or third iteration begins.
    - Ensure the final synthesis uses the full accumulated context.

### Implementation Details
- Maximum iterations: 3.
- Use robust JSON parsing (with regex extraction) for the grading response.
- Ensure source IDs (`[Source N]`) remain unique across accumulated results.

### Validation
- `python3 -m py_compile backend/app/rag/engine.py`

### Dependencies
- Blocked by: None
- Blocks: [2]

---

## Phase 2: E2E Validation

### Objective
Verify that the LLM can autonomously trigger a second search and synthesize results from both iterations.

### Agent: `tester`
### Parallel: false

### Files to Create
- `tests/multi_search_test.py`: A Playwright test case that provides a scenario designed to require refinement (e.g., a broad initial query that needs more specific legal terms).

### Implementation Details
- Assert that the "Refining search..." or similar status message appears.
- Assert that the final response contains citations from multiple search batches.

### Validation
- `pytest tests/multi_search_test.py`

### Dependencies
- Blocked by: [1]
- Blocks: None

---

## File Inventory

| # | File | Phase | Purpose |
|---|------|-------|---------|
| 1 | `backend/app/rag/engine.py` | 1 | Core refactor |
| 2 | `tests/multi_search_test.py` | 2 | E2E Verification |

## Risk Classification

| Phase | Risk | Rationale |
|-------|------|-----------|
| 1 | MEDIUM | Prompt complexity for reliable JSON output and loop state management. |
| 2 | LOW | Standard Playwright verification. |

## Execution Profile

```text
Execution Profile:
- Total phases: 2
- Parallelizable phases: 0
- Sequential-only phases: 2
- Estimated parallel wall time: N/A
- Estimated sequential wall time: 15-20 minutes

Note: All tool calls are auto-approved without user confirmation.
Subagents will exclusively use the gemini-3.1-pro-preview model.
```

| Phase | Agent | Model | Est. Input | Est. Output | Est. Cost |
|-------|-------|-------|-----------|------------|----------|
| 1 | coder | gemini-3.1-pro-preview | 4000 | 1500 | $0.10 |
| 2 | tester | gemini-3.1-pro-preview | 3000 | 500 | $0.05 |
| **Total** | | | **7000** | **2000** | **$0.15** |
