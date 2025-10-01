"""
Multi-Agent System for Code-Switching Benchmark Project
Multiple specialized agents working collaboratively to debug and complete the project
"""

import os
import sys
import time
import threading
import queue
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import pandas as pd
import subprocess
import json
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
load_dotenv(project_root / ".env")

class AgentStatus(Enum):
    IDLE = "idle"
    WORKING = "working"
    WAITING = "waiting"
    COMPLETED = "completed"
    ERROR = "error"

@dataclass
class Task:
    id: str
    description: str
    agent_type: str
    priority: int
    dependencies: List[str]
    data: Dict[str, Any]
    status: str = "pending"

@dataclass
class AgentMessage:
    sender: str
    receiver: str
    message_type: str
    data: Dict[str, Any]
    timestamp: float

class AgentBase:
    def __init__(self, name: str, agent_type: str):
        self.name = name
        self.agent_type = agent_type
        self.status = AgentStatus.IDLE
        self.message_queue = queue.Queue()
        self.thread = None
        self.running = False
        self.completed_tasks = []
        self.current_task = None
        
    def start(self):
        """Start the agent in a separate thread"""
        self.running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.start()
        print(f"🤖 {self.name} started")
        
    def stop(self):
        """Stop the agent"""
        self.running = False
        if self.thread:
            self.thread.join()
        print(f"🛑 {self.name} stopped")
        
    def send_message(self, receiver: str, message_type: str, data: Dict[str, Any]):
        """Send a message to another agent"""
        message = AgentMessage(
            sender=self.name,
            receiver=receiver,
            message_type=message_type,
            data=data,
            timestamp=time.time()
        )
        # This would be handled by the coordinator in a real system
        print(f"📤 {self.name} -> {receiver}: {message_type}")
        
    def _run(self):
        """Main agent loop"""
        while self.running:
            try:
                self.process()
                time.sleep(0.1)  # Small delay to prevent busy waiting
            except Exception as e:
                print(f"❌ {self.name} error: {e}")
                self.status = AgentStatus.ERROR
                
    def process(self):
        """Override in subclasses"""
        pass

class DataCollectionAgent(AgentBase):
    """Agent responsible for data collection and API management"""
    
    def __init__(self):
        super().__init__("DataCollector", "data_collection")
        self.api_status = {}
        self.collected_data = {}
        
    def process(self):
        """Process data collection tasks"""
        if self.status == AgentStatus.IDLE:
            self.check_api_connections()
            self.collect_data()
            
    def check_api_connections(self):
        """Check API connections for all models"""
        self.status = AgentStatus.WORKING
        print(f"🔍 {self.name}: Checking API connections...")
        
        apis = ['gemini', 'cohere', 'mistral']
        for api in apis:
            try:
                # Check if API key exists
                api_key = os.getenv(f"{api.upper()}_API_KEY")
                self.api_status[api] = bool(api_key)
                print(f"  {api.upper()}: {'✅' if self.api_status[api] else '❌'}")
            except Exception as e:
                self.api_status[api] = False
                print(f"  {api.upper()}: ❌ Error - {e}")
                
        self.status = AgentStatus.IDLE
        
    def collect_data(self):
        """Collect data from all APIs"""
        if not all(self.api_status.values()):
            print(f"⚠️ {self.name}: Not all APIs are available")
            return
            
        self.status = AgentStatus.WORKING
        print(f"📊 {self.name}: Starting data collection...")
        
        # Load stimuli data
        stimuli_path = project_root / "data" / "raw" / "stimuli.csv"
        if not stimuli_path.exists():
            print(f"❌ {self.name}: Stimuli file not found")
            self.status = AgentStatus.ERROR
            return
            
        stimuli = pd.read_csv(stimuli_path)
        print(f"📋 {self.name}: Loaded {len(stimuli)} stimuli examples")
        
        # Collect from each API
        for api in ['gemini', 'cohere', 'mistral']:
            if self.api_status[api]:
                self.collect_from_api(api, stimuli)
                
        self.status = AgentStatus.COMPLETED
        print(f"✅ {self.name}: Data collection completed")
        
    def collect_from_api(self, api: str, stimuli: pd.DataFrame):
        """Collect data from a specific API"""
        print(f"🔄 {self.name}: Collecting from {api.upper()}...")
        
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
                print(f"❌ {self.name}: Unknown API {api}")
                return
                
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
            print(f"  ✅ {api.upper()}: {len(df)} examples ({success_count} successful)")
            self.collected_data[api] = df
            
        except Exception as e:
            print(f"❌ {self.name}: Error collecting from {api}: {e}")

