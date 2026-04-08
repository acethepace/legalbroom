---
title: "Legal Query Testing & RAG Engine Optimization"
created: "2026-04-05T01:30:00Z"
status: "approved"
authors: ["TechLead", "User"]
type: "design"
design_depth: "deep"
task_complexity: "complex"
---

# Legal Query Testing & RAG Engine Optimization Design Document

## Problem Statement

The **Legalbroom AI Assistant** is currently experiencing significant latency, with the RAG engine appearing "stuck" for 50-60 seconds during the initial query analysis. This is caused by non-streaming blocking calls to local Llama 3 hardware. Additionally, the assistant lacks comprehensive automated test coverage for its core legal research capabilities across multiple jurisdictions and doctrines.

This project will refactor the RAG engine to support **multi-provider LLM integration** (starting with OpenAI GPT-4o-mini), providing near-instant analysis and synthesis. We will also implement a **Legal Query Validation Suite** that automatically verifies the assistant's accuracy, citation integrity, and tool-calling compliance for 10+ landmark legal queries. — *[Rationale: Resolves confirmed hardware-driven latency while maintaining high reasoning quality.]*

## Requirements

### Functional Requirements

1. **REQ-1 (Multi-provider LLM)**: Implement an `LLMFactory` in the RAG engine to support switching between OpenAI and Ollama via the `LLM_PROVIDER` environment variable.
2. **REQ-2 (OpenAI Integration)**: Integrate **GPT-4o-mini** as the primary LLM provider to resolve the "stuck" analysis issue.
3. **REQ-3 (Corrected Search API)**: Update the CourtListener integration with the provided key (`028a62ec6bfdf7d0cad0f46115f6de26af378a44`) and ensure the tool-calling loop is robust.
4. **REQ-4 (Legal Query Suite)**: Develop an automated test suite (Playwright/Pytest) covering Constitutional, Employment, Administrative, and Criminal Procedure categories.
5. **REQ-5 (Semantic + Citation Validation)**: Test assertions must verify clickable [Source N] citations and the presence of core legal terminology.

### Non-Functional Requirements

1. **REQ-N1 (Performance)**: The initial "Analyzing query..." status should transition to "Searching..." or "Synthesizing..." in under 3 seconds using OpenAI.
2. **REQ-N2 (Security)**: OpenAI and CourtListener keys must be managed server-side via `docker-compose.yml` environment variables.

## Approach

### Selected Approach

**Provider-Agnostic RAG with Automated Legal Validation**

We will implement a factory pattern to abstract the LLM provider, allowing the system to use OpenAI's high-speed cloud inference while retaining local Ollama compatibility. This architecture resolves the latency bottleneck while providing a robust foundation for the new automated legal query test suite. — *[Rationale: Provides the "easy to switch" requirement while isolating provider-specific configurations.]*

### Alternatives Considered

#### Granular Heartbeats (Ollama)

- **Description**: Add periodic status messages during the 60s processing window.
- **Pros**: Maintains local data privacy.
- **Cons**: Does not reduce actual user wait time.
- **Rejected Because**: User indicated the current 60s wait is "too long."

## Architecture

### Component Diagram

```
[React Frontend] <--- WS ---> [FastAPI Backend]
                                     |
                                     v
                            [LLMFactory] ----> [OpenAI (GPT-4o-mini)]
                                     |   `---> [Local Ollama (Llama 3)]
                                     v
                            [RAGEngine] <---> [CourtListener API]
```

### Data Flow

1. **Query**: User asks a legal question via WebSocket.
2. **Model Selection**: `RAGEngine` requests a model instance from `LLMFactory` (defaults to OpenAI).
3. **Fast Analysis**: OpenAI analyzes the query in <2 seconds.
4. **Search**: `RAGEngine` triggers a tool call to CourtListener.
5. **Synthesis**: OpenAI generates a synthesized response with citations.
6. **Validation**: The new Test Suite triggers this flow and asserts on results.

### Key Interfaces

```python
# LLM Factory Signature
class LLMFactory:
    @staticmethod
    def get_model(provider: str = "openai") -> BaseChatModel:
        pass
```

## Agent Team

| Phase | Agent(s) | Parallel | Deliverables |
|-------|----------|----------|--------------|
| 1     | Debugger | No       | `LLMFactory`, API keys, and latency fix. |
| 2     | Tester   | No       | Comprehensive Legal Query Test Suite. |
| 3     | Debugger | No       | Provider switch verification. |

## Risk Assessment

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| OpenAI API failure | HIGH | LOW | `LLMFactory` fallback to local Ollama. |
| Flaky semantic tests | MEDIUM | MEDIUM | Use regex and keyword matching for assertions. |

## Success Criteria

1. "Analyzing query..." status transitions to "Searching..." in **under 3 seconds**.
2. 100% of landmark legal queries in the test suite pass citation and semantic checks.
3. Easy switch verified via `LLM_PROVIDER` environment variable.
