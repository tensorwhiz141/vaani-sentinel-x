#!/usr/bin/env python3
"""
Vaani Sentinel-X Dynamic System Startup Script
Starts both the FastAPI backend and React frontend
"""

import subprocess
import sys
import os
import time
import threading
from pathlib import Path

def run_command(command, cwd=None, name="Process"):
    """Run a command in a subprocess."""
    try:
        print(f"🚀 Starting {name}...")
        process = subprocess.Popen(
            command,
            shell=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Print output in real-time
        for line in iter(process.stdout.readline, ''):
            if line.strip():
                print(f"[{name}] {line.strip()}")
        
        process.wait()
        
    except KeyboardInterrupt:
        print(f"\n⏹️  Stopping {name}...")
        process.terminate()
    except Exception as e:
        print(f"❌ Error running {name}: {e}")

def check_dependencies():
    """Check if required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    # Check Python dependencies
    try:
        import fastapi
        import uvicorn
        import pydantic
        print("✅ Python dependencies found")
    except ImportError as e:
        print(f"❌ Missing Python dependency: {e}")
        print("💡 Install with: pip install -r agents_api/requirements.txt")
        return False
    
    # Check if Node.js is available
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js found: {result.stdout.strip()}")
        else:
            print("❌ Node.js not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found. Please install Node.js")
        return False
    
    return True

def install_frontend_dependencies():
    """Install frontend dependencies if needed."""
    frontend_dir = Path("frontend")
    node_modules = frontend_dir / "node_modules"
    
    if not node_modules.exists():
        print("📦 Installing frontend dependencies...")
        try:
            subprocess.run(['npm', 'install'], cwd=frontend_dir, check=True)
            print("✅ Frontend dependencies installed")
        except subprocess.CalledProcessError:
            print("❌ Failed to install frontend dependencies")
            return False
    else:
        print("✅ Frontend dependencies already installed")
    
    return True

def start_backend():
    """Start the FastAPI backend server."""
    backend_command = "python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
    run_command(backend_command, cwd="agents_api", name="FastAPI Backend")

def start_frontend():
    """Start the React frontend development server."""
    frontend_command = "npm start"
    run_command(frontend_command, cwd="frontend", name="React Frontend")

def main():
    """Main function to start the dynamic system."""
    print("🌟 Vaani Sentinel-X Dynamic System Startup")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed. Please install missing dependencies.")
        sys.exit(1)
    
    # Install frontend dependencies
    if not install_frontend_dependencies():
        print("❌ Frontend setup failed.")
        sys.exit(1)
    
    print("\n🚀 Starting Vaani Sentinel-X Dynamic System...")
    print("📡 Backend API will be available at: http://localhost:8000")
    print("🌐 Frontend will be available at: http://localhost:3000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("\n⚡ Press Ctrl+C to stop both servers\n")
    
    # Start backend and frontend in separate threads
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    frontend_thread = threading.Thread(target=start_frontend, daemon=True)
    
    try:
        # Start backend
        backend_thread.start()
        time.sleep(3)  # Give backend time to start
        
        # Start frontend
        frontend_thread.start()
        
        # Keep main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n⏹️  Shutting down Vaani Sentinel-X Dynamic System...")
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()
