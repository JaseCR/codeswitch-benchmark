#!/usr/bin/env python3
"""
Add visual diversity to the EDA notebook while keeping it simple and accurate
"""

import json
from pathlib import Path

# Read the current notebook
notebook_path = Path("notebooks/03_eda.ipynb")
with open(notebook_path, 'r') as f:
    notebook = json.load(f)

# Add diverse visualization cells
new_cells = [
    {
        "cell_type": "markdown",
        "id": "viz_diversity",
        "metadata": {},
        "source": [
            "## Additional Visualizations\n",
            "\n",
            "Different chart types to explore the data from multiple angles."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "id": "pie_charts",
        "metadata": {},
        "outputs": [],
        "source": [
            "# Pie charts for distribution\n",
            "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))\n",
            "\n",
            "# Stimuli distribution by variety\n",
            "variety_counts = stimuli['variety'].value_counts()\n",
            "ax1.pie(variety_counts.values, labels=variety_counts.index, autopct='%1.1f%%', startangle=90)\n",
            "ax1.set_title('Stimuli Distribution by Variety')\n",
            "\n",
            "# Task distribution\n",
            "task_counts = stimuli['task'].value_counts()\n",
            "ax2.pie(task_counts.values, labels=task_counts.index, autopct='%1.1f%%', startangle=90)\n",
            "ax2.set_title('Stimuli Distribution by Task')\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "id": "scatter_plot",
        "metadata": {},
        "outputs": [],
        "source": [
            "# Scatter plot: Success rate vs Response length\n",
            "plt.figure(figsize=(10, 6))\n",
            "\n",
            "for model, df in responses.items():\n",
            "    if 'success' in df.columns and 'output_text' in df.columns:\n",
            "        # Calculate word count\n",
            "        df['word_count'] = df['output_text'].apply(lambda x: len(str(x).split()) if pd.notna(x) else 0)\n",
            "        \n",
            "        # Plot success rate vs average word count\n",
            "        success_rate = df['success'].mean() * 100\n",
            "        avg_words = df['word_count'].mean()\n",
            "        \n",
            "        plt.scatter(avg_words, success_rate, s=100, label=model.title(), alpha=0.7)\n",
            "        plt.annotate(model.title(), (avg_words, success_rate), \n",
            "                    xytext=(5, 5), textcoords='offset points')\n",
            "\n",
            "plt.xlabel('Average Response Length (words)')\n",
            "plt.ylabel('Success Rate (%)')\n",
            "plt.title('Model Performance: Success Rate vs Response Length')\n",
            "plt.grid(True, alpha=0.3)\n",
            "plt.legend()\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "id": "box_plots",
        "metadata": {},
        "outputs": [],
        "source": [
            "# Box plots for response length distribution\n",
            "plt.figure(figsize=(10, 6))\n",
            "\n",
            "length_data = []\n",
            "model_labels = []\n",
            "\n",
            "for model, df in responses.items():\n",
            "    if 'output_text' in df.columns:\n",
            "        df['word_count'] = df['output_text'].apply(lambda x: len(str(x).split()) if pd.notna(x) else 0)\n",
            "        length_data.append(df['word_count'].values)\n",
            "        model_labels.append(model.title())\n",
            "\n",
            "if length_data:\n",
            "    plt.boxplot(length_data, labels=model_labels)\n",
            "    plt.title('Response Length Distribution by Model')\n",
            "    plt.ylabel('Words per Response')\n",
            "    plt.xlabel('Model')\n",
            "    plt.grid(True, alpha=0.3)\n",
            "    plt.show()"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "id": "heatmap",
        "metadata": {},
        "outputs": [],
        "source": [
            "# Heatmap for model-variety performance\n",
            "if variety_performance:\n",
            "    df_heatmap = pd.DataFrame(variety_performance)\n",
            "    \n",
            "    plt.figure(figsize=(8, 6))\n",
            "    plt.imshow(df_heatmap.values, cmap='RdYlGn', aspect='auto', vmin=0, vmax=100)\n",
            "    \n",
            "    # Add colorbar\n",
            "    cbar = plt.colorbar()\n",
            "    cbar.set_label('Success Rate (%)')\n",
            "    \n",
            "    # Set labels\n",
            "    plt.xticks(range(len(df_heatmap.columns)), df_heatmap.columns)\n",
            "    plt.yticks(range(len(df_heatmap.index)), df_heatmap.index)\n",
            "    \n",
            "    # Add text annotations\n",
            "    for i in range(len(df_heatmap.index)):\n",
            "        for j in range(len(df_heatmap.columns)):\n",
            "            plt.text(j, i, f'{df_heatmap.iloc[i, j]:.1f}', \n",
            "                    ha='center', va='center', fontweight='bold')\n",
            "    \n",
            "    plt.title('Model Performance Heatmap by Language Variety')\n",
            "    plt.xlabel('Model')\n",
            "    plt.ylabel('Language Variety')\n",
            "    plt.tight_layout()\n",
            "    plt.show()"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "id": "line_plot",
        "metadata": {},
        "outputs": [],
        "source": [
            "# Line plot showing performance trends\n",
            "if variety_performance and task_performance:\n",
            "    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))\n",
            "    \n",
            "    # Variety performance lines\n",
            "    df_variety = pd.DataFrame(variety_performance)\n",
            "    for model in df_variety.columns:\n",
            "        ax1.plot(df_variety.index, df_variety[model], marker='o', label=model.title(), linewidth=2)\n",
            "    \n",
            "    ax1.set_title('Success Rate by Language Variety')\n",
            "    ax1.set_xlabel('Language Variety')\n",
            "    ax1.set_ylabel('Success Rate (%)')\n",
            "    ax1.legend()\n",
            "    ax1.grid(True, alpha=0.3)\n",
            "    ax1.tick_params(axis='x', rotation=45)\n",
            "    \n",
            "    # Task performance lines\n",
            "    df_task = pd.DataFrame(task_performance)\n",
            "    for model in df_task.columns:\n",
            "        ax2.plot(df_task.index, df_task[model], marker='s', label=model.title(), linewidth=2)\n",
            "    \n",
            "    ax2.set_title('Success Rate by Task Type')\n",
            "    ax2.set_xlabel('Task Type')\n",
            "    ax2.set_ylabel('Success Rate (%)')\n",
            "    ax2.legend()\n",
            "    ax2.grid(True, alpha=0.3)\n",
            "    ax2.tick_params(axis='x', rotation=45)\n",
            "    \n",
            "    plt.tight_layout()\n",
            "    plt.show()"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "id": "stacked_bar",
        "metadata": {},
        "outputs": [],
        "source": [
            "# Stacked bar chart for success/failure breakdown\n",
            "plt.figure(figsize=(10, 6))\n",
            "\n",
            "models = []\n",
            "success_counts = []\n",
            "failure_counts = []\n",
            "\n",
            "for model, df in responses.items():\n",
            "    if 'success' in df.columns:\n",
            "        models.append(model.title())\n",
            "        success_count = df['success'].sum()\n",
            "        failure_count = len(df) - success_count\n",
            "        success_counts.append(success_count)\n",
            "        failure_counts.append(failure_count)\n",
            "\n",
            "if models:\n",
            "    x = range(len(models))\n",
            "    plt.bar(x, success_counts, label='Successful', color='green', alpha=0.7)\n",
            "    plt.bar(x, failure_counts, bottom=success_counts, label='Failed', color='red', alpha=0.7)\n",
            "    \n",
            "    plt.xlabel('Model')\n",
            "    plt.ylabel('Number of Responses')\n",
            "    plt.title('Response Success/Failure Breakdown by Model')\n",
            "    plt.xticks(x, models)\n",
            "    plt.legend()\n",
            "    plt.grid(True, alpha=0.3)\n",
            "    plt.show()"
        ]
    }
]

# Insert the new cells before the summary
summary_index = len(notebook['cells']) - 1
for i, cell in enumerate(new_cells):
    notebook['cells'].insert(summary_index + i, cell)

# Save the enhanced notebook
with open(notebook_path, 'w') as f:
    json.dump(notebook, f, indent=1)

print("Added diverse visualizations to EDA notebook")
