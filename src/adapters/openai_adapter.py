# OpenAI API Adapter
# Wrapper for calling OpenAI GPT models to analyze code-switching behavior

import openai
from typing import List, Dict, Any, Optional
import time

class OpenAIAdapter:
    """Adapter for OpenAI GPT models with configurable parameters"""
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini", 
                 temperature: float = 0.7, max_tokens: int = 1000,
                 top_p: float = 1.0, frequency_penalty: float = 0.0,
                 presence_penalty: float = 0.0):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        
        # Generation configuration
        self.generation_config = {
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty
        }
    
    def generate_response(self, prompt: str) -> str:
        """Generate response from OpenAI model"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                **self.generation_config
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating response: {e}")
            return None
    
    def generate_multiple_candidates(self, prompt: str, num_candidates: int = 3) -> List[str]:
        """Generate multiple response candidates"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                n=num_candidates,  # Number of choices to generate
                **self.generation_config
            )
            candidates = [choice.message.content for choice in response.choices]
            return candidates
        except Exception as e:
            print(f"Error generating candidates: {e}")
            return []
    
    def generate_with_system_prompt(self, system_prompt: str, user_prompt: str) -> str:
        """Generate response with system and user prompts"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                **self.generation_config
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating response: {e}")
            return None
    
    def update_config(self, **kwargs):
        """Update generation configuration parameters"""
        for key, value in kwargs.items():
            if key in self.generation_config:
                self.generation_config[key] = value
    
    def get_available_models(self) -> List[str]:
        """Get list of available OpenAI models"""
        try:
            models = self.client.models.list()
            # Filter for chat completion models
            chat_models = [
                model.id for model in models.data 
                if model.id.startswith(('gpt-3.5', 'gpt-4', 'o1'))
            ]
            return sorted(chat_models)
        except Exception as e:
            print(f"Error fetching models: {e}")
            return []
    
    def generate_with_retry(self, prompt: str, max_retries: int = 3, delay: float = 1.0) -> str:
        """Generate response with automatic retry on failure"""
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    **self.generation_config
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(delay * (2 ** attempt))  # Exponential backoff
                else:
                    print(f"All {max_retries} attempts failed")
                    return None