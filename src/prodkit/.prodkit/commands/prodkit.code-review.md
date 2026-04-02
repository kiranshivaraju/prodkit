---
description: AI-powered code review for branches, PRs, or commits
---

You are performing an AI-powered code review to ensure code quality, security, and adherence to design principles.

## Context

This command can be run:
- **During `/prodkit.dev`** - Automatically reviews code before PR creation
- **Standalone** - Manually review any branch, PR, or commit range

## Usage

```
/prodkit.code-review                    # Review current branch vs main
/prodkit.code-review --pr 123           # Review PR #123
/prodkit.code-review --branch feature-x # Review specific branch vs main
/prodkit.code-review --commits abc123..def456  # Review commit range
```

## Instructions

### Agent Orchestration (OMC)

If oh-my-claudecode (OMC) is available (check for `mcp__plugin_oh-my-claudecode_t__*` tools), use the following agent delegation strategy. If OMC is not available, proceed with standard execution below.

**Agent delegation:** Fire 2 review agents in parallel:
- **Code quality:** `code-reviewer` agent (model: `sonnet`) for logic, style, performance, and SOLID principle review
- **Security:** `security-reviewer` agent (model: `sonnet`) for OWASP Top 10, secrets, and unsafe patterns
- **Architecture (large diffs >500 lines):** Escalate to `architect` agent (model: `opus`) for architectural review

**Parallel execution:** Code and security reviews always run simultaneously. Architect review runs in parallel when triggered.

### Step 1: Determine What to Review

Check if arguments were provided:

```bash
# If no arguments, review current branch
CURRENT_BRANCH=$(git branch --show-current)

if [ "$CURRENT_BRANCH" = "main" ] || [ "$CURRENT_BRANCH" = "master" ]; then
    echo "❌ Cannot review main/master branch"
    echo "Switch to a feature branch or specify --branch"
    exit 1
fi

BASE_BRANCH="main"
REVIEW_BRANCH="$CURRENT_BRANCH"
```

**If `--pr` provided:**
- Fetch PR details from GitHub API
- Get the head branch and base branch from PR
- Review the diff between base...head

**If `--branch` provided:**
- Set REVIEW_BRANCH to specified branch
- Compare against main

**If `--commits` provided:**
- Review the specified commit range

---

### Step 2: Get Configuration

Read code review settings from `.prodkit/config.yml`:

```bash
REVIEW_ENABLED=$(grep -A3 "code_review:" .prodkit/config.yml | grep "enabled:" | sed 's/.*enabled: //' | tr -d ' ')
BLOCK_ON_SECURITY=$(grep -A3 "code_review:" .prodkit/config.yml | grep "block_on_security:" | sed 's/.*block_on_security: //' | tr -d ' ')
BLOCK_ON_QUALITY=$(grep -A3 "code_review:" .prodkit/config.yml | grep "block_on_quality:" | sed 's/.*block_on_quality: //' | tr -d ' ')

if [ "$REVIEW_ENABLED" = "false" ]; then
    echo "⚠️  Code review is disabled in config"
    echo "Enable in .prodkit/config.yml: code_review.enabled: true"
    exit 0
fi
```

---

### Step 3: Get Code Diff

Extract the diff to review:

```bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  AI CODE REVIEW"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Get diff
DIFF=$(git diff $BASE_BRANCH...$REVIEW_BRANCH)

if [ -z "$DIFF" ]; then
    echo "✓ No changes to review"
    exit 0
fi

# Get statistics
FILES_CHANGED=$(git diff --name-only $BASE_BRANCH...$REVIEW_BRANCH)
STATS=$(git diff --stat $BASE_BRANCH...$REVIEW_BRANCH)

echo "Reviewing: $REVIEW_BRANCH"
echo "Against: $BASE_BRANCH"
echo ""
echo "$STATS"
echo ""
echo "Analyzing..."
echo ""
```

---

### Step 4: Load Design Principles and Security Guidelines

Read project standards to review against:

