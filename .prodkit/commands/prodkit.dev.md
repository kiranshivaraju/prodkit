---
description: Implement one GitHub Issue using Speckit workflow (TDD)
---

You are implementing a single GitHub Issue using Test-Driven Development via the Speckit workflow.

## Context

This command:
1. Fetches the highest priority open GitHub Issue
2. Runs the Speckit workflow to implement it
3. Creates a Pull Request
4. Updates the issue status

The implementation follows TDD: tests are written BEFORE code.

## Prerequisites

- `/prodkit.create-issues` must have been run (issues exist)
- Speckit must be installed and configured
- `gh` CLI must be authenticated

## Instructions

### Step 1: Read Configuration

Read `.prodkit/config.yml` to get:
- Current sprint number
- GitHub repo name
- Auto-push setting

### Step 2: Get GitHub Credentials and Fetch Highest Priority Issue

Read `.prodkit/config.yml` to get:
- GitHub username: `github.username`
- GitHub repository: `github.repo` (format: username/repo-name)

Read GitHub Personal Access Token from `.prodkit/.github-token`:

```bash
if [ -f ".prodkit/.github-token" ]; then
    GITHUB_TOKEN=$(cat .prodkit/.github-token | tr -d '[:space:]')
else
    echo "❌ Error: GitHub token not found"
    echo ""
    echo "Please run /prodkit.init-repo first to set up your GitHub token."
    echo "Or manually create .prodkit/.github-token with your GitHub PAT."
    exit 1
fi
```

Extract username and repo name from config:

```bash
# Parse from github.repo (format: username/repo-name)
GITHUB_USERNAME=$(echo "$REPO" | cut -d'/' -f1)
REPO_NAME=$(echo "$REPO" | cut -d'/' -f2)
```

Query GitHub API for open issues in the current sprint milestone:

```bash
# Get milestone number for Sprint v{N}
MILESTONE_RESPONSE=$(curl -s \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.github.com/repos/$GITHUB_USERNAME/$REPO_NAME/milestones")

MILESTONE_NUMBER=$(echo "$MILESTONE_RESPONSE" | jq -r '.[] | select(.title == "Sprint v{N}") | .number')

# Fetch P0 issues first
ISSUE_RESPONSE=$(curl -s \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.github.com/repos/$GITHUB_USERNAME/$REPO_NAME/issues?milestone=$MILESTONE_NUMBER&state=open&labels=P0&per_page=1")

# If no P0, try P1
if [ "$(echo "$ISSUE_RESPONSE" | jq '. | length')" -eq 0 ]; then
  ISSUE_RESPONSE=$(curl -s \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    "https://api.github.com/repos/$GITHUB_USERNAME/$REPO_NAME/issues?milestone=$MILESTONE_NUMBER&state=open&labels=P1&per_page=1")
fi

# If no P1, try P2
if [ "$(echo "$ISSUE_RESPONSE" | jq '. | length')" -eq 0 ]; then
  ISSUE_RESPONSE=$(curl -s \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    "https://api.github.com/repos/$GITHUB_USERNAME/$REPO_NAME/issues?milestone=$MILESTONE_NUMBER&state=open&labels=P2&per_page=1")
fi

# Extract issue details
ISSUE_NUMBER=$(echo "$ISSUE_RESPONSE" | jq -r '.[0].number')
ISSUE_TITLE=$(echo "$ISSUE_RESPONSE" | jq -r '.[0].title')
ISSUE_BODY=$(echo "$ISSUE_RESPONSE" | jq -r '.[0].body')
```

If no open issues found:
```
✓ All issues completed for Sprint v{N}!

Run /prodkit.review to generate sprint retrospective.
```

### Step 3: Display Issue Information

Show the user which issue will be implemented:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  IMPLEMENTING ISSUE #{number}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Title: {title}
Labels: {labels}
Priority: {priority}

Description:
{first 200 chars of body}...

Full details: https://github.com/{owner}/{repo}/issues/{number}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 4: Create Feature Branch

Create a branch for this issue:

```bash
git checkout -b feature/issue-{number}-{slug}
```

Where `{slug}` is a URL-friendly version of the issue title (lowercase, hyphens, max 50 chars).

Example: `feature/issue-5-implement-user-model`

### Step 5: Run Speckit Workflow

