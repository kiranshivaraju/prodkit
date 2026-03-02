---
description: Research competitors and validate market fit for your product
---

You are helping the user conduct market research for their product to validate the idea and understand the competitive landscape.

## Context

Market research should be done AFTER the PRD is created and BEFORE defining the technical architecture. This ensures the user doesn't invest time building something that already exists or misses key differentiators.

This command reads the PRD (`product/prd.md`) and uses it to research competitors, analyze market gaps, and recommend a differentiation strategy.

## Prerequisites

- `/prodkit.prd` must have been run (PRD exists at `product/prd.md`)

## Instructions

### Step 1: Read the PRD

Read `product/prd.md` to extract:
- Product name
- Problem statement
- Target users
- All planned features
- Value proposition

If `product/prd.md` does not exist:
```
❌ Error: PRD not found at product/prd.md
Please run /prodkit.prd first to create your Product Requirements Document.
```

### Step 2: Identify Competitors

Based on the PRD, research and identify existing products, tools, and services that:
- Solve the same or similar problem
- Target the same user base
- Offer overlapping features

For each competitor, gather:
- **Name** and website/URL
- **Description** — what it does
- **Pricing model** — free, freemium, paid, enterprise
- **Key features** — what it offers
- **Strengths** — what it does well
- **Weaknesses** — where it falls short
- **Target audience** — who uses it

Aim to identify 3-8 competitors. If the space is very niche, fewer is fine.

### Step 3: Build Feature Comparison

Create a feature comparison matrix:
- Rows: each feature from the user's PRD
- Columns: each competitor + the user's product
- Values: ✅ (has it), ❌ (doesn't have it), 🔶 (partial/limited)

### Step 4: Analyze Market Gaps

Based on the competitor research:
- What features do competitors lack that the user's product offers?
- What underserved user segments exist?
- What pain points do competitor users complain about?
- Are there pricing gaps (e.g., no good free/open-source option)?

### Step 5: Assess Risks

Identify potential risks:
- Is the market oversaturated?
- Are there dominant players with strong network effects?
- Is the problem being solved well enough already?
- Are there barriers to entry (data, integrations, regulatory)?

### Step 6: Generate Recommendations

Based on all findings, recommend:
- **Differentiation strategy** — how the user's product should position itself
- **Features to prioritize** — which features matter most for standing out
- **Features to reconsider** — any features that don't add competitive value
- **Go-to-market suggestions** — how to reach the target users

### Step 7: Create the Report

Write the market research report at: `product/market-research.md`

Use this structure:

```markdown
# Market Research Report

## Product Overview

**Product:** [Name from PRD]

**Problem:** [Problem statement from PRD]

**Date:** [Current Date]

## Competitor Analysis

### Competitor 1: [Name]
- **Website:** [URL]
- **Description:** [What it does]
- **Pricing:** [Pricing model]
- **Key Features:** [List]
- **Strengths:** [What it does well]
- **Weaknesses:** [Where it falls short]
- **Target Audience:** [Who uses it]

### Competitor 2: [Name]
[Same structure]

[Continue for all competitors...]

## Feature Comparison

| Feature | Our Product | Competitor 1 | Competitor 2 | ... |
|---------|------------|--------------|--------------|-----|
| Feature A | ✅ | ✅ | ❌ | ... |
| Feature B | ✅ | ❌ | 🔶 | ... |
[Continue for all features...]

## Market Gaps & Opportunities

[Analysis of underserved needs, missing features in the market, pricing gaps]

## Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| [Risk 1] | High/Medium/Low | [How to mitigate] |
[Continue...]

## Differentiation Strategy

[How to position the product to stand out]

## Recommendations

### Features to Prioritize
[Features that provide the strongest competitive advantage]

### Features to Reconsider
[Features that don't add competitive value or are table stakes]

### Go-to-Market
[Suggestions for reaching target users]

## Conclusion

[Summary of findings and overall market viability assessment]
```

### Step 8: Validate Report

Display validation in progress:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  VALIDATING MARKET RESEARCH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Check 1: Report File Exists**
```bash
REPORT_FILE="product/market-research.md"

if [ ! -f "$REPORT_FILE" ]; then
    echo "❌ Validation failed: Market research report not found"
    echo "Expected: $REPORT_FILE"
    exit 1
fi

echo "✓ Market research report exists"
```

**Check 2: Report Has Content**
```bash
if [ ! -s "$REPORT_FILE" ]; then
    echo "❌ Validation failed: Report is empty"
    exit 1
fi

echo "✓ Report has content"
```

**Check 3: Report Has Required Sections**
```bash
MISSING_SECTIONS=()

if ! grep -q "## Competitor Analysis" "$REPORT_FILE"; then MISSING_SECTIONS+=("Competitor Analysis"); fi
if ! grep -q "## Feature Comparison" "$REPORT_FILE"; then MISSING_SECTIONS+=("Feature Comparison"); fi
if ! grep -q "## Market Gaps" "$REPORT_FILE"; then MISSING_SECTIONS+=("Market Gaps & Opportunities"); fi
if ! grep -q "## Risk Assessment" "$REPORT_FILE"; then MISSING_SECTIONS+=("Risk Assessment"); fi
if ! grep -q "## Differentiation Strategy" "$REPORT_FILE"; then MISSING_SECTIONS+=("Differentiation Strategy"); fi
if ! grep -q "## Recommendations" "$REPORT_FILE"; then MISSING_SECTIONS+=("Recommendations"); fi

if [ ${#MISSING_SECTIONS[@]} -gt 0 ]; then
    echo "❌ Validation failed: Report missing required sections: ${MISSING_SECTIONS[*]}"
    exit 1
fi

echo "✓ Report has all required sections"
```

**Check 4: Competitors Identified**
```bash
COMPETITOR_COUNT=$(grep -c "^### Competitor" "$REPORT_FILE" || echo "0")

if [ "$COMPETITOR_COUNT" -lt 1 ]; then
    echo "⚠️  Warning: No competitors identified"
else
    echo "✓ Found $COMPETITOR_COUNT competitor(s) analyzed"
fi
```

Display validation complete:
```
✓ All validation checks passed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 9: Confirm Completion

After creating and validating the report, inform the user:
- ✓ Market research report created at `product/market-research.md`
- Number of competitors analyzed
- Key differentiation opportunities identified
- Next step: Run `/prodkit.product-arch` to define the technical architecture

## Important Notes

- This research is based on Claude's training data and general knowledge — it is not a substitute for real-time market research
- Encourage the user to validate findings with actual user interviews and market data
- Focus on actionable insights, not just listing competitors
- Be honest about risks — if the market is saturated, say so
- The goal is to help the user build something people actually need
