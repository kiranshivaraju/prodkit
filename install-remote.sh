#!/bin/bash

# ProdKit Remote Installer
# Installs ProdKit directly from GitHub

set -e

PRODKIT_REPO="https://github.com/kiranshivaraju/prodkit"
PRODKIT_BRANCH="main"
TEMP_DIR=$(mktemp -d)

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ProdKit Remote Installer"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Get target directory (default to current directory)
TARGET_DIR="${1:-.}"
TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"

echo "Installing ProdKit to: $TARGET_DIR"
echo "Fetching from: $PRODKIT_REPO"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Error: git is not installed"
    echo "Please install git first: https://git-scm.com/"
    exit 1
fi

# Clone ProdKit to temp directory
echo "→ Downloading ProdKit..."
git clone --depth 1 --branch "$PRODKIT_BRANCH" "$PRODKIT_REPO.git" "$TEMP_DIR/prodkit" 2>&1 | grep -v "Cloning into" || true

if [ ! -d "$TEMP_DIR/prodkit" ]; then
    echo "❌ Error: Failed to download ProdKit"
    echo "Please check:"
    echo "  1. Your internet connection"
    echo "  2. The repository URL: $PRODKIT_REPO"
    exit 1
fi

# Run the local install script from the downloaded repo
echo "→ Running installer..."
cd "$TEMP_DIR/prodkit"
chmod +x install.sh
./install.sh "$TARGET_DIR"

# Cleanup
echo "→ Cleaning up..."
rm -rf "$TEMP_DIR"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅ ProdKit installed successfully!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Get started:"
echo "  cd $TARGET_DIR"
echo "  # Open in Claude Code"
echo "  # Run: /prodkit.prd"
echo ""
