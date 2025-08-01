#!/usr/bin/env python3
"""
Quick test script for the FastAPI backend
"""

import sys
import os

# Add the agents_api directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents_api'))

try:
    print("🧪 Testing backend imports...")
    
    # Test main app import
    from main import app
    print("✅ Main app imported successfully")
    
    # Test model imports
    from models.request_models import TranslationRequest
    from models.response_models import TranslationResponse
    print("✅ Models imported successfully")
    
    # Test router imports
    from routers.translation_router import router as translation_router
    print("✅ Routers imported successfully")
    
    print("\n🎉 All backend components imported successfully!")
    print("✅ Backend is ready to run")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure you're in the correct directory and dependencies are installed")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)

if __name__ == "__main__":
    print("\n🚀 Starting FastAPI server test...")
    print("📡 Backend should be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    
    # Start the server
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
