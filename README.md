# ProdKit

**Enterprise-grade product development workflow for AI coding agents**

ProdKit is a framework that brings real-world company development processes to AI-assisted development. Inspired by GitHub's Speckit, ProdKit provides structure and automation for building complete products across multiple sprints.

---

## What is ProdKit?

ProdKit helps you build products systematically by:

1. **Planning** - Define your product vision and break it into sprints
2. **Designing** - Create detailed technical documentation
3. **Implementing** - Automated development with Test-Driven Development (TDD)
4. **Tracking** - GitHub Issues integration for complete visibility
5. **Reviewing** - Sprint retrospectives and code walkthroughs

---

## Key Features

- ✅ **Product-level architecture** - Strategic decisions that apply across all sprints
- ✅ **Sprint-based development** - Organized, incremental feature delivery
- ✅ **GitHub integration** - Issues, PRs, milestones for tracking
- ✅ **Speckit integration** - Automated development with TDD
- ✅ **Detailed documentation** - PRDs, tech specs, and sprint reviews
- ✅ **Test coverage enforcement** - 80% minimum coverage
- ✅ **DRY principle** - Avoid duplication at all costs

---

## Installation

Choose one of the installation methods below:

### Method 1: One-Line Install (Recommended)

Install directly from GitHub without cloning:

```bash
# Install into your project directory
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/prodkit/main/install-remote.sh | bash -s /path/to/your/project

# Or install in current directory
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/prodkit/main/install-remote.sh | bash -s .
```

> **Note:** Replace `YOUR_USERNAME` with the actual GitHub username after you push the repository.

### Method 2: Clone and Install

```bash
# Clone ProdKit
git clone https://github.com/YOUR_USERNAME/prodkit.git
cd prodkit

# Install into your project
./install.sh /path/to/your/project

# Or install in current directory
./install.sh .
```

### Method 3: Manual Install

1. **Download ProdKit:**
   ```bash
   git clone https://github.com/yourusername/prodkit.git
   ```

2. **Copy to your project:**
   ```bash
   cp -r prodkit/.prodkit /path/to/your/project/
   ```

3. **Set up Claude Code commands:**
   ```bash
   cd /path/to/your/project
   mkdir -p .claude/commands
   cd .claude/commands
   ln -s ../../.prodkit/commands/prodkit.prd.md prd.md
   ln -s ../../.prodkit/commands/prodkit.product-arch.md product-arch.md
   ln -s ../../.prodkit/commands/prodkit.init-repo.md init-repo.md
   ln -s ../../.prodkit/commands/prodkit.plan-sprint.md plan-sprint.md
   ln -s ../../.prodkit/commands/prodkit.sprint-tech.md sprint-tech.md
   ln -s ../../.prodkit/commands/prodkit.create-issues.md create-issues.md
   ln -s ../../.prodkit/commands/prodkit.dev.md dev.md
   ln -s ../../.prodkit/commands/prodkit.review.md review.md
   ```

4. **Verify installation:**
   Open your project in Claude Code and type `/` - you should see all ProdKit commands.

---

## Workflow Overview

### One-Time Setup

```bash
/prodkit.prd           # Create Product Requirements Document
/prodkit.product-arch  # Define system architecture
/prodkit.init-repo     # Initialize GitHub repository
```

### Per Sprint

```bash
/prodkit.plan-sprint   # Select features for this sprint
/prodkit.sprint-tech   # Create detailed technical docs
/prodkit.create-issues # Generate GitHub Issues
/prodkit.dev           # Implement one issue (repeat until done)
/prodkit.review        # Generate sprint retrospective
```

---

## Commands Reference

### `/prodkit.prd`

**Create Product Requirements Document**

Defines WHAT the product is and WHY it exists. Contains all features, user stories, and success metrics.

**Output:** `product/prodkit.prd.md`

**Run:** Once per product

---

### `/prodkit.product-arch`

**Define Product-Level Architecture**

Creates strategic technical documentation including system architecture, tech stack, security standards, API conventions, and testing strategy. Also creates Speckit constitution for development defaults.

**Output:**
- `product/tech-docs/` (6 documents)
- `.speckit/constitution.md`

**Run:** Once per product (or when major architectural changes needed)

---

### `/prodkit.init-repo`

**Initialize GitHub Repository**

Sets up project structure, CI/CD pipeline, testing framework, and GitHub repository with branch protection.

**Output:**
- Project structure (src/, tests/, docs/)
- `.gitignore`, `README.md`
- GitHub Actions CI/CD
- Sprint v1 milestone

**Run:** Once per product

---

