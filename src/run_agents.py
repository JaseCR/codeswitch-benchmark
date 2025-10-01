#!/usr/bin/env python3
"""
Main orchestrator for running the multi-agent system
This script coordinates all agents to debug and complete the project
"""

import os
import sys
import time
import threading
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Main function to run all agents"""
    print("🚀 Starting Multi-Agent Code-Switching Benchmark System")
    print("=" * 60)
    
    # Change to project root
    os.chdir(project_root)
    print(f"📁 Working directory: {project_root}")
    
    # Import and run the specialized debug agents
    try:
        from debug_agents import run_complete_project_fix
        
        print("\n🤖 Running specialized debug agents...")
        success = run_complete_project_fix()
        
        if success:
            print("\n🎉 All agents completed successfully!")
        else:
            print("\n⚠️ Some agents encountered issues")
            
    except ImportError as e:
        print(f"❌ Error importing debug agents: {e}")
        return False
    except Exception as e:
        print(f"❌ Error running agents: {e}")
        return False
        
    # Run the multi-agent system
    try:
        print("\n🤖 Starting multi-agent coordination system...")
        from multi_agent_system import run_multi_agent_system
        
        # Run the multi-agent system
        run_multi_agent_system()
        
    except ImportError as e:
        print(f"❌ Error importing multi-agent system: {e}")
        return False
    except Exception as e:
        print(f"❌ Error running multi-agent system: {e}")
        return False
        
    print("\n🏁 Multi-agent system completed!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
