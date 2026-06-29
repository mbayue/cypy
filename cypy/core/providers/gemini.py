from cypy.core.providers.base import LLMProvider

try:
    from google import genai
    from google.genai import types
except Exception:
    genai = None
    types = None


class GeminiProvider(LLMProvider):
    """
    Google Gemini provider using the google-genai SDK.
    Extracted from the original utils.py implementation~ ♪
    """

    @property
    def provider_name(self):
        return "Google Gemini"

    def translate_image(self, image, prompt):
        if genai is None:
            raise ImportError(
                "google-genai package is not installed. "
                "Install it with: pip install google-genai"
            )

        client = genai.Client(api_key=self.api_key)

        # Try with full config first, fallback if library version doesn't support it~
        if types is not None:
            try:
                response = client.models.generate_content(
                    model=self.model_name,
                    contents=[image, prompt],
                    config=types.GenerateContentConfig(
                        temperature=0,
                        top_p=0.1,
                        top_k=1,
                        response_mime_type="application/json"
                    )
                )
                return response.text
            except Exception as e:
                self._check_api_key_error(e)

                # Retry without response_mime_type
                try:
                    response = client.models.generate_content(
                        model=self.model_name,
                        contents=[image, prompt],
                        config=types.GenerateContentConfig(
                            temperature=0,
                            top_p=0.1,
                            top_k=1
                        )
                    )
                    return response.text
                except Exception as e2:
                    self._check_api_key_error(e2)

        # Final fallback without types
        try:
            response = client.models.generate_content(
                model=self.model_name,
                contents=[image, prompt],
                config={
                    "temperature": 0,
                    "top_p": 0.1,
                    "top_k": 1,
                    "response_mime_type": "application/json"
                }
            )
            return response.text
        except Exception as e:
            self._check_api_key_error(e)

            try:
                response = client.models.generate_content(
                    model=self.model_name,
                    contents=[image, prompt]
                )
                return response.text
            except Exception as final_err:
                self._check_api_key_error(final_err)
                raise final_err

    @staticmethod
    def _check_api_key_error(err):
        """Check if an error is related to API key issues and raise ValueError if so."""
        err_str = str(err).lower()
        if any(keyword in err_str for keyword in [
            "api key expired", "api_key_invalid", "api key", "api_key"
        ]):
            raise ValueError("API_KEY_ERROR")
