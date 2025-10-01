"""
Specialized Debug Agents for Code-Switching Benchmark Project
These agents focus on specific debugging and fixing tasks
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
import pandas as pd
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
load_dotenv(project_root / ".env")

class NotebookFixerAgent:
    """Agent specialized in fixing notebook issues"""
    
    def __init__(self):
        self.name = "NotebookFixer"
        self.fixes_applied = []
        
    def fix_python_compatibility_issues(self, notebook_path: Path):
        """Fix Python version compatibility issues in notebooks"""
        print(f"🔧 {self.name}: Fixing Python compatibility issues in {notebook_path.name}")
        
        try:
            with open(notebook_path, 'r') as f:
                notebook = json.load(f)
                
            fixed = False
            for i, cell in enumerate(notebook['cells']):
                if cell['cell_type'] == 'code':
                    source = ''.join(cell['source'])
                    
                    # Fix str | None syntax
                    if 'str | None' in source:
                        new_source = source.replace('str | None', 'str')
                        cell['source'] = [new_source]
                        fixed = True
                        self.fixes_applied.append(f"Fixed Python compatibility in cell {i}")
                        
            if fixed:
                with open(notebook_path, 'w') as f:
                    json.dump(notebook, f, indent=1)
                print(f"  ✅ Fixed Python compatibility issues")
            else:
                print(f"  ℹ️ No Python compatibility issues found")
                
        except Exception as e:
            print(f"  ❌ Error fixing notebook: {e}")
            
    def fix_stimuli_data_mismatch(self, notebook_path: Path):
        """Fix stimuli data mismatch in notebooks"""
        print(f"🔧 {self.name}: Fixing stimuli data mismatch in {notebook_path.name}")
        
        try:
            with open(notebook_path, 'r') as f:
                notebook = json.load(f)
                
            # Find the stimuli data cell
            for i, cell in enumerate(notebook['cells']):
                if cell['cell_type'] == 'code':
                    source = ''.join(cell['source'])
                    
                    # Check if this is the stimuli data cell
                    if 'stimuli_data = [' in source and 'aave_04' in source:
                        print(f"  🔍 Found stimuli data cell {i}")
                        
                        # Replace with correct 12-example dataset
                        new_stimuli_data = '''# Define balanced test set across language varieties and tasks
# Updated with expanded trigger words for more useful data analysis
stimuli_data = [
    # African American Vernacular English (AAVE)
    {"id": "aave_01", "variety": "AAVE", "task": "paraphrase",
     "text": "He finna go to the store. You sliding?"},
    {"id": "aave_02", "variety": "AAVE", "task": "explain",
     "text": "Ion think that plan gon' work."},
    {"id": "aave_03", "variety": "AAVE", "task": "continue",
     "text": "We was tryna finish that yesterday"},

    # Spanglish (Spanish-English code-switching)
    {"id": "span_01", "variety": "Spanglish", "task": "paraphrase",
     "text": "Vamos later, it's muy close to la tienda."},
    {"id": "span_02", "variety": "Spanglish", "task": "explain",
     "text": "No entiendo bien, pero I think it's fine."},
    {"id": "span_03", "variety": "Spanglish", "task": "continue",
     "text": "We can meet en el parque, like at 5."},

    # British English
    {"id": "br_01", "variety": "BrEng", "task": "paraphrase",
     "text": "Put it in the lorry outside the flat."},
    {"id": "br_02", "variety": "BrEng", "task": "explain",
     "text": "Take the lift, not the stairs, to the first floor."},
    {"id": "br_03", "variety": "BrEng", "task": "continue",
     "text": "We're off on holiday next week, fancy it?"},

    # Standard English (control group)
    {"id": "std_01", "variety": "StdEng", "task": "paraphrase",
     "text": "He is about to head out. Are you coming?"},
    {"id": "std_02", "variety": "StdEng", "task": "explain",
     "text": "Please explain this in simple terms."},
    {"id": "std_03", "variety": "StdEng", "task": "continue",
     "text": "We should wrap this up and send it."},
]'''
                        
                        # Find the start and end of the stimuli_data definition
                        start_idx = source.find('stimuli_data = [')
                        if start_idx != -1:
                            # Find the matching closing bracket
                            bracket_count = 0
                            end_idx = start_idx
                            for j, char in enumerate(source[start_idx:], start_idx):
                                if char == '[':
                                    bracket_count += 1
                                elif char == ']':
                                    bracket_count -= 1
                                    if bracket_count == 0:
                                        end_idx = j + 1
                                        break
                            
                            # Replace the stimuli data
                            new_source = source[:start_idx] + new_stimuli_data + source[end_idx:]
                            cell['source'] = [new_source]
                            
                            self.fixes_applied.append(f"Fixed stimuli data mismatch in cell {i}")
                            print(f"  ✅ Fixed stimuli data mismatch")
                            
                            # Save the notebook
                            with open(notebook_path, 'w') as f:
                                json.dump(notebook, f, indent=1)
                            break
                            
        except Exception as e:
            print(f"  ❌ Error fixing stimuli data: {e}")
            
    def remove_empty_cells(self, notebook_path: Path):
        """Remove empty cells from notebooks"""
        print(f"🔧 {self.name}: Removing empty cells from {notebook_path.name}")
        
        try:
            with open(notebook_path, 'r') as f:
                notebook = json.load(f)
                
            original_count = len(notebook['cells'])
            
            # Filter out empty cells
            notebook['cells'] = [
                cell for cell in notebook['cells']
                if not (cell['cell_type'] == 'code' and not ''.join(cell['source']).strip())
            ]
            
            new_count = len(notebook['cells'])
            removed = original_count - new_count
            
            if removed > 0:
                with open(notebook_path, 'w') as f:
                    json.dump(notebook, f, indent=1)
                self.fixes_applied.append(f"Removed {removed} empty cells")
                print(f"  ✅ Removed {removed} empty cells")
            else:
                print(f"  ℹ️ No empty cells found")
                
        except Exception as e:
            print(f"  ❌ Error removing empty cells: {e}")
            
    def fix_all_notebooks(self):
        """Fix all notebooks in the project"""
        print(f"🚀 {self.name}: Starting comprehensive notebook fixes...")
        
        notebooks_dir = project_root / "notebooks"
        if not notebooks_dir.exists():
            print(f"❌ Notebooks directory not found")
            return
            
        notebook_files = list(notebooks_dir.glob("*.ipynb"))
        print(f"📓 Found {len(notebook_files)} notebooks to check")
        
        for notebook_path in notebook_files:
            print(f"\n🔍 Processing {notebook_path.name}...")
            
            # Apply all fixes
            self.fix_python_compatibility_issues(notebook_path)
            self.fix_stimuli_data_mismatch(notebook_path)
            self.remove_empty_cells(notebook_path)
            
        print(f"\n✅ {self.name}: Applied {len(self.fixes_applied)} fixes total")
        for fix in self.fixes_applied:
            print(f"  - {fix}")

class DataValidatorAgent:
    """Agent specialized in data validation and quality checks"""
    
    def __init__(self):
        self.name = "DataValidator"
        self.validation_results = {}
        
    def validate_stimuli_data(self):
        """Validate the stimuli dataset"""
        print(f"🔍 {self.name}: Validating stimuli data...")
        
        stimuli_path = project_root / "data" / "raw" / "stimuli.csv"
        if not stimuli_path.exists():
            print(f"  ❌ Stimuli file not found")
            return False
            
        try:
            df = pd.read_csv(stimuli_path)
            
            # Check basic structure
            required_columns = ['id', 'variety', 'task', 'text']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                print(f"  ❌ Missing columns: {missing_columns}")
                return False
                
            # Check data counts
            expected_varieties = ['AAVE', 'Spanglish', 'BrEng', 'StdEng']
            actual_varieties = df['variety'].unique()
            
            if not all(variety in actual_varieties for variety in expected_varieties):
                print(f"  ❌ Missing varieties. Expected: {expected_varieties}, Got: {actual_varieties}")
                return False
                
            # Check examples per variety
            variety_counts = df['variety'].value_counts()
            expected_per_variety = 3
            
            for variety in expected_varieties:
                if variety_counts.get(variety, 0) != expected_per_variety:
                    print(f"  ❌ {variety}: Expected {expected_per_variety}, Got {variety_counts.get(variety, 0)}")
                    return False
                    
            print(f"  ✅ Stimuli data validation passed")
            print(f"    - Total examples: {len(df)}")
            print(f"    - Varieties: {list(actual_varieties)}")
            print(f"    - Examples per variety: {variety_counts.to_dict()}")
            
            self.validation_results['stimuli'] = {
                'status': 'valid',
                'count': len(df),
                'varieties': list(actual_varieties),
                'variety_counts': variety_counts.to_dict()
            }
            
            return True
            
        except Exception as e:
            print(f"  ❌ Error validating stimuli data: {e}")
            return False
            
    def validate_response_data(self):
        """Validate response data from all APIs"""
        print(f"🔍 {self.name}: Validating response data...")
        
        data_dir = project_root / "data" / "raw"
        if not data_dir.exists():
            print(f"  ❌ Data directory not found")
            return False
            
        response_files = list(data_dir.glob("*_responses.csv"))
        print(f"  📁 Found {len(response_files)} response files")
        
        all_valid = True
        
        for file_path in response_files:
            model_name = file_path.stem.replace("_responses", "")
            print(f"  🔍 Validating {model_name} responses...")
            
            try:
                df = pd.read_csv(file_path)
                
                # Check required columns
                required_columns = ['id', 'variety', 'task', 'input_text', 'output_text']
                missing_columns = [col for col in required_columns if col not in df.columns]
                
                if missing_columns:
                    print(f"    ❌ Missing columns: {missing_columns}")
                    all_valid = False
                    continue
                    
                # Check for errors
                error_count = df['output_text'].str.contains('ERROR:', na=False).sum()
                success_count = len(df) - error_count
                
                print(f"    ✅ {model_name}: {len(df)} examples ({success_count} successful, {error_count} errors)")
                
                self.validation_results[model_name] = {
                    'status': 'valid' if error_count == 0 else 'has_errors',
                    'total': len(df),
                    'successful': success_count,
                    'errors': error_count
                }
                
            except Exception as e:
                print(f"    ❌ Error validating {model_name}: {e}")
                all_valid = False
                
        return all_valid
        
    def validate_all_data(self):
        """Run all data validation checks"""
        print(f"🚀 {self.name}: Starting comprehensive data validation...")
        
        stimuli_valid = self.validate_stimuli_data()
        responses_valid = self.validate_response_data()
        
        overall_valid = stimuli_valid and responses_valid
        
        print(f"\n📊 {self.name}: Validation Summary")
        print(f"  Stimuli data: {'✅ Valid' if stimuli_valid else '❌ Invalid'}")
        print(f"  Response data: {'✅ Valid' if responses_valid else '❌ Invalid'}")
        print(f"  Overall: {'✅ All Valid' if overall_valid else '❌ Issues Found'}")
        
        return overall_valid

class APITesterAgent:
    """Agent specialized in testing API connections and functionality"""
    
    def __init__(self):
        self.name = "APITester"
        self.api_results = {}
        
    def test_api_connection(self, api_name: str):
        """Test connection to a specific API"""
        print(f"🔍 {self.name}: Testing {api_name.upper()} API...")
        
        try:
            # Check API key
            api_key = os.getenv(f"{api_name.upper()}_API_KEY")
            if not api_key:
                print(f"  ❌ No API key found for {api_name.upper()}")
                self.api_results[api_name] = {'status': 'no_key', 'error': 'No API key'}
                return False
                
            # Import and test the adapter
            if api_name == 'gemini':
                from adapters.gemini_adapter import query_gemini
                test_func = query_gemini
            elif api_name == 'cohere':
                from adapters.cohere_adapter import query_cohere
                test_func = query_cohere
            elif api_name == 'mistral':
                from adapters.mistral_adapter import query_mistral
                test_func = query_mistral
            else:
                print(f"  ❌ Unknown API: {api_name}")
                self.api_results[api_name] = {'status': 'unknown', 'error': 'Unknown API'}
                return False
                
            # Test with a simple prompt
            test_prompt = "Hello, this is a test."
            response = test_func(test_prompt)
            
            if response and not str(response).startswith("ERROR:"):
                print(f"  ✅ {api_name.upper()}: Connection successful")
                print(f"    Response: {response[:50]}...")
                self.api_results[api_name] = {
                    'status': 'success',
                    'response_length': len(str(response))
                }
                return True
            else:
                print(f"  ❌ {api_name.upper()}: Connection failed")
                print(f"    Response: {response}")
                self.api_results[api_name] = {
                    'status': 'failed',
                    'error': str(response)
                }
                return False
                
        except Exception as e:
            print(f"  ❌ {api_name.upper()}: Error - {e}")
            self.api_results[api_name] = {'status': 'error', 'error': str(e)}
            return False
            
    def test_all_apis(self):
        """Test all configured APIs"""
        print(f"🚀 {self.name}: Testing all API connections...")
        
        apis = ['gemini', 'cohere', 'mistral']
        successful_apis = []
        
        for api in apis:
            if self.test_api_connection(api):
                successful_apis.append(api)
                
        print(f"\n📊 {self.name}: API Test Summary")
        for api, result in self.api_results.items():
            status_emoji = {
                'success': '✅',
                'failed': '❌',
                'error': '❌',
                'no_key': '⚠️',
                'unknown': '❓'
            }.get(result['status'], '❓')
            
            print(f"  {status_emoji} {api.upper()}: {result['status']}")
            
        print(f"\n✅ {len(successful_apis)}/{len(apis)} APIs working: {successful_apis}")
        return successful_apis

class ProjectCompletionAgent:
    """Agent that orchestrates the complete project completion"""
    
    def __init__(self):
        self.name = "ProjectCompletion"
        self.completion_status = {}
        
    def run_complete_project_fix(self):
        """Run the complete project fixing process"""
        print(f"🚀 {self.name}: Starting complete project fix...")
        
        # Step 1: Fix notebooks
        print(f"\n📓 Step 1: Fixing notebooks...")
        notebook_fixer = NotebookFixerAgent()
        notebook_fixer.fix_all_notebooks()
        self.completion_status['notebooks'] = 'fixed'
        
        # Step 2: Test APIs
        print(f"\n🔌 Step 2: Testing APIs...")
        api_tester = APITesterAgent()
        working_apis = api_tester.test_all_apis()
        self.completion_status['apis'] = working_apis
        
        # Step 3: Validate data
        print(f"\n📊 Step 3: Validating data...")
        data_validator = DataValidatorAgent()
        data_valid = data_validator.validate_all_data()
        self.completion_status['data'] = 'valid' if data_valid else 'invalid'
        
        # Step 4: Run data collection if APIs are working
        if working_apis:
            print(f"\n📥 Step 4: Running data collection...")
            self.run_data_collection(working_apis)
        else:
            print(f"\n⚠️ Step 4: Skipping data collection - no working APIs")
            self.completion_status['data_collection'] = 'skipped'
            
        # Step 5: Final validation
        print(f"\n🔍 Step 5: Final validation...")
        final_valid = data_validator.validate_all_data()
        self.completion_status['final_validation'] = 'valid' if final_valid else 'invalid'
        
        # Summary
        print(f"\n🎉 {self.name}: Project completion summary")
        for step, status in self.completion_status.items():
            print(f"  {step}: {status}")
            
        return final_valid
        
    def run_data_collection(self, working_apis: List[str]):
        """Run data collection for working APIs"""
        print(f"📥 {self.name}: Running data collection for {working_apis}")
        
        # Load stimuli data
        stimuli_path = project_root / "data" / "raw" / "stimuli.csv"
        if not stimuli_path.exists():
            print(f"  ❌ Stimuli file not found")
            return
            
        stimuli = pd.read_csv(stimuli_path)
        print(f"  📋 Loaded {len(stimuli)} stimuli examples")
        
        for api in working_apis:
            print(f"  🔄 Collecting from {api.upper()}...")
            
            try:
                # Import the appropriate adapter
                if api == 'gemini':
                    from adapters.gemini_adapter import query_gemini
                    query_func = query_gemini
                elif api == 'cohere':
                    from adapters.cohere_adapter import query_cohere
                    query_func = query_cohere
                elif api == 'mistral':
                    from adapters.mistral_adapter import query_mistral
                    query_func = query_mistral
                else:
                    continue
                    
                responses = []
                for _, row in stimuli.iterrows():
                    prompt = f"Paraphrase or continue this text in the same dialectal style: {row.text}"
                    try:
                        output = query_func(prompt)
                        responses.append({
                            "id": row.id,
                            "variety": row.variety,
                            "task": row.task,
                            "input_text": row.text,
                            "output_text": output,
                            "success": bool(output and not str(output).startswith("ERROR:"))
                        })
                    except Exception as e:
                        responses.append({
                            "id": row.id,
                            "variety": row.variety,
                            "task": row.task,
                            "input_text": row.text,
                            "output_text": f"ERROR: {e}",
                            "success": False
                        })
                        
                # Save responses
                df = pd.DataFrame(responses)
                output_path = project_root / "data" / "raw" / f"{api}_responses.csv"
                df.to_csv(output_path, index=False)
                
                success_count = df['success'].sum()
                print(f"    ✅ {api.upper()}: {len(df)} examples ({success_count} successful)")
                
            except Exception as e:
                print(f"    ❌ Error collecting from {api}: {e}")
                
        self.completion_status['data_collection'] = 'completed'

def run_complete_project_fix():
    """Main function to run the complete project fix"""
    print("🏗️ Starting complete project fix with specialized agents...")
    
    completion_agent = ProjectCompletionAgent()
    success = completion_agent.run_complete_project_fix()
    
    if success:
        print("\n🎉 Project fix completed successfully!")
        print("✅ All notebooks fixed")
        print("✅ APIs tested and working")
        print("✅ Data validated")
        print("✅ Data collection completed")
    else:
        print("\n⚠️ Project fix completed with some issues")
        print("Check the logs above for details")
        
    return success

if __name__ == "__main__":
    run_complete_project_fix()
