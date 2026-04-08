---
title: "CourtListener Integration Implementation Plan"
design_ref: "docs/maestro/plans/2026-04-04-courtlistener-integration-design.md"
created: "2026-04-04T14:30:00Z"
status: "draft"
total_phases: 6
estimated_files: 10
task_complexity: "complex"
---

# CourtListener Integration Implementation Plan

## Plan Overview

- **Total phases**: 6
- **Agents involved**: `coder`, `tester`, `debugger`
- **Estimated effort**: Complex refactor including service implementation, tool-calling integration, and UI overhaul.

## Dependency Graph

```
Phase 1 (Foundation)
    |
Phase 2 (CourtListener Service)
    |
Phase 3 (RAG Engine & Tool-Calling)
    |
Phase 4 (Frontend Refactor)
    |
Phase 5 (System Cleanup)
    |
Phase 6 (Automated Testing)
```

## Execution Strategy

| Stage | Phases | Execution | Agent Count | Notes |
|-------|--------|-----------|-------------|-------|
| 1     | Phase 1 | Sequential | 1 | Config & Env |
| 2     | Phase 2 | Sequential | 1 | Backend Service |
| 3     | Phase 3 | Sequential | 1 | Tool-Calling |
| 4     | Phase 4 | Sequential | 1 | UI Transition |
| 5     | Phase 5 | Sequential | 1 | Removal of old code |
| 6     | Phase 6 | Sequential | 1 | E2E Validation |

---

## Phase 1: Foundation & Configuration

### Objective
Configure the project for CourtListener integration, including environment variables and dependency updates.

### Agent: `coder`
### Parallel: No

### Files to Modify
- `.env.example` — Add `COURTLISTENER_API_KEY`.
- `docker-compose.yml` — Pass `COURTLISTENER_API_KEY` to the backend.
- `backend/requirements.txt` — Add `httpx` for async API calls.

### Validation
- `docker compose config` to verify the new env vars are mapped.

---

## Phase 2: CourtListener Service Implementation

### Objective
Implement the dedicated `CourtListenerService` to handle API interactions.

### Agent: `coder`
### Parallel: No

### Files to Create
- `backend/app/services/courtlistener.py` — Async client for CourtListener Search API. Implements mapping from raw JSON to the internal `Citation` schema.

### Implementation Details
- Use `httpx.AsyncClient` for networking.
- Handle rate limits and common API errors.
- Include methods for: `search(query: str, limit: int = 5)`.

### Validation
- Run a standalone test script `tests/test_courtlistener_service.py` to verify API connectivity and mapping.

---

## Phase 3: RAG Engine Refactor (Tool-Calling)

### Objective
Update the `RAGEngine` to support AI-driven tool-calling for searches.

### Agent: `coder`
### Parallel: No

### Files to Modify
- `backend/app/rag/engine.py` — Implement tool-calling logic using LangChain. Define the `search_courtlistener` tool and update the prompt template.
- `backend/main.py` — Update the WebSocket handler to support tool execution status messages.

### Implementation Details
- Update the system prompt to explicitly instruct Llama 3 on when and how to use the search tool.
- Implement "Searching..." and "Synthesizing..." status flags in the WebSocket stream.

### Validation
- Query the WebSocket with a legal question and verify (via logs) that the tool is triggered.

---

## Phase 4: Frontend UI Overhaul

### Objective
Refactor the React UI to focus on chat and the new side-panel search results.

### Agent: `coder`
### Parallel: No

### Files to Modify
- `frontend/src/app/page.tsx` — Remove `Upload` button logic. Update dashboard to handle search result metadata.
- `frontend/src/components/SourcesPanel.tsx` — Update to display CourtListener case details (Court, Date, Snippet).
- `frontend/src/hooks/useChat.ts` — Update message state to handle new citation schema and status updates.

### Files to Delete
- `frontend/src/components/PDFViewer.tsx` — No longer needed.

### Validation
- Build and run the frontend; verify that the search results appear correctly in the side panel when a citation is clicked.

---

## Phase 5: System Cleanup

### Objective
Remove all legacy code related to local PDF ingestion and vector storage.

### Agent: `coder`
### Parallel: No

### Files to Delete
- `backend/app/ingestion/parser.py`
- `backend/app/ingestion/chunker.py`
- `backend/app/vector_store.py`
- `tests/create_test_pdf.py`
- `tests/validate_ingestion.py`

### Files to Modify
- `backend/main.py` — Remove `/upload` endpoint and vector store initialization.

### Validation
- `docker compose build` succeeds without the removed files.

---

## Phase 6: Automated Testing & Verification

### Objective
Execute the full E2E test suite to verify the new integration.

### Agent: `tester`
### Parallel: No

### Files to Create
- `tests/e2e_search_test.py` — Playwright script to verify the full flow: Query -> AI Search -> Synthesis -> Citation Interaction.

### Validation
- All test steps in `e2e_search_test.py` pass.

---

## File Inventory

| # | File | Phase | Purpose |
|---|------|-------|---------|
| 1 | `backend/app/services/courtlistener.py` | 2 | API Client |
| 2 | `backend/app/rag/engine.py` | 3 | Tool-calling refactor |
| 3 | `frontend/src/app/page.tsx` | 4 | UI Transition |
| 4 | `frontend/src/components/SourcesPanel.tsx` | 4 | Search metadata UI |
| 5 | `tests/e2e_search_test.py` | 6 | E2E automation |

## Execution Profile

```
Execution Profile:
- Total phases: 6
- Parallelizable phases: 0
- Sequential-only phases: 6
- Estimated sequential wall time: 8-10 agent turns per phase avg.

Note: Native parallel execution is disabled for this plan due to the high degree of refactoring and shared file modifications (main.py, etc.).
```
