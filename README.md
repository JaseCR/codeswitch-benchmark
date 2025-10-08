# Code-Switching Benchmark

A comprehensive research project for analyzing how different language models (Gemini, Mistral, and Cohere) handle code-switching in multilingual contexts, featuring both Jupyter notebook analysis and a beautiful web application.

🌐 **[Try the Live Demo](#)** (Deploy instructions below)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## Project Overview

This repository contains tools and analysis for evaluating the performance of various language models on code-switching tasks. Code-switching refers to the practice of alternating between two or more languages or language varieties in conversation or writing.

**Now deployable to the cloud!** Share this benchmark tool with anyone via a public URL.

## 🌟 Features

- **Interactive Web Application**: Beautiful, functional website for real-time testing
- **Multi-Model Support**: Gemini, Mistral, and Cohere integration
- **Language Variety Testing**: AAVE, Spanglish, British English, and Standard English
- **Real-time Visualizations**: Interactive charts and analysis
- **Jupyter Notebook Analysis**: Comprehensive data collection and EDA
- **Cloud Deployment Ready**: Deploy to Render, Railway, or Heroku with one click
- **User-Friendly Explanations**: Comprehensive tooltips and guides for all metrics

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

## 🌐 Deployment

Want to make this accessible to everyone? Deploy it to the cloud!

See the **[Deployment Guide](DEPLOYMENT.md)** for detailed instructions on deploying to:
- **Render** (Recommended - Free tier available)
- **Railway** (Free tier available)
- **Heroku** (Requires paid plan)

### Quick Deploy to Render

1. Push this repo to your GitHub
2. Go to [Render.com](https://render.com/) and connect your repo
3. Render will auto-deploy using `render.yaml`
4. Share your live URL with the world! 🚀

## 📝 API Keys

When using the live website, users need to provide their own API keys:
- [Gemini API Key](https://makersuite.google.com/app/apikey) - Free tier available
- [Mistral API Key](https://console.mistral.ai/) - Free tier available
- [Cohere API Key](https://dashboard.cohere.ai/) - Free tier available

API keys are never stored on the server and are only used for the current session.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - Feel free to use this project for research and education purposes.
