---
title: "Legal AI Assistant MVP"
created: "2026-04-04T12:00:00Z"
status: "approved"
authors: ["TechLead", "User"]
type: "design"
design_depth: "standard"
task_complexity: "complex"
---

# Legal AI Assistant MVP Design Document

## Problem Statement

The **Legalbroom AI Assistant** is a full-stack MVP designed to provide high-precision semantic search and chat-based summaries for legal documents (PDFs). Legal professionals often struggle to find specific precedents within large document sets and need reliable citations that link back to the source text. 

Current general-purpose RAG systems often fail to capture the hierarchical structure of legal documents (e.g., Articles, Sections) and provide vague citations. This project aims to bridge that gap by implementing **Section-Aware Chunking** and a specialized **Citations UI** in React that supports **Highlight + Sync Scroll** to verify the assistant's claims directly against the original PDF context.

## Requirements

### Functional Requirements

1. **REQ-1 (Ingestion)**: Implement **Section-Aware Chunking** using a robust PDF parser (e.g., PyMuPDF) to detect hierarchical markers (e.g., 'Article IV', 'Section 1') and use those as hard boundaries for the semantic chunker.
2. **REQ-2 (Chat UI)**: Build a React chat interface that displays 'Sources' in a side panel, supporting **Highlight + Sync Scroll** to the original PDF text when a citation is clicked.
3. **REQ-3 (Automated Testing)**: Use **BrowserMCP (Computer Use)** to automatically:
   a) Navigate to localhost:3000.
   b) Upload a dummy 'precedent.pdf'.
   c) Query the chat and verify that a citation link appears in the UI.
4. **REQ-4 (Auto-Debugging)**: A **Debugger Agent** must automatically fix React code if the Tester Agent finds a UI bug during automated testing.

### Non-Functional Requirements

1. **REQ-N1 (Local Inference)**: Use **Local Llama 3 (via Ollama)** for all LLM-driven tasks (summarization, citation extraction).
2. **REQ-N2 (Persistence)**: Mount a shared local `data/` directory to both FastAPI and Qdrant containers for PDF storage and vector store persistence.
3. **REQ-N3 (Real-time Sync)**: Use **WebSockets (WS)** for bidirectional JSON communication between React and FastAPI for chat and citation metadata sync.

### Constraints

- Backend: Python/FastAPI + LangChain.
- Vector Store: Qdrant (Local Docker).
- Frontend: Next.js + Tailwind.

## Approach

### Selected Approach

**Pragmatic Legal RAG**

We'll build a robust RAG pipeline using FastAPI and Qdrant, leveraging **Section-Aware Chunking** (PyMuPDF-based) to ensure our citation metadata captures hierarchical document structure (Articles, Sections) for high-precision highlights. — *[Rationale: Balancing precision and MVP speed with proven libraries]*

### Alternatives Considered

#### Deep Semantic Extraction

- **Description**: Adds a dedicated metadata-extraction layer (e.g. Docling) and a reranker.
- **Pros**: Peak accuracy for irregular layouts.
- **Cons**: High complexity, latency, and operational overhead.
- **Rejected Because**: The pragmatic approach is sufficient for the MVP's scope and provides faster feedback loops.

### Decision Matrix

| Criterion | Weight | Pragmatic Legal RAG | Deep Semantic Extraction |
|-----------|--------|----------------------|---------------------------|
| Citation Precision | 40% | 4: Section-aware chunking | 5: Dedicated extraction + reranker |
| MVP Speed | 30% | 5: Standard libraries | 3: Pipeline complexity |
| System Latency | 20% | 4: Standard RAG flow | 2: Extra preprocessing |
| Operational Ease | 10% | 5: Simple Docker setup | 3: More dependencies |
| **Weighted Total** | | **4.5** | **3.6** |

## Architecture

### Component Diagram

```
[React/Next.js] <--- WS ---> [FastAPI] <---> [Qdrant]
      |                        |              |
      v                        v              v
[PDF Side Panel]         [Ollama/Llama 3] [Local /data]
```

### Data Flow

1. **Ingestion**: User uploads PDF → FastAPI extracts text/headers/coordinates → Chunks by section → Stores in Qdrant with page/coordinate metadata.
2. **Retrieval**: User queries via WebSocket → FastAPI retrieves relevant chunks → Llama 3 generates a response with structured citation IDs.
3. **Visualization**: FastAPI sends the response + metadata to React → React displays the message → User clicks a citation link → Side panel scrolls/highlights the original PDF section based on the metadata.

### Key Interfaces

```typescript
// WebSocket Message Schema
interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  citations?: Citation[];
}

interface Citation {
  id: string;
  text: string;
  pageNumber: number;
  coordinates: { x: number; y: number; width: number; height: number };
}
```

## Agent Team

| Phase | Agent(s) | Parallel | Deliverables |
|-------|----------|----------|--------------|
| 1     | Architect | No       | Design & Implementation Plan |
| 2     | Coder    | No       | Backend (FastAPI, Qdrant) & Frontend (React/WS) |
| 3     | Tester   | No       | Automated Browser-based Testing (Upload/Query/Citation) |
| 4     | Debugger | No       | UI bug fixes (if tests fail) and final verification |

## Risk Assessment

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| Local Llama 3 Latency | MEDIUM | HIGH | Stream responses via WebSockets for interactive feedback. |
| PDF Layout Complexity | MEDIUM | MEDIUM | Robust pattern-based parsing with fallback to character-based splitting. |
| Citation Metadata Accuracy | HIGH | MEDIUM | Strict JSON-based citation schema and page-level chunking metadata. |

## Success Criteria

1. **FastAPI/Qdrant/React** containers are running and communicating correctly.
2. **'precedent.pdf'** is correctly ingested and indexed by section-aware chunking.
3. Chat response for **'Summarize article 4'** includes a clickable citation link.
4. Clicking the citation **highlights the correct text** in the side-panel PDF viewer.
5. **Automated test** (BrowserMCP) passes without manual intervention.