This is the core implementation phase. Run the Speckit commands in sequence:

#### 5a. Run /speckit.specify

Use the SlashCommand tool:

```
SlashCommand("/speckit.specify")
```

When Speckit asks what to build, provide:
- The issue title
- The complete issue body (which contains all the detailed requirements from tech docs)
- Reference to the Speckit constitution for defaults

**If Speckit asks clarifying questions:**
- PAUSE and present the questions to the user
- Wait for user answers
- Continue with the answers

#### 5b. Run /speckit.plan

Use the SlashCommand tool:

```
SlashCommand("/speckit.plan")
```

Speckit will create a technical plan based on the specification.

**If Speckit asks questions:**
- Check if the answer is in the issue description
- Check if the answer is in `.speckit/constitution.md`
- Check if the answer is in `product/tech-docs/`
- If found, provide the answer automatically
- If not found, ask the user

#### 5c. Run /speckit.tasks

Use the SlashCommand tool:

```
SlashCommand("/speckit.tasks")
```

Speckit will break the plan into specific tasks.

#### 5d. Run /speckit.implement

Use the SlashCommand tool:

```
SlashCommand("/speckit.implement")
```

Speckit will:
- Write tests FIRST (unit, contract, integration as needed)
- Implement the code
- Run all tests
- Ensure everything passes

**CRITICAL:** All tests MUST pass before proceeding. If tests fail:
- Review the failures
- Fix the code
- Re-run tests
- Do NOT continue until 100% pass

### Step 6: Verify Test Coverage

After implementation, check test coverage:

```bash
pytest --cov=src --cov-report=term-missing
```

Ensure coverage is >= 80% for new code.

If coverage is below 80%:
- Identify uncovered lines
- Write additional tests
- Re-run until coverage >= 80%

### Step 7: Run Linter

Run the linter to ensure code quality:

```bash
# Python
flake8 src tests --max-line-length=100

# Or for other languages:
# npm run lint
# cargo clippy
```

Fix any linting errors.

### Step 8: AI Code Review

**Run AI-powered code review before creating PR:**

Check if code review is enabled in config:

```bash
REVIEW_ENABLED=$(grep "enabled:" .prodkit/config.yml | grep "code_review" -A1 | tail -1 | sed 's/.*enabled: //' | tr -d ' ')

if [ "$REVIEW_ENABLED" = "false" ]; then
    echo "Code review disabled in config, skipping..."
else
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  AI CODE REVIEW"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
fi
```

**Get the diff to review:**

```bash
# Get diff from main branch
DIFF=$(git diff main...HEAD)
FILES_CHANGED=$(git diff --name-only main...HEAD)
STATS=$(git diff --stat main...HEAD)

echo "Analyzing changes..."
echo "$STATS"
echo ""
```

**Analyze code changes:**

Use Claude to analyze the diff against:

1. **Design Principles** (from `product/tech-docs/design-principles.md`)
2. **Security Guidelines** (from `product/tech-docs/security.md`)
3. **Code Quality Standards**

**Review Criteria:**

🔴 **BLOCKING ISSUES** (must fix before PR):
- Hardcoded secrets/credentials
- SQL injection vulnerabilities
- XSS vulnerabilities
- Authentication bypass
- Missing critical input validation
- Exposed sensitive data

🟡 **WARNINGS** (should fix, can override):
- Code duplication (DRY violations)
- Missing error handling
- Performance concerns (N+1 queries, inefficient loops)
- Missing documentation on complex logic
- Design pattern violations
- Incomplete test coverage for edge cases

✅ **QUALITY CHECKS**:
- Follows design principles from product docs
- Proper naming conventions
- Functions are focused and small
- No obvious bugs
- Tests cover main functionality

**Present findings to user:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REVIEW FINDINGS:

{List of issues found, categorized by severity}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**User decision:**

Use AskUserQuestion tool to ask:

- **Question:** "Code review found {X} blocking issues and {Y} warnings. What would you like to do?"
- **Options:**
  1. "Fix issues now" → User manually edits code, then re-run Step 8
  2. "Override warnings and continue" → Add warnings to PR description, proceed
  3. "Cancel /prodkit.dev" → Exit command