```bash
DESIGN_PRINCIPLES=""
SECURITY_GUIDELINES=""

if [ -f "product/tech-docs/design-principles.md" ]; then
    DESIGN_PRINCIPLES=$(cat product/tech-docs/design-principles.md)
fi

if [ -f "product/tech-docs/security.md" ]; then
    SECURITY_GUIDELINES=$(cat product/tech-docs/security.md)
fi
```

---

### Step 5: AI Analysis

**Use Claude to analyze the diff comprehensively.**

Review the code changes against these criteria:

#### 🔴 BLOCKING SECURITY ISSUES

Critical security vulnerabilities that MUST be fixed:

1. **Hardcoded Credentials**
   - Check for: API keys, passwords, tokens, secrets in code
   - Example: `API_KEY = "sk-1234567890"`
   - Example: `password = "admin123"`

2. **SQL Injection Vulnerabilities**
   - Check for: String concatenation in SQL queries
   - Example: `query = "SELECT * FROM users WHERE id = " + user_id`
   - Should use: Parameterized queries or ORMs

3. **XSS Vulnerabilities**
   - Check for: Unescaped user input in HTML/templates
   - Example: Direct insertion of user data without sanitization
   - Should use: Template escaping, CSP headers

4. **Authentication/Authorization Bypass**
   - Check for: Missing auth checks on sensitive endpoints
   - Example: Admin routes without authentication
   - Example: Direct object references without permission checks

5. **Exposed Sensitive Data**
   - Check for: Logging passwords, tokens, PII
   - Example: `logger.info(f"User password: {password}")`
   - Example: Error messages revealing system details

6. **Insecure Cryptography**
   - Check for: Weak hashing (MD5, SHA1 for passwords)
   - Example: Using `hashlib.md5()` for passwords
   - Should use: bcrypt, argon2, scrypt

---

#### 🟡 QUALITY WARNINGS

Issues that should be fixed but can be overridden:

1. **DRY Violations (Code Duplication)**
   - Check for: Repeated code blocks > 5 lines
   - Check for: Multiple functions with similar logic
   - Suggest: Extract to shared function/class

2. **Missing Error Handling**
   - Check for: Try/catch blocks missing
   - Check for: No validation of external inputs
   - Check for: Unhandled edge cases (null, empty, invalid)

3. **Performance Concerns**
   - Check for: N+1 database queries
   - Check for: Inefficient loops (nested O(n²))
   - Check for: Missing database indexes on queried fields
   - Check for: Large objects in memory

4. **Design Pattern Violations**
   - Check against: Design principles from `product/tech-docs/design-principles.md`
   - Check for: God classes (too many responsibilities)
   - Check for: Tight coupling
   - Check for: Violation of SOLID principles

5. **Missing Documentation**
   - Check for: Complex logic without comments
   - Check for: Public APIs without docstrings
   - Check for: Magic numbers without explanation

6. **Naming Issues**
   - Check for: Non-descriptive variable names (x, tmp, data)
   - Check for: Inconsistent naming conventions
   - Check for: Misleading names

---

#### ✅ QUALITY CHECKS

Positive checks:

- Code follows design principles
- Proper use of language idioms
- Functions are focused and small (< 50 lines)
- Clear separation of concerns
- Tests cover the changes
- No obvious bugs or logic errors

---

### Step 6: Generate Review Report

Create a structured review report:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REVIEW FINDINGS FOR: {branch name}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FILES REVIEWED:
{list files}

CHANGES:
{stats}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**If blocking issues found:**

```
🔴 BLOCKING ISSUES ({count})

These MUST be fixed before merging:

1. {file}:{line} - {issue type}
   Problem: {description}
   Risk: {security/data loss/corruption impact}
   Fix: {suggested fix}

2. {file}:{line} - {issue type}
   ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**If warnings found:**

```
🟡 WARNINGS ({count})

Should be addressed:

1. {file}:{line} - {issue type}
   Problem: {description}
   Impact: {code quality/maintainability impact}
   Suggestion: {how to improve}

2. {file}:{line} - {issue type}
   ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**If all passed:**

