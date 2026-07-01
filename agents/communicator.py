from .base import BaseAgent

class AnalystCommunicatorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            system_instruction="You are a Data Analyst Communicator. You will receive the output of executed Python analysis code. Your job is to translate this raw output into a clear, business-friendly summary and answer any user questions."
        )

    def communicate(self, user_query: str, execution_result: str) -> str:
        prompt = f"User Query: {user_query}\n\nExecution Result (from python code):\n{execution_result}\n\nPlease summarize the findings and answer the user."
        return self.generate(prompt)
