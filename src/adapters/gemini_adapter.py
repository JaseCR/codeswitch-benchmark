# Google Gemini API Adapter
# Wrapper for calling Google Gemini models to analyze code-switching behavior

import google.generativeai as genai
from typing import List, Dict, Any, Optional

class GeminiAdapter:
    """Adapter for Google Gemini models with configurable parameters"""
    
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash", 
                 temperature: float = 0.7, max_tokens: int = 2048,
                 top_p: float = 0.8, top_k: int = 40):
        genai.configure(api_key=api_key)
        
        # Generation configuration
        self.generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            max_output_tokens=max_tokens,
            candidate_count=1
        )
        
        # Safety settings for code-switching research
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_ONLY_HIGH"  # More permissive for research
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH", 
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
        
        self.model = genai.GenerativeModel(
            model_name=model,
            generation_config=self.generation_config,
            safety_settings=self.safety_settings
        )
    
    def generate_response(self, prompt: str) -> str:
        """Generate response from Gemini model"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating response: {e}")
            return None
    
    def generate_multiple_candidates(self, prompt: str, num_candidates: int = 3) -> List[str]:
        """Generate multiple response candidates"""
        # Temporarily update candidate count
        original_count = self.generation_config.candidate_count
        self.generation_config.candidate_count = num_candidates
        
        try:
            response = self.model.generate_content(prompt)
            candidates = [candidate.text for candidate in response.candidates]
            return candidates
        except Exception as e:
            print(f"Error generating candidates: {e}")
            return []
        finally:
            # Restore original candidate count
            self.generation_config.candidate_count = original_count
    
    def update_config(self, **kwargs):
        """Update generation configuration parameters"""
        for key, value in kwargs.items():
            if hasattr(self.generation_config, key):
                setattr(self.generation_config, key, value)
        
        # Recreate model with new config
        self.model = genai.GenerativeModel(
            model_name=self.model.model_name,
            generation_config=self.generation_config,
            safety_settings=self.safety_settings
        )