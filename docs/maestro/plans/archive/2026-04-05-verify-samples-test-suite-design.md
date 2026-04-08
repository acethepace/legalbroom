---
title: "Landmark Scenario Relevance Suite"
created: "2026-04-05T14:30:00Z"
status: "approved"
authors: ["TechLead", "User"]
type: "design"
design_depth: "quick"
task_complexity: "medium"
---

# Landmark Scenario Relevance Suite Design Document

## Problem Statement

The Legalbroom AI Assistant provides users with four landmark legal scenarios (Constitutional, Employment, Corporate, and Administrative) as primary examples of its capabilities. Currently, while individual domain tests exist, there is no automated verification ensuring that these specific scenarios consistently result in high-quality, relevant precedents. This project will implement a dedicated automated test suite that executes these scenarios through the specialized **Case Analysis** interface and asserts that specific landmark cases (e.g., *Terry v. Ohio*, *Howey*) are correctly retrieved and cited in the final analysis.

## Requirements

### Functional Requirements

1. **REQ-1**: Create a new automated test suite `tests/legal_queries/test_landmark_samples.py`.
2. **REQ-2**: Implement test cases for the four primary sample legal scenarios (Vehicle Search, Non-Compete, Piercing the Veil, SEC/Crypto).
3. **REQ-3**: Assert that each scenario results in at least one valid `[Source N]` citation marker.
4. **REQ-4**: Assert that the response contains the specific landmark case name intended for that scenario (e.g., *Terry v. Ohio*).
5. **REQ-5**: Assert the presence of core legal terminology relevant to each domain.

### Non-Functional Requirements

1. **REQ-N1**: Tests must execute through the specialized `/analysis` frontend route.
2. **REQ-N2**: Tests must use case-insensitive matching for landmark names to increase resilience.

## Approach

### Selected Approach

**Landmark Scenario Relevance Suite**

We will implement a new Playwright/Pytest suite in `tests/legal_queries/test_landmark_samples.py` that inherits from the existing `BaseLegalTest`.

**Execution Flow:**
1.  **Browser Setup**: Use the `chat_client` fixture to navigate to `http://localhost:3000/analysis`.
2.  **Scenario Injection**: Submit the full text of each primary landmark legal scenario.
3.  **Real-time Monitoring**: Wait for the "Synthesizing answer..." status.
4.  **High-Precision Assertions**:
    *   **Citation Presence**: Verify `[Source N]` markers.
    *   **Landmark Case Match**: Regex match for landmark names (e.g., *Miranda*, *Chevron*).
    *   **Keyword Presence**: Match domain-specific terminology.

## Agent Team

| Phase | Agent(s) | Parallel | Deliverables |
|-------|----------|----------|--------------|
| 1     | tester   | No       | Standalone landmark relevance suite |

## Risk Assessment

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| Brittle Landmark Assertions | MEDIUM | MEDIUM | Use case-insensitive regex for landmark names. |
| Slow Search/Synthesis | LOW | HIGH | Set generous Playwright timeouts (90s+) for `verify_query`. |
| API Rate Limiting | MEDIUM | LOW | Ensure tests run sequentially. |

## Success Criteria

1. New test suite `tests/legal_queries/test_landmark_samples.py` passes 100% of scenarios.
2. All landmark scenarios correctly trigger the synthesis loop and cite expected precedents.