class DataProcessingAgent(AgentBase):
    """Agent responsible for data processing and analysis"""
    
    def __init__(self):
        super().__init__("DataProcessor", "data_processing")
        self.processed_data = {}
        
    def process(self):
        """Process data analysis tasks"""
        if self.status == AgentStatus.IDLE:
            self.check_for_new_data()
            
    def check_for_new_data(self):
        """Check for new data files to process"""
        data_dir = project_root / "data" / "raw"
        if not data_dir.exists():
            return
            
        # Look for response files
        response_files = list(data_dir.glob("*_responses.csv"))
        if not response_files:
            return
            
        self.status = AgentStatus.WORKING
        print(f"🔧 {self.name}: Processing data files...")
        
        for file_path in response_files:
            self.process_response_file(file_path)
            
        self.status = AgentStatus.IDLE
        
    def process_response_file(self, file_path: Path):
        """Process a response file and calculate metrics"""
        try:
            df = pd.read_csv(file_path)
            model_name = file_path.stem.replace("_responses", "")
            
            print(f"  📊 {self.name}: Processing {model_name} data...")
            
            # Calculate metrics
            df["input_len"] = df["input_text"].apply(lambda x: len(str(x).split()))
            df["output_len"] = df["output_text"].apply(lambda x: len(str(x).split()))
            df["length_ratio"] = df["output_len"] / df["input_len"]
            
            # Calculate token overlap
            def token_overlap(input_text, output_text):
                input_words = set(str(input_text).lower().split())
                output_words = set(str(output_text).lower().split())
                if not input_words:
                    return 0
                return len(input_words & output_words) / len(input_words)
                
            df["token_overlap"] = df.apply(lambda r: token_overlap(r["input_text"], r["output_text"]), axis=1)
            
            # Save processed data
            processed_path = project_root / "data" / "processed" / f"{model_name}_scored.csv"
            processed_path.parent.mkdir(exist_ok=True)
            df.to_csv(processed_path, index=False)
            
            print(f"    ✅ {model_name}: Processed {len(df)} examples")
            self.processed_data[model_name] = df
            
        except Exception as e:
            print(f"❌ {self.name}: Error processing {file_path}: {e}")

