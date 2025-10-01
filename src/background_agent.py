"""
Background Agent for Automatic Problem Solving
Handles Python environment issues, missing packages, and import errors automatically
"""

import os
import sys
import subprocess
import importlib
import warnings
from pathlib import Path
from typing import List, Dict, Any, Optional

class BackgroundAgent:
    def __init__(self):
        self.project_root = self._find_project_root()
        self.installed_packages = set()
        self.required_packages = {
            'pandas': 'pandas',
            'numpy': 'numpy', 
            'matplotlib': 'matplotlib',
            'seaborn': 'seaborn',
            'plotly': 'plotly',
            'wordcloud': 'wordcloud',
            'tqdm': 'tqdm',
            'sklearn': 'scikit-learn',
            'dotenv': 'python-dotenv',
            'mistralai': 'mistralai',
            'cohere': 'cohere',
            'openai': 'openai',
            'google.generativeai': 'google-generativeai'
        }
        
    def _find_project_root(self):
        """Find the project root directory"""
        current_dir = Path.cwd()
        
        # Check current directory first
        if (current_dir / ".env").exists() or (current_dir / "src").exists():
            return current_dir
            
        # Walk up the directory tree
        for parent in current_dir.parents:
            if (parent / ".env").exists() or (parent / "src").exists():
                return parent
                
        return current_dir  # Fallback
    
    def run_command(self, command: str, description: str = "") -> bool:
        """Run a shell command and return success status"""
        try:
            if description:
                print(f"🔧 {description}")
            
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                if description:
                    print(f" {description} - Success")
                return True
            else:
                if description:
                    print(f" {description} - Failed: {result.stderr}")
                return False
                
        except Exception as e:
            if description:
                print(f" {description} - Error: {e}")
            return False
    
    def install_package(self, package_name: str) -> bool:
        """Install a Python package using pip"""
        if package_name in self.installed_packages:
            return True
            
        print(f"📦 Installing {package_name}...")
        
        # Try different installation methods
        commands = [
            f"python3 -m pip install {package_name}",
            f"pip3 install {package_name}",
            f"pip install {package_name}"
        ]
        
        for cmd in commands:
            if self.run_command(cmd, f"Installing {package_name}"):
                self.installed_packages.add(package_name)
                return True
        
        print(f" Failed to install {package_name}")
        return False
    
    def check_and_install_packages(self) -> bool:
        """Check for missing packages and install them automatically"""
        print(" Checking required packages...")
        
        missing_packages = []
        
        for import_name, package_name in self.required_packages.items():
            try:
                # Handle special cases for import names
                if import_name == 'sklearn':
                    import sklearn
                elif import_name == 'google.generativeai':
                    import google.generativeai
                else:
                    importlib.import_module(import_name)
                print(f" {import_name} - Available")
            except ImportError:
                print(f" {import_name} - Missing")
                missing_packages.append(package_name)
        
        if missing_packages:
            print(f"\n📦 Installing {len(missing_packages)} missing packages...")
            for package in missing_packages:
                if not self.install_package(package):
                    return False
        else:
            print(" All required packages are available!")
        
        return True
    
    def setup_environment(self) -> bool:
        """Set up the Python environment"""
        print(" Background Agent - Setting up environment...")
        print("=" * 60)
        
        # Change to project root
        original_dir = os.getcwd()
        if os.getcwd() != str(self.project_root):
            print(f"📁 Changing to project root: {self.project_root}")
            os.chdir(self.project_root)
        
        # Add src to Python path
        src_path = self.project_root / "src"
        if src_path.exists() and str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))
            print(f" Added {src_path} to Python path")
        
        # Check and install packages
        if not self.check_and_install_packages():
            print(" Package installation failed")
            return False
        
        # Load environment variables
        try:
            from dotenv import load_dotenv
            load_dotenv()
            print(" Environment variables loaded")
        except ImportError:
            print("  python-dotenv not available, skipping .env loading")
        
        print("\n🎉 Environment setup complete!")
        return True
    
    def fix_common_issues(self) -> Dict[str, bool]:
        """Fix common Python environment issues"""
        print("\n🔧 Fixing common issues...")
        
        issues_fixed = {}
        
        # Issue 1: pip not defined
        try:
            import pip
            issues_fixed['pip_import'] = True
        except ImportError:
            print("🔧 Fixing 'pip not defined' issue...")
            # This usually means we need to use subprocess instead
            issues_fixed['pip_import'] = False
            print(" Will use subprocess for pip commands")
        
        # Issue 2: Module not found errors
        if self.check_and_install_packages():
            issues_fixed['missing_modules'] = True
        else:
            issues_fixed['missing_modules'] = False
        
        # Issue 3: Path issues
        src_path = self.project_root / "src"
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))
            issues_fixed['path_issues'] = True
        else:
            issues_fixed['path_issues'] = False
        
        return issues_fixed
    
    def run_full_setup(self) -> bool:
        """Run complete background setup"""
        print("🤖 Background Agent Starting...")
        print("This agent will automatically solve common Python environment issues.")
        print("=" * 70)
        
        # Setup environment
        if not self.setup_environment():
            print(" Environment setup failed")
            return False
        
        # Fix common issues
        issues = self.fix_common_issues()
        
        print("\n Issues Fixed:")
        for issue, fixed in issues.items():
            status = " Fixed" if fixed else "  Not Fixed"
            print(f"  {issue}: {status}")
        
        print("\n🎉 Background Agent setup complete!")
        print("Your Python environment should now be ready for the notebooks.")
        
        return True

# Convenience functions for easy import
def run_background_agent():
    """Run the background agent to fix common issues"""
    agent = BackgroundAgent()
    return agent.run_full_setup()

def fix_imports():
    """Quick fix for import issues"""
    agent = BackgroundAgent()
    return agent.check_and_install_packages()

def setup_environment():
    """Quick environment setup"""
    agent = BackgroundAgent()
    return agent.setup_environment()

# Auto-run when imported
if __name__ == "__main__":
    run_background_agent()
else:
    # When imported, run a quick setup
    try:
        agent = BackgroundAgent()
        agent.setup_environment()
    except Exception as e:
        print(f"  Background agent setup failed: {e}")
        print("You can manually run: from background_agent import run_background_agent; run_background_agent()")
