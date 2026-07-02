import os
import re
from pydantic import BaseModel
from typing import TypeVar, Type, Optional

T = TypeVar("T", bound=BaseModel)

class BaseAgent:
    def __init__(self, system_instruction: str = ""):
        self.provider = os.getenv("LLM_PROVIDER", "gemini").lower()
        self.system_instruction = system_instruction
        
        if self.provider == "openai":
            from openai import OpenAI
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = os.getenv("MODEL_NAME", "gpt-4o-mini")
        elif self.provider == "anthropic":
            from anthropic import Anthropic
            self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            self.model = os.getenv("MODEL_NAME", "claude-3-5-sonnet-20241022")
        else:
            from google import genai
            self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
            self.model = os.getenv("MODEL_NAME", "gemini-2.5-flash")

    def generate(self, prompt: str, response_schema: Optional[Type[T]] = None) -> str | T:
        """Calls the configured LLM provider and parses output if response_schema is given."""
        if self.provider == "openai":
            return self._generate_openai(prompt, response_schema)
        elif self.provider == "anthropic":
            return self._generate_anthropic(prompt, response_schema)
        else:
            return self._generate_gemini(prompt, response_schema)

    def _generate_openai(self, prompt: str, response_schema: Optional[Type[T]]) -> str | T:
        messages = [
            {"role": "system", "content": self.system_instruction},
            {"role": "user", "content": prompt}
        ]
        if response_schema:
            # OpenAI's Structured Outputs
            response = self.client.beta.chat.completions.parse(
                model=self.model,
                messages=messages,
                response_format=response_schema
            )
            return response.choices[0].message.parsed
        else:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return response.choices[0].message.content

    def _generate_anthropic(self, prompt: str, response_schema: Optional[Type[T]]) -> str | T:
        messages = [{"role": "user", "content": prompt}]
        # Anthropic doesn't have native pydantic parsing yet, so we instruct it to output JSON
        sys_prompt = self.system_instruction
        if response_schema:
            sys_prompt += "\nCRITICAL: Output ONLY valid JSON matching the requested schema."
            
        response = self.client.messages.create(
            model=self.model,
            system=sys_prompt,
            messages=messages,
            max_tokens=4096
        )
        text = response.content[0].text
        
        if response_schema:
            text = text.strip()
            match = re.search(r'(\{.*\}|\[.*\])', text, re.DOTALL)
            if match:
                text = match.group(1)
            return response_schema.model_validate_json(text)
        return text

    def _generate_gemini(self, prompt: str, response_schema: Optional[Type[T]]) -> str | T:
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
            text = response.text.strip()
            match = re.search(r'(\{.*\}|\[.*\])', text, re.DOTALL)
            if match:
                text = match.group(1)
            return response_schema.model_validate_json(text)
        return response.text
