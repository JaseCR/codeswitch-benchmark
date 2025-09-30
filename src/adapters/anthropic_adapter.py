# Anthropic Claude API Adapter
# Wrapper for calling Anthropic Claude models to analyze code-switching behavior

import anthropic
from typing import List, Dict, Any, Optional
import time

class AnthropicAdapter:
    """Adapter for Anthropic Claude models with configurable parameters"""
    
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022", 
                 temperature: float = 0.7, max_tokens: int = 1000,
                 top_p: float = 1.0, top_k: int = None):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        
        # Generation configuration
        self.generation_config = {
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "top_k": top_k
        }
    
    def generate_response(self, prompt: str) -> str:
        """Generate response from Claude model"""
        try:
            response = self.client.messages.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                **self.generation_config
            )
            return response.content[0].text
        except Exception as e:
            print(f"Error generating response: {e}")
            return None
    
    def generate_with_system_prompt(self, system_prompt: str, user_prompt: str) -> str:
        """Generate response with system and user prompts"""
        try:
            response = self.client.messages.create(
                model=self.model,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ],
                **self.generation_config
            )
            return response.content[0].text
        except Exception as e:
            print(f"Error generating response: {e}")
            return None
    
    def generate_multiple_candidates(self, prompt: str, num_candidates: int = 3) -> List[str]:
        """Generate multiple response candidates by making multiple calls"""
        candidates = []
        for i in range(num_candidates):
            try:
                response = self.client.messages.create(
                    model=self.model,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    **self.generation_config
                )
                candidates.append(response.content[0].text)
            except Exception as e:
                print(f"Error generating candidate {i+1}: {e}")
                candidates.append(None)
        
        return [c for c in candidates if c is not None]
    
    def update_config(self, **kwargs):
        """Update generation configuration parameters"""
        for key, value in kwargs.items():
            if key in self.generation_config:
                self.generation_config[key] = value
    
    def get_available_models(self) -> List[str]:
        """Get list of available Anthropic models"""
        # Anthropic doesn't have a public models list API, so we return known models
        return [
            "claude-3-5-sonnet-20241022",  # Latest and most capable
            "claude-3-5-haiku-20241022",   # Fast and efficient
            "claude-3-opus-20240229",      # Most capable of Claude 3
            "claude-3-sonnet-20240229",    # Balanced performance
            "claude-3-haiku-20240307"      # Fastest
        ]
    
    def generate_with_retry(self, prompt: str, max_retries: int = 3, delay: float = 1.0) -> str:
        """Generate response with automatic retry on failure"""
        for attempt in range(max_retries):
            try:
                response = self.client.messages.create(
                    model=self.model,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    **self.generation_config
                )
                return response.content[0].text
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(delay * (2 ** attempt))  # Exponential backoff
                else:
                    print(f"All {max_retries} attempts failed")
                    return None
    
    def generate_streaming(self, prompt: str):
        """Generate streaming response from Claude model"""
        try:
            with self.client.messages.stream(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                **self.generation_config
            ) as stream:
                for text in stream.text_stream:
                    yield text
        except Exception as e:
            print(f"Error in streaming response: {e}")
            yield None