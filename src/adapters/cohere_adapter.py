import os, cohere
from dotenv import load_dotenv
load_dotenv()  # load .env if running standalone

_COHERE_KEY = os.getenv("COHERE_API_KEY")
_client = cohere.Client(_COHERE_KEY)

def query_cohere(prompt: str, model: str = "command-r-plus-08-2024", temperature: float = 0.3, max_tokens: int = 200) -> str:
    """
    Return ONE sentence paraphrase/continuation in the SAME style. No lists or explanations.
    """
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
                print(f"Retry attempt {attempt + 1} failed: {inner_e}")
                pass
        raise e