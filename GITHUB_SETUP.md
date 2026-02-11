# Setting Up ProdKit on GitHub

This guide explains how to push ProdKit to GitHub so others can use it.

## Step 1: Initialize Git Repository

If not already done:

```bash
cd /path/to/prodkit
git init
```

## Step 2: Create GitHub Repository

### Option A: Using GitHub CLI (Recommended)

```bash
gh repo create prodkit --public --source=. --description="Enterprise-grade product development workflow for AI coding agents"
```

### Option B: Using GitHub Web Interface

1. Go to https://github.com/new
2. Repository name: `prodkit`
3. Description: `Enterprise-grade product development workflow for AI coding agents`
4. Visibility: Public
5. Do NOT initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

Then connect your local repo:

```bash
git remote add origin https://github.com/kiranshivaraju/prodkit.git
```

## Step 3: Commit and Push

```bash
# Stage all files
git add .

# Create initial commit
git commit -m "feat: initial release of ProdKit

ProdKit is an enterprise-grade product development workflow framework
for AI coding agents. Includes:

- Product Requirements Document (PRD) creation
- Product and sprint-level architecture documentation
- GitHub integration with issues, PRs, and milestones
- Speckit integration for TDD development
- Automated sprint reviews

Commands:
- /prodkit.prd - Create PRD
- /prodkit.product-arch - Define architecture
- /prodkit.init-repo - Initialize repository
- /prodkit.plan-sprint - Plan sprint
- /prodkit.sprint-tech - Create technical specs
- /prodkit.create-issues - Generate GitHub issues
- /prodkit.dev - Implement issue with TDD
- /prodkit.review - Generate sprint review

Inspired by GitHub Speckit"

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 4: Set Up Repository

### Add Topics

Add relevant topics to help people discover ProdKit:

```bash
gh repo edit --add-topic "ai"
gh repo edit --add-topic "claude-code"
gh repo edit --add-topic "development-workflow"
gh repo edit --add-topic "tdd"
gh repo edit --add-topic "github-integration"
gh repo edit --add-topic "project-management"
gh repo edit --add-topic "sprint-planning"
```

Or via web:
- Go to your repository
- Click the gear icon next to "About"
- Add topics: `ai`, `claude-code`, `development-workflow`, `tdd`, `github-integration`

### Set Repository Description

```bash
gh repo edit --description "Enterprise-grade product development workflow for AI coding agents"
```

### Add Website

```bash
gh repo edit --homepage "https://github.com/kiranshivaraju/prodkit"
```

## Step 5: Create a Release

### Tag the First Release

```bash
git tag -a v1.0.0 -m "ProdKit v1.0.0 - Initial Release

Features:
- Complete product development workflow
- 8 slash commands for Claude Code
- GitHub integration
- Speckit integration for TDD
- Sprint-based development
- Comprehensive documentation"

git push origin v1.0.0
```

### Create GitHub Release

```bash
gh release create v1.0.0 \
  --title "ProdKit v1.0.0 - Initial Release" \
  --notes "## ProdKit v1.0.0

**First stable release!**

### Features

- ✅ Complete product development workflow
- ✅ 8 slash commands for Claude Code
- ✅ GitHub integration (issues, PRs, milestones)
- ✅ Speckit integration for automated TDD
- ✅ Sprint-based development
- ✅ Comprehensive documentation

### Commands

- \`/prodkit.prd\` - Create Product Requirements Document
- \`/prodkit.product-arch\` - Define system architecture
- \`/prodkit.init-repo\` - Initialize GitHub repository
- \`/prodkit.plan-sprint\` - Plan sprint features
- \`/prodkit.sprint-tech\` - Create sprint technical docs
- \`/prodkit.create-issues\` - Generate GitHub Issues
- \`/prodkit.dev\` - Implement issue with TDD (uses Speckit)
- \`/prodkit.review\` - Generate sprint retrospective

### Installation

\`\`\`bash
git clone https://github.com/kiranshivaraju/prodkit.git
cd prodkit
./install.sh /path/to/your/project
\`\`\`

### Documentation

- 📖 [README](README.md) - Full documentation
- 🚀 [Quick Start](QUICKSTART.md) - Get started in 5 minutes
- 🤝 [Contributing](CONTRIBUTING.md) - Contribution guidelines

### Requirements

- Claude Code
- GitHub CLI (gh)
- Git
- Speckit (optional, for /dev command)

---

**Ready to build?** See [QUICKSTART.md](QUICKSTART.md) to get started!"
```

## Step 6: Update README with Correct URLs

After pushing, update all placeholder URLs in README.md:

1. Replace `kiranshivaraju` with your actual GitHub username
2. Replace `yourusername` with your GitHub username

```bash
# Example using sed (macOS)
sed -i '' 's/kiranshivaraju/your-actual-username/g' README.md
sed -i '' 's/yourusername/your-actual-username/g' README.md QUICKSTART.md CONTRIBUTING.md

# Commit the changes
git add README.md QUICKSTART.md CONTRIBUTING.md
git commit -m "docs: update URLs with actual GitHub username"
git push
```

## Step 7: Add Badges (Optional)

Add badges to your README for polish:

```markdown
# ProdKit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub release](https://img.shields.io/github/v/release/kiranshivaraju/prodkit)](https://github.com/kiranshivaraju/prodkit/releases)
[![GitHub stars](https://img.shields.io/github/stars/kiranshivaraju/prodkit)](https://github.com/kiranshivaraju/prodkit/stargazers)
```

## Step 8: Set Up GitHub Pages (Optional)

If you want a website for ProdKit:

```bash
gh repo edit --enable-pages --pages-branch main
```

## Step 9: Enable Discussions

```bash
gh repo edit --enable-discussions
```

## Step 10: Share Your Work!

Share ProdKit with the community:

- Tweet about it with #ClaudeCode #AI #DevTools
- Share on LinkedIn
- Post in relevant Discord/Slack communities
- Share on Reddit (r/ClaudeAI, r/programming)
- Write a blog post about how you built it

## Repository Settings Checklist

After setup, verify these settings:

- ✅ Public repository
- ✅ Topics added
- ✅ Description set
- ✅ License (MIT)
- ✅ README displayed
- ✅ v1.0.0 release created
- ✅ Discussions enabled (optional)
- ✅ GitHub Pages enabled (optional)

## Sample Repository URLs

After setup, your repository will have:

- **Main page:** `https://github.com/kiranshivaraju/prodkit`
- **Releases:** `https://github.com/kiranshivaraju/prodkit/releases`
- **Issues:** `https://github.com/kiranshivaraju/prodkit/issues`
- **Discussions:** `https://github.com/kiranshivaraju/prodkit/discussions`
- **Clone URL:** `https://github.com/kiranshivaraju/prodkit.git`

## Maintenance

### For Future Updates

```bash
# Make changes
git add .
git commit -m "feat: add new feature"
git push

# Create new release
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin v1.1.0
gh release create v1.1.0 --title "v1.1.0" --notes "Release notes here"
```

---

**Congratulations!** ProdKit is now live on GitHub. 🎉

## How Users Will Install ProdKit

Users can now install ProdKit in multiple ways:

### Method 1: One-Line Install (Recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/kiranshivaraju/prodkit/main/install-remote.sh | bash -s /path/to/project
```

### Method 2: Clone and Install

```bash
git clone https://github.com/kiranshivaraju/prodkit.git
cd prodkit
./install.sh /path/to/project
```

### Method 3: Manual Install

See README.md for manual installation instructions.

**Remember to update `kiranshivaraju` in README.md and QUICKSTART.md with your actual GitHub username!**
