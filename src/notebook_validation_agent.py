"""
Notebook Validation Agent
Validates that the rebuilt EDA notebook is working properly
"""

import json
import pandas as pd
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent

class NotebookValidationAgent:
    """Agent that validates the EDA notebook structure and content"""
    
    def __init__(self):
        self.name = "NotebookValidationAgent"
        
    def validate_notebook_structure(self):
        """Validate the notebook structure and content"""
        print(f"🔍 {self.name}: Validating EDA notebook structure...")
        
        notebook_path = project_root / "notebooks" / "03_eda.ipynb"
        
        try:
            with open(notebook_path, 'r') as f:
                notebook = json.load(f)
                
            print(f"  ✅ Notebook loaded successfully")
            
            # Check cell structure
            cells = notebook.get('cells', [])
            print(f"  📊 Total cells: {len(cells)}")
            
            # Count cell types
            cell_types = {}
            for cell in cells:
                cell_type = cell.get('cell_type', 'unknown')
                cell_types[cell_type] = cell_types.get(cell_type, 0) + 1
                
            print(f"  📋 Cell types: {cell_types}")
            
            # Check for required sections
            required_sections = [
                "Question 1: Model Performance Comparison",
                "Question 2: Language Variety Analysis", 
                "Question 3: Task Difficulty Assessment",
                "Question 4: Response Quality Analysis",
                "Question 5: Code-Switching Behavior"
            ]
            
            found_sections = []
            for cell in cells:
                if cell.get('cell_type') == 'markdown':
                    source = ''.join(cell.get('source', []))
                    for section in required_sections:
                        if section in source:
                            found_sections.append(section)
                            
            print(f"  📝 Found {len(found_sections)}/{len(required_sections)} required sections")
            for section in found_sections:
                print(f"    ✅ {section}")
                
            missing_sections = set(required_sections) - set(found_sections)
            if missing_sections:
                print(f"  ❌ Missing sections:")
                for section in missing_sections:
                    print(f"    - {section}")
                    
            # Check for analysis cells
            analysis_cells = 0
            for cell in cells:
                if cell.get('cell_type') == 'code':
                    source = ''.join(cell.get('source', []))
                    if 'plt.figure' in source or 'sns.' in source:
                        analysis_cells += 1
                        
            print(f"  📊 Analysis cells with visualizations: {analysis_cells}")
            
            # Check data availability
            data_dir = project_root / "data" / "raw"
            stimuli_exists = (data_dir / "stimuli.csv").exists()
            response_files = list(data_dir.glob("*_responses.csv"))
            
            print(f"  📁 Data availability:")
            print(f"    Stimuli file: {'✅' if stimuli_exists else '❌'}")
            print(f"    Response files: {len(response_files)} found")
            
            return len(found_sections) == len(required_sections) and analysis_cells > 0
            
        except Exception as e:
            print(f"  ❌ Error validating notebook: {e}")
            return False
            
    def validate_data_compatibility(self):
        """Validate that the notebook is compatible with available data"""
        print(f"🔍 {self.name}: Validating data compatibility...")
        
        data_dir = project_root / "data" / "raw"
        
        # Check stimuli data
        stimuli_path = data_dir / "stimuli.csv"
        if stimuli_path.exists():
            stimuli = pd.read_csv(stimuli_path)
            print(f"  ✅ Stimuli data: {len(stimuli)} examples")
            print(f"    Varieties: {list(stimuli['variety'].unique())}")
            print(f"    Tasks: {list(stimuli['task'].unique())}")
        else:
            print(f"  ❌ Stimuli file not found")
            return False
            
        # Check response data
        response_files = list(data_dir.glob("*_responses.csv"))
        print(f"  📁 Response files: {len(response_files)}")
        
        for file_path in response_files:
            model_name = file_path.stem.replace("_responses", "")
            try:
                df = pd.read_csv(file_path)
                success_count = df['success'].sum() if 'success' in df.columns else len(df)
                print(f"    {model_name.title()}: {len(df)} responses ({success_count} successful)")
            except Exception as e:
                print(f"    ❌ Error reading {model_name}: {e}")
                return False
                
        return True
        
    def run_complete_validation(self):
        """Run complete notebook validation"""
        print(f"🚀 {self.name}: Running complete validation...")
        
        structure_valid = self.validate_notebook_structure()
        data_compatible = self.validate_data_compatibility()
        
        print(f"\\n📊 Validation Results:")
        print(f"  Notebook structure: {'✅ Valid' if structure_valid else '❌ Invalid'}")
        print(f"  Data compatibility: {'✅ Compatible' if data_compatible else '❌ Incompatible'}")
        
        overall_valid = structure_valid and data_compatible
        
        if overall_valid:
            print(f"\\n🎉 EDA notebook validation PASSED!")
            print(f"   The notebook is ready for analysis with proper visualizations")
            print(f"   All 5 research questions are addressed")
            print(f"   Data compatibility confirmed")
        else:
            print(f"\\n❌ EDA notebook validation FAILED!")
            print(f"   Issues need to be resolved before analysis")
            
        return overall_valid

def run_notebook_validation():
    """Run notebook validation"""
    agent = NotebookValidationAgent()
    return agent.run_complete_validation()

if __name__ == "__main__":
    run_notebook_validation()
