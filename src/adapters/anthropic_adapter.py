import os, anthropic
from dotenv import load_dotenv
load_dotenv()  # load .env if running standalone

_ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
_client = anthropic.Anthropic(api_key=_ANTHROPIC_KEY)

def query_claude(prompt: str, model: str = "claude-3-5-sonnet-20241022", temperature: float = 0.3, max_tokens: int = 200) -> str:
    """
    Return ONE sentence paraphrase/continuation in the SAME style. No lists or explanations.
    """
    resp = _client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}]
    )
    # Concatenate only text parts
    return "".join(p.text for p in resp.content if getattr(p, "type", "") == "text")


# Alias for consistency with other adapters
def query_anthropic(prompt: str, model: str = "claude-3-5-sonnet-20241022", temperature: float = 0.3, max_tokens: int = 200) -> str:
    """
    Alias for query_claude for consistency with other adapter functions
    """
    return query_claude(prompt, model, temperature, max_tokens)