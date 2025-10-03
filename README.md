# Code-Switching Benchmark

A comprehensive research project for analyzing how different language models (Gemini, Mistral, and Cohere) handle code-switching in multilingual contexts, featuring both Jupyter notebook analysis and a beautiful web application.

## Project Overview

This repository contains tools and analysis for evaluating the performance of various language models on code-switching tasks. Code-switching refers to the practice of alternating between two or more languages or language varieties in conversation or writing.

## 🌟 Features

- **Interactive Web Application**: Beautiful, functional website for real-time testing
- **Multi-Model Support**: Gemini, Mistral, and Cohere integration
- **Language Variety Testing**: AAVE, Spanglish, British English, and Standard English
- **Real-time Visualizations**: Interactive charts and analysis
- **Jupyter Notebook Analysis**: Comprehensive data collection and EDA

## Repository Structure

```
codeswitch-benchmark/
│
├── app.py                        # Main Flask web application
├── requirements_web.txt          # Web app dependencies
├── README_WEB.md                # Web app documentation
│
├── data/
│   ├── raw/                     # Raw stimuli CSVs and model responses
│   └── processed/               # Cleaned or scored data
│
├── notebooks/
│   ├── 01_collect.ipynb         # Data collection from APIs
│   ├── 02_clean_and_score.ipynb # Data cleaning and scoring
│   └── 03_eda.ipynb             # Exploratory data analysis
│
├── src/
│   ├── adapters/                # API adapters (Gemini, Mistral, Cohere)
│   │   ├── gemini_adapter.py
│   │   ├── mistral_adapter.py
│   │   └── cohere_adapter.py
│   ├── metrics.py               # Scoring functions
│   ├── run_batch.py             # Batch processing utilities
│   └── utils.py                 # Utility functions
│
├── static/                      # Web app static files
│   ├── css/style.css            # Custom styling
│   └── js/main.js               # Interactive JavaScript
│
├── templates/                   # Web app HTML templates
│   ├── base.html                # Base template
│   ├── index.html               # Dashboard
│   ├── test.html                # Testing interface
│   └── results.html             # Results page
│
├── requirements.txt             # Core dependencies
└── README.md                    # This file
```

## 🚀 Quick Start

### Web Application
```bash
# Install web app dependencies
pip install -r requirements_web.txt

# Run the web application
python app.py

# Open in browser: http://localhost:5001
```

### Jupyter Notebooks
```bash
# Install core dependencies
pip install -r requirements.txt

# Start Jupyter
jupyter notebook
```

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd codeswitch-benchmark
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys**
   ```bash
   cp .env.example .env
   # Edit .env with your actual API keys
   ```

## Usage

### Running Experiments

Use the batch processing script to run experiments across multiple models:

```bash
python src/run_batch.py --stimuli data/raw/stimuli.csv --output data/raw/responses/
```

### Analyzing Results

1. **Data Collection**: Use `01_collect_data.ipynb` to gather model responses
2. **Scoring**: Use `02_clean_and_score.ipynb` to compute metrics
3. **Visualization**: Use `03_eda.ipynb` for exploratory data analysis

## Metrics

The project computes various linguistic metrics including:
- **Marker Retention**: Percentage of linguistic markers preserved in model outputs
- **Semantic Similarity**: Cosine similarity between original and generated text
- **Code-Switching Patterns**: Analysis of language alternation patterns

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

[Add your license information here]# Mistral AI Integration Complete
