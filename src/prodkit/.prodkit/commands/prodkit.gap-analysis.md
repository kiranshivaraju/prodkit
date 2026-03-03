---
description: Audit documents for gaps, missing details, and cross-document inconsistencies
---

You are helping the user find gaps in their ProdKit documents before proceeding to the next workflow step. This is a comprehensive audit that checks individual documents AND cross-document consistency including user flow traceability.

## Context

ProdKit documents build on each other: PRD → Market Research → Architecture → Sprint Plan → Sprint Tech Docs → Implementation. Gaps in early documents cascade into problems during development. This command catches issues early.

Run this after creating or updating any document.

## Instructions

### Step 1: Scan for Existing Documents

Check which documents exist and report what was found:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PRODKIT GAP ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Check for:
- `product/prd.md`
- `product/market-research.md`
- `product/tech-docs/architecture.md`
- `product/tech-docs/design-principles.md`
- `product/tech-docs/security.md`
- `product/tech-docs/data-architecture.md`
- `product/tech-docs/api-strategy.md`
- `product/tech-docs/testing-strategy.md`
- `.speckit/constitution.md`
- `sprints/v{N}/sprint-plan.md` (check all sprint directories)
- `sprints/v{N}/tech-docs/data-models.md`
- `sprints/v{N}/tech-docs/api-endpoints.md`
- `sprints/v{N}/tech-docs/implementation-plan.md`
- `sprints/v{N}/tech-docs/component-design.md`

Read the current sprint number from `.prodkit/config.yml`.

If no documents exist at all:
```
No ProdKit documents found. Run /prodkit.prd to get started.
```

Display which documents were found:
```
Documents found:
  ✓ product/prd.md
  ✓ product/market-research.md
  ✗ product/tech-docs/architecture.md (not created yet)
  ...
```

### Step 2: Analyze Individual Documents for Gaps

For each document that exists, read it thoroughly and check for gaps. Use the severity levels:

- 🔴 **CRITICAL** — Will block development or cause implementation failures
- 🟡 **WARNING** — Should be fixed, may cause confusion or rework
- 🔵 **INFO** — Minor improvement, nice to have

#### 2a. PRD (`product/prd.md`)

Check for:
- 🔴 Missing required sections: Product Overview, Problem Statement, Features, User Workflows, Success Metrics
- 🔴 Features without descriptions or user stories
- 🔴 Features without priority levels (Critical/High/Medium/Low)
- 🟡 Success metrics that aren't measurable (e.g., "users like it" vs "1000 signups in 30 days")
- 🟡 Vague problem statement (less than 2 sentences or no specific pain point)
- 🟡 User workflows that don't specify step-by-step actions
- 🟡 No dependencies specified between features
- 🔵 Missing Out of Scope section
- 🔵 Missing Roadmap/phases
- 🔵 No appendix or references

#### 2b. Market Research (`product/market-research.md`)

Check for:
- 🔴 Fewer than 3 competitors analyzed
- 🔴 Missing Feature Comparison matrix
- 🔴 Missing Differentiation Strategy section
- 🟡 Competitors without pricing information
- 🟡 Risk Assessment without severity levels or mitigations
- 🟡 Feature comparison that doesn't include all PRD features
- 🔵 Missing Go-to-Market suggestions
- 🔵 No conclusion with viability assessment

#### 2c. Product Architecture (`product/tech-docs/`)

For each of the 6 documents, check:

**architecture.md:**
- 🔴 No tech stack defined (language, framework, database missing)
- 🔴 No reasoning for tech choices (just listed without "why")
- 🟡 No architecture diagram or component overview
- 🟡 Missing scalability considerations
- 🔵 No security architecture section

**design-principles.md:**
- 🔴 No coding standards specified
- 🟡 No folder/code organization structure
- 🟡 Missing naming conventions
- 🔵 No error handling patterns

**security.md:**
- 🔴 No authentication mechanism specified (JWT, OAuth, sessions)
- 🔴 No input validation/sanitization rules
- 🟡 Missing authorization model (RBAC, ABAC)
- 🟡 No data encryption strategy

**data-architecture.md:**
- 🔴 No database choice or reasoning
- 🟡 No migration strategy
- 🟡 Missing data modeling principles (normalization, UUIDs, timestamps)
- 🔵 No backup/recovery plan

**api-strategy.md:**
- 🔴 No API style defined (REST, GraphQL)
- 🔴 No endpoint conventions or examples
- 🟡 Missing pagination strategy
- 🟡 No versioning strategy
- 🔵 Missing rate limiting

**testing-strategy.md:**
- 🔴 No test types defined (unit, contract, integration)
- 🔴 No coverage targets
- 🟡 No test organization/folder structure
- 🔵 No CI/CD testing approach

#### 2d. Sprint Plan (`sprints/v{N}/sprint-plan.md`)

Check for:
- 🔴 No sprint goal defined
- 🔴 Zero features selected
- 🔴 Features without acceptance/success criteria
- 🟡 Sprint goal that isn't specific or measurable
- 🟡 No dependencies between features documented
- 🟡 Missing effort estimates
- 🔵 No "Out of Scope" for this sprint
- 🔵 No risks identified

#### 2e. Sprint Tech Docs (`sprints/v{N}/tech-docs/`)