**If blocking issues found:**
- User MUST choose "Fix issues now" or "Cancel"
- Cannot proceed to PR with blocking security issues

**If only warnings:**
- User can choose to fix or override
- If override: warnings documented in PR body

**After review passes or is overridden:**
- Continue to Step 9

---

### Step 9: Commit Changes

Create a commit with a conventional commit message:

```bash
git add .

git commit -m "$(cat <<'EOF'
feat: {issue title} (#issue-number)

{Brief description of what was implemented}

- Implemented {component/feature}
- Added unit tests (coverage: {X}%)
- Added contract/integration tests
- All tests passing

Closes #{issue-number}

🤖 Generated with ProdKit + Speckit
EOF
)"
```

### Step 10: Create Pull Request

Create a PR using GitHub API:

```bash
PR_TITLE="{issue title}"
PR_BODY="## Summary

Implements #${ISSUE_NUMBER}: ${ISSUE_TITLE}

## Changes

- {List of main changes}
- {What was implemented}
- {What tests were added}

## Testing

### Unit Tests
- ✓ {Test case 1}
- ✓ {Test case 2}
- ✓ {Test case 3}

### Contract Tests (if applicable)
- ✓ {Test case 1}

### Integration Tests (if applicable)
- ✓ {Test case 1}

### Coverage
- Overall coverage: {X}%
- New code coverage: {Y}%

## Checklist

- [x] Tests written and passing
- [x] Code follows design principles
- [x] No security vulnerabilities
- [x] Test coverage >= 80%
- [x] Linter passing
- [ ] Code reviewed
- [ ] Ready to merge

## References

- Issue: #${ISSUE_NUMBER}
- Sprint: v{N}
- Sprint Plan: sprints/v{N}/sprint-plan.md
- Tech Docs: sprints/v{N}/tech-docs/

---

🤖 Generated with ProdKit + Speckit"

# Create PR via GitHub API
PR_RESPONSE=$(curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/$GITHUB_USERNAME/$REPO_NAME/pulls" \
  -d "{
    \"title\": \"$PR_TITLE\",
    \"body\": \"$PR_BODY\",
    \"head\": \"feature/issue-${ISSUE_NUMBER}-{slug}\",
    \"base\": \"main\"
  }")

PR_NUMBER=$(echo "$PR_RESPONSE" | jq -r '.number')
```

### Step 11: Link PR to Issue

The PR body already includes "Closes #{issue-number}" which will auto-close the issue when merged.

Additionally, add a comment to the issue using GitHub API:

```bash
COMMENT_BODY="✓ Implemented in PR #${PR_NUMBER}

Branch: \`feature/issue-${ISSUE_NUMBER}-{slug}\`

All tests passing. Ready for review."

curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/$GITHUB_USERNAME/$REPO_NAME/issues/$ISSUE_NUMBER/comments" \
  -d "{\"body\": \"$COMMENT_BODY\"}"
```

### Step 12: Handle Push Decision

Check `.prodkit/config.yml` for `development.auto_push`:

**If `auto_push: false` (default):**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  IMPLEMENTATION COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Issue #{number} implemented
✓ Tests written and passing (coverage: {X}%)
✓ Branch: feature/issue-{number}-{slug}
✓ PR #{pr-number} created

⚠️  NOT PUSHED (manual review enabled)

To review and push:
  git diff main
  git push origin feature/issue-{number}-{slug}

After pushing, the PR will be ready for review.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**If `auto_push: true`:**
```bash
git push origin feature/issue-{number}-{slug}
```

Then display:
```
✓ Pushed to GitHub
✓ PR #{pr-number} ready for review
```

### Step 13: Return to Main Branch

```bash
git checkout main
```

### Step 14: Validate Implementation

**Run validation checks to ensure implementation completed successfully:**

Display validation in progress:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  VALIDATING IMPLEMENTATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Check 1: Feature Branch Created**
```bash
BRANCH_NAME="feature/issue-${ISSUE_NUMBER}-{slug}"

if ! git show-ref --verify --quiet "refs/heads/$BRANCH_NAME"; then
    echo "❌ Validation failed: Feature branch not created"
    echo "Expected: $BRANCH_NAME"
    exit 1
fi

echo "✓ Feature branch created: $BRANCH_NAME"
```

