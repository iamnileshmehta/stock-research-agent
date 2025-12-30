import os
from google import genai
from app.llm.base import BaseLLM


class GeminiLLM(BaseLLM):
    def __init__(self, model: str = "gemini-2.5-flash"):
        self.client = genai.Client(
            api_key=os.environ["GOOGLE_API_KEY"]
        )
        self.model = model

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return response.text
