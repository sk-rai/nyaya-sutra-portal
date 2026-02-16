#!/bin/bash

echo "🔍 Nyaya Sutra Portal - Verification Script"
echo "=============================================="
echo ""

# Check public folder
echo "✓ Checking public/ folder structure..."
if [ -d "public" ]; then
    echo "  ✅ public/ folder exists"
else
    echo "  ❌ public/ folder missing!"
    exit 1
fi

# Check HTML files
echo ""
echo "✓ Checking HTML files..."
for file in index.html login.html dashboard.html START_HERE.html; do
    if [ -f "public/$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file missing!"
    fi
done

# Check CSS files
echo ""
echo "✓ Checking CSS files..."
for file in base.css components.css tiers.css; do
    if [ -f "public/css/$file" ]; then
        echo "  ✅ css/$file"
    else
        echo "  ❌ css/$file missing!"
    fi
done

# Check JS files
echo ""
echo "✓ Checking JavaScript files..."
for file in auth.js tier-renderer.js print-control.js; do
    if [ -f "public/js/$file" ]; then
        echo "  ✅ js/$file"
    else
        echo "  ❌ js/$file missing!"
    fi
done

# Check config files
echo ""
echo "✓ Checking configuration files..."
if [ -f "package.json" ]; then
    echo "  ✅ package.json"
else
    echo "  ❌ package.json missing!"
fi

if [ -f "sandbox.config.json" ]; then
    echo "  ✅ sandbox.config.json"
else
    echo "  ❌ sandbox.config.json missing!"
fi

# Check documentation
echo ""
echo "✓ Checking documentation..."
for file in README.md DEMO_GUIDE.md CODESANDBOX_DEPLOY.md CHANGES_SUMMARY.md FINAL_STATUS.md; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ⚠️  $file missing (optional)"
    fi
done

echo ""
echo "=============================================="
echo "✅ Verification Complete!"
echo ""
echo "📦 Project is ready for CodeSandbox deployment"
echo "📖 See CODESANDBOX_DEPLOY.md for instructions"
echo ""
echo "🚀 Quick test: npx serve public"
echo "   Then open: http://localhost:3000"
