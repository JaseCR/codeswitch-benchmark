#!/bin/bash

# Multi-Agent System Launcher for Code-Switching Benchmark
# This script starts all agents to debug and complete the project

echo "🚀 Starting Multi-Agent Code-Switching Benchmark System"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Error: Virtual environment not found. Please create one first:"
    echo "   python3 -m venv .venv"
    echo "   source .venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Check if required packages are installed
echo "📦 Checking required packages..."
python -c "import pandas, numpy, matplotlib, seaborn, tqdm, dotenv" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing required packages. Installing..."
    pip install pandas numpy matplotlib seaborn tqdm python-dotenv
fi

# Run the multi-agent system
echo "🤖 Starting multi-agent system..."
python src/run_agents.py

echo "🏁 Multi-agent system completed!"
