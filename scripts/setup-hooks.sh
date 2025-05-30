#!/bin/bash
# GhostKit Git Hooks Setup Script
# Installs and configures all security and quality gates for development

set -e  # Exit on any error

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔒 GhostKit Security Gates Setup${NC}"
echo -e "${BLUE}================================${NC}"

# Get the repository root directory
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$REPO_ROOT"

# Create git hooks directory if it doesn't exist
if [ ! -d ".git/hooks" ]; then
    echo -e "${YELLOW}Creating .git/hooks directory...${NC}"
    mkdir -p .git/hooks
fi

# Check if scripts/git-hooks directory exists
if [ ! -d "scripts/git-hooks" ]; then
    echo -e "${RED}Error: scripts/git-hooks directory not found!${NC}"
    echo -e "${YELLOW}Creating scripts/git-hooks directory...${NC}"
    mkdir -p scripts/git-hooks
    
    # If pre-commit hook doesn't exist in source, create a minimal one
    if [ ! -f "scripts/git-hooks/pre-commit" ]; then
        echo -e "${YELLOW}Creating basic pre-commit hook...${NC}"
        cat > scripts/git-hooks/pre-commit << 'EOL'
#!/bin/bash
echo "🔍 GhostKit pre-commit hook running..."

# Check import formatting with isort
if command -v isort &> /dev/null; then
    echo "📋 Checking import sorting..."
    isort --check-only --profile black . || {
        echo "❌ Import sorting issues found! Run 'isort --profile black .' to fix."
        exit 1
    }
fi

# Check code formatting with black
if command -v black &> /dev/null; then
    echo "🎨 Checking code formatting..."
    black --check . || {
        echo "❌ Code needs formatting! Run 'black .' to fix."
        echo "💡 Tip: Use 'black --diff .' to see proposed changes."
        exit 1
    }
fi

# Run flake8 syntax check
if command -v flake8 &> /dev/null; then
    echo "🐍 Running syntax check..."
    flake8 . --count --select=E9,F63,F7,F82 --statistics || {
        echo "❌ Critical syntax errors detected! Fix before committing."
        exit 1
    }
fi

# Run bandit security scan
if command -v bandit &> /dev/null; then
    echo "🔒 Running security checks..."
    bandit -r . -x tests,docs --severity-level high || {
        echo "❌ HIGH SEVERITY security issues found! Fix before committing."
        exit 1
    }
fi

# Check for merge conflict markers
echo "🔀 Checking for merge conflict markers..."
if grep -r "<<<<<<< HEAD" --include="*.py" .; then
    echo "❌ Found merge conflict markers! Resolve conflicts before committing."
    exit 1
fi

echo "✅ All quality and security gates passed!"
exit 0
EOL
    fi
fi

# Copy all hooks from scripts/git-hooks to .git/hooks
echo -e "${BLUE}Copying git hooks...${NC}"
for hook in scripts/git-hooks/*; do
    if [ -f "$hook" ]; then
        hook_name=$(basename "$hook")
        echo -e "${YELLOW}Installing $hook_name hook...${NC}"
        cp "$hook" .git/hooks/
        
        # Make the hook executable
        chmod +x .git/hooks/"$hook_name"
        
        # For Windows with Git Bash, ensure proper line endings
        if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
            sed -i 's/\r$//' .git/hooks/"$hook_name"
        fi
    fi
done

# Check for development dependencies
echo -e "${BLUE}Checking development dependencies...${NC}"
if [ -f "requirements-dev.txt" ]; then
    if command -v pip &> /dev/null; then
        echo -e "${YELLOW}Do you want to install development dependencies? (y/n)${NC}"
        read -r install_deps
        if [[ "$install_deps" =~ ^[Yy] ]]; then
            echo -e "${BLUE}Installing development dependencies...${NC}"
            pip install -r requirements-dev.txt
        else
            echo -e "${YELLOW}Skipping dependency installation.${NC}"
            echo -e "${YELLOW}To install manually, run: pip install -r requirements-dev.txt${NC}"
        fi
    else
        echo -e "${RED}pip not found! Please install Python and pip to install dependencies.${NC}"
    fi
else
    echo -e "${RED}requirements-dev.txt not found! Development dependencies not installed.${NC}"
fi

echo -e "${GREEN}✅ Git hooks setup complete!${NC}"
echo -e "${BLUE}Installed hooks:${NC}"
ls -la .git/hooks/

echo -e "\n${YELLOW}To verify the setup, try making a change and committing:${NC}"
echo -e "git add ."
echo -e "git commit -m \"[TEST] Verify git hooks setup\"\n"

exit 0
