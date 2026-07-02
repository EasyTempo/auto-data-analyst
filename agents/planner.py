from .base import BaseAgent
from pydantic import BaseModel
from typing import List

class AnalysisStep(BaseModel):
    step_number: int
    description: str
    target_columns: List[str]

class WorkflowPlan(BaseModel):
    goal: str
    steps: List[AnalysisStep]
    expected_outcome: str

class WorkflowPlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            system_instruction="You are a Lead Data Scientist. Given a data profile of one or multiple datasets and a user goal, you design a step-by-step workflow for data cleaning, analysis, and visualization. If multiple tables are provided, consider merging them. Include steps to generate plots like wordclouds, time-series line charts, or correlation heatmaps if appropriate. CRITICAL: You MUST output ONLY valid JSON. DO NOT output any conversational text, markdown formatting, or prefixes like 'Planning workflow...'."
        )

    def plan(self, profile: str, user_goal: str) -> WorkflowPlan:
        prompt = f"Data Profile:\n{profile}\n\nUser Goal: {user_goal}\n\nCreate a detailed step-by-step data analysis plan."
        return self.generate(prompt, response_schema=WorkflowPlan)
