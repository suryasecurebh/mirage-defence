"""
NeuroHoneypot - Setup Verification Script
Checks if everything is ready for the demo
"""
import sys
import subprocess
import os

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python version:", f"{version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print("❌ Python version too old:", f"{version.major}.{version.minor}.{version.micro}")
        print("   Required: Python 3.8 or higher")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    required = [
        'flask',
        'requests',
        'pandas',
        'numpy',
        'sklearn',
        'streamlit'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print("\n⚠️  Missing packages. Install with:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def check_files():
    """Check if all required files exist"""
    required_files = [
        'honeypot.py',
        'orchestrator.py',
        'decision.py',
        'sim_attacker.py',
        'dashboard.py',
        'ai/feature_cluster.py',
        'requirements.txt',
        'README.md',
        'run_all.bat'
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - NOT FOUND")
            missing.append(file)
    
    if missing:
        print("\n⚠️  Some files are missing!")
        return False
    
    return True

def check_directories():
    """Check if required directories exist"""
    dirs = ['data', 'ai']
    
    for directory in dirs:
        if os.path.exists(directory):
            print(f"✅ {directory}/")
        else:
            print(f"⚠️  {directory}/ - Creating...")
            os.makedirs(directory, exist_ok=True)
            print(f"✅ {directory}/ created")
    
    return True

def check_ports():
    """Check if required ports are available"""
    import socket
    
    ports = {
        5000: 'Honeypot',
        5001: 'Orchestrator',
        8501: 'Dashboard'
    }
    
    all_free = True
    for port, name in ports.items():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        
        if result == 0:
            print(f"⚠️  Port {port} ({name}) - ALREADY IN USE")
            all_free = False
        else:
            print(f"✅ Port {port} ({name}) - Available")
    
    if not all_free:
        print("\n⚠️  Some ports are in use. You may need to:")
        print("   1. Stop running services")
        print("   2. Or use: netstat -ano | findstr :<port>")
        print("   3. Then: taskkill /PID <PID> /F")
    
    return all_free

def main():
    """Main verification"""
    print("="*60)
    print("🍯 NeuroHoneypot - Setup Verification")
    print("="*60)
    
    print("\n1️⃣ Checking Python Version...")
    python_ok = check_python_version()
    
    print("\n2️⃣ Checking Dependencies...")
    deps_ok = check_dependencies()
    
    print("\n3️⃣ Checking Files...")
    files_ok = check_files()
    
    print("\n4️⃣ Checking Directories...")
    dirs_ok = check_directories()
    
    print("\n5️⃣ Checking Ports...")
    ports_ok = check_ports()
    
    print("\n" + "="*60)
    
    if python_ok and deps_ok and files_ok and dirs_ok:
        print("✅ System Ready!")
        print("="*60)
        print("\nNext steps:")
        print("  1. Run: .\\run_all.bat")
        print("  2. Wait 15 seconds for services to start")
        print("  3. Open: http://localhost:8501")
        print("  4. Run: python sim_attacker.py full")
        print("  5. Run: python decision.py")
        print("\nGood luck with your conference demo! 🚀")
        return True
    else:
        print("❌ Setup Incomplete")
        print("="*60)
        print("\nPlease fix the issues above before running the demo.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

