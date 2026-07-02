from .base import BaseAgent
from pydantic import BaseModel

class CodeResponse(BaseModel):
    thoughts: str
    python_code: str

class DataScientistAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            system_instruction="You are a Data Scientist writing Python code to analyze a dictionary of pandas DataFrames named `dfs` (already loaded in memory, keyed by filename). Write python code to achieve the given plan. Always print() any metrics or results so they can be captured. For time-series use datetime, for text use wordcloud, for high-dimensional use seaborn correlation heatmaps. If you create any plots, ALWAYS save them to the 'static_plots' directory (e.g., plt.savefig('static_plots/plot_1.png')). DO NOT use plt.show(). Print the filepath of any saved plots so the UI can display them. CRITICAL: You MUST output ONLY valid JSON. DO NOT output any conversational text or markdown."
        )


    def generate_code(self, profile: str, plan: str, previous_code: str = None, error_message: str = None) -> CodeResponse:
        prompt = f"Data Profile:\n{profile}\n\nAnalysis Plan:\n{plan}\n\nWrite python code to execute this plan. The datasets are available in the dictionary `dfs`, keyed by their filenames."
        if previous_code and error_message:
            prompt += f"\n\nPREVIOUS CODE FAILED:\n```python\n{previous_code}\n```\nERROR:\n{error_message}\n\nPlease fix the error and provide the corrected code."
        return self.generate(prompt, response_schema=CodeResponse)