```
✅ PASSED ALL CHECKS

Code quality: Good
Security: No issues found
Design: Follows principles
Tests: Adequate coverage

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### Step 7: User Decision

**If called from `/prodkit.dev` (integrated mode):**

Use AskUserQuestion tool:

```
Question: "Code review complete. Found {X} blocking issues, {Y} warnings."
Options:
1. "Fix issues now" (if blocking issues exist)
2. "Override and continue" (if only warnings)
3. "Cancel"
```

**Response based on choice:**
- **Fix issues**: Exit code review, let user edit, will be called again
- **Override**: Return success with warnings (warnings added to PR body)
- **Cancel**: Exit `/prodkit.dev`

**If standalone mode:**

Just display the report. No action required.

```
Review complete!

To fix issues:
1. Edit the code on branch: {branch}
2. Commit changes
3. Run /prodkit.code-review again to verify

Or create PR with warnings documented.
```

---

### Step 8: Save Review Report (Optional)

For standalone reviews, optionally save report:

```bash
REPORT_FILE="code-review-$(date +%Y%m%d-%H%M%S).md"

cat > "$REPORT_FILE" << EOF
# Code Review Report

**Branch:** $REVIEW_BRANCH
**Base:** $BASE_BRANCH
**Date:** $(date)
**Reviewer:** AI (Claude)

## Summary

- Files changed: {count}
- Blocking issues: {count}
- Warnings: {count}

## Findings

{Full report from Step 6}

EOF

echo "Review report saved to: $REPORT_FILE"
```

---

### Step 9: Validate Review Completed

Run validation:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  VALIDATING REVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Check 1: Diff Analyzed**
```bash
if [ -z "$DIFF" ]; then
    echo "⚠️  Warning: No diff to analyze"
else
    echo "✓ Code diff analyzed"
fi
```

**Check 2: Design Principles Loaded**
```bash
if [ -z "$DESIGN_PRINCIPLES" ]; then
    echo "⚠️  Warning: Design principles not found"
    echo "Create product/tech-docs/design-principles.md for better reviews"
else
    echo "✓ Design principles loaded"
fi
```

**Check 3: Security Guidelines Loaded**
```bash
if [ -z "$SECURITY_GUIDELINES" ]; then
    echo "⚠️  Warning: Security guidelines not found"
    echo "Create product/tech-docs/security.md for security reviews"
else
    echo "✓ Security guidelines loaded"
fi
```

**Check 4: Review Completed**
```bash
echo "✓ Review analysis complete"
```

Display validation complete:
```
✓ All validation checks passed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### Step 10: Exit with Status

**Exit codes:**
- `0` - Review passed or only warnings (can proceed)
- `1` - Blocking issues found (must fix)
- `2` - Configuration error or invalid usage

If integrated in `/prodkit.dev`, use exit code to determine whether to continue.

---

## Important Guidelines

### Security Review Focus

**Always check for:**
- Credentials in code (even in comments)
- SQL concatenation (any string building for queries)
- User input directly in HTML/templates
- Missing authentication checks
- Weak crypto (MD5, SHA1 for passwords)
- Logging sensitive data

### Code Quality Focus

**Look for:**
- Functions > 50 lines (should be split)
- Nested loops > 2 levels deep
- Copy-pasted code
- Unclear variable names (x, data, tmp, val)
- Missing error handling on external calls
- Magic numbers without explanation

### Balance

- Be thorough but not pedantic
- Focus on real issues, not style nitpicks
- Prioritize security > quality > style
- Suggest improvements, don't demand perfection
- Context matters - sometimes "violations" are justified

---

## Output

After this command:
- Code review report displayed
- Blocking issues flagged (if any)
- Warnings noted (if any)
- User can fix issues or proceed
- Optional: Report saved to file
- Exit code indicates pass/fail status

This enables both automated review in workflows and manual review anytime.

## Next Step
This command is complete. The next step in the ProdKit workflow is:
→ `/prodkit.review` (generate sprint retrospective when sprint is complete)
