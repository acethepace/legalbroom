---
title: "CourtListener Integration & Live Search"
created: "2026-04-04T14:00:00Z"
status: "approved"
authors: ["TechLead", "User"]
type: "design"
design_depth: "standard"
task_complexity: "complex"
---

# CourtListener Integration Design Document

## Problem Statement

The **Legalbroom AI Assistant** is being refactored from a local document RAG system into a live search-integrated legal researcher. Legal professionals need to find relevant precedents across a vast database of existing case law, which is often difficult to search using traditional keyword-based systems.

This project will integrate the **CourtListener API** directly into the assistant's workflow. We will remove the current "Upload PDF" and "Local Search" features. Instead, the assistant will use **AI-Driven (Tool Calling)** to automatically search the CourtListener database based on user queries, synthesizing top results into a single, professional response with verifiable citations. — *[Rationale: Pivoting to live search increases the assistant's utility and reduces infrastructure complexity associated with document storage.]*

## Requirements

### Functional Requirements

1. **REQ-1 (Search Service)**: Implement a dedicated `CourtListenerService` in the FastAPI backend to handle search queries, data mapping (API JSON to internal citation model), and error handling.
2. **REQ-2 (AI-Driven Search)**: Integrate tool-calling into the `RAGEngine` (Llama 3) to allow the model to trigger searches on CourtListener automatically when legal context is required.
3. **REQ-3 (Synthesized Chat)**: Update the React frontend to display synthesized responses where clickable citations link directly to the CourtListener case details in the side panel.
4. **REQ-4 (System Cleanup)**: Completely remove the `PDFParser`, `SectionAwareChunker`, local PDF storage volumes, and the `/upload` API endpoint.

### Non-Functional Requirements

1. **REQ-N1 (API Security)**: Store the provided CourtListener API key as a server-side environment variable (`COURTLISTENER_API_KEY`).
2. **REQ-N2 (Real-time Feedback)**: Maintain the WebSocket-based streaming architecture to provide "Searching..." and "Synthesizing..." status updates to the user.
3. **REQ-N3 (Citation Integrity)**: Ensure that every claim made by the LLM is traceable back to a `[Source N]` marker corresponding to a verified CourtListener result.

### Constraints

- Backend: Python/FastAPI + LangChain.
- Search API: CourtListener (Free Law Project).
- Frontend: Next.js + Tailwind.
- Inference: Local Llama 3 (via Ollama).

## Approach

### Selected Approach

**Live AI-Driven Legal Search**

We'll transition to a live search architecture where the LLM (Llama 3) uses tool-calling to query CourtListener on-demand. Top results will be injected as ephemeral context for the current question, allowing for a lightweight and highly relevant RAG pipeline without permanent indexing. — *[Rationale: This approach provides the most up-to-date case law while eliminating the maintenance of a local vector index for millions of potential cases.]*

### Alternatives Considered

#### Hybrid Local/Remote RAG

- **Description**: Keep the local PDF ingestion and add CourtListener as a fallback.
- **Pros**: Handles both personal documents and public case law.
- **Cons**: High architectural complexity; confusing UI for mixed source citations.
- **Rejected Because**: The user explicitly requested removing the local document system in favor of direct live search.

## Architecture

### Component Diagram

```
[React Frontend] <--- WS ---> [FastAPI Backend] <---> [CourtListener API]
      |                             |
      v                             v
[Sources Side Panel]         [RAG Engine (Llama 3)]
```

### Data Flow

1. **Query**: User asks a legal question via WebSocket.
2. **Analysis**: `RAGEngine` analyzes the query and identifies the need for case law research.
3. **Search**: `RAGEngine` triggers a tool call to `CourtListenerService.search(query)`.
4. **Synthesis**: Backend retrieves case summaries/snippets, injects them into the LLM prompt, and generates a synthesized answer.
5. **Display**: Backend streams the response + case metadata to the React UI via WebSockets.
6. **Interaction**: User clicks a citation link; the Side Panel displays the full metadata and a link to the original CourtListener case.

### Key Interfaces

```typescript
// Updated Citation Schema for CourtListener
interface Citation {
  id: string; // Source N
  title: string; // Case name
  court: string;
  date_filed: string;
  snippet: string;
  url: string; // Direct link to CourtListener
}
```

## Agent Team

| Phase | Agent(s) | Parallel | Deliverables |
|-------|----------|----------|--------------|
| 1     | Architect | No       | Implementation Plan for CourtListener Integration |
| 2     | Coder    | No       | Backend (Service + Engine) & Frontend (Search UI) |
| 3     | Tester   | No       | Automated Search & Synthesis tests |
| 4     | Debugger | No       | Root cause fixes for API/UI bugs |

## Risk Assessment

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| CourtListener API Latency | MEDIUM | HIGH | Implement explicit "Searching..." status messages in the chat UI. |
| API Rate Limiting | MEDIUM | MEDIUM | Implement server-side caching for frequent queries. |
| Synthesis Quality | HIGH | LOW | Refine prompt templates with clear examples of citation mapping. |

## Success Criteria

1. **CourtListenerService** successfully retrieves and maps cases from the API.
2. **LLM** autonomously identifies when to search and calls the tool correctly.
3. **Chat response** contains clickable citations that update the side panel.
4. **All local ingestion code** and PDF volumes are successfully removed.
5. **E2E tests** pass for a multi-case legal research query.