### `/prodkit.plan-sprint`

**Plan Sprint Features**

Select which features from the PRD to build in this sprint. Define sprint goal and success criteria.

**Output:** `sprints/v{N}/sprint-plan.md`

**Run:** Once per sprint

---

### `/prodkit.sprint-tech`

**Create Sprint Technical Documentation**

Detailed implementation specs for sprint features including data models, API endpoints, component design, and step-by-step implementation plan.

**Output:** `sprints/v{N}/tech-docs/`
- `data-models.md`
- `api-endpoints.md`
- `implementation-plan.md`
- `component-design.md`

**Run:** Once per sprint

---

### `/prodkit.create-issues`

**Generate GitHub Issues**

Converts sprint technical documentation into detailed GitHub Issues with complete specifications, testing requirements, and acceptance criteria.

**Output:**
- GitHub Issues (created via API)
- `sprints/v{N}/issues-summary.md`

**Run:** Once per sprint

---

### `/prodkit.dev`

**Implement One GitHub Issue**

Fetches the highest priority open issue and implements it using Speckit's TDD workflow. Writes tests first, implements code, creates PR.

**Flow:**
1. Fetch highest priority issue
2. Create feature branch
3. Run Speckit workflow (specify → plan → tasks → implement)
4. Write tests FIRST (unit, contract, integration)
5. Implement code
6. Verify all tests pass
7. Create Pull Request
8. Link PR to issue

**Run:** Repeatedly until all sprint issues are complete

---

### `/prodkit.review`

**Generate Sprint Retrospective**

Creates comprehensive sprint review with metrics, code walkthrough, accomplishments, and recommendations for next sprint.

**Output:** `sprints/v{N}/sprint-review.md`

**Run:** Once at the end of each sprint

---

## File Structure

After setup, your project will look like:

```
your-project/
├── .prodkit/
│   ├── config.yml          # ProdKit configuration
│   └── commands/           # Slash command definitions
│       ├── prd.md
│       ├── product-arch.md
│       ├── init-repo.md
│       ├── plan-sprint.md
│       ├── sprint-tech.md
│       ├── create-issues.md
│       ├── dev.md
│       └── review.md
│
├── .speckit/
│   └── constitution.md     # Speckit development defaults
│
├── product/
│   ├── prd.md              # Product Requirements Document
│   └── tech-docs/          # Product-level technical docs
│       ├── architecture.md
│       ├── design-principles.md
│       ├── security.md
│       ├── data-architecture.md
│       ├── api-strategy.md
│       └── testing-strategy.md
│
├── sprints/
│   ├── v1/
│   │   ├── sprint-plan.md
│   │   ├── tech-docs/
│   │   │   ├── data-models.md
│   │   │   ├── api-endpoints.md
│   │   │   ├── implementation-plan.md
│   │   │   └── component-design.md
│   │   ├── issues-summary.md
│   │   └── sprint-review.md
│   └── v2/
│       └── ...
│
├── src/                    # Source code
├── tests/
│   ├── unit/
│   ├── contract/
│   └── integration/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
└── README.md
```

---

## Example: Building a Web Scraper

### Step 1: Define Product

```bash
$ /prodkit.prd
```

You define:
- Product: Web Scraper SaaS
- Features: Auth, Scraping Engine, Scheduling, API, Dashboard, Export
- 15 total features identified

### Step 2: Architecture

```bash
$ /prodkit.product-arch
```

Decisions made:
- Python + FastAPI + PostgreSQL + Redis
- JWT authentication
- REST API
- Microservices architecture
- TDD with pytest

### Step 3: Initialize Repo

```bash
$ /prodkit.init-repo
```

Creates project structure and GitHub repo.

### Step 4: Plan Sprint 1

```bash
$ /prodkit.plan-sprint
```

You select:
- Feature 1: User Authentication
- Feature 2: Basic Scraping Engine

Sprint goal: "Enable users to authenticate and perform basic web scraping"

### Step 5: Technical Design

```bash
$ /prodkit.sprint-tech
```

Creates detailed specs:
- User, RefreshToken data models
- POST /auth/register, POST /auth/login endpoints
- AuthService, ScraperEngine components
- Complete implementation plan

### Step 6: Create GitHub Issues

```bash
$ /prodkit.create-issues
```

Creates 18 issues:
- #1: [P0][infrastructure] Database migrations
- #2: [P0][feature] Implement User model
- #3: [P0][unit-test] User model tests
- ... and 15 more

### Step 7: Development

```bash
$ /prodkit.dev
```

