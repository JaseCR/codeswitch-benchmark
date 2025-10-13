import os
from dotenv import load_dotenv
load_dotenv()  # load .env if running standalone

try:
    import cohere
    _COHERE_KEY = os.getenv("COHERE_API_KEY")
    _client = cohere.Client(_COHERE_KEY) if _COHERE_KEY else None
except ImportError:
    _client = None
    _COHERE_KEY = None

def query_cohere(prompt: str, model: str = "command-r-plus-08-2024", temperature: float = 0.3, max_tokens: int = 200) -> str:
    """
    Return ONE sentence paraphrase/continuation in the SAME style. No lists or explanations.
    """
    if not _client:
        return "Cohere API client not available. Please check your API key."
    
    try:
        # Use the new Chat API
        resp = _client.chat(
            model=model,
            message=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stop_sequences=["\n\n"]
        )
        return resp.text.strip()
    except Exception as e:
        # Fallback to other models if command-r-plus-08-2024 fails
        if model == "command-r-plus-08-2024":
            try:
                resp = _client.chat(
                    model="command-r-08-2024",
                    message=prompt,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    stop_sequences=["\n\n"]
                )
                return resp.text.strip()
            except Exception as inner_e:
                print(f"Retry failed: {inner_e}")
                pass
        raise e