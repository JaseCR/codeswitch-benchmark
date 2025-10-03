"""
Analysis Cells Agent
Adds detailed analysis cells with proper visualizations to the EDA notebook
"""

import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent

class AnalysisCellsAgent:
    """Agent that adds detailed analysis cells to the EDA notebook"""
    
    def __init__(self):
        self.name = "AnalysisCellsAgent"
        
    def add_detailed_analysis_cells(self):
        """Add detailed analysis cells to the EDA notebook"""
        print(f"📊 {self.name}: Adding detailed analysis cells...")
        
        notebook_path = project_root / "notebooks" / "03_eda.ipynb"
        
        # Read the existing notebook
        with open(notebook_path, 'r') as f:
            notebook = json.load(f)
        
        # Create detailed analysis cells
        analysis_cells = [
            self._create_data_overview_analysis(),
            self._create_success_rate_analysis(),
            self._create_variety_performance_analysis(),
            self._create_task_difficulty_analysis(),
            self._create_response_quality_analysis(),
            self._create_dialectal_consistency_analysis(),
            self._create_comprehensive_summary()
        ]
        
        # Insert analysis cells after the setup cell
        setup_index = 1  # After title and setup
        for i, cell in enumerate(analysis_cells):
            notebook["cells"].insert(setup_index + i, cell)
        
        # Save the updated notebook
        with open(notebook_path, 'w') as f:
            json.dump(notebook, f, indent=1)
            
        print(f"  ✅ Added {len(analysis_cells)} detailed analysis cells")
        return True
        
    def _create_data_overview_analysis(self):
        """Create data overview analysis cell"""
        return {
            "cell_type": "code",
            "execution_count": None,
            "id": "data_overview_analysis",
            "metadata": {},
            "outputs": [],
            "source": [
                "# Data Overview Analysis\n",
                "\n",
                "# Display basic dataset information\n",
                "print(\"📊 Dataset Overview\")\n",
                "print(\"=\" * 50)\n",
                "print(f\"Total stimuli examples: {len(stimuli)}\")\n",
                "print(f\"Language varieties: {list(stimuli['variety'].unique())}\")\n",
                "print(f\"Task types: {list(stimuli['task'].unique())}\")\n",
                "print(f\"Models with responses: {list(responses.keys())}\")\n",
                "\n",
                "# Display stimuli distribution\n",
                "print(\"\\n📋 Stimuli Distribution:\")\n",
                "variety_counts = stimuli['variety'].value_counts()\n",
                "task_counts = stimuli['task'].value_counts()\n",
                "\n",
                "print(\"\\nBy Language Variety:\")\n",
                "for variety, count in variety_counts.items():\n",
                "    print(f\"  {variety}: {count} examples\")\n",
                "\n",
                "print(\"\\nBy Task Type:\")\n",
                "for task, count in task_counts.items():\n",
                "    print(f\"  {task.title()}: {count} examples\")\n",
                "\n",
                "# Create distribution visualizations\n",
                "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))\n",
                "\n",
                "# Variety distribution pie chart\n",
                "colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']\n",
                "wedges, texts, autotexts = ax1.pie(variety_counts.values, labels=variety_counts.index, \n",
                "                                   autopct='%1.1f%%', colors=colors, startangle=90)\n",
                "ax1.set_title('Distribution by Language Variety', fontsize=14, fontweight='bold')\n",
                "\n",
                "# Task distribution bar chart\n",
                "bars = ax2.bar(task_counts.index, task_counts.values, color=['#1f77b4', '#ff7f0e', '#2ca02c'])\n",
                "ax2.set_title('Distribution by Task Type', fontsize=14, fontweight='bold')\n",
                "ax2.set_xlabel('Task Type')\n",
                "ax2.set_ylabel('Number of Examples')\n",
                "\n",
                "# Add value labels on bars\n",
                "for bar, count in zip(bars, task_counts.values):\n",
                "    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, \n",
                "            str(count), ha='center', va='bottom', fontweight='bold')\n",
                "\n",
                "plt.tight_layout()\n",
                "plt.show()\n",
                "\n",
                "# Display response data summary\n",
                "print(\"\\n📈 Response Data Summary:\")\n",
                "for model, df in responses.items():\n",
                "    if 'success' in df.columns:\n",
                "        success_count = df['success'].sum()\n",
                "        success_rate = (success_count / len(df)) * 100\n",
                "        print(f\"  {model.title()}: {len(df)} responses, {success_count} successful ({success_rate:.1f}%)\")\n",
                "    else:\n",
                "        print(f\"  {model.title()}: {len(df)} responses (no success data)\")"
            ]
        }
        
    def _create_success_rate_analysis(self):
        """Create success rate analysis cell"""
        return {
            "cell_type": "code",
            "execution_count": None,
            "id": "success_rate_analysis",
            "metadata": {},
            "outputs": [],
            "source": [
                "# Question 1: Model Performance Comparison - Success Rates\n",
                "\n",
                "# Calculate success rates by model\n",
                "success_rates = {}\n",
                "for model, df in responses.items():\n",
                "    if 'success' in df.columns:\n",
                "        success_rate = df['success'].mean() * 100\n",
                "        success_rates[model] = success_rate\n",
                "        print(f\"{model.title()}: {success_rate:.1f}% success rate\")\n",
                "\n",
                "# Create success rate visualization\n",
                "if success_rates:\n",
                "    plt.figure(figsize=(10, 6))\n",
                "    models = list(success_rates.keys())\n",
                "    rates = list(success_rates.values())\n",
                "    \n",
                "    bars = plt.bar(models, rates, color=['#1f77b4', '#ff7f0e', '#2ca02c'])\n",
                "    plt.title('Model Success Rates', fontsize=16, fontweight='bold')\n",
                "    plt.xlabel('Model', fontsize=12)\n",
                "    plt.ylabel('Success Rate (%)', fontsize=12)\n",
                "    plt.ylim(0, 100)\n",
                "    \n",
                "    # Add value labels on bars\n",
                "    for bar, rate in zip(bars, rates):\n",
                "        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, \n",
                "                f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')\n",
                "    \n",
                "    plt.grid(axis='y', alpha=0.3)\n",
                "    plt.tight_layout()\n",
                "    plt.show()\n",
                "\n",
                "    # Summary statistics\n",
                "print(f\"\\n📊 Success Rate Summary:\")\n",
                "print(f\"Best performing model: {max(success_rates, key=success_rates.get)} ({max(success_rates.values()):.1f}%)\")\n",
                "print(f\"Worst performing model: {min(success_rates, key=success_rates.get)} ({min(success_rates.values()):.1f}%)\")\n",
                "print(f\"Average success rate: {np.mean(list(success_rates.values())):.1f}%\")\n",
                "\n",
                "# Performance gap analysis\n",
                "max_rate = max(success_rates.values())\n",
                "min_rate = min(success_rates.values())\n",
                "gap = max_rate - min_rate\n",
                "print(f\"Performance gap: {gap:.1f} percentage points\")"
            ]
        }
        
    def _create_variety_performance_analysis(self):
        """Create variety performance analysis cell"""
        return {
            "cell_type": "code",
            "execution_count": None,
            "id": "variety_performance_analysis",
            "metadata": {},
            "outputs": [],
            "source": [
                "# Question 2: Language Variety Analysis\n",
                "\n",
                "# Calculate success rates by variety for each model\n",
                "variety_performance = {}\n",
                "\n",
                "for model, df in responses.items():\n",
                "    if 'success' in df.columns and 'variety' in df.columns:\n",
                "        variety_success = df.groupby('variety')['success'].mean() * 100\n",
                "        variety_performance[model] = variety_success\n",
                "\n",
                "# Create variety performance heatmap\n",
                "if variety_performance:\n",
                "    # Prepare data for heatmap\n",
                "    heatmap_data = pd.DataFrame(variety_performance).fillna(0)\n",
                "    \n",
                "    plt.figure(figsize=(10, 8))\n",
                "    sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='RdYlGn', \n",
                "                vmin=0, vmax=100, cbar_kws={'label': 'Success Rate (%)'})\n",
                "    plt.title('Model Performance by Language Variety', fontsize=16, fontweight='bold')\n",
                "    plt.xlabel('Model', fontsize=12)\n",
                "    plt.ylabel('Language Variety', fontsize=12)\n",
                "    plt.tight_layout()\n",
                "    plt.show()\n",
                "\n",
                "    # Create variety difficulty ranking\n",
                "    variety_avg = heatmap_data.mean(axis=1).sort_values(ascending=True)\n",
                "    \n",
                "    plt.figure(figsize=(10, 6))\n",
                "    bars = plt.barh(variety_avg.index, variety_avg.values, \n",
                "                   color=['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4'])\n",
                "    plt.title('Language Variety Difficulty Ranking\\n(Lower = More Difficult)', \n",
                "              fontsize=16, fontweight='bold')\n",
                "    plt.xlabel('Average Success Rate (%)', fontsize=12)\n",
                "    plt.ylabel('Language Variety', fontsize=12)\n",
                "    \n",
                "    # Add value labels\n",
                "    for bar, value in zip(bars, variety_avg.values):\n",
                "        plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, \n",
                "                f'{value:.1f}%', ha='left', va='center', fontweight='bold')\n",
                "    \n",
                "    plt.grid(axis='x', alpha=0.3)\n",
                "    plt.tight_layout()\n",
                "    plt.show()\n",
                "\n",
                "    print(f\"\\n📊 Variety Difficulty Ranking (Hardest to Easiest):\")\n",
                "    for i, (variety, rate) in enumerate(variety_avg.items(), 1):\n",
                "        print(f\"{i}. {variety}: {rate:.1f}% average success\")\n",
                "\n",
                "    # Model-specific variety performance\n",
                "    print(f\"\\n📊 Model Performance by Variety:\")\n",
                "    for model in heatmap_data.columns:\n",
                "        print(f\"\\n{model.title()}:\")\n",
                "        model_performance = heatmap_data[model].sort_values(ascending=False)\n",
                "        for variety, rate in model_performance.items():\n",
                "            print(f\"  {variety}: {rate:.1f}%\")"
            ]
        }
        
    def _create_task_difficulty_analysis(self):
        """Create task difficulty analysis cell"""
        return {
            "cell_type": "code",
            "execution_count": None,
            "id": "task_difficulty_analysis",
            "metadata": {},
            "outputs": [],
            "source": [
                "# Question 3: Task Difficulty Assessment\n",
                "\n",
                "# Calculate success rates by task for each model\n",
                "task_performance = {}\n",
                "\n",
                "for model, df in responses.items():\n",
                "    if 'success' in df.columns and 'task' in df.columns:\n",
                "        task_success = df.groupby('task')['success'].mean() * 100\n",
                "        task_performance[model] = task_success\n",
                "\n",
                "# Create task performance visualization\n",
                "if task_performance:\n",
                "    # Prepare data for grouped bar chart\n",
                "    task_df = pd.DataFrame(task_performance).fillna(0)\n",
                "    \n",
                "    plt.figure(figsize=(12, 8))\n",
                "    x = np.arange(len(task_df.index))\n",
                "    width = 0.25\n",
                "    \n",
                "    for i, model in enumerate(task_df.columns):\n",
                "        plt.bar(x + i*width, task_df[model], width, label=model.title(), alpha=0.8)\n",
                "    \n",
                "    plt.title('Model Performance by Task Type', fontsize=16, fontweight='bold')\n",
                "    plt.xlabel('Task Type', fontsize=12)\n",
                "    plt.ylabel('Success Rate (%)', fontsize=12)\n",
                "    plt.xticks(x + width, task_df.index, rotation=45)\n",
                "    plt.legend()\n",
                "    plt.ylim(0, 100)\n",
                "    plt.grid(axis='y', alpha=0.3)\n",
                "    plt.tight_layout()\n",
                "    plt.show()\n",
                "\n",
                "    # Task difficulty ranking\n",
                "    task_avg = task_df.mean(axis=1).sort_values(ascending=True)\n",
                "    \n",
                "    plt.figure(figsize=(10, 6))\n",
                "    bars = plt.barh(task_avg.index, task_avg.values, \n",
                "                   color=['#d62728', '#ff7f0e', '#2ca02c'])\n",
                "    plt.title('Task Difficulty Ranking\\n(Lower = More Difficult)', \n",
                "              fontsize=16, fontweight='bold')\n",
                "    plt.xlabel('Average Success Rate (%)', fontsize=12)\n",
                "    plt.ylabel('Task Type', fontsize=12)\n",
                "    \n",
                "    # Add value labels\n",
                "    for bar, value in zip(bars, task_avg.values):\n",
                "        plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, \n",
                "                f'{value:.1f}%', ha='left', va='center', fontweight='bold')\n",
                "    \n",
                "    plt.grid(axis='x', alpha=0.3)\n",
                "    plt.tight_layout()\n",
                "    plt.show()\n",
                "\n",
                "    print(f\"\\n📊 Task Difficulty Ranking (Hardest to Easiest):\")\n",
                "    for i, (task, rate) in enumerate(task_avg.items(), 1):\n",
                "        print(f\"{i}. {task.title()}: {rate:.1f}% average success\")\n",
                "\n",
                "    # Model-specific task performance\n",
                "    print(f\"\\n📊 Model Performance by Task:\")\n",
                "    for model in task_df.columns:\n",
                "        print(f\"\\n{model.title()}:\")\n",
                "        model_performance = task_df[model].sort_values(ascending=False)\n",
                "        for task, rate in model_performance.items():\n",
                "            print(f\"  {task.title()}: {rate:.1f}%\")"
            ]
        }
        
    def _create_response_quality_analysis(self):
        """Create response quality analysis cell"""
        return {
            "cell_type": "code",
            "execution_count": None,
            "id": "response_quality_analysis",
            "metadata": {},
            "outputs": [],
            "source": [
                "# Question 4: Response Quality Analysis\n",
                "\n",
                "# Calculate response length metrics\n",
                "response_metrics = {}\n",
                "\n",
                "for model, df in responses.items():\n",
                "    if 'output_text' in df.columns:\n",
                "        # Calculate response lengths (word count)\n",
                "        df['response_length'] = df['output_text'].apply(lambda x: len(str(x).split()) if pd.notna(x) else 0)\n",
                "        \n",
                "        # Calculate input lengths for comparison\n",
                "        df['input_length'] = df['input_text'].apply(lambda x: len(str(x).split()) if pd.notna(x) else 0)\n",
                "        \n",
                "        # Calculate length ratio\n",
                "        df['length_ratio'] = df['response_length'] / df['input_length'].replace(0, 1)\n",
                "        \n",
                "        response_metrics[model] = {\n",
                "            'avg_response_length': df['response_length'].mean(),\n",
                "            'avg_length_ratio': df['length_ratio'].mean(),\n",
                "            'response_length_std': df['response_length'].std()\n",
                "        }\n",
                "\n",
                "# Create response length comparison\n",
                "if response_metrics:\n",
                "    models = list(response_metrics.keys())\n",
                "    avg_lengths = [response_metrics[model]['avg_response_length'] for model in models]\n",
                "    \n",
                "    plt.figure(figsize=(10, 6))\n",
                "    bars = plt.bar(models, avg_lengths, color=['#1f77b4', '#ff7f0e', '#2ca02c'])\n",
                "    plt.title('Average Response Length by Model', fontsize=16, fontweight='bold')\n",
                "    plt.xlabel('Model', fontsize=12)\n",
                "    plt.ylabel('Average Words per Response', fontsize=12)\n",
                "    \n",
                "    # Add value labels\n",
                "    for bar, length in zip(bars, avg_lengths):\n",
                "        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, \n",
                "                f'{length:.1f}', ha='center', va='bottom', fontweight='bold')\n",
                "    \n",
                "    plt.grid(axis='y', alpha=0.3)\n",
                "    plt.tight_layout()\n",
                "    plt.show()\n",
                "\n",
                "    # Create length ratio analysis\n",
                "    length_ratios = [response_metrics[model]['avg_length_ratio'] for model in models]\n",
                "    \n",
                "    plt.figure(figsize=(10, 6))\n",
                "    bars = plt.bar(models, length_ratios, color=['#1f77b4', '#ff7f0e', '#2ca02c'])\n",
                "    plt.title('Response Length Ratio by Model\\n(Response Length / Input Length)', \n",
                "              fontsize=16, fontweight='bold')\n",
                "    plt.xlabel('Model', fontsize=12)\n",
                "    plt.ylabel('Length Ratio', fontsize=12)\n",
                "    plt.axhline(y=1, color='red', linestyle='--', alpha=0.7, label='1:1 Ratio')\n",
                "    \n",
                "    # Add value labels\n",
                "    for bar, ratio in zip(bars, length_ratios):\n",
                "        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, \n",
                "                f'{ratio:.2f}', ha='center', va='bottom', fontweight='bold')\n",
                "    \n",
                "    plt.legend()\n",
                "    plt.grid(axis='y', alpha=0.3)\n",
                "    plt.tight_layout()\n",
                "    plt.show()\n",
                "\n",
                "    print(f\"\\n📊 Response Quality Summary:\")\n",
                "    for model in models:\n",
                "        metrics = response_metrics[model]\n",
                "        print(f\"{model.title()}:\")\n",
                "        print(f\"  Average response length: {metrics['avg_response_length']:.1f} words\")\n",
                "        print(f\"  Length ratio: {metrics['avg_length_ratio']:.2f}\")\n",
                "        print(f\"  Length variability: {metrics['response_length_std']:.1f} words\")\n",
                "\n",
                "    # Response length distribution\n",
                "    plt.figure(figsize=(12, 8))\n",
                "    for i, (model, df) in enumerate(responses.items()):\n",
                "        if 'response_length' in df.columns:\n",
                "            plt.subplot(2, 2, i+1)\n",
                "            plt.hist(df['response_length'], bins=10, alpha=0.7, color=['#1f77b4', '#ff7f0e', '#2ca02c'][i])\n",
                "            plt.title(f'{model.title()} Response Length Distribution')\n",
                "            plt.xlabel('Words per Response')\n",
                "            plt.ylabel('Frequency')\n",
                "            plt.grid(alpha=0.3)\n",
                "    \n",
                "    plt.tight_layout()\n",
                "    plt.show()"
            ]
        }
        
    def _create_dialectal_consistency_analysis(self):
        """Create dialectal consistency analysis cell"""
        return {
            "cell_type": "code",
            "execution_count": None,
            "id": "dialectal_consistency_analysis",
            "metadata": {},
            "outputs": [],
            "source": [
                "# Question 5: Code-Switching Behavior Analysis\n",
                "\n",
                "# Analyze dialectal consistency by variety\n",
                "variety_consistency = {}\n",
                "\n",
                "for model, df in responses.items():\n",
                "    if 'variety' in df.columns and 'success' in df.columns:\n",
                "        # Calculate success rate by variety (as proxy for dialectal consistency)\n",
                "        variety_success = df.groupby('variety')['success'].mean()\n",
                "        variety_consistency[model] = variety_success\n",
                "\n",
                "# Create dialectal consistency visualization\n",
                "if variety_consistency:\n",
                "    # Prepare data for grouped analysis\n",
                "    consistency_df = pd.DataFrame(variety_consistency).fillna(0)\n",
                "    \n",
                "    plt.figure(figsize=(12, 8))\n",
                "    x = np.arange(len(consistency_df.index))\n",
                "    width = 0.25\n",
                "    \n",
                "    for i, model in enumerate(consistency_df.columns):\n",
                "        plt.bar(x + i*width, consistency_df[model], width, label=model.title(), alpha=0.8)\n",
                "    \n",
                "    plt.title('Dialectal Consistency by Model and Variety\\n(Success Rate as Consistency Proxy)', \n",
                "              fontsize=16, fontweight='bold')\n",
                "    plt.xlabel('Language Variety', fontsize=12)\n",
                "    plt.ylabel('Consistency Score (Success Rate)', fontsize=12)\n",
                "    plt.xticks(x + width, consistency_df.index, rotation=45)\n",
                "    plt.legend()\n",
                "    plt.ylim(0, 1)\n",
                "    plt.grid(axis='y', alpha=0.3)\n",
                "    plt.tight_layout()\n",
                "    plt.show()\n",
                "\n",
                "    # Create consistency ranking\n",
                "    model_consistency = consistency_df.mean(axis=0).sort_values(ascending=False)\n",
                "    \n",
                "    plt.figure(figsize=(10, 6))\n",
                "    bars = plt.bar(model_consistency.index, model_consistency.values, \n",
                "                   color=['#2ca02c', '#ff7f0e', '#1f77b4'])\n",
                "    plt.title('Overall Dialectal Consistency Ranking', fontsize=16, fontweight='bold')\n",
                "    plt.xlabel('Model', fontsize=12)\n",
                "    plt.ylabel('Average Consistency Score', fontsize=12)\n",
                "    \n",
                "    # Add value labels\n",
                "    for bar, value in zip(bars, model_consistency.values):\n",
                "        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, \n",
                "                f'{value:.3f}', ha='center', va='bottom', fontweight='bold')\n",
                "    \n",
                "    plt.grid(axis='y', alpha=0.3)\n",
                "    plt.tight_layout()\n",
                "    plt.show()\n",
                "\n",
                "    print(f\"\\n📊 Dialectal Consistency Ranking:\")\n",
                "    for i, (model, score) in enumerate(model_consistency.items(), 1):\n",
                "        print(f\"{i}. {model.title()}: {score:.3f} average consistency\")\n",
                "\n",
                "    # Variety-specific consistency analysis\n",
                "    print(f\"\\n📊 Consistency by Variety:\")\n",
                "    for variety in consistency_df.index:\n",
                "        variety_scores = consistency_df.loc[variety].sort_values(ascending=False)\n",
                "        print(f\"\\n{variety}:\")\n",
                "        for model, score in variety_scores.items():\n",
                "            print(f\"  {model.title()}: {score:.3f}\")\n",
                "\n",
                "    # Create consistency heatmap\n",
                "    plt.figure(figsize=(10, 8))\n",
                "    sns.heatmap(consistency_df, annot=True, fmt='.3f', cmap='RdYlGn', \n",
                "                vmin=0, vmax=1, cbar_kws={'label': 'Consistency Score'})\n",
                "    plt.title('Dialectal Consistency Heatmap', fontsize=16, fontweight='bold')\n",
                "    plt.xlabel('Model', fontsize=12)\n",
                "    plt.ylabel('Language Variety', fontsize=12)\n",
                "    plt.tight_layout()\n",
                "    plt.show()"
            ]
        }
        
    def _create_comprehensive_summary(self):
        """Create comprehensive summary cell"""
        return {
            "cell_type": "code",
            "execution_count": None,
            "id": "comprehensive_summary",
            "metadata": {},
            "outputs": [],
            "source": [
                "# Comprehensive Analysis Summary\n",
                "\n",
                "print(\"🎯 COMPREHENSIVE ANALYSIS SUMMARY\")\n",
                "print(\"=\" * 60)\n",
                "\n",
                "# Key Findings\n",
                "print(\"\\n📊 KEY FINDINGS:\")\n",
                "\n",
                "# 1. Model Performance\n",
                "if 'success_rates' in locals():\n",
                "    best_model = max(success_rates, key=success_rates.get)\n",
                "    worst_model = min(success_rates, key=success_rates.get)\n",
                "    print(f\"\\n1. MODEL PERFORMANCE:\")\n",
                "    print(f\"   • Best performing model: {best_model.title()} ({success_rates[best_model]:.1f}%)\")\n",
                "    print(f\"   • Worst performing model: {worst_model.title()} ({success_rates[worst_model]:.1f}%)\")\n",
                "    print(f\"   • Performance gap: {success_rates[best_model] - success_rates[worst_model]:.1f} percentage points\")\n",
                "\n",
                "# 2. Language Variety Analysis\n",
                "if 'variety_avg' in locals():\n",
                "    hardest_variety = variety_avg.index[0]\n",
                "    easiest_variety = variety_avg.index[-1]\n",
                "    print(f\"\\n2. LANGUAGE VARIETY ANALYSIS:\")\n",
                "    print(f\"   • Most challenging variety: {hardest_variety} ({variety_avg[hardest_variety]:.1f}%)\")\n",
                "    print(f\"   • Least challenging variety: {easiest_variety} ({variety_avg[easiest_variety]:.1f}%)\")\n",
                "    print(f\"   • Variety difficulty range: {variety_avg.max() - variety_avg.min():.1f} percentage points\")\n",
                "\n",
                "# 3. Task Difficulty\n",
                "if 'task_avg' in locals():\n",
                "    hardest_task = task_avg.index[0]\n",
                "    easiest_task = task_avg.index[-1]\n",
                "    print(f\"\\n3. TASK DIFFICULTY:\")\n",
                "    print(f\"   • Most difficult task: {hardest_task.title()} ({task_avg[hardest_task]:.1f}%)\")\n",
                "    print(f\"   • Easiest task: {easiest_task.title()} ({task_avg[easiest_task]:.1f}%)\")\n",
                "    print(f\"   • Task difficulty range: {task_avg.max() - task_avg.min():.1f} percentage points\")\n",
                "\n",
                "# 4. Response Quality\n",
                "if 'response_metrics' in locals():\n",
                "    print(f\"\\n4. RESPONSE QUALITY:\")\n",
                "    for model, metrics in response_metrics.items():\n",
                "        print(f\"   • {model.title()}: {metrics['avg_response_length']:.1f} words avg, {metrics['avg_length_ratio']:.2f} ratio\")\n",
                "\n",
                "# 5. Dialectal Consistency\n",
                "if 'model_consistency' in locals():\n",
                "    most_consistent = model_consistency.index[0]\n",
                "    least_consistent = model_consistency.index[-1]\n",
                "    print(f\"\\n5. DIALECTAL CONSISTENCY:\")\n",
                "    print(f\"   • Most consistent model: {most_consistent.title()} ({model_consistency[most_consistent]:.3f})\")\n",
                "    print(f\"   • Least consistent model: {least_consistent.title()} ({model_consistency[least_consistent]:.3f})\")\n",
                "\n",
                "# Research Implications\n",
                "print(f\"\\n🔬 RESEARCH IMPLICATIONS:\")\n",
                "print(f\"   • Current LLMs show varying capabilities in handling code-switching\")\n",
                "print(f\"   • Some language varieties are consistently more challenging\")\n",
                "print(f\"   • Task complexity affects model performance significantly\")\n",
                "print(f\"   • Response patterns reveal model-specific behaviors\")\n",
                "print(f\"   • Dialectal consistency varies across models and varieties\")\n",
                "\n",
                "# Recommendations\n",
                "print(f\"\\n💡 RECOMMENDATIONS:\")\n",
                "print(f\"   • Focus on improving performance for challenging varieties\")\n",
                "print(f\"   • Develop specialized training for difficult tasks\")\n",
                "print(f\"   • Consider model-specific optimization strategies\")\n",
                "print(f\"   • Expand dataset to include more diverse examples\")\n",
                "print(f\"   • Implement consistency metrics for evaluation\")\n",
                "\n",
                "print(f\"\\n✅ Analysis complete! This EDA provides comprehensive insights into\")\n",
                "print(f\"   code-switching behavior across different language models and varieties.\")"
            ]
        }
        
    def run_analysis_cells_addition(self):
        """Run the analysis cells addition process"""
        print(f"🚀 {self.name}: Adding detailed analysis cells to EDA notebook...")
        
        if not self.add_detailed_analysis_cells():
            print(f"❌ Failed to add analysis cells")
            return False
            
        print(f"✅ {self.name}: Analysis cells addition completed successfully!")
        return True

def run_analysis_cells():
    """Run the analysis cells addition process"""
    agent = AnalysisCellsAgent()
    return agent.run_analysis_cells_addition()

if __name__ == "__main__":
    run_analysis_cells()
