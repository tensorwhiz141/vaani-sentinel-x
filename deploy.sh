#!/bin/bash

# Vaani Sentinel-X Deployment Script
# This script helps deploy the backend to various platforms

set -e

echo "🚀 Vaani Sentinel-X Deployment Script"
echo "======================================"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ Node.js version: $(node --version)"
echo "✅ npm version: $(npm --version)"

# Navigate to backend directory
cd web-ui/nextjs-voice-panel

echo "📦 Installing dependencies..."
npm install

echo "🔧 Checking environment configuration..."
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env 2>/dev/null || echo "Please create .env file manually"
fi

echo "🧪 Running health check..."
npm run start &
SERVER_PID=$!

# Wait for server to start
sleep 5

# Test health endpoint
if curl -f http://localhost:5000/health > /dev/null 2>&1; then
    echo "✅ Health check passed!"
else
    echo "❌ Health check failed!"
fi

# Stop the test server
kill $SERVER_PID 2>/dev/null || true

echo ""
echo "🎉 Deployment preparation complete!"
echo ""
echo "Next steps for Render deployment:"
echo "1. Push your code to GitHub"
echo "2. Connect your GitHub repo to Render"
echo "3. Create a new Web Service"
echo "4. Set build command: cd web-ui/nextjs-voice-panel && npm install"
echo "5. Set start command: cd web-ui/nextjs-voice-panel && npm start"
echo "6. Add environment variables in Render dashboard"
echo ""
echo "Environment variables to set in Render:"
echo "- JWT_SECRET (generate a secure random string)"
echo "- SECRET_KEY (generate a secure random string)"
echo "- NODE_ENV=production"
echo "- PORT=10000 (Render will set this automatically)"
echo ""
echo "📚 See README.md for detailed deployment instructions"
