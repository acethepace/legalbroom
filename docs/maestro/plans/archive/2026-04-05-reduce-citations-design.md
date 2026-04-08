---
title: "Citation Filtering Design Document"
created: "2026-04-05T02:00:00Z"
status: "approved"
authors: ["TechLead", "User"]
type: "design"
design_depth: "quick"
task_complexity: "medium"
---

# Citation Filtering Design Document

## Problem Statement

Currently, the Legal AI Assistant returns all search results from CourtListener as citations in the UI, regardless of whether the LLM actually found them relevant and cited them in its response. This clutters the UI with unrelated citations. We need a way for the LLM's actual usage of sources to determine which citations are displayed.

## Requirements

### Functional Requirements

1. **REQ-1**: Intercept the generated text stream from the LLM and accumulate the full response.
2. **REQ-2**: Parse the accumulated text to find all instances of `[Source N]`.
3. **REQ-3**: Filter the `all_citations` payload so only those sources explicitly cited by the LLM are yielded to the frontend.

## Approach

### Selected Approach

**Post-generation regex filtering**

We will update `backend/app/rag/engine.py` to intercept the streamed response from the LLM, accumulate the full text, and use a regular expression (e.g., `\[Source (\d+)\]`) to extract the exact source IDs cited by the model. 
Before yielding the final `{"type": "citations", "payload": ...}` message to the frontend, we will filter the `all_citations` array to include only those citations whose IDs match the extracted source IDs.

## Agent Team

| Phase | Agent(s) | Parallel | Deliverables |
|-------|----------|----------|--------------|
| 1     | coder    | No       | Filter logic in engine.py |
| 2     | debugger | No       | Test validation |

## Risk Assessment

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| The LLM cites sources incorrectly | MEDIUM | LOW | The system prompt strictly enforces the `[Source N]` format. Regex can handle minor spacing issues. |

## Success Criteria

1. Only citations that are actually present in the LLM's text output as `[Source N]` are displayed in the Sources Panel.
