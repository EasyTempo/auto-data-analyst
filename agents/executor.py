from .base import BaseAgent
from pydantic import BaseModel

class CodeResponse(BaseModel):
    thoughts: str
    python_code: str

class DataScientistAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            system_instruction="You are a Data Scientist writing Python code to analyze a pandas DataFrame named `df` (which is already loaded in memory). Write pandas code to achieve the given plan. Always print() any metrics or results so they can be captured. If you create any plots, ALWAYS save them to the 'static_plots' directory (e.g., plt.savefig('static_plots/plot_1.png')). DO NOT use plt.show(). Print the filepath of any saved plots so the UI can display them."
        )


    def generate_code(self, profile: str, plan: str, previous_code: str = None, error_message: str = None) -> CodeResponse:
        prompt = f"Data Profile:\n{profile}\n\nAnalysis Plan:\n{plan}\n\nWrite python code using pandas to execute this plan. The dataframe is available as 'df'."
        if previous_code and error_message:
            prompt += f"\n\nPREVIOUS CODE FAILED:\n```python\n{previous_code}\n```\nERROR:\n{error_message}\n\nPlease fix the error and provide the corrected code."
        return self.generate(prompt, response_schema=CodeResponse)
