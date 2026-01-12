#!/bin/bash
# Quick test script for ModelVault
# This shows how to test ModelVault commands

echo "=========================================="
echo "ModelVault Test Script"
echo "=========================================="
echo ""

# Check if we're in a Git repo
if [ ! -d ".git" ]; then
    echo "⚠️  Warning: Not in a Git repository"
    echo "   ModelVault requires a Git repository to work"
    echo ""
fi

# Show help
echo "1. Showing ModelVault help:"
echo "----------------------------------------"
python3 -m modelvault.cli --help 2>/dev/null || echo "   (Run: python3 -m modelvault.cli --help)"
echo ""

# Show current Git status
echo "2. Current Git Status:"
echo "----------------------------------------"
git rev-parse --short HEAD 2>/dev/null && echo "   Current commit: $(git rev-parse --short HEAD)"
git status --short 2>/dev/null || echo "   (Not a Git repo)"
echo ""

# Check for config file
echo "3. Configuration Check:"
echo "----------------------------------------"
if [ -f ".modelvaultrc" ]; then
    echo "   ✓ .modelvaultrc found"
    cat .modelvaultrc
else
    echo "   ⚠️  .modelvaultrc not found"
    echo "   Create one from .modelvaultrc.example"
fi
echo ""

# Show metadata if it exists
echo "4. Metadata Check:"
echo "----------------------------------------"
if [ -f ".model_meta.json" ]; then
    echo "   ✓ .model_meta.json found"
    echo "   Run 'modelvault list' to see stored models"
else
    echo "   No .model_meta.json yet (will be created on first store)"
fi
echo ""

echo "=========================================="
echo "To test ModelVault:"
echo "=========================================="
echo ""
echo "1. Create a test model file:"
echo "   echo 'test model' > test_model.pkl"
echo ""
echo "2. Store it:"
echo "   python3 -m modelvault.cli store test_model.pkl my_model"
echo ""
echo "3. List stored models:"
echo "   python3 -m modelvault.cli list"
echo ""
echo "4. Load a model:"
echo "   python3 -m modelvault.cli load <commit_hash> restored.pkl"
echo ""
