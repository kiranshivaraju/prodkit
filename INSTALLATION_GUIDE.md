# ProdKit Installation Guide

This document explains how ProdKit can be installed once it's published to GitHub.

## For Users Installing ProdKit

Once ProdKit is published to GitHub, users will have **three installation methods**:

---

### Method 1: One-Line Install (Recommended) ⭐

**What it does:** Downloads and installs ProdKit directly without cloning the repository.

**Command:**
```bash
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/prodkit/main/install-remote.sh | bash -s /path/to/your/project
```

**Example:**
```bash
# Create a new project
mkdir my-product
cd my-product

# Install ProdKit
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/prodkit/main/install-remote.sh | bash -s .

# Start using
# (Open in Claude Code)
# Run: /prodkit.prd
```

**Advantages:**
- ✅ Fastest method
- ✅ No need to clone the repository
- ✅ Always gets latest version
- ✅ Automatic cleanup

---

### Method 2: Clone and Install

**What it does:** Clones the repository first, then runs the installer.

**Commands:**
```bash
# Clone ProdKit
git clone https://github.com/YOUR_USERNAME/prodkit.git

# Install into a project
cd prodkit
./install.sh /path/to/your/project
```

**Example:**
```bash
# Clone ProdKit
git clone https://github.com/YOUR_USERNAME/prodkit.git
cd prodkit

# Create and setup a new project
mkdir ../my-product
./install.sh ../my-product

# Or install in existing project
./install.sh /path/to/existing/project
```

**Advantages:**
- ✅ Can inspect code before installing
- ✅ Can contribute/modify ProdKit
- ✅ Works offline after cloning

---

### Method 3: Manual Install

**What it does:** Manually copy files and set up symlinks.

**Steps:**
```bash
# 1. Download .prodkit directory
git clone https://github.com/YOUR_USERNAME/prodkit.git
cp -r prodkit/.prodkit /path/to/your/project/

# 2. Create symlinks for Claude Code
cd /path/to/your/project
mkdir -p .claude/commands
cd .claude/commands

ln -s ../../.prodkit/commands/prodkit.prd.md prodkit.prd.md
ln -s ../../.prodkit/commands/prodkit.product-arch.md prodkit.product-arch.md
ln -s ../../.prodkit/commands/prodkit.init-repo.md prodkit.init-repo.md
ln -s ../../.prodkit/commands/prodkit.plan-sprint.md prodkit.plan-sprint.md
ln -s ../../.prodkit/commands/prodkit.sprint-tech.md prodkit.sprint-tech.md
ln -s ../../.prodkit/commands/prodkit.create-issues.md prodkit.create-issues.md
ln -s ../../.prodkit/commands/prodkit.dev.md prodkit.dev.md
ln -s ../../.prodkit/commands/prodkit.review.md prodkit.review.md

# 3. Create placeholder directories
cd ../../
mkdir -p product sprints
```

**Advantages:**
- ✅ Full control over installation
- ✅ Can customize installation
- ✅ Educational (see how it works)

---

## What Gets Installed

Regardless of method, ProdKit installs into your project:

```
your-project/
├── .prodkit/
│   ├── config.yml              # Configuration file
│   └── commands/               # Command implementations
│       ├── prodkit.prd.md
│       ├── prodkit.product-arch.md
│       ├── prodkit.init-repo.md
│       ├── prodkit.plan-sprint.md
│       ├── prodkit.sprint-tech.md
│       ├── prodkit.create-issues.md
│       ├── prodkit.dev.md
│       └── prodkit.review.md
│
├── .claude/
│   └── commands/               # Symlinks for Claude Code
│       ├── prodkit.prd.md → ../../.prodkit/commands/prodkit.prd.md
│       ├── prodkit.product-arch.md → ...
│       └── ... (8 symlinks total)
│
├── product/                    # Created by installer
└── sprints/                    # Created by installer
```

---

## Available Commands After Installation

Once installed, open your project in Claude Code and type `/` to see:

- `/prodkit.prd` - Create Product Requirements Document
- `/prodkit.product-arch` - Define system architecture
- `/prodkit.init-repo` - Initialize GitHub repository
- `/prodkit.plan-sprint` - Plan sprint features
- `/prodkit.sprint-tech` - Create sprint technical docs
- `/prodkit.create-issues` - Generate GitHub Issues
- `/prodkit.dev` - Implement one issue with TDD
- `/prodkit.review` - Generate sprint retrospective

---

## How the Remote Installer Works

The `install-remote.sh` script:

1. **Downloads** ProdKit from GitHub to a temporary directory
2. **Runs** the local `install.sh` script
3. **Cleans up** the temporary directory
4. **Reports** success

**Under the hood:**
```bash
# User runs:
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/prodkit/main/install-remote.sh | bash -s .

# Script does:
1. git clone --depth 1 https://github.com/YOUR_USERNAME/prodkit.git /tmp/prodkit
2. /tmp/prodkit/install.sh .
3. rm -rf /tmp/prodkit
```

---

## Comparison to Speckit

| Feature | Speckit | ProdKit |
|---------|---------|---------|
| **Purpose** | Feature-level development | Product-level development |
| **Installation** | `git clone` + setup | `curl` one-liner OR `git clone` |
| **Commands** | `/speckit.specify`, etc. | `/prodkit.prd`, etc. |
| **Scope** | Single features | Complete products across sprints |
| **Integration** | Standalone | Uses Speckit for `/prodkit.dev` |

---

## For Maintainers: Publishing to GitHub

To make ProdKit available for users:

1. **Push to GitHub:**
   ```bash
   git init
   gh repo create prodkit --public --source=.
   git add .
   git commit -m "feat: initial release"
   git push -u origin main
   ```

2. **Update placeholders:**
   Replace `YOUR_USERNAME` in:
   - `README.md`
   - `QUICKSTART.md`
   - `install-remote.sh`
   - `GITHUB_SETUP.md`

3. **Create release:**
   ```bash
   git tag -a v1.0.0 -m "Initial release"
   git push origin v1.0.0
   gh release create v1.0.0
   ```

4. **Share the install command:**
   ```bash
   curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/prodkit/main/install-remote.sh | bash -s .
   ```

See `GITHUB_SETUP.md` for complete publishing instructions.

---

## Troubleshooting

### Installation fails with "Failed to download ProdKit"

**Cause:** Repository not public or doesn't exist

**Solution:**
- Check the repository URL
- Ensure repository is public
- Check internet connection

### Commands don't show up in Claude Code

**Cause:** Claude Code hasn't refreshed

**Solution:**
- Restart Claude Code
- Or verify symlinks exist: `ls -la .claude/commands/`

### Permission denied when running install script

**Cause:** Script not executable

**Solution:**
```bash
chmod +x install.sh
./install.sh .
```

---

## Next Steps

After installation:

1. ✅ Open project in Claude Code
2. ✅ Type `/prodkit.prd` to start
3. ✅ Follow the workflow (see `QUICKSTART.md`)
4. ✅ Build your product!

For detailed usage, see:
- `README.md` - Complete documentation
- `QUICKSTART.md` - 5-minute getting started guide
- `CONTRIBUTING.md` - How to contribute to ProdKit
