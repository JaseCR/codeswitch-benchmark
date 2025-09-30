"""
Debug Agent for Cohere API Issues
Automatically handles path resolution, environment loading, and API key validation
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import cohere

class CohereDebugAgent:
    def __init__(self):
        self.project_root = None
        self.env_file_path = None
        self.api_key = None
        self.client = None
        
    def find_project_root(self):
        """Find the project root directory by looking for .env file"""
        current_dir = Path.cwd()
        
        # Check current directory first
        if (current_dir / ".env").exists():
            self.project_root = current_dir
            self.env_file_path = current_dir / ".env"
            return self.project_root
            
        # Walk up the directory tree
        for parent in current_dir.parents:
            if (parent / ".env").exists():
                self.project_root = parent
                self.env_file_path = parent / ".env"
                return self.project_root
                
        # If still not found, try the expected location
        expected_root = Path("/Users/jase/codeswitch-benchmark")
        if expected_root.exists() and (expected_root / ".env").exists():
            self.project_root = expected_root
            self.env_file_path = expected_root / ".env"
            return self.project_root
            
        raise FileNotFoundError("Could not find .env file in project root")
    
    def setup_environment(self):
        """Set up environment variables and working directory"""
        print("🔍 Cohere Debug Agent Starting...")
        print("=" * 50)
        
        # Find project root
        try:
            self.find_project_root()
            print(f"✅ Found project root: {self.project_root}")
            print(f"✅ Found .env file: {self.env_file_path}")
        except FileNotFoundError as e:
            print(f"❌ {e}")
            return False
            
        # Change to project root if needed
        if Path.cwd() != self.project_root:
            print(f"📁 Changing directory from {Path.cwd()} to {self.project_root}")
            os.chdir(self.project_root)
            
        # Load environment variables
        load_dotenv()
        print("✅ Environment variables loaded")
        
        # Get API key
        self.api_key = os.getenv("COHERE_API_KEY")
        if not self.api_key:
            print("❌ COHERE_API_KEY not found in environment")
            return False
            
        print(f"✅ API key found (prefix: {self.api_key[:7]})")
        print(f"✅ API key length: {len(self.api_key)} characters")
        
        # Validate API key format
        if not self.api_key.startswith("SgUydfHhIvNdOIOlpUpF576awpLNCslYtg91SII1"):
            print("⚠️  Warning: API key format might be unexpected")
            
        # Initialize Cohere client
        try:
            self.client = cohere.Client(self.api_key)
            print("✅ Cohere client initialized")
        except Exception as e:
            print(f"❌ Failed to initialize Cohere client: {e}")
            return False
            
        return True
    
    def test_api_connection(self):
        """Test API connection with different models"""
        print("\n🧪 Testing Cohere API Connection...")
        print("=" * 50)
        
        models_to_try = [
            "command-r-plus-08-2024",  # Latest Chat API model
            "command-r-08-2024",       # Chat API model
            "command-a-03-2025"        # Alternative model
        ]
        
        for model in models_to_try:
            try:
                print(f"\n🔄 Testing {model}...")
                response = self.client.chat(
                    model=model,
                    message="Say hello in one word.",
                    max_tokens=10
                )
                result = response.text.strip()
                print(f"✅ {model} works: {result}")
                return True
            except Exception as e:
                error_msg = str(e)
                if "401" in error_msg or "403" in error_msg:
                    print(f"❌ {model}: Authentication failed (invalid API key)")
                elif "429" in error_msg:
                    print(f"❌ {model}: Rate limit exceeded")
                else:
                    print(f"❌ {model}: {error_msg[:100]}")
                    
        return False
    
    def diagnose_issues(self):
        """Run comprehensive diagnosis"""
        print("\n🔧 Running Comprehensive Diagnosis...")
        print("=" * 50)
        
        # Check environment setup
        if not self.setup_environment():
            return False
            
        # Test API connection
        if not self.test_api_connection():
            print("\n❌ API connection failed. Possible issues:")
            print("   1. Invalid or expired API key")
            print("   2. Billing/account issues")
            print("   3. Rate limits exceeded")
            print("   4. Model access restrictions")
            print("\n🔧 Recommended actions:")
            print("   1. Check your Cohere dashboard for valid API key")
            print("   2. Verify billing is set up correctly")
            print("   3. Check if you have access to the models")
            print("   4. Try regenerating your API key")
            return False
            
        print("\n✅ All tests passed! Cohere API is working correctly.")
        return True
    
    def fix_notebook_paths(self):
        """Fix path issues in notebooks"""
        print("\n🔧 Fixing Notebook Path Issues...")
        print("=" * 50)
        
        # Add src to path for imports
        src_path = self.project_root / "src"
        if src_path.exists():
            if str(src_path) not in sys.path:
                sys.path.insert(0, str(src_path))
                print(f"✅ Added {src_path} to Python path")
            else:
                print(f"✅ {src_path} already in Python path")
        else:
            print(f"❌ Source directory not found: {src_path}")
            return False
            
        return True
    
    def run_full_diagnosis(self):
        """Run complete diagnosis and fix issues"""
        print("🚀 Cohere Debug Agent - Full Diagnosis")
        print("=" * 60)
        
        # Run diagnosis
        if not self.diagnose_issues():
            return False
            
        # Fix paths
        if not self.fix_notebook_paths():
            return False
            
        print("\n🎉 All systems operational!")
        print("You can now use the Cohere API in your notebooks.")
        return True

# Convenience function for easy import
def debug_cohere():
    """Quick debug function for notebooks"""
    agent = CohereDebugAgent()
    return agent.run_full_diagnosis()

# Test function
if __name__ == "__main__":
    debug_cohere()
