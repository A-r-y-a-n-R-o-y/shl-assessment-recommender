import os

from google import genai


class LLM:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        self.client = genai.Client(api_key=api_key)

        self.model = "gemini-2.5-flash"

    def generate(self, prompt: str) -> str:
        """
        Generate a response from Gemini.
        """

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        if response.text:
            return response.text.strip()

        return "I couldn't generate a response."