"""
Test Setup Script
Verifies that your environment is correctly configured
"""

from dotenv import load_dotenv
import os
import sys

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_section(text):
    print(f"\n{text}")
    print("-"*60)

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✓ Python version is compatible")
        return True
    else:
        print("✗ Python 3.8 or higher is required")
        return False

def check_packages():
    """Check if required packages are installed"""
    packages = {
        'gradio': 'gradio',
        'python-dotenv': 'dotenv',
        'openai': 'openai',
        'anthropic': 'anthropic'
    }
    
    results = {}
    
    for package_name, import_name in packages.items():
        try:
            __import__(import_name)
            print(f"✓ {package_name:20} installed")
            results[package_name] = True
        except ImportError:
            print(f"✗ {package_name:20} NOT installed")
            results[package_name] = False
    
    return results

def check_env_file():
    """Check .env file"""
    if not os.path.exists('.env'):
        print("✗ .env file NOT found")
        print("\nPlease create a .env file with your API keys:")
        print("\nExample .env file content:")
        print("-"*60)
        print("OPENAI_API_KEY= "YOUR_TOKEN_HERE"  # Replace with your token
        print("ANTHROPIC_API_KEY= "YOUR_TOKEN_HERE"  # Replace with your token
        print("-"*60)
        return False
    
    print("✓ .env file found")
    return True

def check_api_keys():
    """Check if API keys are loaded"""
    load_dotenv()
    
    openai_key = os.getenv("OPENAI_API_KEY")
    claude_key = os.getenv("ANTHROPIC_API_KEY")
    
    has_keys = False
    
    if openai_key:
        # Mask the key for security
        masked = openai_key[:10] + "..." + openai_key[-4:]
        print(f"✓ OpenAI API Key loaded: {masked}")
        has_keys = True
    else:
        print("✗ OpenAI API Key NOT found in .env")
    
    if claude_key:
        masked = claude_key[:10] + "..." + claude_key[-4:]
        print(f"✓ Claude API Key loaded: {masked}")
        has_keys = True
    else:
        print("✗ Claude API Key NOT found in .env")
    
    if not has_keys:
        print("\n⚠️  No API keys found! You need at least one API key to use the applications.")
    
    return has_keys

def test_openai_connection():
    """Test OpenAI API connection"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Try a minimal API call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=5
        )
        
        print("✓ OpenAI API connection successful")
        return True
    
    except Exception as e:
        print(f"✗ OpenAI API connection failed: {str(e)[:100]}")
        return False

def test_claude_connection():
    """Test Claude API connection"""
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        # Try a minimal API call
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=5,
            messages=[{"role": "user", "content": "Hi"}]
        )
        
        print("✓ Claude API connection successful")
        return True
    
    except Exception as e:
        print(f"✗ Claude API connection failed: {str(e)[:100]}")
        return False

def main():
    print_header("🔍 Career Advisor Setup Test")
    
    # Check Python version
    print_section("1. Checking Python Version")
    python_ok = check_python_version()
    
    # Check packages
    print_section("2. Checking Installed Packages")
    packages = check_packages()
    
    # Check .env file
    print_section("3. Checking .env File")
    env_exists = check_env_file()
    
    # Check API keys
    print_section("4. Checking API Keys")
    if env_exists:
        has_keys = check_api_keys()
    else:
        has_keys = False
    
    # Test API connections
    if has_keys:
        print_section("5. Testing API Connections")
        
        if packages.get('openai') and os.getenv("OPENAI_API_KEY"):
            test_openai_connection()
        
        if packages.get('anthropic') and os.getenv("ANTHROPIC_API_KEY"):
            test_claude_connection()
    
    # Summary
    print_header("📋 Summary")
    
    all_good = True
    
    if not python_ok:
        print("❌ Python version issue")
        all_good = False
    
    if not all(packages.values()):
        print("❌ Some packages are missing")
        print("\nTo install missing packages, run:")
        for pkg, installed in packages.items():
            if not installed:
                print(f"  pip install {pkg}")
        all_good = False
    
    if not env_exists or not has_keys:
        print("❌ API keys not configured")
        all_good = False
    
    if all_good:
        print("\n✅ Everything is set up correctly!")
        print("\nYou can now run your applications:")
        print("  python career_advisor.py")
        print("  python cover_letter.py")
        print("  python resume_polisher.py")
        print("\nOr run all at once:")
        print("  python run_all_apps.py")
    else:
        print("\n⚠️  Please fix the issues above before running the applications.")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")