#!/bin/bash
set -e

echo "🧪 Dashboard Validation"
echo "======================"

# Check if dist directory exists
if [ ! -d "dist" ]; then
    echo "❌ dist/ directory not found"
    exit 1
fi

# Check if index.html exists
if [ ! -f "dist/index.html" ]; then
    echo "❌ dist/index.html not found"
    exit 1
fi
echo "✅ index.html exists"

# Check if static files are copied
if [ ! -d "dist/static" ]; then
    echo "❌ dist/static/ directory not found"
    exit 1
fi
echo "✅ static/ directory exists"

# Check if CSS exists
if [ ! -f "dist/static/style.css" ]; then
    echo "❌ dist/static/style.css not found"
    exit 1
fi
echo "✅ style.css exists"

# Validate HTML contains expected content
if ! grep -q "PR Dashboard" dist/index.html; then
    echo "❌ index.html missing title"
    exit 1
fi
echo "✅ HTML contains title"

if ! grep -qi "chart\.js" dist/index.html; then
    echo "❌ index.html missing Chart.js"
    exit 1
fi
echo "✅ Chart.js included"

if ! grep -q "metricsData" dist/index.html; then
    echo "❌ index.html missing metrics data"
    exit 1
fi
echo "✅ Metrics data embedded"

echo ""
echo "✅ All validation checks passed!"
