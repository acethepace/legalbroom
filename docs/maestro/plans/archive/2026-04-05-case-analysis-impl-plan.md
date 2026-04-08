---
title: "Case Analysis Page and RAG Agent Upgrade Implementation Plan"
design_ref: "docs/maestro/plans/2026-04-05-case-analysis-design.md"
created: "2026-04-05T03:15:00Z"
status: "draft"
total_phases: 3
estimated_files: 5
task_complexity: "complex"
---

# Case Analysis Page and RAG Agent Upgrade Implementation Plan

## Plan Overview

- **Total phases**: 3
- **Agents involved**: `coder`, `tester`
- **Estimated effort**: Implementation of a new Next.js route, refactoring the RAG engine for a multi-step evaluation process, and creating e2e tests.

## Dependency Graph

```text
Phase 1 (Frontend UI)
    |
Phase 2 (Backend Two-Step RAG)
    |
Phase 3 (End-to-End Testing)
```

## Execution Strategy

| Stage | Phases | Execution | Agent Count | Notes |
|-------|--------|-----------|-------------|-------|
| 1     | Phase 1 | Sequential | 1 | Frontend |
| 2     | Phase 2 | Sequential | 1 | Backend |
| 3     | Phase 3 | Sequential | 1 | Testing |

## Phase 1: Frontend UI

### Objective
Create the new `/analysis` page where lawyers can enter case details, and update the home page to redirect there.

### Agent: `coder`
### Parallel: false

### Files to Create
- `frontend/src/app/analysis/page.tsx` — The new route for case analysis. Integrates the `AnalysisForm` and existing `SourcesPanel`.
- `frontend/src/components/AnalysisForm.tsx` — Form component with a large text area for entering case details.

### Files to Modify
- `frontend/src/app/page.tsx` — Update the existing Search button to use `next/navigation` to redirect to `/analysis`.
- `frontend/src/hooks/useChat.ts` — Modify or extend to handle sending the larger case details payload and managing the granular status updates.

### Implementation Details
- Ensure the `AnalysisForm` sends a JSON payload structured appropriately for the WebSocket endpoint (e.g., `{"case_details": "..."}`).
- Handle the new status messages gracefully in the UI.

### Validation
- `npm run build` in the `frontend` directory.

### Dependencies
- Blocked by: None
- Blocks: [2]

---

## Phase 2: Backend Two-Step RAG

### Objective
Extend the `RAGEngine` to perform the intermediate relevance grading step before synthesis.

### Agent: `coder`
### Parallel: false

### Files to Modify
- `backend/app/rag/engine.py` — Update `stream_answer` to support the new two-step flow. After fetching from CourtListener, make a prompt call to the LLM to grade the relevance of each case against the `case_details`. Filter the cases, then proceed to the final synthesis. Add intermediate `yield {"type": "status", "text": "Grading case relevance..."}`.
- `backend/main.py` — Update the WebSocket endpoint logic if the expected payload structure changes to support `case_details`.

### Implementation Details
- Use LangChain to structure the grading prompt (e.g., "Given these case details, identify which of the following search results are highly relevant...").
- Parse the grading response to filter the `cl_results` list.
- Pass only the filtered list to the final synthesis prompt.
- Retain the newly built citation filtering from the previous session.

### Validation
- `python3 -m py_compile backend/app/rag/engine.py`

### Dependencies
- Blocked by: [1]
- Blocks: [3]

---

## Phase 3: End-to-End Testing

### Objective
Verify the full flow from the frontend form submission to the two-step backend analysis.

### Agent: `tester`
### Parallel: false

### Files to Create
- `tests/e2e_case_analysis_test.py` — Playwright test script.

### Implementation Details
- Navigate to `/analysis`.
- Fill the case details text area with a sample legal scenario.
- Submit the form.
- Assert that the "Grading case relevance..." status appears.
- Assert that the final summary cites the relevant cases.

### Validation
- `pytest tests/e2e_case_analysis_test.py`

### Dependencies
- Blocked by: [2]
- Blocks: None

---

## File Inventory

| # | File | Phase | Purpose |
|---|------|-------|---------|
| 1 | `frontend/src/app/analysis/page.tsx` | 1 | New UI Route |
| 2 | `frontend/src/components/AnalysisForm.tsx` | 1 | Form Component |
| 3 | `frontend/src/app/page.tsx` | 1 | Redirect Logic |
| 4 | `frontend/src/hooks/useChat.ts` | 1 | WS Hook Updates |
| 5 | `backend/app/rag/engine.py` | 2 | Relevance Grading Logic |
| 6 | `backend/main.py` | 2 | WS Payload Handling |
| 7 | `tests/e2e_case_analysis_test.py` | 3 | Playwright Tests |

## Risk Classification

| Phase | Risk | Rationale |
|-------|------|-----------|
| 1     | LOW | Standard Next.js routing and component creation. |
| 2     | HIGH | Complex prompt engineering required to reliably grade cases. |
| 3     | MEDIUM | Playwright tests involving LLM streaming can be flaky. |

## Execution Profile

```text
Execution Profile:
- Total phases: 3
- Parallelizable phases: 0 (in 0 batches)
- Sequential-only phases: 3
- Estimated parallel wall time: N/A
- Estimated sequential wall time: 30 minutes

Note: Native subagents currently run without user approval gates.
All tool calls are auto-approved without user confirmation.
```

| Phase | Agent | Model | Est. Input | Est. Output | Est. Cost |
|-------|-------|-------|-----------|------------|----------|
| 1 | coder | gemini-3.1-pro-preview | 4000 | 1000 | $0.08 |
| 2 | coder | gemini-3.1-pro-preview | 6000 | 1000 | $0.10 |
| 3 | tester | gemini-3.1-pro-preview | 3000 | 500 | $0.05 |
| **Total** | | | **13000** | **2500** | **$0.23** |