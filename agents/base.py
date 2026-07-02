import os
from google import genai
from pydantic import BaseModel
from typing import TypeVar, Type, Optional

T = TypeVar("T", bound=BaseModel)

class BaseAgent:
    def __init__(self, system_instruction: str = ""):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your_api_key_here":
            # Fallback to default if not set, or throw error.
            # In a real app we'd want strict checking.
            pass
            
        self.client = genai.Client(api_key=api_key)
        self.system_instruction = system_instruction
        self.model = "gemini-2.5-flash" # Use flash model to avoid free tier quota issues

    def generate(self, prompt: str, response_schema: Optional[Type[T]] = None) -> str | T:
        """
        Calls the LLM. If response_schema is provided, returns parsed Pydantic object.
        """
        config = {"system_instruction": self.system_instruction}
        
        if response_schema:
            config["response_mime_type"] = "application/json"
            config["response_schema"] = response_schema
            
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=config,
        )
        
        if response_schema:
            import re
            text = response.text.strip()
            # Extract only the JSON block to prevent parsing errors from conversational text
            match = re.search(r'(\{.*\}|\[.*\])', text, re.DOTALL)
            if match:
                text = match.group(1)
            return response_schema.model_validate_json(text)
        return response.text
