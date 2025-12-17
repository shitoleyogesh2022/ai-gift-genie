#!/usr/bin/env python3
"""
🎄 AI Christmas Gift Generator Launcher
"""
import subprocess
import sys
import os
import webbrowser
import time
from pathlib import Path
from dotenv import load_dotenv

def install_requirements():
    """Install backend requirements"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", 
            "backend/requirements.txt"
        ])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def start_backend():
    """Start FastAPI backend"""
    print("🚀 Starting backend server...")
    backend_process = subprocess.Popen([
        sys.executable, "backend/main.py"
    ], cwd=Path.cwd())
    
    # Wait for server to start
    time.sleep(3)
    return backend_process

def open_frontend():
    """Open frontend in browser"""
    frontend_path = Path.cwd() / "frontend" / "index.html"
    print(f"🌐 Opening frontend: {frontend_path}")
    webbrowser.open(f"file://{frontend_path}")

def main():
    print("🎄 AI Christmas Gift Generator")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("backend/main.py").exists():
        print("❌ Please run this from the ai_christmas_gift_generator directory")
        return
    
    # Install dependencies
    if not install_requirements():
        return
    
    # Load environment variables
    load_dotenv()
    
    # Check API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  GOOGLE_API_KEY not found in environment")
        print("Make sure you have a .env file with your API key")
    else:
        print("✅ API key loaded successfully")
    
    try:
        # Start backend
        backend_process = start_backend()
        
        print("✅ Backend started on http://localhost:8003")
        print("📱 API Documentation: http://localhost:8003/docs")
        
        # Open frontend
        open_frontend()
        
        print("\n🎁 Christmas Gift Generator is ready!")
        print("Press Ctrl+C to stop the server")
        
        # Keep running
        backend_process.wait()
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
        if 'backend_process' in locals():
            backend_process.terminate()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()