Implements Issue #1 using Speckit:
- Writes tests first
- Implements code
- All tests pass
- Creates PR #1

```bash
$ /prodkit.dev
```

Implements Issue #2...

(Repeat 18 times until all issues done)

### Step 8: Sprint Review

```bash
$ /prodkit.review
```

Generates comprehensive review:
- 18/18 issues completed (100%)
- 15 PRs merged
- 92% test coverage
- Code walkthrough
- Ready for Sprint v2

### Step 9: Sprint 2

```bash
$ /prodkit.plan-sprint
```

Select next features (Scheduling, Dashboard) and repeat!

---

## Prerequisites

Before installing ProdKit, ensure you have:

1. **Claude Code** - ProdKit uses Claude Code slash commands
   - Download from https://claude.com/claude-code

2. **Git** - Version control
   ```bash
   # Verify installation
   git --version
   ```

3. **GitHub Personal Access Token (PAT)** - For GitHub API integration
   - Go to https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select scopes: `repo`, `workflow`
   - Copy and save the token securely
   - You'll provide this token when running ProdKit commands

4. **Speckit** (Optional) - For automated development with `/prodkit.dev`
   ```bash
   # Install Speckit
   git clone https://github.com/github/spec-kit.git
   cd spec-kit
   # Follow installation instructions in their README
   ```

5. **jq** (Optional but recommended) - For parsing JSON from GitHub API
   ```bash
   # macOS
   brew install jq

   # Linux (Debian/Ubuntu)
   sudo apt install jq
   ```

---

## Configuration

Edit `.prodkit/config.yml` to customize:

```yaml
project:
  name: "my-project"
  type: "python"  # or node, go, rust, etc.

github:
  repo: "username/repo-name"

testing:
  framework: "pytest"  # or jest, etc.
  min_coverage: 80

development:
  workflow: "speckit"
  auto_push: false  # Manual review before pushing
```

---

## Best Practices

### Planning

- **Start small** - Sprint v1 should focus on foundation (auth, core models)
- **Realistic scope** - 2-4 weeks of work per sprint
- **Dependencies** - Build features in logical order

### Technical Documentation

- **Be extremely detailed** - The more detail in tech docs, the fewer questions during development
- **Include ALL edge cases** - What happens when inputs are null, empty, invalid?
- **Specify error messages** - Don't say "return error", say exactly what the error should be

### Development

- **Test-Driven Development** - ALWAYS write tests BEFORE code
- **DRY Principle** - Avoid duplication at all costs
- **Code quality** - 80% test coverage minimum, linter must pass
- **Security** - Follow security standards from product/tech-docs/security.md

### GitHub Issues

- **Complete specifications** - Copy ALL details from tech docs into issue descriptions
- **Clear acceptance criteria** - Specific, measurable, testable
- **Testing requirements** - List exactly what tests are needed

---

## FAQ

### Q: How is ProdKit different from Speckit?

**Speckit** is feature-focused (build one feature at a time).

**ProdKit** is product-focused (build entire products across multiple sprints with strategic architecture).

ProdKit uses Speckit for the development phase (`/prodkit.dev`).

### Q: Do I need to use GitHub?

Yes, ProdKit integrates with GitHub for issue tracking, PRs, and milestones. This provides visibility and mimics real company workflows.

### Q: Can I customize the workflow?

Yes! Edit the command files in `.prodkit/commands/` to customize the workflow.

### Q: What if Speckit asks questions during /prodkit.dev?

The detailed tech docs and Speckit constitution should answer 90% of questions. If Speckit still asks, ProdKit will pause and ask you for input.

### Q: Can I use this for non-Python projects?

Yes! ProdKit supports any language. Update `.prodkit/config.yml` with your language/framework.

### Q: How do I run /prodkit.dev overnight without interruptions?

Make sure:
1. Sprint tech docs are extremely detailed
2. Speckit constitution has comprehensive defaults
3. Test your first few `/prodkit.dev` runs to ensure no questions are asked

---

## Troubleshooting

### GitHub CLI not authenticated

```bash
gh auth login
```

### Speckit not found

Install Speckit:
```bash
# Follow instructions at https://github.com/github/spec-kit
```

### Tests failing during /prodkit.dev

- Review test failures
- Fix the code or tests
- Re-run until all tests pass
- ProdKit will not create PR until tests pass

---

## Credits

- Inspired by [GitHub Speckit](https://github.com/github/spec-kit)
- Built for use with Claude Code
- Follows enterprise software development best practices

---

## License

[Your license here]

---

**Ready to build?** Start with `/prodkit.prd` and create your first product!

🤖 Generated with ProdKit