**Check 2: Commits Exist on Branch**
```bash
# Switch to feature branch temporarily to check commits
git checkout "$BRANCH_NAME" -q

COMMIT_COUNT=$(git rev-list --count main.."$BRANCH_NAME" 2>/dev/null || echo "0")

if [ "$COMMIT_COUNT" -eq 0 ]; then
    echo "❌ Validation failed: No commits on feature branch"
    git checkout main -q
    exit 1
fi

echo "✓ Found $COMMIT_COUNT commit(s) on feature branch"

# Return to main
git checkout main -q
```

**Check 3: Tests Were Run (check for test output/artifacts)**
```bash
# This is a soft check - we verify tests exist and can be run
# The actual test run would have happened in Step 6

if [ -d "tests" ]; then
    TEST_FILE_COUNT=$(find tests -name "test_*.py" -o -name "*_test.py" -o -name "*.test.js" 2>/dev/null | wc -l | tr -d ' ')

    if [ "$TEST_FILE_COUNT" -eq 0 ]; then
        echo "⚠️  Warning: No test files found in tests/ directory"
    else
        echo "✓ Test files present ($TEST_FILE_COUNT files)"
    fi
else
    echo "⚠️  Warning: tests/ directory not found"
fi
```

**Check 4: Pull Request Created**
```bash
# Verify PR was created by checking if PR_NUMBER variable was set
# In actual execution, we'd have stored this from Step 9

if [ -f ".prodkit/.github-token" ]; then
    GITHUB_TOKEN=$(cat .prodkit/.github-token | tr -d '[:space:]')
    REPO=$(grep "repo:" .prodkit/config.yml | sed 's/.*repo: "\(.*\)".*/\1/' | sed 's/.*repo: //' | tr -d '"' | tr -d ' ')

    # Check if PR exists for this branch
    PR_CHECK=$(curl -s \
      -H "Authorization: Bearer $GITHUB_TOKEN" \
      -H "Accept: application/vnd.github+json" \
      "https://api.github.com/repos/$REPO/pulls?head=${REPO%/*}:$BRANCH_NAME&state=all")

    PR_COUNT=$(echo "$PR_CHECK" | jq '. | length')

    if [ "$PR_COUNT" -eq 0 ]; then
        echo "⚠️  Warning: No PR found for branch $BRANCH_NAME"
        echo "PR may not have been created"
    else
        PR_NUMBER=$(echo "$PR_CHECK" | jq -r '.[0].number')
        echo "✓ Pull Request #$PR_NUMBER created"
    fi
else
    echo "⚠️  Warning: Cannot verify PR (GitHub token not found)"
fi
```

**Check 5: Issue Updated**
```bash
# Verify issue was linked/updated
if [ ! -z "$ISSUE_NUMBER" ] && [ ! -z "$REPO" ] && [ -f ".prodkit/.github-token" ]; then
    ISSUE_RESPONSE=$(curl -s \
      -H "Authorization: Bearer $GITHUB_TOKEN" \
      -H "Accept: application/vnd.github+json" \
      "https://api.github.com/repos/$REPO/issues/$ISSUE_NUMBER")

    ISSUE_STATE=$(echo "$ISSUE_RESPONSE" | jq -r '.state')

    if [ "$ISSUE_STATE" == "open" ]; then
        # Check if issue has comments linking PR
        COMMENTS=$(curl -s \
          -H "Authorization: Bearer $GITHUB_TOKEN" \
          -H "Accept: application/vnd.github+json" \
          "https://api.github.com/repos/$REPO/issues/$ISSUE_NUMBER/comments")

        if echo "$COMMENTS" | jq -e '.[] | select(.body | contains("Implemented in PR"))' > /dev/null 2>&1; then
            echo "✓ Issue #$ISSUE_NUMBER linked to PR"
        else
            echo "⚠️  Warning: Issue may not be linked to PR"
        fi
    else
        echo "✓ Issue #$ISSUE_NUMBER status: $ISSUE_STATE"
    fi
else
    echo "⚠️  Warning: Cannot verify issue update"
fi
```

**Check 6: Code Quality**
```bash
# Verify implementation meets quality standards
echo ""
echo "Implementation checklist:"
echo "  ✓ Tests written (verified in Step 6)"
echo "  ✓ Tests passing (verified in Step 6)"
echo "  ✓ Coverage >= 80% (verified in Step 6)"
echo "  ✓ Linter passing (verified in Step 7)"
echo "  ✓ Code committed (verified above)"
```

