"""
Real-time Agent Dashboard
Shows the status of all agents working on the project
"""

import os
import sys
import time
import threading
from pathlib import Path
from typing import Dict, List, Any
import json

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class AgentDashboard:
    """Real-time dashboard for monitoring agent activities"""
    
    def __init__(self):
        self.agents = {}
        self.running = False
        self.update_interval = 1.0
        
    def add_agent(self, name: str, agent_type: str, status: str = "idle"):
        """Add an agent to the dashboard"""
        self.agents[name] = {
            'type': agent_type,
            'status': status,
            'last_update': time.time(),
            'tasks_completed': 0,
            'current_task': None,
            'progress': 0
        }
        
    def update_agent(self, name: str, **kwargs):
        """Update agent information"""
        if name in self.agents:
            self.agents[name].update(kwargs)
            self.agents[name]['last_update'] = time.time()
            
    def start_monitoring(self):
        """Start the dashboard monitoring"""
        self.running = True
        monitor_thread = threading.Thread(target=self._monitor_loop)
        monitor_thread.daemon = True
        monitor_thread.start()
        
    def stop_monitoring(self):
        """Stop the dashboard monitoring"""
        self.running = False
        
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.running:
            self._display_dashboard()
            time.sleep(self.update_interval)
            
    def _display_dashboard(self):
        """Display the current dashboard"""
        # Clear screen (works on most terminals)
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print("🤖 Multi-Agent Code-Switching Benchmark Dashboard")
        print("=" * 60)
        print(f"⏰ {time.strftime('%H:%M:%S')} | Agents: {len(self.agents)}")
        print()
        
        # Display agent status
        for name, info in self.agents.items():
            status_emoji = {
                'idle': '😴',
                'working': '⚡',
                'completed': '✅',
                'error': '❌',
                'waiting': '⏳'
            }.get(info['status'], '❓')
            
            print(f"{status_emoji} {name} ({info['type']})")
            print(f"   Status: {info['status']}")
            if info['current_task']:
                print(f"   Task: {info['current_task']}")
            if info['progress'] > 0:
                print(f"   Progress: {info['progress']}%")
            print(f"   Completed: {info['tasks_completed']} tasks")
            print()
            
        # Display project status
        self._display_project_status()
        
    def _display_project_status(self):
        """Display overall project status"""
        print("📊 Project Status")
        print("-" * 30)
        
        # Check data files
        data_dir = project_root / "data"
        if data_dir.exists():
            raw_files = list((data_dir / "raw").glob("*.csv")) if (data_dir / "raw").exists() else []
            processed_files = list((data_dir / "processed").glob("*.csv")) if (data_dir / "processed").exists() else []
            
            print(f"📁 Data Files: {len(raw_files)} raw, {len(processed_files)} processed")
        else:
            print("📁 Data Files: No data directory")
            
        # Check notebooks
        notebooks_dir = project_root / "notebooks"
        if notebooks_dir.exists():
            notebook_files = list(notebooks_dir.glob("*.ipynb"))
            print(f"📓 Notebooks: {len(notebook_file)} files")
        else:
            print("📓 Notebooks: No notebooks directory")
            
        # Check API status
        api_keys = {
            'Gemini': bool(os.getenv('GEMINI_API_KEY')),
            'Cohere': bool(os.getenv('COHERE_API_KEY')),
            'Mistral': bool(os.getenv('MISTRAL_API_KEY'))
        }
        
        working_apis = [api for api, status in api_keys.items() if status]
        print(f"🔌 APIs: {len(working_apis)}/{len(api_keys)} working ({', '.join(working_apis)})")
        
        print()
        print("Press Ctrl+C to stop monitoring")

def create_dashboard():
    """Create and configure the dashboard"""
    dashboard = AgentDashboard()
    
    # Add all agents
    dashboard.add_agent("DataCollector", "data_collection", "idle")
    dashboard.add_agent("DataProcessor", "data_processing", "idle")
    dashboard.add_agent("NotebookManager", "notebook_management", "idle")
    dashboard.add_agent("QualityAssurance", "quality_assurance", "idle")
    dashboard.add_agent("APITester", "api_testing", "idle")
    dashboard.add_agent("Coordinator", "coordination", "idle")
    
    return dashboard

def run_dashboard():
    """Run the dashboard"""
    dashboard = create_dashboard()
    
    try:
        dashboard.start_monitoring()
        
        # Simulate some agent activity
        time.sleep(2)
        dashboard.update_agent("APITester", status="working", current_task="Testing API connections")
        
        time.sleep(3)
        dashboard.update_agent("APITester", status="completed", tasks_completed=1)
        dashboard.update_agent("DataCollector", status="working", current_task="Collecting data from APIs")
        
        time.sleep(5)
        dashboard.update_agent("DataCollector", status="completed", tasks_completed=1)
        dashboard.update_agent("DataProcessor", status="working", current_task="Processing response data")
        
        time.sleep(3)
        dashboard.update_agent("DataProcessor", status="completed", tasks_completed=1)
        dashboard.update_agent("NotebookManager", status="working", current_task="Fixing notebook issues")
        
        time.sleep(4)
        dashboard.update_agent("NotebookManager", status="completed", tasks_completed=1)
        dashboard.update_agent("QualityAssurance", status="working", current_task="Running quality checks")
        
        time.sleep(3)
        dashboard.update_agent("QualityAssurance", status="completed", tasks_completed=1)
        dashboard.update_agent("Coordinator", status="completed", tasks_completed=1)
        
        # Keep running until interrupted
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
    finally:
        dashboard.stop_monitoring()

if __name__ == "__main__":
    run_dashboard()