**data-models.md:**
- 🔴 Models with fields missing types or constraints
- 🔴 No validation rules specified (regex, min/max, required/optional)
- 🔴 Missing relationships between models
- 🟡 No migration SQL
- 🟡 No indexes defined

**api-endpoints.md:**
- 🔴 Endpoints without request/response examples
- 🔴 Missing error responses (only happy path documented)
- 🔴 No test cases per endpoint
- 🟡 Missing authentication requirements per endpoint
- 🟡 No specific error codes (e.g., "VALIDATION_ERROR")

**implementation-plan.md:**
- 🔴 Steps that don't specify which files to create
- 🔴 No dependency ordering between steps
- 🟡 No testing requirements per step
- 🔵 Missing timeline estimates

**component-design.md:**
- 🔴 Methods without parameter types or return types
- 🔴 No exception/error handling specified
- 🟡 Missing dependencies between components
- 🔵 No test coverage notes

### Step 3: Cross-Document Consistency Checks (User Flow Gaps)

This is the most critical analysis. Check that documents connect properly end-to-end.

#### 3a. PRD → Sprint Plan

- 🔴 Features in sprint plan that don't exist in the PRD
- 🟡 Feature priorities in sprint plan that contradict PRD priorities
- 🟡 Sprint plan dependencies that don't align with PRD feature dependencies

#### 3b. PRD → Market Research

- 🟡 PRD features not included in the market research feature comparison matrix
- 🟡 High-priority features not addressed in differentiation strategy

#### 3c. PRD → Architecture

- 🔴 PRD features that require capabilities not covered by the tech stack (e.g., PRD says "real-time notifications" but architecture has no WebSocket/SSE)
- 🔴 PRD user authentication requirements not covered in security.md
- 🟡 API strategy that doesn't accommodate PRD user workflows

#### 3d. Sprint Plan → Sprint Tech Docs

- 🔴 Features in sprint plan with NO corresponding data models
- 🔴 Features in sprint plan with NO corresponding API endpoints
- 🔴 Features in sprint plan with NO corresponding component designs
- 🟡 Acceptance criteria from sprint plan not mapped to test cases in api-endpoints.md
- 🟡 Implementation plan doesn't cover all sprint plan features

#### 3e. User Workflow Traceability

For EACH user workflow defined in the PRD:

Trace it through the entire document chain:
1. **PRD workflow** → Does a sprint plan feature cover it?
2. **Sprint plan feature** → Do data models support the data it needs?
3. **Data models** → Do API endpoints expose operations on that data?
4. **API endpoints** → Do components implement the business logic?
5. **Components** → Do test cases verify the workflow works?

If any step in the trace is missing, flag it:
- 🔴 **Broken trace**: "User workflow '{name}' has no API endpoints to support it"
- 🔴 **Broken trace**: "User workflow '{name}' requires data not covered by any model"
- 🟡 **Incomplete trace**: "User workflow '{name}' has endpoints but no test cases"

### Step 4: Generate Gap Report

Write the gap analysis report to `product/gap-analysis.md`.

Use this structure:

```markdown
# Gap Analysis Report

**Date:** [Current Date]

**Documents Analyzed:** [count]

## Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | [X] |
| 🟡 Warning | [Y] |
| 🔵 Info | [Z] |

**Overall Readiness:** [Ready / Needs Work / Not Ready]

## Critical Gaps (Must Fix)

### [Document Name]
1. [Gap description and what to add]
2. [Gap description and what to add]

## Cross-Document Inconsistencies

### User Flow Gaps
1. [Workflow trace that's broken and what's missing]
2. [Documents that contradict each other]

### Missing Connections
1. [Feature in sprint plan with no tech doc coverage]
2. [API endpoint with no corresponding component]

## Warnings (Should Fix)

### [Document Name]
1. [Gap description]

## Info (Nice to Have)

### [Document Name]
1. [Suggestion]

## Recommended Actions

1. **Fix first:** [Most critical document to update]
2. **Then:** [Next document]
3. **Finally:** [Remaining items]

After fixing, run `/prodkit.gap-analysis` again to verify.
```

### Step 5: Validate Report

```bash
REPORT_FILE="product/gap-analysis.md"

if [ ! -f "$REPORT_FILE" ]; then
    echo "❌ Validation failed: Gap analysis report not found"
    exit 1
fi

echo "✓ Gap analysis report created"
```

### Step 6: Confirm Completion

Display a summary:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  GAP ANALYSIS COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Documents analyzed: [X]
Critical gaps: [X]
Warnings: [Y]
Info: [Z]

Report: product/gap-analysis.md

[If critical gaps found:]
⚠️  Fix critical gaps before proceeding to the next step.
After fixing, run /prodkit.gap-analysis again.

[If no critical gaps:]
✓ No critical gaps found. Ready to proceed!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Important Notes

- Only analyze documents that exist — don't flag missing documents that haven't been created yet (e.g., don't flag missing sprint tech docs if the user just finished the PRD)
- Cross-document checks only apply between documents that both exist
- Be specific about what's missing — don't just say "needs more detail", say exactly what detail is needed
- The user flow traceability check is the highest-value analysis — prioritize it
- This command can be run multiple times — each run should reflect the current state of documents