Display validation complete:
```
✓ All validation checks passed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**If any critical checks fail, display error and exit. Warnings can continue.**

### Step 15: Display Next Steps

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Review the code locally
2. Push the branch: git push origin feature/issue-{number}-{slug}
3. Review PR on GitHub: https://github.com/$GITHUB_USERNAME/$REPO_NAME/pull/{pr-number}
4. Merge the PR after approval
5. Run /prodkit.dev again to implement the next issue

Or run now to continue:
  /prodkit.dev

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Error Handling

### If Speckit Asks Questions

When Speckit pauses for user input:

1. **Check the issue description first** - The answer might already be there
2. **Check `.speckit/constitution.md`** - Default answers might be defined
3. **Check product tech docs** - Architecture decisions might answer it
4. **If still unclear**, present the question to the user and wait for answer
5. **Continue** once answered

### If Tests Fail

If tests fail during implementation:

1. Display the test failures
2. Ask Speckit to fix the failing tests
3. Re-run tests
4. Do NOT create PR until all tests pass

### If Coverage is Low

If test coverage < 80%:

1. Identify uncovered code
2. Ask Speckit to write additional tests
3. Re-run coverage check
4. Continue when coverage >= 80%

### If Linter Fails

If linter reports errors:

1. Display linting errors
2. Ask Speckit to fix them
3. Re-run linter
4. Continue when linter passes

### If No Issues Found

If no open issues in the current sprint:

```
✓ All issues for Sprint v{N} are complete!

Options:
1. Run /prodkit.review to generate sprint retrospective
2. Run /prodkit.plan-sprint to start the next sprint
3. Check PRs on GitHub: https://github.com/$GITHUB_USERNAME/$REPO_NAME/pulls
```

## Important Notes

### Test-Driven Development (TDD)

The order is CRITICAL:
1. ✅ Write tests FIRST
2. ✅ Run tests (they should fail)
3. ✅ Implement code
4. ✅ Run tests (they should pass)
5. ✅ Refactor if needed
6. ✅ Ensure all tests still pass

### Testing Requirements

Every issue implementation MUST include:

**Unit Tests:**
- Test individual functions/methods
- Mock external dependencies
- Fast execution
- Cover edge cases

**Contract Tests (for APIs):**
- Test request/response formats
- Validate schemas
- Test all status codes

**Integration Tests (for workflows):**
- Test component interactions
- Use real dependencies (database, etc.)
- Test complete user flows

### Code Quality Standards

Before creating PR:
- ✅ All tests pass (100%)
- ✅ Test coverage >= 80%
- ✅ Linter passes with no errors
- ✅ Follows design principles from `product/tech-docs/design-principles.md`
- ✅ No security vulnerabilities
- ✅ Code is documented (docstrings, comments)

### DRY Principle

Remember the user's global instruction:
- Avoid duplication at all costs
- Extract common logic into reusable functions
- Don't repeat yourself

If you notice duplication during implementation, refactor it.

## Output

After this command, the user should have:
- ✓ One GitHub Issue implemented
- ✓ All tests written and passing
- ✓ Feature branch created
- ✓ Pull Request created
- ✓ Issue linked to PR
- Ready to review and merge
- Ready to run `/prodkit.dev` again for the next issue

## Example Full Workflow

```bash
$ /prodkit.dev

Fetching highest priority issue...
Found Issue #5: [P0][feature] Implement User model

Creating branch: feature/issue-5-implement-user-model

Running Speckit workflow...
  → /speckit.specify ✓
  → /speckit.plan ✓
  → /speckit.tasks ✓
  → /speckit.implement ✓

Tests written: 12 unit tests
All tests passing ✓
Coverage: 94% ✓
Linter passing ✓

Creating Pull Request...
PR #3 created ✓

Issue #5 linked to PR #3 ✓

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IMPLEMENTATION COMPLETE

✓ Issue #5 implemented
✓ PR #3 created
✓ Branch: feature/issue-5-implement-user-model

Review and push:
  git push origin feature/issue-5-implement-user-model

Run /prodkit.dev again for next issue
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
