#!/usr/bin/env python3
"""
Enhanced Snake Game Setup Script
Helps users get started quickly with the game
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required Python packages"""
    print("🔧 Installing Python requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        return False

def check_arduino_files():
    """Check if Arduino files exist"""
    arduino_file = "snake_game_enhanced.ino"
    if os.path.exists(arduino_file):
        print(f"✅ Arduino file found: {arduino_file}")
        return True
    else:
        print(f"❌ Arduino file missing: {arduino_file}")
        return False

def check_python_files():
    """Check if Python files exist"""
    python_file = "snake_display.py"
    if os.path.exists(python_file):
        print(f"✅ Python display file found: {python_file}")
        return True
    else:
        print(f"❌ Python display file missing: {python_file}")
        return False

def detect_com_ports():
    """Try to detect available COM ports"""
    print("\n🔍 Detecting COM ports...")
    try:
        import serial.tools.list_ports
        ports = serial.tools.list_ports.comports()
        if ports:
            print("Available ports:")
            for port in ports:
                print(f"  📡 {port.device} - {port.description}")
        else:
            print("No COM ports detected")
    except ImportError:
        print("pyserial not installed yet - run setup first")

def main():
    print("🐍 Enhanced Snake Game Setup")
    print("=" * 40)
    
    # Check files
    arduino_ok = check_arduino_files()
    python_ok = check_python_files()
    
    if not (arduino_ok and python_ok):
        print("\n❌ Missing required files!")
        return
    
    # Install requirements
    if not install_requirements():
        return
    
    # Detect ports
    detect_com_ports()
    
    print("\n🎯 Next Steps:")
    print("1. Connect your Arduino with the circuit")
    print("2. Upload snake_game_enhanced.ino to Arduino")
    print("3. Note your Arduino COM port")
    print("4. Run: python snake_display.py COM3")
    print("   (Replace COM3 with your actual port)")
    
    print("\n🎮 Ready to play Snake!")

if __name__ == "__main__":
    main() 