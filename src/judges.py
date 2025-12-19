import os
import json
import google.generativeai as genai
from abc import ABC, abstractmethod
from dotenv import load_dotenv

# Load environment variables (API Keys)
load_dotenv()


class BaseJudge(ABC):
    """
    Abstract Interface for any AI Judge (Gemini, OpenAI, Llama, etc.)
    """

    @abstractmethod
    def evaluate(self, prompt):
        pass


class GeminiJudge(BaseJudge):
    def __init__(self, model_name="gemini-2.5-flash", temperature=0.1):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("❌ GEMINI_API_KEY not found in .env file!")

        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config={
                "response_mime_type": "application/json",
                "temperature": temperature,
            },
        )

    def evaluate(self, prompt):
        """
        Sends the prompt to Google Gemini and parses the JSON response.
        """
        try:
            response = self.model.generate_content(prompt)

            # Gemini usually returns a clean JSON string because we requested 'application/json'
            response_text = response.text

            # Parse string to JSON object
            try:
                result_json = json.loads(response_text)
                return result_json
            except json.JSONDecodeError:
                # Fallback if model returns Markdown ticks like ```json ... ```
                cleaned_text = (
                    response_text.replace("```json", "").replace("```", "").strip()
                )
                return json.loads(cleaned_text)

        except Exception as e:
            print(f"⚠️ Error calling Gemini: {e}")
            return {"score": 0, "reasoning": f"System Error: {str(e)}"}


# Factory function to pick the right judge
def get_judge(config):
    provider = config.get("judge_provider", "google").lower()

    if provider == "google":
        return GeminiJudge(
            model_name=config.get("judge_model", "gemini-2.5-flash"),
            temperature=config.get("temperature", 0.1),
        )
    elif provider == "openai":
        # Placeholder for future OpenAI implementation
        raise NotImplementedError("OpenAI Judge not implemented yet.")
    else:
        raise ValueError(f"Unknown provider: {provider}")
