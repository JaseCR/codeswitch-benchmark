# Batch Processing Script
# Script to run models in bulk and collect responses for code-switching analysis

import argparse
import pandas as pd
import os
import openai
from typing import List, Dict
from pathlib import Path
from tqdm import tqdm
from dotenv import load_dotenv

# Import adapters
from adapters.openai_adapter import OpenAIAdapter
from adapters.gemini_adapter import GeminiAdapter
from adapters.anthropic_adapter import AnthropicAdapter
from adapters.cohere_adapter import CohereAdapter

# Load environment variables
load_dotenv()

def initialize_adapter(model_name: str):
    """Initialize the appropriate adapter based on model name"""
    api_key = None
    
    if model_name == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        # Try different models based on quota availability
        models_to_try = ["gpt-3.5-turbo", "gpt-4o-mini", "gpt-4o"]
        
        for model in models_to_try:
            try:
                # Test if model works
                test_client = openai.OpenAI(api_key=api_key)
                test_client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=1
                )
                print(f"✅ Using {model} for OpenAI")
                return OpenAIAdapter(api_key=api_key, model=model, temperature=0.5, max_tokens=500)
            except Exception as e:
                print(f"❌ {model} failed: {e}")
                continue
        
        raise Exception("No working OpenAI models found. Check your quota and billing.")
    elif model_name == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        return GeminiAdapter(api_key=api_key, model="gemini-2.5-flash", temperature=0.5, max_tokens=500)
    elif model_name == "anthropic":
        api_key = os.getenv("ANTHROPIC_API_KEY")
        return AnthropicAdapter(api_key=api_key, model="claude-3-5-sonnet-20241022", temperature=0.5, max_tokens=500)
    elif model_name == "cohere":
        api_key = os.getenv("COHERE_API_KEY")
        return CohereAdapter(api_key=api_key, model="command", temperature=0.5, max_tokens=500)
    else:
        raise ValueError(f"Unknown model: {model_name}")

def run_batch_experiment(stimuli_file: str, output_dir: str, models: List[str]) -> None:
    """
    Run batch experiment across multiple models.
    
    Args:
        stimuli_file: Path to stimuli CSV file
        output_dir: Directory to save results
        models: List of model names to test
    """
    # Load stimuli data
    stimuli_df = pd.read_csv(stimuli_file)
    print(f"Loaded {len(stimuli_df)} stimuli from {stimuli_file}")
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Process each model
    for model_name in models:
        print(f"\n=== Processing {model_name.upper()} ===")
        
        try:
            # Initialize adapter
            adapter = initialize_adapter(model_name)
            
            # Process stimuli
            responses = []
            for i, row in tqdm(stimuli_df.iterrows(), total=len(stimuli_df), desc=f"Processing {model_name}"):
                # Create task-specific prompt
                if row.task == "paraphrase":
                    prompt = f"Paraphrase this text in the same dialectal style: {row.text}"
                elif row.task == "explain":
                    prompt = f"Explain this text in simple terms while preserving the dialectal style: {row.text}"
                elif row.task == "continue":
                    prompt = f"Continue this text in the same dialectal style: {row.text}"
                else:
                    prompt = f"Process this text while maintaining the dialectal style: {row.text}"
                
                # Generate response
                output = adapter.generate_response(prompt)
                
                responses.append({
                    "id": row.id,
                    "variety": row.variety,
                    "task": row.task,
                    "input_text": row.text,
                    "output_text": output,
                    "model": model_name
                })
            
            # Save results
            results_df = pd.DataFrame(responses)
            output_file = os.path.join(output_dir, f"{model_name}_responses.csv")
            results_df.to_csv(output_file, index=False)
            print(f"✅ Saved {len(responses)} responses to {output_file}")
            
        except Exception as e:
            print(f"❌ Error processing {model_name}: {e}")
            continue
    
    print(f"\n🎉 Batch experiment completed! Results saved to {output_dir}")

def main():
    """Main function for command-line execution"""
    parser = argparse.ArgumentParser(description="Run code-switching batch experiment")
    parser.add_argument("--stimuli", default="../data/raw/stimuli.csv", help="Path to stimuli CSV file")
    parser.add_argument("--output", default="../data/raw", help="Output directory")
    parser.add_argument("--models", nargs="+", default=["openai", "gemini"],
                       help="Models to test")
    
    args = parser.parse_args()
    run_batch_experiment(args.stimuli, args.output, args.models)

if __name__ == "__main__":
    main()