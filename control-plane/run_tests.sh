#!/bin/bash
# Test runner for NexusML control plane

set -e

echo "Running NexusML Control Plane Tests"
echo "======================================"

# Install dev dependencies
echo "Installing dev dependencies..."
pip install -e ".[dev]" -q

# Run tests
echo ""
echo "Running tests..."
pytest tests/ -v --tb=short

echo ""
echo "Tests complete"
