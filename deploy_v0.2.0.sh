#!/bin/bash

echo "=========================================="
echo "🚀 DEPLOYMENT SCRIPT v0.2.0"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Verify tests
echo -e "${YELLOW}Step 1: Running final tests...${NC}"
python3 test_final_profitability.py
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Tests failed! Aborting deployment.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ All tests passed!${NC}"
echo ""

# Step 2: Check Git status
echo -e "${YELLOW}Step 2: Checking Git status...${NC}"
git status
echo ""

# Step 3: Push to Git
echo -e "${YELLOW}Step 3: Pushing to Git...${NC}"
read -p "Push to Git? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Check if remote exists
    if git remote | grep -q origin; then
        echo "Pushing to origin..."
        git push origin main
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Successfully pushed to Git!${NC}"
        else
            echo -e "${RED}❌ Git push failed!${NC}"
            echo "You may need to set up remote or check credentials"
        fi
    else
        echo -e "${YELLOW}⚠️  No remote 'origin' found${NC}"
        echo "To add remote, run:"
        echo "  git remote add origin <your-repo-url>"
    fi
else
    echo "Skipping Git push"
fi
echo ""

# Step 4: Create Git tag
echo -e "${YELLOW}Step 4: Creating Git tag...${NC}"
read -p "Create tag v0.2.0? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git tag -a v0.2.0 -m "Release v0.2.0: Anti-Loss Protection System"
    if git remote | grep -q origin; then
        git push origin v0.2.0
        echo -e "${GREEN}✅ Tag created and pushed!${NC}"
    else
        echo -e "${GREEN}✅ Tag created locally!${NC}"
    fi
else
    echo "Skipping tag creation"
fi
echo ""

# Step 5: Upload to PyPI
echo -e "${YELLOW}Step 5: Uploading to PyPI...${NC}"
echo "Package files:"
ls -lh dist/
echo ""

read -p "Upload to PyPI? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Check if twine is installed
    if ! command -v twine &> /dev/null; then
        echo "Installing twine..."
        pip3 install twine
    fi
    
    echo ""
    echo "Uploading to PyPI..."
    echo "You will need your PyPI credentials:"
    echo "  Username: __token__"
    echo "  Password: <your-pypi-token>"
    echo ""
    
    python3 -m twine upload dist/*
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Successfully uploaded to PyPI!${NC}"
        echo ""
        echo "Package is now available at:"
        echo "  https://pypi.org/project/ipaytools/0.2.0/"
        echo ""
        echo "Users can install with:"
        echo "  pip install ipaytools==0.2.0"
        echo "  pip install --upgrade ipaytools"
    else
        echo -e "${RED}❌ PyPI upload failed!${NC}"
        echo "Common issues:"
        echo "  - Invalid credentials"
        echo "  - Version already exists"
        echo "  - Network issues"
    fi
else
    echo "Skipping PyPI upload"
fi
echo ""

# Summary
echo "=========================================="
echo "📊 DEPLOYMENT SUMMARY"
echo "=========================================="
echo ""
echo "Version: 0.2.0"
echo "Package: ipaytools"
echo ""
echo "Features:"
echo "  ✓ Anti-Loss Protection System"
echo "  ✓ Auto fee adjustment"
echo "  ✓ Transaction rejection for unprofitable fees"
echo "  ✓ Real-time profitability validation"
echo "  ✓ 20% minimum profit margin"
echo "  ✓ 30% safety buffer"
echo ""
echo "Files built:"
ls -1 dist/
echo ""
echo -e "${GREEN}🎉 Deployment process completed!${NC}"
echo "=========================================="