class NotebookAgent(AgentBase):
    """Agent responsible for notebook maintenance and debugging"""
    
    def __init__(self):
        super().__init__("NotebookManager", "notebook_management")
        self.notebook_status = {}
        
    def process(self):
        """Process notebook maintenance tasks"""
        if self.status == AgentStatus.IDLE:
            self.check_notebooks()
            
    def check_notebooks(self):
        """Check and fix notebook issues"""
        self.status = AgentStatus.WORKING
        print(f"📓 {self.name}: Checking notebooks...")
        
        notebooks_dir = project_root / "notebooks"
        if not notebooks_dir.exists():
            print(f"❌ {self.name}: Notebooks directory not found")
            self.status = AgentStatus.ERROR
            return
            
        notebook_files = list(notebooks_dir.glob("*.ipynb"))
        
        for notebook_path in notebook_files:
            self.check_notebook(notebook_path)
            
        self.status = AgentStatus.IDLE
        
    def check_notebook(self, notebook_path: Path):
        """Check and fix a specific notebook"""
        try:
            print(f"  🔍 {self.name}: Checking {notebook_path.name}...")
            
            # Read notebook
            with open(notebook_path, 'r') as f:
                notebook = json.load(f)
                
            issues_found = []
            
            # Check for common issues
            for i, cell in enumerate(notebook['cells']):
                if cell['cell_type'] == 'code':
                    source = ''.join(cell['source'])
                    
                    # Check for Python version compatibility issues
                    if 'str | None' in source:
                        issues_found.append(f"Cell {i}: Python version compatibility issue")
                        
                    # Check for empty cells
                    if not source.strip():
                        issues_found.append(f"Cell {i}: Empty code cell")
                        
            if issues_found:
                print(f"    ⚠️ {notebook_path.name}: {len(issues_found)} issues found")
                for issue in issues_found:
                    print(f"      - {issue}")
            else:
                print(f"    ✅ {notebook_path.name}: No issues found")
                
            self.notebook_status[notebook_path.name] = {
                'issues': len(issues_found),
                'status': 'ok' if not issues_found else 'needs_fix'
            }
            
        except Exception as e:
            print(f"❌ {self.name}: Error checking {notebook_path}: {e}")

class QualityAssuranceAgent(AgentBase):
    """Agent responsible for quality assurance and validation"""
    
    def __init__(self):
        super().__init__("QualityAssurance", "quality_assurance")
        self.quality_metrics = {}
        
    def process(self):
        """Process quality assurance tasks"""
        if self.status == AgentStatus.IDLE:
            self.run_quality_checks()
            
    def run_quality_checks(self):
        """Run comprehensive quality checks"""
        self.status = AgentStatus.WORKING
        print(f"🔍 {self.name}: Running quality checks...")
        
        # Check data quality
        self.check_data_quality()
        
        # Check code quality
        self.check_code_quality()
        
        # Check project structure
        self.check_project_structure()
        
        self.status = AgentStatus.IDLE
        
    def check_data_quality(self):
        """Check data quality across all files"""
        print(f"  📊 {self.name}: Checking data quality...")
        
        data_dir = project_root / "data"
        if not data_dir.exists():
            print(f"    ❌ Data directory not found")
            return
            
        # Check raw data
        raw_dir = data_dir / "raw"
        if raw_dir.exists():
            raw_files = list(raw_dir.glob("*.csv"))
            print(f"    📁 Raw data: {len(raw_files)} files")
            
            for file_path in raw_files:
                try:
                    df = pd.read_csv(file_path)
                    print(f"      ✅ {file_path.name}: {len(df)} rows")
                except Exception as e:
                    print(f"      ❌ {file_path.name}: Error - {e}")
                    
        # Check processed data
        processed_dir = data_dir / "processed"
        if processed_dir.exists():
            processed_files = list(processed_dir.glob("*.csv"))
            print(f"    📁 Processed data: {len(processed_files)} files")
            
    def check_code_quality(self):
        """Check code quality"""
        print(f"  🔧 {self.name}: Checking code quality...")
        
        src_dir = project_root / "src"
        if not src_dir.exists():
            print(f"    ❌ Source directory not found")
            return
            
        python_files = list(src_dir.rglob("*.py"))
        print(f"    🐍 Python files: {len(python_files)}")
        
        for file_path in python_files:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    
                # Basic quality checks
                issues = []
                if len(content.split('\n')) > 1000:
                    issues.append("File too long")
                if 'TODO' in content or 'FIXME' in content:
                    issues.append("Contains TODO/FIXME")
                    
                if issues:
                    print(f"      ⚠️ {file_path.name}: {', '.join(issues)}")
                else:
                    print(f"      ✅ {file_path.name}: OK")
                    
            except Exception as e:
                print(f"      ❌ {file_path.name}: Error - {e}")
                
    def check_project_structure(self):
        """Check project structure"""
        print(f"  📁 {self.name}: Checking project structure...")
        
        required_dirs = ['src', 'notebooks', 'data']
        required_files = ['requirements.txt', 'README.md']
        
        for dir_name in required_dirs:
            dir_path = project_root / dir_name
            if dir_path.exists():
                print(f"    ✅ {dir_name}/ directory exists")
            else:
                print(f"    ❌ {dir_name}/ directory missing")
                
        for file_name in required_files:
            file_path = project_root / file_name
            if file_path.exists():
                print(f"    ✅ {file_name} exists")
            else:
                print(f"    ❌ {file_name} missing")

