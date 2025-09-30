# Code-Switch Benchmark

A data science project for analyzing how different GPT models (OpenAI, Gemini, Claude, and Cohere) handle code-switching in multilingual contexts.

## Project Overview

This repository contains tools and analysis for evaluating the performance of various language models on code-switching tasks. Code-switching refers to the practice of alternating between two or more languages or language varieties in conversation or writing.

## Repository Structure

```
codeswitch-benchmark/
│
├── data/
│   ├── raw/                # Raw stimuli CSVs and model responses
│   └── processed/          # Cleaned or scored data (scores.csv, etc.)
│
├── notebooks/
│   ├── 01_collect_data.ipynb     # Calls APIs and gathers model outputs
│   ├── 02_clean_and_score.ipynb  # Computes metrics (marker retention, etc.)
│   └── 03_eda.ipynb              # Visualizations and comparisons
│
├── src/
│   ├── adapters/                 # API call wrappers for each model
│   │   ├── openai_adapter.py
│   │   ├── gemini_adapter.py
│   │   ├── anthropic_adapter.py
│   │   └── cohere_adapter.py
│   ├── metrics.py                # Metric functions (tokenization, similarity, etc.)
│   ├── utils.py                  # Helper functions
│   └── run_batch.py              # Script to call models in bulk
│
├── .gitignore                    # Ignore venv, env, and large data
├── requirements.txt              # Python dependencies
├── .env.example                  # Template for API keys
└── README.md                     # This file
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

[Add your license information here]