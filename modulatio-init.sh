#!/bin/bash
set -e

echo "🚀 Initializing Modulatio project for The Invisible Boy Manuscript..."
echo ""

# Ensure we're in the project directory
if [ ! -f "README.md" ]; then
    echo "❌ Error: README.md not found. Please run this script from the project root."
    echo "   cd ~/the-invisible-boy-manuscript"
    exit 1
fi

# Check if Modulatio is installed
if ! command -v modulatio &> /dev/null; then
    echo "❌ Error: Modulatio is not installed or not in PATH."
    echo "   Try: source ~/modulatio/.venv/bin/activate"
    exit 1
fi

echo "✅ Modulatio found: $(modulatio --version)"
echo ""

# Create vault directory
echo "📁 Creating vault directory structure..."
mkdir -p vault/projects
mkdir -p vault/runs
mkdir -p vault/templates

# Initialize project
echo ""
echo "🔧 Initializing invisible-boy-project..."
modulatio init invisible-boy-project --vault ./vault

echo ""
echo "✅ Project initialized!"
echo ""
echo "📖 Next steps:"
echo ""
echo "1. Configure providers (add your API keys):"
echo "   modulatio config"
echo ""
echo "2. Create agents from MODULATIO_CONFIG.md prompts:"
echo "   - LEADER (Claude 3.5 Sonnet)"
echo "   - ARCHITECT (Claude 3.5 Sonnet)"
echo "   - BUILDER (Grok or GPT-4o)"
echo "   - VERIFICATION (Claude 3.5 Sonnet)"
echo ""
echo "3. Start a chapter development job:"
echo "   modulatio new-job"
echo ""
echo "4. Follow the conversational workflow"
echo ""
echo "🎯 Documentation:"
echo "   - Config: 00_MASTER_CONTROL/MODULATIO_CONFIG.md"
echo "   - Setup: SETUP.md"
echo "   - Modulatio: https://modulatio.ai"
echo ""
