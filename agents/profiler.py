from .base import BaseAgent

class DataProfilerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            system_instruction="You are an expert Data Profiler. Your job is to analyze data metadata (columns, types, basic stats) and identify potential issues like missing values, skewness, or format inconsistencies. Output a concise textual summary."
        )

    def profile(self, metadata: str) -> str:
        prompt = f"Analyze the following data metadata and provide a profiling report:\n\n{metadata}"
        return self.generate(prompt)
