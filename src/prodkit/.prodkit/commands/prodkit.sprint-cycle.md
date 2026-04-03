---
description: Run the full sprint cycle from planning to review
---

You are orchestrating a complete sprint cycle, chaining ProdKit commands from planning through review.

## Context

This command automates the entire sprint lifecycle by running each ProdKit phase in sequence. It eliminates manual handoffs between commands and ensures nothing is skipped.

## Prerequisites

- Product architecture docs must exist (`/prodkit.product-arch` completed)
- GitHub repo must be initialized (`/prodkit.init-repo` completed)
- `.prodkit/config.yml` must exist with repo and sprint configuration

## Agent Orchestration (OMC)

If oh-my-claudecode (OMC) is available (check for `mcp__plugin_oh-my-claudecode_t__*` tools), wrap the entire sprint cycle in `ralph` mode for guaranteed completion with verification. Use `ultrawork` for parallel phases where applicable.

If OMC is not available, proceed with standard sequential execution below.

## Instructions

### Sprint Cycle Pipeline

Execute the following commands in order. Each step must complete successfully before proceeding to the next.

#### Phase 1: Planning
```
/prodkit.plan-sprint
```
- Analyzes PRD and product-arch docs
- Selects features for the sprint
- Creates sprint plan with milestone

**Gate:** Sprint plan exists at `sprints/v{N}/sprint-plan.md`

#### Phase 2: Technical Specifications
```
/prodkit.sprint-tech
```
- Creates detailed tech docs for sprint features
- Generates data models, API endpoints, implementation plans

**Gate:** Tech docs exist in `sprints/v{N}/tech-docs/`

#### Phase 3: Gap Analysis
```
/prodkit.gap-analysis
```
- Audits cross-document consistency
- Identifies missing specs or contradictions
- Fixes gaps before implementation begins

**Gate:** Gap analysis report shows no critical gaps remaining

#### Phase 4: Issue Creation
```
/prodkit.create-issues
```
- Generates GitHub issues from tech docs
- Sets priorities, labels, and dependencies
- Assigns to sprint milestone

**Gate:** All issues created and assigned to milestone

#### Phase 5: Development
```
/prodkit.dev
```
- Implements each issue using TDD workflow
- Creates feature branches and PRs
- Runs for each issue in priority order

**Gate:** All sprint issues have merged PRs

#### Phase 5b: Test Validation
```
/prodkit.test
```
- Runs full test suite with coverage and branch analysis
- Audits test quality (empty tests, missing assertions, happy-path-only)
- Cross-references tests against sprint tech doc specifications
- Fixes any incomplete tests before proceeding

**Gate:** All tests pass, no critical quality issues, spec coverage acceptable

#### Phase 6: Code Review
```
/prodkit.code-review
```
- Reviews all PRs created during the sprint
- Checks code quality, security, and test coverage

**Gate:** All reviews pass with no blocking issues

#### Phase 7: Sprint Review
```
/prodkit.review
```
- Generates sprint retrospective
- Collects metrics and learnings
- Recommends next sprint priorities

**Gate:** Sprint review exists at `sprints/v{N}/sprint-review.md`

### Error Handling

- If any phase fails, stop and report the failure with context
- Do not skip phases — each builds on the previous
- If a gap analysis finds critical issues, fix them before proceeding to issue creation

### Progress Tracking

After each phase, report:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SPRINT CYCLE PROGRESS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ Phase 1: Planning          — Complete
  ✅ Phase 2: Tech Specs        — Complete
  ▶️  Phase 3: Gap Analysis      — In Progress
  ⬜ Phase 4: Issue Creation    — Pending
  ⬜ Phase 5: Development       — Pending
  ⬜ Phase 6: Code Review       — Pending
  ⬜ Phase 7: Sprint Review     — Pending
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Output

After this command completes, the user has:
- A fully executed sprint from plan to review
- All issues implemented, reviewed, and merged
- Sprint retrospective with metrics and recommendations
- Ready to start the next sprint cycle
