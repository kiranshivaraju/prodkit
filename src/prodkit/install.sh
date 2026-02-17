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
ln -sf ../../.prodkit/commands/prodkit.code-review.md prodkit.code-review.md
ln -sf ../../.prodkit/commands/prodkit.review.md prodkit.review.md

cd "$TARGET_DIR"

# Install Speckit for /prodkit.dev workflow
echo "→ Installing Speckit (required for /prodkit.dev)..."

# Check if Speckit is already installed
if [ -d "$TARGET_DIR/.speckit" ]; then
    echo "  ℹ️  Speckit already installed, skipping..."
else
    # Clone Speckit to a temp directory
    TEMP_SPECKIT=$(mktemp -d)
    if git clone --depth 1 https://github.com/github/spec-kit.git "$TEMP_SPECKIT" 2>/dev/null; then
        # Copy Speckit's command templates
        if [ -d "$TEMP_SPECKIT/templates/commands" ]; then
            echo "  → Setting up Speckit commands..."
            # Create .speckit directory
            mkdir -p "$TARGET_DIR/.speckit/commands"

            # Copy Speckit command files with speckit. prefix
            cd "$TEMP_SPECKIT/templates/commands"
            for cmd in *.md; do
                if [ -f "$cmd" ]; then
                    # Copy with speckit. prefix
                    cp "$cmd" "$TARGET_DIR/.speckit/commands/speckit.$cmd"
                fi
            done
            cd - > /dev/null

            # Copy Speckit constitution template
            if [ -f "$TEMP_SPECKIT/templates/constitution-template.md" ]; then
                mkdir -p "$TARGET_DIR/.speckit"
                cp "$TEMP_SPECKIT/templates/constitution-template.md" "$TARGET_DIR/.speckit/constitution-template.md"
            fi

            # Create symlinks in .claude/commands for Speckit commands
            cd "$TARGET_DIR/.claude/commands"
            for cmd in "$TARGET_DIR/.speckit/commands/"*.md; do
                if [ -f "$cmd" ]; then
                    cmdname=$(basename "$cmd")
                    ln -sf "../../.speckit/commands/$cmdname" "$cmdname"
                fi
            done
            cd "$TARGET_DIR"

            echo "  ✓ Speckit installed successfully"
        else
            echo "  ⚠️  Speckit structure not as expected, you may need to install manually"
        fi

        # Cleanup
        rm -rf "$TEMP_SPECKIT"
    else
        echo "  ⚠️  Could not download Speckit automatically"
        echo "  You can install it manually from: https://github.com/github/spec-kit"
    fi
fi

# Create placeholder directories
echo "→ Creating placeholder directories..."
mkdir -p "$TARGET_DIR/product"
mkdir -p "$TARGET_DIR/sprints"
mkdir -p "$TARGET_DIR/.prodkit/.state"

# Create .gitignore if it doesn't exist
if [ ! -f "$TARGET_DIR/.gitignore" ]; then
    echo "→ Creating .gitignore..."
    cat > "$TARGET_DIR/.gitignore" << 'EOF'
# ProdKit
.prodkit/cache/
.prodkit/.github-token
.prodkit/.state/

# OS
.DS_Store
Thumbs.db

# IDEs
.vscode/
.idea/
*.swp
*.swo
EOF
else
    # Ensure ProdKit entries are in existing .gitignore
    if ! grep -q ".prodkit/.github-token" "$TARGET_DIR/.gitignore"; then
        echo "→ Adding .prodkit/.github-token to .gitignore..."
        echo "" >> "$TARGET_DIR/.gitignore"
        echo "# GitHub token (sensitive)" >> "$TARGET_DIR/.gitignore"
        echo ".prodkit/.github-token" >> "$TARGET_DIR/.gitignore"
    fi
    if ! grep -q ".prodkit/.state/" "$TARGET_DIR/.gitignore"; then
        echo "→ Adding .prodkit/.state/ to .gitignore..."
        if ! grep -q "# ProdKit" "$TARGET_DIR/.gitignore"; then
            echo "" >> "$TARGET_DIR/.gitignore"
            echo "# ProdKit state files" >> "$TARGET_DIR/.gitignore"
        fi
        echo ".prodkit/.state/" >> "$TARGET_DIR/.gitignore"
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅ ProdKit installed successfully!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "ProdKit commands:"
echo "  /prodkit.prd            - Create Product Requirements Document"
echo "  /prodkit.product-arch   - Define system architecture"
echo "  /prodkit.init-repo      - Initialize GitHub repository"
echo "  /prodkit.plan-sprint    - Plan sprint features"
echo "  /prodkit.sprint-tech    - Create sprint technical docs"
echo "  /prodkit.create-issues  - Generate GitHub Issues"
echo "  /prodkit.dev            - Implement one issue with TDD (uses Speckit)"
echo "  /prodkit.code-review    - AI code review for branches/PRs"
echo "  /prodkit.review         - Generate sprint retrospective"
echo ""
echo "Speckit commands (used by /prodkit.dev):"
echo "  /speckit.specify        - Define requirements"
echo "  /speckit.plan           - Create technical plan"
echo "  /speckit.tasks          - Break into tasks"
echo "  /speckit.implement      - Implement with TDD"
echo ""
echo "Next steps:"
echo "  1. cd $TARGET_DIR"
echo "  2. Open in Claude Code"
echo "  3. Run: /prodkit.prd"
echo ""
echo "📖 Documentation: See README.md"
echo ""
