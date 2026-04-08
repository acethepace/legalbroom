---
title: "Legal Query Testing & RAG Engine Optimization Implementation Plan"
design_ref: "docs/maestro/plans/2026-04-05-legal-query-testing-design.md"
created: "2026-04-05T01:45:00Z"
status: "draft"
total_phases: 5
estimated_files: 8
task_complexity: "complex"
---

# Legal Query Testing & RAG Engine Optimization Implementation Plan

## Plan Overview

- **Total phases**: 5
- **Agents involved**: `debugger`, `tester`
- **Estimated effort**: Complex refactor of the RAG engine foundation combined with a significant expansion of the automated test suite.

## Dependency Graph

```
Phase 1 (Foundation & Keys)
    |
Phase 2 (LLM Factory & Core Refactor)
    |
Phase 3 (Legal Query Test Infrastructure)
    |
Phase 4 (Semantic Validation & Suite Expansion)
    |
Phase 5 (Provider Switch Verification)
```

## Execution Strategy

| Stage | Phases | Execution | Agent Count | Notes |
|-------|--------|-----------|-------------|-------|
| 1     | Phase 1 | Sequential | 1 | Config & API Keys |
| 2     | Phase 2 | Sequential | 1 | Backend Factory Pattern |
| 3     | Phase 3 | Sequential | 1 | Test Harness |
| 4     | Phase 4 | Sequential | 1 | 10+ Query Assertions |
| 5     | Phase 5 | Sequential | 1 | Final Switch Check |

---

## Phase 1: Foundation & Keys

### Objective
Update the project configuration with the new OpenAI and CourtListener API keys and enable non-buffered logging.

### Agent: `debugger`
### Parallel: No

### Files to Modify
- `.env.example` — Add `OPENAI_API_KEY`, `LLM_PROVIDER`, and update `COURTLISTENER_API_KEY`.
- `docker-compose.yml` — Pass new environment variables to the backend and ensure `PYTHONUNBUFFERED=1`.
- `backend/requirements.txt` — Add `langchain-openai`.

### Validation
- `docker compose config` to verify the new env vars are correctly mapped.

---

## Phase 2: LLM Factory & Core Refactor

### Objective
Implement the `LLMFactory` and refactor the `RAGEngine` to use provider-agnostic model instantiation.

### Agent: `debugger`
### Parallel: No

### Files to Create
- `backend/app/rag/factory.py` — Implement `LLMFactory` with support for `openai` and `ollama` providers.

### Files to Modify
- `backend/app/rag/engine.py` — Update `__init__` to consume the factory and remove hardcoded `ChatOllama` dependencies. Revert/cleanup debug logs.

### Implementation Details
- `LLMFactory` should use `LLM_PROVIDER` env var to determine the default.
- Support `gpt-4o-mini` for OpenAI and `llama3:8b` for Ollama.

### Validation
- Start backend and verify (via logs) that it initializes the OpenAI provider by default.

---

## Phase 3: Legal Query Test Infrastructure

### Objective
Setup the directory structure and shared utilities for the new legal query test suite.

### Agent: `tester`
### Parallel: No

### Files to Create
- `tests/legal_queries/conftest.py` — Shared fixtures for legal query tests (browser setup, common helpers).
- `tests/legal_queries/test_base.py` — Base test class with reusable assertion logic for citations and status messages.

### Validation
- Run `pytest tests/legal_queries/` and verify the harness initializes correctly.

---

## Phase 4: Semantic Validation & Suite Expansion

### Objective
Implement the 10+ landmark legal query tests with specific semantic and citation assertions.

### Agent: `tester`
### Parallel: No

### Files to Create
- `tests/legal_queries/test_constitutional.py` — Fourth Amendment, Qualified Immunity.
- `tests/legal_queries/test_employment.py` — Constructive Dismissal, Non-competes.
- `tests/legal_queries/test_admin_corporate.py` — Chevron, SEC/Crypto.
- `tests/legal_queries/test_criminal.py` — Miranda, Sixth Amendment.

### Implementation Details
- Use regex-based semantic assertions (e.g., `expect(page.locator(...)).to_contain_text(re.compile(r"search|seizure", re.I))`).
- Verify `[Source N]` clickable links.

### Validation
- `pytest tests/legal_queries/` — All 10+ cases must pass.

---

## Phase 5: Provider Switch Verification

### Objective
Verify that the system can still function when switched back to local Ollama.

### Agent: `debugger`
### Parallel: No

### Validation
- Switch `LLM_PROVIDER=ollama` in `.env`.
- Run `python3 tests/test_ws_direct.py` to verify tool-calling still works (even if slow).
- Switch back to `openai` for final handoff.

---

## File Inventory

| # | File | Phase | Purpose |
|---|------|-------|---------|
| 1 | `backend/app/rag/factory.py` | 2 | Multi-provider abstraction |
| 2 | `backend/app/rag/engine.py` | 2 | Engine refactor |
| 3 | `tests/legal_queries/conftest.py` | 3 | Test harness setup |
| 4 | `tests/legal_queries/test_constitutional.py` | 4 | Landmark query assertions |
| 5 | `tests/legal_queries/test_employment.py` | 4 | Landmark query assertions |
| 6 | `tests/legal_queries/test_admin_corporate.py` | 4 | Landmark query assertions |
| 7 | `tests/legal_queries/test_criminal.py` | 4 | Landmark query assertions |

## Execution Profile

```
Execution Profile:
- Total phases: 5
- Parallelizable phases: 0
- Sequential-only phases: 5
- Estimated sequential wall time: 8-10 agent turns per phase avg.

Note: Native parallel execution is disabled to ensure the foundational factory pattern is fully verified before the test suite expansion begins.
```
