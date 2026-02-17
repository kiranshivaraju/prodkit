# ProdKit Quick Start Guide

Get up and running with ProdKit in 5 minutes.

## Prerequisites

Before you start, make sure you have:

- ✅ Claude Code installed
- ✅ Git installed
- ✅ GitHub Personal Access Token (instructions provided during setup)
- ✅ Speckit installed (optional, automatically installed by ProdKit)

## Installation

```bash
# Install ProdKit globally
uv tool install prodkit-cli --from git+https://github.com/kiranshivaraju/prodkit.git

# Initialize in your project directory
mkdir my-new-product
cd my-new-product
prodkit init . --ai claude
```

Then open the project directory in Claude Code.

## Your First Product

### Step 1: Create PRD (5 minutes)

In Claude Code, type:

```
/prodkit.prd
```

Answer Claude's questions about your product:
- What problem does it solve?
- Who are the users?
- What are the main features?

**Output:** `product/prd.md`

### Step 2: Define Architecture (10 minutes)

```
/prodkit.product-arch
```

Choose your tech stack:
- Programming language (Python, Node.js, etc.)
- Database (PostgreSQL, MongoDB, etc.)
- Framework (FastAPI, Express, etc.)

**Output:** `product/tech-docs/` + `.speckit/constitution.md`

### Step 3: Initialize Repository (5 minutes)

```
/prodkit.init-repo
```

This sets up:
- Project structure (src/, tests/)
- CI/CD pipeline
- GitHub repository
- Sprint v1 milestone

**Output:** Complete project structure + GitHub repo

### Step 4: Plan First Sprint (10 minutes)

```
/prodkit.plan-sprint
```

Select 2-4 features from your PRD to build first.

Recommendation: Start with authentication and core models.

**Output:** `sprints/v1/sprint-plan.md`

### Step 5: Create Technical Specs (15 minutes)

```
/prodkit.sprint-tech
```

Claude will create detailed technical documentation:
- Data models with schemas
- API endpoints with examples
- Component designs
- Implementation plan

**Output:** `sprints/v1/tech-docs/`

### Step 6: Generate GitHub Issues (5 minutes)

```
/prodkit.create-issues
```

Converts tech docs into GitHub Issues.

**Output:** 10-20 GitHub Issues created

### Step 7: Start Development (30 minutes per issue)

```
/prodkit.dev
```

This command:
1. Picks highest priority open issue
2. Uses Speckit to implement it with TDD
3. Writes tests first
4. Implements code
5. Creates Pull Request

Run repeatedly until all issues are done:

```
/prodkit.dev
/prodkit.dev
/prodkit.dev
... (repeat)
```

### Step 8: Sprint Review (10 minutes)

When sprint is complete:

```
/prodkit.review
```

Generates comprehensive sprint retrospective.

**Output:** `sprints/v1/sprint-review.md`

## Example Timeline

Building a simple auth + CRUD app:

| Day | Activity | Command | Time |
|-----|----------|---------|------|
| 1 | Define product | `/prodkit.prd` | 1 hour |
| 1 | Architecture | `/prodkit.product-arch` | 1 hour |
| 1 | Setup repo | `/prodkit.init-repo` | 30 min |
| 2 | Plan sprint | `/prodkit.plan-sprint` | 1 hour |
| 2 | Tech specs | `/prodkit.sprint-tech` | 2 hours |
| 2 | Create issues | `/prodkit.create-issues` | 30 min |
| 3-5 | Development | `/prodkit.dev` (x15) | 3 days |
| 5 | Sprint review | `/prodkit.review` | 1 hour |

**Total:** ~5 days to first working product

## Tips for Success

### Planning Phase

- **Be thorough in the PRD** - The more detail, the better
- **Start small** - Sprint v1 should be foundation only
- **Consider dependencies** - Build in logical order

### Technical Specs

- **Extreme detail** - Include ALL validation rules, error cases
- **Examples everywhere** - JSON examples, SQL queries, code snippets
- **Complete acceptance criteria** - Make it testable

### Development

- **Run /prodkit.dev in batches** - Do 3-5 issues, then review
- **Review PRs manually** - Don't auto-merge everything
- **Test coverage matters** - Aim for 80%+

### Common Mistakes to Avoid

❌ Planning too many features in Sprint v1
✅ Start with 2-3 core features

❌ Vague technical specs
✅ Include every validation rule and error case

❌ Skipping tests
✅ Follow TDD - tests first, always

❌ Not reviewing code
✅ Review PRs before merging

## What to Build First?

Good Sprint v1 features:
- ✅ User authentication
- ✅ Core data models
- ✅ Basic CRUD operations
- ✅ Database setup

Bad Sprint v1 features:
- ❌ Advanced analytics
- ❌ Email notifications
- ❌ Third-party integrations
- ❌ Admin dashboard

## Getting Help

- 📖 Full documentation: See `README.md`
- 🐛 Found a bug? Open an issue
- 💡 Have an idea? Open a discussion
- 🤝 Want to contribute? See `CONTRIBUTING.md`

## Next Steps

After your first sprint:

1. Review what worked and what didn't
2. Plan Sprint v2 with `/prodkit.plan-sprint`
3. Repeat the process

Each sprint gets faster as you learn the workflow!

---

**Ready?** Run `/prodkit.prd` and start building! 🚀
