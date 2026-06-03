#!/bin/bash
set -e

echo "Setting up Modulatio development environment for The Invisible Boy Manuscript..."

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip and install dependencies
echo "Installing dependencies..."
pip install --upgrade pip setuptools wheel
pip install -e ".[dev]"

echo "Running Modulatio setup..."
modulatIO setup

echo "✅ Setup complete! Activate the environment with: source .venv/bin/activate"
