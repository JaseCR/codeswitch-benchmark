"""
Code Quality Assurance Agent
Checks for bugs, human-like writing, and proper commit practices
"""

import os
import sys
import re
import ast
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class CodeQualityAgent:
    """Agent that ensures code quality and human-like writing"""
    
    def __init__(self):
        self.name = "CodeQualityAgent"
        self.issues_found = []
        self.suggestions = []
        
    def check_python_syntax(self, file_path: Path):
        """Check Python files for syntax errors"""
        print(f"🔍 Checking Python syntax: {file_path.name}")
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Try to parse the AST
            ast.parse(content)
            print(f"  ✅ Syntax OK")
            return True
            
        except SyntaxError as e:
            print(f"  ❌ Syntax Error: {e}")
            self.issues_found.append(f"Syntax error in {file_path.name}: {e}")
            return False
        except Exception as e:
            print(f"  ❌ Parse Error: {e}")
            self.issues_found.append(f"Parse error in {file_path.name}: {e}")
            return False
            
    def check_human_like_comments(self, file_path: Path):
        """Check for human-like comments and docstrings"""
        print(f"💬 Checking comments: {file_path.name}")
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Look for TODO/FIXME comments
            todo_pattern = r'#\s*(TODO|FIXME|HACK|XXX)'
            todos = re.findall(todo_pattern, content, re.IGNORECASE)
            
            if todos:
                print(f"  ⚠️ Found {len(todos)} TODO/FIXME comments")
                for todo in todos:
                    self.issues_found.append(f"TODO/FIXME in {file_path.name}: {todo}")
            else:
                print(f"  ✅ No TODO/FIXME comments")
                
            # Check for docstrings
            docstring_pattern = r'""".*?"""'
            docstrings = re.findall(docstring_pattern, content, re.DOTALL)
            
            if docstrings:
                print(f"  ✅ Found {len(docstrings)} docstrings")
            else:
                print(f"  ⚠️ No docstrings found")
                self.suggestions.append(f"Consider adding docstrings to {file_path.name}")
                
        except Exception as e:
            print(f"  ❌ Error checking comments: {e}")
            
    def check_variable_naming(self, file_path: Path):
        """Check for human-readable variable names"""
        print(f"📝 Checking variable names: {file_path.name}")
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Look for single-letter variables (except common ones)
            single_letter_pattern = r'\b[a-hj-z]\b(?=\s*=)'
            single_letters = re.findall(single_letter_pattern, content)
            
            if single_letters:
                print(f"  ⚠️ Found single-letter variables: {single_letters}")
                self.suggestions.append(f"Consider more descriptive variable names in {file_path.name}")
            else:
                print(f"  ✅ Variable names look good")
                
            # Check for overly technical names
            tech_pattern = r'\b(util|helper|temp|tmp|data|obj|item)\d*\b'
            tech_names = re.findall(tech_pattern, content, re.IGNORECASE)
            
            if tech_names:
                print(f"  ⚠️ Found generic names: {tech_names}")
                self.suggestions.append(f"Consider more specific names in {file_path.name}")
                
        except Exception as e:
            print(f"  ❌ Error checking variable names: {e}")
            
    def check_error_handling(self, file_path: Path):
        """Check for proper error handling"""
        print(f"🛡️ Checking error handling: {file_path.name}")
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Look for try/except blocks
            try_blocks = content.count('try:')
            except_blocks = content.count('except')
            
            if try_blocks > 0:
                print(f"  ✅ Found {try_blocks} try/except blocks")
            else:
                print(f"  ⚠️ No error handling found")
                self.suggestions.append(f"Consider adding error handling to {file_path.name}")
                
            # Check for bare except clauses
            bare_except_pattern = r'except\s*:'
            bare_excepts = re.findall(bare_except_pattern, content)
            
            if bare_excepts:
                print(f"  ⚠️ Found {len(bare_excepts)} bare except clauses")
                self.issues_found.append(f"Bare except clauses in {file_path.name}")
            else:
                print(f"  ✅ No bare except clauses")
                
        except Exception as e:
            print(f"  ❌ Error checking error handling: {e}")
            
    def check_commit_quality(self):
        """Check git commit messages for human-like quality"""
        print(f"📝 Checking commit quality...")
        
        try:
            # Get recent commits
            import subprocess
            result = subprocess.run(['git', 'log', '--oneline', '-10'], 
                                  capture_output=True, text=True, cwd=project_root)
            
            if result.returncode == 0:
                commits = result.stdout.strip().split('\n')
                print(f"  📊 Found {len(commits)} recent commits")
                
                # Check commit message quality
                good_commits = 0
                for commit in commits:
                    if commit:
                        message = commit.split(' ', 1)[1] if ' ' in commit else commit
                        
                        # Check for good practices
                        if (len(message) > 10 and 
                            not message.startswith('WIP') and
                            not message.startswith('temp') and
                            not message.startswith('fix') or 'fix' in message.lower()):
                            good_commits += 1
                
                print(f"  ✅ {good_commits}/{len(commits)} commits have good messages")
                
                if good_commits < len(commits) * 0.7:
                    self.suggestions.append("Consider improving commit message quality")
                    
            else:
                print(f"  ⚠️ Could not check git commits")
                
        except Exception as e:
            print(f"  ❌ Error checking commits: {e}")
            
    def check_file_organization(self):
        """Check overall file organization"""
        print(f"📁 Checking file organization...")
        
        # Check for proper directory structure
        required_dirs = ['src', 'notebooks', 'data']
        missing_dirs = []
        
        for dir_name in required_dirs:
            dir_path = project_root / dir_name
            if not dir_path.exists():
                missing_dirs.append(dir_name)
                
        if missing_dirs:
            print(f"  ❌ Missing directories: {missing_dirs}")
            self.issues_found.append(f"Missing directories: {missing_dirs}")
        else:
            print(f"  ✅ All required directories present")
            
        # Check for README
        readme_path = project_root / "README.md"
        if readme_path.exists():
            print(f"  ✅ README.md exists")
        else:
            print(f"  ⚠️ README.md missing")
            self.suggestions.append("Add a README.md file")
            
    def run_comprehensive_check(self):
        """Run all quality checks"""
        print(f"🚀 {self.name}: Starting comprehensive quality check...")
        
        # Check file organization
        self.check_file_organization()
        
        # Check commit quality
        self.check_commit_quality()
        
        # Check Python files
        src_dir = project_root / "src"
        if src_dir.exists():
            python_files = list(src_dir.rglob("*.py"))
            print(f"\n🐍 Checking {len(python_files)} Python files...")
            
            for file_path in python_files:
                print(f"\n📄 {file_path.name}")
                self.check_python_syntax(file_path)
                self.check_human_like_comments(file_path)
                self.check_variable_naming(file_path)
                self.check_error_handling(file_path)
        
        # Summary
        print(f"\n📊 Quality Check Summary:")
        print(f"  Issues found: {len(self.issues_found)}")
        print(f"  Suggestions: {len(self.suggestions)}")
        
        if self.issues_found:
            print(f"\n❌ Issues to fix:")
            for issue in self.issues_found:
                print(f"  - {issue}")
                
        if self.suggestions:
            print(f"\n💡 Suggestions for improvement:")
            for suggestion in self.suggestions:
                print(f"  - {suggestion}")
                
        if not self.issues_found and not self.suggestions:
            print(f"\n🎉 All quality checks passed!")
            
        return len(self.issues_found) == 0

def run_quality_check():
    """Run the quality assurance check"""
    agent = CodeQualityAgent()
    return agent.run_comprehensive_check()

if __name__ == "__main__":
    run_quality_check()
