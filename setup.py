#!/usr/bin/env python3
"""
Setup script for the Insurance Advisor Chatbot.
This script helps with the initial setup of the project.
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def print_step(message):
    """Print a step message with styling."""
    print("\n" + "=" * 80)
    print(f" 🔷 {message}")
    print("=" * 80)

def print_success(message):
    """Print a success message with styling."""
    print(f"\n ✅ {message}")

def print_error(message):
    """Print an error message with styling."""
    print(f"\n ❌ {message}")

def create_virtual_env():
    """Create a virtual environment."""
    print_step("Creating virtual environment")
    
    # Determine the correct command based on the OS
    if platform.system() == "Windows":
        venv_cmd = [sys.executable, "-m", "venv", "venv"]
    else:
        venv_cmd = [sys.executable, "-m", "venv", "venv"]
    
    try:
        subprocess.run(venv_cmd, check=True)
        print_success("Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to create virtual environment: {e}")
        return False

def install_requirements():
    """Install required packages."""
    print_step("Installing required packages")
    
    # Determine the path to pip based on the OS
    if platform.system() == "Windows":
        pip_path = os.path.join("venv", "Scripts", "pip")
    else:
        pip_path = os.path.join("venv", "bin", "pip")
    
    # Check if project_requirements.txt exists
    req_file = "project_requirements.txt"
    if not os.path.exists(req_file):
        print_error(f"Requirements file '{req_file}' not found")
        return False
    
    try:
        subprocess.run([pip_path, "install", "-U", "pip"], check=True)
        subprocess.run([pip_path, "install", "-r", req_file], check=True)
        print_success("Required packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install requirements: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist."""
    print_step("Setting up environment file")
    
    if os.path.exists(".env"):
        print("A .env file already exists. Do you want to overwrite it? (y/n): ", end="")
        if input().lower() != "y":
            print("Keeping existing .env file")
            return True
    
    # Create from example file if it exists
    if os.path.exists(".env.example"):
        shutil.copy(".env.example", ".env")
        print_success(".env file created from example template")
        print("\n⚠️  Please edit the .env file to add your API keys")
        return True
    else:
        # Create a basic .env file
        with open(".env", "w") as f:
            f.write("# Google API Key for Gemini\n")
            f.write("GOOGLE_API_KEY=your_google_api_key_here\n")
        print_success("Basic .env file created")
        print("\n⚠️  Please edit the .env file to add your API keys")
        return True

def create_sample_folders():
    """Create necessary folders if they don't exist."""
    print_step("Creating necessary folders")
    
    folders = ["assets", "sample_insurance_policies"]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
    
    print_success("Necessary folders created")
    return True

def print_next_steps():
    """Print next steps for the user."""
    print_step("Next Steps")
    
    # Determine activation command based on OS
    if platform.system() == "Windows":
        activate_cmd = ".\\venv\\Scripts\\activate"
    else:
        activate_cmd = "source venv/bin/activate"
    
    print("""
To start using the Insurance Advisor Chatbot:

1. Activate the virtual environment:
   {}

2. Edit the .env file to add your Google API key:
   - Get a key from https://aistudio.google.com/app/apikey
   - Add it to the .env file: GOOGLE_API_KEY=your_key_here

3. Run the application:
   streamlit run app.py

4. Open your browser at http://localhost:8501

For more information, check the documentation in the docs/ directory.
    """.format(activate_cmd))

def main():
    """Main execution function."""
    print("\n🤖 Welcome to the Insurance Advisor Chatbot Setup 🤖\n")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 10):
        print_error("Python 3.10 or higher is required")
        print(f"Current version: {sys.version}")
        return 1
    
    # Run setup steps
    steps = [
        ("Creating virtual environment", create_virtual_env),
        ("Installing requirements", install_requirements),
        ("Setting up environment file", create_env_file),
        ("Creating necessary folders", create_sample_folders)
    ]
    
    for step_name, step_func in steps:
        print(f"\nPerforming: {step_name}...")
        if not step_func():
            print_error(f"Setup failed at step: {step_name}")
            return 1
    
    print_next_steps()
    print("\n🎉 Setup completed successfully! 🎉\n")
    return 0

if __name__ == "__main__":
    sys.exit(main())