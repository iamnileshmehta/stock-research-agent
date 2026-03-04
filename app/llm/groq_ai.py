import os
from groq import Groq, GroqError
from app.llm.base import BaseLLM

class GroqLLM(BaseLLM):
    def __init__(self, model: str = "llama-3.3-70b-versatile"):
        # Safely fetch API key to avoid KeyError if missing
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set.")
            
        self.client = Groq(api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> str:
        try:
            # Groq uses the 'messages' parameter (list of dicts), not 'contents'
            chat_completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7, # Added for more natural responses
                max_tokens=1024  # Optional safety cap
            )
            return chat_completion.choices[0].message.content
            
        except GroqError as e:
            # Log or handle specific API errors (rate limits, timeouts, etc.)
            print(f"Groq API Error: {e}")
            return f"Error generating response: {str(e)}"
