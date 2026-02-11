#!/bin/bash

# ProdKit Installation Script
# This script installs ProdKit into your project

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ProdKit Installer"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Get the target directory (current directory by default, or first argument)
TARGET_DIR="${1:-.}"
TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"

echo "Installing ProdKit to: $TARGET_DIR"
echo ""

# Check if .prodkit already exists
if [ -d "$TARGET_DIR/.prodkit" ]; then
    echo "⚠️  ProdKit is already installed in this directory."
    read -p "Do you want to overwrite? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 1
    fi
    rm -rf "$TARGET_DIR/.prodkit"
fi

# Create .prodkit directory structure
echo "→ Creating .prodkit directory..."
mkdir -p "$TARGET_DIR/.prodkit/commands"

# Copy config and commands
echo "→ Copying configuration..."
cp "$SCRIPT_DIR/.prodkit/config.yml" "$TARGET_DIR/.prodkit/config.yml"

echo "→ Copying command files..."
cp "$SCRIPT_DIR/.prodkit/commands/"*.md "$TARGET_DIR/.prodkit/commands/"

# Create .claude/commands directory
echo "→ Setting up Claude Code commands..."
mkdir -p "$TARGET_DIR/.claude/commands"

# Create symlinks in .claude/commands
cd "$TARGET_DIR/.claude/commands"

echo "→ Creating command symlinks..."
ln -sf ../../.prodkit/commands/prodkit.prd.md prodkit.prd.md
ln -sf ../../.prodkit/commands/prodkit.product-arch.md prodkit.product-arch.md
ln -sf ../../.prodkit/commands/prodkit.init-repo.md prodkit.init-repo.md
ln -sf ../../.prodkit/commands/prodkit.plan-sprint.md prodkit.plan-sprint.md
ln -sf ../../.prodkit/commands/prodkit.sprint-tech.md prodkit.sprint-tech.md
ln -sf ../../.prodkit/commands/prodkit.create-issues.md prodkit.create-issues.md
ln -sf ../../.prodkit/commands/prodkit.dev.md prodkit.dev.md
ln -sf ../../.prodkit/commands/prodkit.review.md prodkit.review.md

cd "$TARGET_DIR"

# Create placeholder directories
echo "→ Creating placeholder directories..."
mkdir -p "$TARGET_DIR/product"
mkdir -p "$TARGET_DIR/sprints"

# Create .gitignore if it doesn't exist
if [ ! -f "$TARGET_DIR/.gitignore" ]; then
    echo "→ Creating .gitignore..."
    cat > "$TARGET_DIR/.gitignore" << 'EOF'
# ProdKit
.prodkit/cache/

# OS
.DS_Store
Thumbs.db

# IDEs
.vscode/
.idea/
*.swp
*.swo
EOF
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅ ProdKit installed successfully!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Available commands:"
echo "  /prodkit.prd            - Create Product Requirements Document"
echo "  /prodkit.product-arch   - Define system architecture"
echo "  /prodkit.init-repo      - Initialize GitHub repository"
echo "  /prodkit.plan-sprint    - Plan sprint features"
echo "  /prodkit.sprint-tech    - Create sprint technical docs"
echo "  /prodkit.create-issues  - Generate GitHub Issues"
echo "  /prodkit.dev            - Implement one issue with TDD"
echo "  /prodkit.review         - Generate sprint retrospective"
echo ""
echo "Next steps:"
echo "  1. cd $TARGET_DIR"
echo "  2. Open in Claude Code"
echo "  3. Run: /prodkit.prd"
echo ""
echo "📖 Documentation: See README.md"
echo ""
