#!/usr/bin/env python3
"""
Code-Switching Benchmark Web Application
A beautiful, functional website for testing language model code-switching capabilities
"""

from flask import Flask, render_template, request, jsonify, session
import os
import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import plotly.graph_objs as go
import plotly.utils
from datetime import datetime
import threading
import time

# Import our existing adapters
import sys
sys.path.append('src')
from adapters.gemini_adapter import GeminiAdapter
from adapters.mistral_adapter import query_mistral
from adapters.cohere_adapter import query_cohere

app = Flask(__name__)
app.secret_key = 'code-switching-benchmark-2024'

# Configure matplotlib for web
plt.style.use('seaborn-v0_8-colorblind')
sns.set_palette("husl")

class CodeSwitchingTester:
    def __init__(self):
        self.results = []
        self.test_prompts = [
            {
                "id": "aave_1",
                "variety": "AAVE",
                "task": "paraphrase",
                "text": "Yo, I'm finna go to the store real quick, you want anything?",
                "expected_markers": ["finna", "yo", "real quick"]
            },
            {
                "id": "spanglish_1", 
                "variety": "Spanglish",
                "task": "continue",
                "text": "Hola, ¿cómo estás? I'm doing bien, gracias.",
                "expected_markers": ["hola", "cómo", "bien", "gracias"]
            },
            {
                "id": "breng_1",
                "variety": "BrEng", 
                "task": "explain",
                "text": "That's brilliant! Fancy a cuppa? The lift's broken again.",
                "expected_markers": ["brilliant", "fancy", "cuppa", "lift"]
            },
            {
                "id": "stdeng_1",
                "variety": "StdEng",
                "task": "paraphrase", 
                "text": "Please send the document to the office by tomorrow.",
                "expected_markers": ["please", "send", "document", "office"]
            }
        ]
    
    def test_model(self, model_name, api_key, prompt_data):
        """Test a single model with a prompt"""
        try:
            if model_name == "gemini":
                adapter = GeminiAdapter(api_key=api_key)
                response = adapter.generate_response(prompt_data["text"])
            elif model_name == "mistral":
                # Set environment variable for mistral
                os.environ["MISTRAL_API_KEY"] = api_key
                response = query_mistral(prompt_data["text"])
            elif model_name == "cohere":
                # Set environment variable for cohere
                os.environ["COHERE_API_KEY"] = api_key
                response = query_cohere(prompt_data["text"])
            else:
                return {"error": f"Unknown model: {model_name}"}
            
            # Analyze code-switching retention
            markers_found = []
            if response and isinstance(response, str):
                for marker in prompt_data["expected_markers"]:
                    if marker.lower() in response.lower():
                        markers_found.append(marker)
            
            retention_rate = len(markers_found) / len(prompt_data["expected_markers"])
            
            return {
                "model": model_name,
                "variety": prompt_data["variety"],
                "task": prompt_data["task"],
                "input_text": prompt_data["text"],
                "output_text": response if response else "No response generated",
                "expected_markers": prompt_data["expected_markers"],
                "found_markers": markers_found,
                "retention_rate": retention_rate,
                "response_length": len(response.split()) if response and isinstance(response, str) else 0,
                "success": True,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "model": model_name,
                "variety": prompt_data["variety"],
                "task": prompt_data["task"],
                "input_text": prompt_data["text"],
                "output_text": f"Error: {str(e)}",
                "expected_markers": prompt_data["expected_markers"],
                "found_markers": [],
                "retention_rate": 0,
                "response_length": 0,
                "success": False,
                "timestamp": datetime.now().isoformat()
            }
    
    def run_comprehensive_test(self, api_keys):
        """Run comprehensive test across all models and prompts"""
        results = []
        
        for prompt in self.test_prompts:
            for model_name, api_key in api_keys.items():
                if api_key:  # Only test if API key is provided
                    result = self.test_model(model_name, api_key, prompt)
                    results.append(result)
                    time.sleep(0.5)  # Rate limiting
        
        self.results = results
        return results

tester = CodeSwitchingTester()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/test')
def test_page():
    """Interactive testing page"""
    return render_template('test.html')

@app.route('/results')
def results_page():
    """Results and analysis page"""
    return render_template('results.html')

