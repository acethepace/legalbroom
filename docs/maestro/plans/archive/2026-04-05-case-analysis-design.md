---
title: "Case Analysis Page and RAG Agent Upgrade"
created: "2026-04-05T03:00:00Z"
status: "approved"
authors: ["TechLead", "User"]
type: "design"
design_depth: "standard"
task_complexity: "complex"
---

# Case Analysis Page and RAG Agent Upgrade Design Document

## Problem Statement

The search button on the UI currently does nothing. Lawyers need a dedicated space to enter case details and receive a tailored legal analysis. The assistant must search CourtListener, intelligently score and filter the retrieved cases for relevance to the provided details in a two-step process, and synthesize a comprehensive summary, streaming granular status updates along the way. — *[Rationale: The two-step process ensures the LLM decides the most relevant cases before synthesis, improving accuracy.]*

## Requirements

### Functional Requirements

1. **REQ-1**: Create a new Next.js page at `/analysis` containing a text area form for lawyers to input case details.
2. **REQ-2**: Update the existing Search button on the UI to redirect users to this new `/analysis` page.
3. **REQ-3**: Extend the backend `RAGEngine` to perform a two-step analysis: first fetching CourtListener cases and scoring their relevance against the user's case details, then synthesizing a final summary.

### Non-Functional Requirements

1. **REQ-N1**: The WebSocket connection must stream granular status updates (e.g., "Searching...", "Grading case relevance...", "Synthesizing summary...") to the frontend to mitigate perceived latency.

### Constraints

- Must integrate cleanly with the existing FastAPI backend and Next.js frontend architecture.
- Follow the orchestrator instruction to delegate implementation tasks specifically to the `gemini-3.1-pro-preview` model for subagents.

## Approach

### Selected Approach

**Two-Step RAG Agent**

The frontend will host a dedicated `/analysis` page where lawyers enter case details. This triggers the backend `RAGEngine` via WebSocket. The LLM extracts search keywords from the details, fetches CourtListener results, explicitly scores the relevance of each result against the case details (the intermediate grading step), and filters the list before synthesizing a final, tailored legal summary. Statuses like "Grading case relevance..." are streamed throughout. — *[Rationale: This unified stream minimizes latency round trips while fulfilling the requirement for the LLM to internally decide relevance.]*

### Alternatives Considered

#### Separate Scoring API

- **Description**: Create a standard REST endpoint `/api/analyze_relevance` that takes the case details, fetches cases, and returns a scored list. The frontend then sends the scored list to the existing WebSocket endpoint for synthesis.
- **Pros**: Decouples the scoring step from the synthesis step, making testing easier.
- **Cons**: Increases frontend complexity by requiring it to orchestrate multiple backend calls. Adds a round trip.
- **Rejected Because**: Adds unnecessary round-trip latency and complicates the frontend's state management for status tracking.

### Decision Matrix

| Criterion | Weight | Two-Step RAG Agent | Separate Scoring API |
|-----------|--------|--------------------|----------------------|
| Latency | 40% | 4: Avoids extra round trips | 2: Adds a round trip |
| Code Complexity | 30% | 4: Keeps logic encapsulated in backend | 2: Splits orchestration across stack |
| Granular Status | 30% | 5: Easy to stream status via WS | 3: REST call hides status |
| **Weighted Total** | | **4.3** | **2.3** |

## Architecture

### Component Diagram

```
[Next.js Client] --> (Redirect) --> [/analysis Page Form]
                                         |
                                         v
                                   [WebSocket Stream]
                                         |
                                         v
[FastAPI Backend] --> [RAGEngine (Extract Keywords)] --> [CourtListener API]
                                         |
                                         v
                            [RAGEngine (Grade Relevance)]
                                         |
                                         v
                            [RAGEngine (Synthesize)] --> [Next.js Client]
```

### Data Flow

1. User clicks Search -> redirected to `/analysis`.
2. User enters case details and submits.
3. Next.js opens a WebSocket to FastAPI with the case details payload.
4. RAGEngine calls CourtListener based on keywords extracted from details.
5. RAGEngine streams "Grading case relevance..." to frontend.
6. A sub-agent LLM call grades relevance, returning a filtered list of cases.
7. RAGEngine streams "Synthesizing summary..." to frontend.
8. The final LLM call synthesizes the case analysis and streams content and the filtered citations payload.

### Key Interfaces

```typescript
// Frontend payload
interface CaseAnalysisRequest {
  case_details: string;
}

// WebSocket Status Update
interface StatusMessage {
  type: "status";
  text: string;
}
```

## Agent Team

| Phase | Agent(s) | Parallel | Deliverables |
|-------|----------|----------|--------------|
| 1     | coder    | No       | Frontend UI (`/analysis` page, redirection) |
| 2     | coder    | No       | Backend two-step RAG update |
| 3     | tester   | No       | End-to-end testing |

## Risk Assessment

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| Two-step grading increases latency | MEDIUM | HIGH | Provide granular, streamed status updates over the WebSocket to keep the user engaged. |
| The LLM scores cases inconsistently | HIGH | MEDIUM | Provide a strong few-shot system prompt for the grading step that strictly defines relevance based on the lawyer's case details. |

## Success Criteria

1. The Search button redirects to the new `/analysis` page.
2. Form submission connects via WebSocket and streams "Grading case relevance..." and other granular statuses.
3. The final response only cites cases the LLM has explicitly evaluated as relevant.
