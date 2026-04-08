---
title: "Landmark Scenario Relevance Suite Implementation Plan"
design_ref: "docs/maestro/plans/2026-04-05-verify-samples-test-suite-design.md"
created: "2026-04-05T14:45:00Z"
status: "approved"
total_phases: 1
estimated_files: 1
task_complexity: "medium"
---

# Landmark Scenario Relevance Suite Implementation Plan

## Plan Overview

- **Total phases**: 1
- **Agents involved**: `tester`
- **Estimated effort**: Simple implementation of a consolidated test file using existing Playwright infrastructure.

## Dependency Graph

```text
Phase 1 (Landmark Relevance Test Suite)
```

## Execution Strategy

| Stage | Phases | Execution | Agent Count | Notes |
|-------|--------|-----------|-------------|-------|
| 1     | Phase 1 | Sequential | 1 | Test Implementation |

---

## Phase 1: Landmark Relevance Test Suite

### Objective
Create a new test file `tests/legal_queries/test_landmark_samples.py` that automates the verification of the four primary landmark legal scenarios via the Case Analysis interface.

### Agent: tester
### Parallel: false

### Files to Create

- `tests/legal_queries/test_landmark_samples.py` — Contains `TestLandmarkRelevance(BaseLegalTest)` with test methods for Constitutional, Employment, Corporate, and Administrative law scenarios.

### Implementation Details

Implement the following test cases using the `verify_query` helper, targeting the `/analysis` page:

1. **Constitutional Law (Vehicle Search)**:
   - Scenario: "A police officer stopped a vehicle for a minor traffic violation... search the glove compartment without a warrant..."
   - Landmark: "Terry v. Ohio"
   - Keywords: ["Fourth Amendment", "reasonable expectation of privacy", "warrantless search"]
   - Assertion: `[Source N]` present, landmark name present.

2. **Employment Law (Non-Compete)**:
   - Scenario: "senior marketing executive... non-compete agreement... North American continent for 24 months..."
   - Landmark: "BDO Seidman" (or similar relevant NY non-compete precedent)
   - Keywords: ["non-compete", "unreasonable", "geographic scope"]
   - Assertion: `[Source N]` present, landmark name or "unreasonable" present.

3. **Corporate Law (Piercing the Veil)**:
   - Scenario: "creditor attempting to collect $500,000 judgment against a defunct LLC... personal mortgage payments..."
   - Landmark: "NetJets Aviation" (or similar relevant Delaware piercing precedent)
   - Keywords: ["corporate veil", "alter ego", "undercapitalized"]
   - Assertion: `[Source N]` present, landmark name present.

4. **Administrative Law (SEC/Crypto)**:
   - Scenario: "independent contractors challenging a Department of Labor ruling... shift away from Chevron deference..."
   - Landmark: "Howey" or "Loper Bright"
   - Keywords: ["Chevron", "deference", "statutory interpretation"]
   - Assertion: `[Source N]` present, landmark name present.

### Validation

- `pytest tests/legal_queries/test_landmark_samples.py`

### Dependencies

- Blocked by: None
- Blocks: None

---

## File Inventory

| # | File | Phase | Purpose |
|---|------|-------|---------|
| 1 | `tests/legal_queries/test_landmark_samples.py` | 1 | Consolidated relevance suite |

## Risk Classification

| Phase | Risk | Rationale |
|-------|------|-----------|
| 1     | LOW | Purely additive test code using proven infrastructure. |

## Execution Profile

```text
Execution Profile:
- Total phases: 1
- Parallelizable phases: 0
- Sequential-only phases: 1
- Estimated parallel wall time: N/A
- Estimated sequential wall time: 10 minutes

Note: All tool calls are auto-approved without user confirmation.
```

| Phase | Agent | Model | Est. Input | Est. Output | Est. Cost |
|-------|-------|-------|-----------|------------|----------|
| 1 | tester | gemini-3.1-pro-preview | 2000 | 1000 | $0.06 |
| **Total** | | | **2000** | **1000** | **$0.06** |