@app.route('/api/test', methods=['POST'])
def api_test():
    """API endpoint for running tests"""
    data = request.json
    api_keys = {
        'gemini': data.get('gemini_key', ''),
        'mistral': data.get('mistral_key', ''),
        'cohere': data.get('cohere_key', '')
    }
    
    # Filter out empty keys
    api_keys = {k: v for k, v in api_keys.items() if v.strip()}
    
    if not api_keys:
        return jsonify({"error": "Please provide at least one API key"})
    
    # Run tests
    results = tester.run_comprehensive_test(api_keys)
    
    return jsonify({
        "success": True,
        "results": results,
        "summary": generate_summary(results)
    })

@app.route('/api/visualize', methods=['POST'])
def api_visualize():
    """Generate visualizations for results"""
    results = request.json.get('results', [])
    
    if not results:
        return jsonify({"error": "No results to visualize"})
    
    # Create visualizations
    charts = create_visualizations(results)
    
    return jsonify({
        "success": True,
        "charts": charts
    })

def generate_summary(results):
    """Generate summary statistics"""
    if not results:
        return {}
    
    df = pd.DataFrame(results)
    
    summary = {
        "total_tests": len(results),
        "successful_tests": len(df[df['success'] == True]),
        "models_tested": df['model'].nunique(),
        "varieties_tested": df['variety'].nunique(),
        "average_retention_rate": df['retention_rate'].mean(),
        "model_performance": df.groupby('model')['retention_rate'].mean().to_dict(),
        "variety_difficulty": df.groupby('variety')['retention_rate'].mean().to_dict()
    }
    
    return summary

def create_visualizations(results):
    """Create beautiful visualizations"""
    df = pd.DataFrame(results)
    charts = {}
    
    # 1. Model Performance Comparison
    model_perf = df.groupby('model')['retention_rate'].mean().reset_index()
    fig1 = go.Figure(data=[
        go.Bar(
            x=model_perf['model'],
            y=model_perf['retention_rate'],
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1'],
            text=[f"{x:.1%}" for x in model_perf['retention_rate']],
            textposition='auto'
        )
    ])
    fig1.update_layout(
        title="🎯 Model Performance: Code-Switching Retention",
        xaxis_title="Model",
        yaxis_title="Retention Rate",
        yaxis=dict(tickformat='.0%'),
        template="plotly_white"
    )
    charts['model_performance'] = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    
    # 2. Variety Difficulty Heatmap
    variety_perf = df.pivot_table(
        index='variety', 
        columns='model', 
        values='retention_rate', 
        aggfunc='mean'
    ).fillna(0)
    
    fig2 = go.Figure(data=go.Heatmap(
        z=variety_perf.values,
        x=variety_perf.columns,
        y=variety_perf.index,
        colorscale='RdYlGn',
        text=[[f"{x:.1%}" for x in row] for row in variety_perf.values],
        texttemplate="%{text}",
        textfont={"size": 12}
    ))
    fig2.update_layout(
        title="🌍 Code-Switching Retention by Language Variety",
        xaxis_title="Model",
        yaxis_title="Language Variety",
        template="plotly_white"
    )
    charts['variety_heatmap'] = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    
    # 3. Response Length Analysis
    fig3 = go.Figure()
    for model in df['model'].unique():
        model_data = df[df['model'] == model]
        fig3.add_trace(go.Box(
            y=model_data['response_length'],
            name=model.title(),
            boxpoints='outliers'
        ))
    fig3.update_layout(
        title="📏 Response Length Distribution by Model",
        xaxis_title="Model",
        yaxis_title="Response Length (words)",
        template="plotly_white"
    )
    charts['response_length'] = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    
    # 4. Success Rate by Task
    task_perf = df.groupby(['task', 'model'])['success'].mean().reset_index()
    fig4 = go.Figure()
    for model in df['model'].unique():
        model_data = task_perf[task_perf['model'] == model]
        fig4.add_trace(go.Bar(
            x=model_data['task'],
            y=model_data['success'],
            name=model.title()
        ))
    fig4.update_layout(
        title="✅ Success Rate by Task Type",
        xaxis_title="Task Type",
        yaxis_title="Success Rate",
        yaxis=dict(tickformat='.0%'),
        template="plotly_white",
        barmode='group'
    )
    charts['task_success'] = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    
    return charts

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
