# Modulatio Development Setup

This project uses **Modulatio**, a multi-model agent framework for running long, high-stakes projects with real quality control.

## Requirements

- **Python 3.12+** (required by Modulatio)
- `pip` or `uv` package manager

## Quick Install

### Option 1: Using the setup script (recommended)

```bash
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual installation

```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Install dependencies
pip install -e ".[dev]"

# Run Modulatio setup wizard
modulatIO setup
```

### Option 3: Using uv (faster)

```bash
uv venv
uv pip install -e ".[dev]"
modulatIO setup
```

## Verify Installation

```bash
modulatIO --version
modulatIO --help
```

## Activate Environment

After installation, always activate the environment before working:

```bash
source .venv/bin/activate
```

## Documentation

- Modulatio docs: https://modulatio.ai
- Getting started: https://modulatio.ai/getting-started/install/
- CLI reference: https://modulatio.ai/reference/cli/

## Troubleshooting

If you encounter issues during installation, see:
https://modulatio.ai/getting-started/install/

Common issue: Older Python versions may fail during wheel compilation. Ensure you're using **Python 3.12 or later**.
