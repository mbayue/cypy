import io
import base64
import json

from cypy.core.providers.base import LLMProvider

try:
    import requests
except ImportError:
    requests = None


class OpenRouterProvider(LLMProvider):
    """
    OpenRouter provider using the OpenAI-compatible REST API.
    Supports hundreds of models including Claude, Llama, Mistral, Gemini, etc.
    Uses only `requests` — no extra SDK needed~ ♪

    Get your API key at: https://openrouter.ai/keys
    Browse models at: https://openrouter.ai/models
    """

    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    @property
    def provider_name(self):
        return "OpenRouter"

    def translate_image(self, image, prompt):
        if requests is None:
            raise ImportError(
                "requests package is not installed. "
                "Install it with: pip install requests"
            )

        # Convert PIL Image to base64 data URI
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        data_uri = f"data:image/png;base64,{img_base64}"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/indravoyager/cypy",
            "X-Title": "cypy Manga Translator",
        }

        payload = {
            "model": self.model_name,
            "temperature": 0,
            "top_p": 0.1,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": data_uri},
                        },
                        {
                            "type": "text",
                            "text": prompt,
                        },
                    ],
                }
            ],
        }

        response = requests.post(
            self.BASE_URL,
            headers=headers,
            json=payload,
            timeout=120,
        )

        if response.status_code == 401:
            raise ValueError("API_KEY_ERROR")

        if response.status_code == 402:
            raise ValueError("API_KEY_ERROR")

        if response.status_code != 200:
            error_detail = ""
            try:
                error_detail = response.json().get("error", {}).get("message", "")
            except Exception:
                error_detail = response.text[:200]
            raise RuntimeError(
                f"OpenRouter API error {response.status_code}: {error_detail}"
            )

        result = response.json()

        # Extract the text content from OpenAI-compatible response
        try:
            content = result["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            raise RuntimeError(f"Unexpected OpenRouter response format: {e}")

        return content
