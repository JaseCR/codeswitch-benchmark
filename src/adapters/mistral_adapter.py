import os
from mistralai import Mistral
from dotenv import load_dotenv
load_dotenv()  # load .env if running standalone

_MISTRAL_KEY = os.getenv("MISTRAL_API_KEY")
_client = Mistral(api_key=_MISTRAL_KEY)

def query_mistral(prompt: str, model: str = "mistral-large-latest", temperature: float = 0.3, max_tokens: int = 200) -> str:
    """
    Return ONE sentence paraphrase/continuation in the SAME style. No lists or explanations.
    """
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
            except:
                pass
        raise e
