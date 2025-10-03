# Code-Switching Benchmark Web Application

A beautiful, functional website for testing language model code-switching capabilities across different linguistic varieties.

## 🌟 Features

- **Interactive Testing Interface**: Test models with your own API keys
- **Real-time Visualizations**: Beautiful charts and analysis generated on-the-fly
- **Multi-Model Support**: Gemini, Mistral, and Cohere integration
- **Language Variety Testing**: AAVE, Spanglish, British English, and Standard English
- **Responsive Design**: Works perfectly on desktop and mobile
- **Colorful UI**: Modern, gradient-based design with smooth animations

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements_web.txt
```

### 2. Run the Application
```bash
python app.py
```

### 3. Open in Browser
Navigate to `http://localhost:5001`

## 🎯 How It Works

### Testing Process
1. **Enter API Keys**: Provide your API keys for Gemini, Mistral, and/or Cohere
2. **Run Tests**: The system tests each model with carefully crafted code-switching prompts
3. **View Results**: Get detailed visualizations showing how well models preserve dialectal markers

### Test Cases
- **4 Language Varieties**: AAVE, Spanglish, BrEng, StdEng
- **3 Task Types**: Paraphrase, Continue, Explain
- **12 Total Tests**: Comprehensive coverage across all combinations

### Evaluation Metrics
- **Marker Retention Rate**: Percentage of dialectal markers preserved
- **Response Quality**: Length and coherence analysis
- **Success Rate**: Successful API responses
- **Variety Consistency**: Performance across linguistic varieties

## 🎨 Visualizations

The application generates beautiful, interactive visualizations including:

- **Model Performance Comparison**: Bar charts showing retention rates
- **Language Variety Heatmaps**: Color-coded difficulty analysis
- **Response Length Analysis**: Box plots and distributions
- **Task Success Rates**: Grouped bar charts by task type
- **Dialectal Consistency**: Marker retention analysis

## 🔧 API Integration

### Supported Models
- **Gemini**: Google's advanced language model
- **Mistral**: High-performance open-source model
- **Cohere**: Enterprise-grade language AI

### API Key Setup
1. **Gemini**: Get your key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Mistral**: Get your key from [Mistral Console](https://console.mistral.ai/)
3. **Cohere**: Get your key from [Cohere Dashboard](https://dashboard.cohere.ai/)

## 🎨 Design Features

- **Gradient Backgrounds**: Beautiful color transitions
- **Smooth Animations**: Hover effects and transitions
- **Responsive Cards**: Adaptive layouts for all screen sizes
- **Interactive Charts**: Plotly-powered visualizations
- **Modern Typography**: Inter font family for readability
- **Color-Coded Varieties**: Distinct colors for each language variety

## 📱 Responsive Design

The application is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones
- All modern browsers

## 🔒 Security

- API keys are handled securely and not stored
- All requests are made client-side to your specified APIs
- No data is permanently stored on the server

## 🛠️ Technical Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Visualizations**: Plotly.js
- **Styling**: Bootstrap 5 + Custom CSS
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Inter)

## 📊 Sample Results

The application provides comprehensive analysis including:
- Overall performance metrics
- Model-specific comparisons
- Language variety difficulty rankings
- Task-specific success rates
- Detailed response analysis

## 🎯 Use Cases

- **Researchers**: Study language model behavior across dialects
- **Developers**: Test model capabilities for multilingual applications
- **Educators**: Demonstrate code-switching concepts
- **Linguists**: Analyze dialectal preservation in AI systems

## 🚀 Getting Started

1. Clone the repository
2. Install dependencies: `pip install -r requirements_web.txt`
3. Run the application: `python app.py`
4. Open `http://localhost:5001` in your browser
5. Enter your API keys and start testing!

## 📝 License

This project is part of the Code-Switching Benchmark research initiative.

---

**Built with ❤️ for linguistic diversity and AI fairness research.**
