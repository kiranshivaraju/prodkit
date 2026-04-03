---
description: Run tests, validate coverage, and audit test completeness against specs
---

You are running a comprehensive test validation for the current project. This goes beyond "run tests and check coverage" — it audits whether tests are structurally complete, checks for common test anti-patterns, and traces test cases back to sprint tech doc specifications.

## Context

This command solves two problems:
1. **Tests don't always run** — This command explicitly runs the full test suite with coverage
2. **Tests are sometimes incomplete** — This command detects stub tests, missing assertions, happy-path-only coverage, and missing spec-prescribed test cases

Run this command:
- After `/prodkit.dev` to verify test quality before PR review
- Standalone anytime to audit test health
- As part of `/prodkit.sprint-cycle` between development and code review

## Agent Orchestration (OMC)

If oh-my-claudecode (OMC) is available (check for `mcp__plugin_oh-my-claudecode_t__*` tools), use the following agent delegation strategy. If OMC is not available, proceed with standard execution below.

**Agent delegation:**
- **Test execution & coverage:** Delegate to `test-engineer` agent for running tests and analyzing coverage
- **Spec-mapping analysis:** Delegate to `analyst` agent (model: `opus`) for cross-referencing tech docs against test code
- **Fix mode:** Delegate to `test-engineer` agent for writing missing tests

**Parallel execution:** Test execution and spec-mapping analysis can run in parallel since they are independent.

## Prerequisites

- Project must have a test directory (`tests/`)
- `.prodkit/config.yml` must exist with testing configuration
- For spec-mapping: sprint tech docs must exist in `sprints/v{N}/tech-docs/`

## Instructions

### Step 1: Read Configuration

```bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  PRODKIT TEST VALIDATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
```

Read `.prodkit/config.yml` to get:
- `testing.framework` (pytest, jest, etc.)
- `testing.min_coverage` (default: 80)
- Current sprint number

Detect project type from config or file presence:
- Python: `pyproject.toml` or `setup.py` → pytest
- Node: `package.json` → jest/vitest
- Go: `go.mod` → go test
- Rust: `Cargo.toml` → cargo test

### Step 2: Run Full Test Suite

Run the test suite with coverage and branch analysis:

**Python (pytest):**
```bash
echo "→ Running test suite..."
pytest --cov=src --cov-branch --cov-report=term-missing -v 2>&1
TEST_EXIT_CODE=$?
```

**Node (jest):**
```bash
npx jest --coverage --verbose 2>&1
TEST_EXIT_CODE=$?
```

**Go:**
```bash
go test ./... -v -cover 2>&1
TEST_EXIT_CODE=$?
```

Display results:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  TEST RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tests run: {total}
  ✅ Passed: {passed}
  ❌ Failed: {failed}
  ⏭️  Skipped: {skipped}

Exit code: {TEST_EXIT_CODE}
```

**If any tests fail, report the failures but continue with the audit.** Test failures are reported separately from test quality issues.

### Step 3: Coverage Analysis

Parse coverage output and check thresholds:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  COVERAGE ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**3a. Overall coverage:**
- 🔴 FAIL if overall coverage < `min_coverage` from config
- ✅ PASS if coverage >= threshold
- Report: `Overall: {X}% (minimum: {min_coverage}%)`

**3b. Per-file coverage:**
- 🔴 FAIL if any source file has 0% coverage (completely untested)
- 🟡 WARN if any source file has < 50% coverage
- List uncovered files:
  ```
  Files with 0% coverage (UNTESTED):
    🔴 src/services/notification_service.py
    🔴 src/utils/email.py

  Files below 50% coverage:
    🟡 src/models/user.py (42%)
    🟡 src/api/auth.py (38%)
  ```

**3c. Branch coverage:**
- Report branch coverage percentage
- Flag functions with untested branches:
  ```
  Untested branches:
    🟡 src/services/auth.py:45 → else branch not covered
    🟡 src/models/user.py:23 → except clause not covered
  ```

**3d. Source files without test files:**
- For each file in `src/`, check if a corresponding test file exists in `tests/`
- Naming convention: `src/services/auth.py` → `tests/test_auth.py` or `tests/services/test_auth.py` or `tests/unit/test_auth.py`
- 🟡 WARN for source files with no corresponding test file

### Step 4: Structural Test Quality Audit

This is the key differentiator. Read all test files and check for anti-patterns that indicate incomplete tests.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  TEST QUALITY AUDIT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### 4a. Empty Test Bodies

Search for test functions with no meaningful content:

```python
# Patterns to detect:
def test_something():
    pass