class CoordinatorAgent(AgentBase):
    """Main coordinator agent that manages all other agents"""
    
    def __init__(self):
        super().__init__("Coordinator", "coordination")
        self.agents = {}
        self.task_queue = queue.Queue()
        self.project_status = "initializing"
        
    def add_agent(self, agent: AgentBase):
        """Add an agent to the system"""
        self.agents[agent.name] = agent
        print(f"➕ Added agent: {agent.name}")
        
    def start_all_agents(self):
        """Start all agents"""
        print("🚀 Starting multi-agent system...")
        for agent in self.agents.values():
            agent.start()
        self.project_status = "running"
        
    def stop_all_agents(self):
        """Stop all agents"""
        print("🛑 Stopping multi-agent system...")
        for agent in self.agents.values():
            agent.stop()
        self.project_status = "stopped"
        
    def process(self):
        """Main coordination loop"""
        if self.status == AgentStatus.IDLE:
            self.monitor_agents()
            self.coordinate_tasks()
            
    def monitor_agents(self):
        """Monitor agent status and health"""
        for agent_name, agent in self.agents.items():
            if agent.status == AgentStatus.ERROR:
                print(f"⚠️ {agent_name} is in error state")
                # Could implement recovery logic here
                
    def coordinate_tasks(self):
        """Coordinate tasks between agents"""
        # Check if data collection is complete
        data_agent = self.agents.get("DataCollector")
        if data_agent and data_agent.status == AgentStatus.COMPLETED:
            # Trigger data processing
            processing_agent = self.agents.get("DataProcessor")
            if processing_agent and processing_agent.status == AgentStatus.IDLE:
                print("🔄 Triggering data processing...")
                
        # Check if all tasks are complete
        all_complete = all(
            agent.status in [AgentStatus.COMPLETED, AgentStatus.IDLE] 
            for agent in self.agents.values()
        )
        
        if all_complete and self.project_status == "running":
            print("🎉 All agents have completed their tasks!")
            self.project_status = "completed"

def create_multi_agent_system():
    """Create and configure the multi-agent system"""
    print("🏗️ Creating multi-agent system...")
    
    # Create coordinator
    coordinator = CoordinatorAgent()
    
    # Create specialized agents
    data_collector = DataCollectionAgent()
    data_processor = DataProcessingAgent()
    notebook_manager = NotebookAgent()
    quality_assurance = QualityAssuranceAgent()
    
    # Add agents to coordinator
    coordinator.add_agent(data_collector)
    coordinator.add_agent(data_processor)
    coordinator.add_agent(notebook_manager)
    coordinator.add_agent(quality_assurance)
    
    return coordinator

def run_multi_agent_system():
    """Run the complete multi-agent system"""
    coordinator = create_multi_agent_system()
    
    try:
        # Start all agents
        coordinator.start_all_agents()
        
        # Run for a specified time or until completion
        start_time = time.time()
        max_runtime = 300  # 5 minutes
        
        while coordinator.project_status == "running" and (time.time() - start_time) < max_runtime:
            time.sleep(1)
            
        # Stop all agents
        coordinator.stop_all_agents()
        
        print(f"🏁 Multi-agent system completed with status: {coordinator.project_status}")
        
    except KeyboardInterrupt:
        print("⏹️ Interrupted by user")
        coordinator.stop_all_agents()
    except Exception as e:
        print(f"❌ System error: {e}")
        coordinator.stop_all_agents()

if __name__ == "__main__":
    run_multi_agent_system()
