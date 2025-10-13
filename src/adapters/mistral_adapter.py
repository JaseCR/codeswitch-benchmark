import os
from dotenv import load_dotenv
load_dotenv()  # load .env if running standalone

# Try different import patterns for different mistralai versions
try:
    from mistralai import Mistral
    _MISTRAL_KEY = os.getenv("MISTRAL_API_KEY")
    _client = Mistral(api_key=_MISTRAL_KEY) if _MISTRAL_KEY else None
except (ImportError, AttributeError):
    try:
        from mistralai.client import MistralClient
        _MISTRAL_KEY = os.getenv("MISTRAL_API_KEY")
        _client = MistralClient(api_key=_MISTRAL_KEY) if _MISTRAL_KEY else None
    except ImportError:
        _client = None
        _MISTRAL_KEY = None

def query_mistral(prompt: str, model: str = "mistral-large-latest", temperature: float = 0.3, max_tokens: int = 200) -> str:
    """
    Return ONE sentence paraphrase/continuation in the SAME style. No lists or explanations.
    """
    if not _client:
        return "Mistral API client not available. Please check your API key."
    
    try:
        # Use the Mistral chat completions API
        response = _client.chat.complete(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        # Fallback to other models if mistral-large-latest fails
        if model == "mistral-large-latest":
            try:
                response = _client.chat.complete(
                    model="mistral-medium-latest",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                return response.choices[0].message.content.strip()
            except Exception as inner_e:
                print(f"Retry failed: {inner_e}")
                pass
        raise e