def test_something():
    ...

def test_something():
    """TODO: implement"""
```

- 🔴 CRITICAL: Test function with `pass` or `...` as the only statement
- 🔴 CRITICAL: Test function with only a docstring and no assertions
- Report: `🔴 {file}:{line} — test_{name} has empty body (stub test)`

#### 4b. Assert-Free Tests

Search for test functions that execute code but never assert anything:

```python
# Bad — runs code but verifies nothing:
def test_create_user():
    user = User(name="test", email="test@test.com")
    user.save()
    # No assertion!
```

Check that every test function contains at least one of:
- `assert` statement
- `pytest.raises`
- `self.assert*` (unittest style)
- `expect(` (jest style)
- `t.Error` / `t.Fatal` (Go style)

- 🔴 CRITICAL: Test function with zero assertions
- Report: `🔴 {file}:{line} — test_{name} has no assertions`

#### 4c. Tautological Assertions

Search for assertions that always pass:

```python
# Bad — always passes:
assert True
assert 1 == 1
assert "hello" == "hello"
assert result is not None  # when result is a literal
```

- 🟡 WARNING: `assert True`, `assert 1 == 1`, or other tautologies
- Report: `🟡 {file}:{line} — tautological assertion (always passes)`

#### 4d. Happy-Path-Only Test Files

Check if test files only test success cases with no error/failure tests:

Indicators of missing error path tests:
- No `pytest.raises` or `assertRaises` in the file
- No test names containing "invalid", "error", "fail", "wrong", "bad", "reject", "unauthorized", "forbidden", "not_found"
- No assertions checking for 4xx/5xx status codes
- No assertions checking for exception messages

- 🟡 WARNING: Test file has only happy-path tests
- Report: `🟡 {file} — no error/failure test cases found (happy-path only)`

#### 4e. Missing Boundary Tests

For models with validation rules (from tech docs or code), check if tests include boundary values:

- Check for tests with values like: `""` (empty string), `None`/`null`, `0`, `-1`, very long strings, special characters
- 🔵 INFO: No boundary value tests detected for validated fields
- Report: `🔵 {file} — consider adding boundary tests (empty, null, max-length)`

#### 4f. Test Count vs Complexity

Compare the number of test functions against the complexity of what they test:

- If a source file has > 5 public functions/methods but < 3 test functions → 🟡 WARNING
- Report: `🟡 {source_file} has {X} functions but only {Y} tests`

### Step 5: Spec-Mapping (Tech Doc Traceability)

Cross-reference sprint tech doc test specifications against actual test code.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SPEC TRACEABILITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Read the current sprint number from `.prodkit/config.yml`.

#### 5a. API Endpoint Test Mapping

Read `sprints/v{N}/tech-docs/api-endpoints.md` and extract:
- Each endpoint (method + path)
- Prescribed test cases per endpoint
- Error responses that should be tested

For each prescribed test case, search for a corresponding test function:
- Match by endpoint name and test description
- Use fuzzy matching (e.g., "Test 400 validation error for POST /auth/register" → `test_register_validation_error` or `test_register_invalid_input`)

```
POST /auth/register:
  ✅ Test successful registration      → test_auth.py::test_register_success
  ✅ Test duplicate email rejection     → test_auth.py::test_register_duplicate_email
  ❌ Test invalid email format          → MISSING
  ❌ Test password too short            → MISSING

GET /users/{id}:
  ✅ Test get existing user             → test_users.py::test_get_user
  ❌ Test get non-existent user (404)   → MISSING
  ❌ Test unauthorized access (401)     → MISSING
```

- 🔴 CRITICAL: Endpoint has zero test functions
- 🟡 WARNING: Endpoint has tests but missing prescribed error cases

#### 5b. Data Model Test Mapping

Read `sprints/v{N}/tech-docs/data-models.md` and extract:
- Each model and its fields
- Validation rules (required, regex, min/max, unique)
- Relationships

Check for corresponding tests:
- Model creation with valid data
- Validation rejection with invalid data
- Relationship integrity

```
User model:
  ✅ Test creation with valid data      → test_user_model.py::test_create_user
  ✅ Test email validation              → test_user_model.py::test_invalid_email
  ❌ Test required field missing         → MISSING
  ❌ Test unique constraint violation    → MISSING
```

#### 5c. Component Test Mapping

Read `sprints/v{N}/tech-docs/component-design.md` and extract:
- Each component/service and its methods
- Expected behaviors and error cases

Check for corresponding tests.

#### 5d. Summary

```
Spec Traceability Summary:
  API Endpoints: {X}/{Y} test cases covered ({Z}%)
  Data Models:   {X}/{Y} test cases covered ({Z}%)
  Components:    {X}/{Y} test cases covered ({Z}%)

  Missing test cases: {total_missing}
```

### Step 6: Generate Test Report

Write the test validation report to `product/test-report.md` (or `sprints/v{N}/test-report.md` if sprint-scoped).

Use this structure:

```markdown
# Test Validation Report

**Date:** [Current Date]
**Sprint:** v{N}
**Branch:** {current branch}

## Summary

| Category | Status |
|----------|--------|
| Test Suite | ✅ {passed}/{total} passing |
| Overall Coverage | ✅ {X}% (min: {min}%) |
| Branch Coverage | {X}% |
| Test Quality | {X} critical, {Y} warnings |
| Spec Traceability | {X}% coverage |

**Overall:** [PASS / NEEDS WORK / FAIL]

## Test Failures

{If any tests failed, list them with error messages}

## Coverage Gaps

### Untested Files
{Files with 0% coverage}

### Low Coverage Files
{Files below 50% coverage}

## Test Quality Issues

### 🔴 Critical (Must Fix)
1. {file}:{line} — {description}

### 🟡 Warnings (Should Fix)
1. {file}:{line} — {description}

### 🔵 Info (Nice to Have)
1. {description}

## Spec Traceability Gaps

### Missing Test Cases
{Prescribed tests from tech docs that don't exist in code}

## Recommended Actions

1. **Fix first:** {Most critical issues}
2. **Then:** {Next priority}
3. **Finally:** {Remaining items}

After fixing, run `/prodkit.test` again to verify.
```

### Step 7: Fix Mode (When user requests)

If the user explicitly asks to fix the test gaps (or runs with `--fix` intent):

1. Read the missing test cases from the spec traceability report
2. Read the structural issues (empty tests, assert-free tests)
3. For each issue:
   - **Empty/stub tests:** Read the corresponding source code and tech doc spec, then write a complete test implementation
   - **Assert-free tests:** Add appropriate assertions based on what the test is executing
   - **Missing spec tests:** Generate new test functions based on the tech doc test case descriptions
4. Re-run the test suite after fixes
5. Re-run the audit to verify fixes

**Important:** When writing tests:
- Follow TDD principles — tests should test behavior, not implementation
- Use the project's existing test patterns and fixtures
- Include edge cases and error paths
- Each test should have a clear, descriptive name
- Each test must have at least one meaningful assertion

### Step 8: Save State

Save test validation state for other commands to verify:

```bash
mkdir -p .prodkit/.state

cat > .prodkit/.state/test-validation-latest.json << EOF
{
  "completed": true,
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "branch": "$(git branch --show-current)",
  "tests_passed": ${TESTS_PASSED},
  "tests_failed": ${TESTS_FAILED},
  "coverage_pct": ${COVERAGE_PCT},
  "critical_issues": ${CRITICAL_COUNT},
  "warning_issues": ${WARNING_COUNT},
  "spec_coverage_pct": ${SPEC_COVERAGE_PCT},
  "status": "${OVERALL_STATUS}"
}
EOF
```

### Step 9: Display Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  TEST VALIDATION COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tests:      {passed}/{total} passing
Coverage:   {X}% (branch: {Y}%)
Quality:    {critical} critical, {warnings} warnings
Spec Map:   {X}% of prescribed tests exist

Report: product/test-report.md

[If critical issues found:]
⚠️  Fix critical test issues before proceeding.
Run /prodkit.test again after fixes.
Or run /prodkit.test --fix to auto-generate missing tests.

[If no critical issues:]
✅ All test checks passed. Ready to proceed!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Important Notes

- **Always run tests first** — structural audit means nothing if tests don't pass
- **Spec mapping is fuzzy** — it uses heuristic matching between doc descriptions and test names. False positives are possible. When in doubt, flag as INFO not CRITICAL
- **Don't block on INFO items** — only CRITICAL issues should block the workflow
- **This command is idempotent** — safe to run multiple times, each run reflects current state
- **Branch coverage matters** — 100% line coverage with 0% branch coverage means untested conditionals

## Next Step

This command is complete. The next step in the ProdKit workflow is:
→ `/prodkit.code-review` (run code review on the implementation)
→ Or run `/prodkit.test --fix` to auto-generate missing tests
