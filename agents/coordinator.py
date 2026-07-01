import pandas as pd
from security.data_guard import DataPrivacyGuard
from agents.profiler import DataProfilerAgent
from agents.planner import WorkflowPlannerAgent
from agents.executor import DataScientistAgent
from agents.communicator import AnalystCommunicatorAgent
from mcp_server.code_sandbox import sandbox_globals, execute_python

class AutoDataAnalyst:
    def __init__(self):
        self.profiler = DataProfilerAgent()
        self.planner = WorkflowPlannerAgent()
        self.executor = DataScientistAgent()
        self.communicator = AnalystCommunicatorAgent()

    def process_data(self, df: pd.DataFrame, user_goal: str):
        yield "System", "Redacting PII and extracting safe metadata..."
        redacted_df = DataPrivacyGuard.redact_dataframe(df)
        metadata = DataPrivacyGuard.extract_safe_metadata(redacted_df)
        
        # Load the dataframe into the sandbox globals for MCP to execute against
        sandbox_globals['df'] = redacted_df

        yield "Data Profiler", "Profiling data metadata..."
        profile_report = self.profiler.profile(metadata)
        yield "Profile Report", profile_report

        yield "Workflow Planner", "Planning workflow..."
        plan = self.planner.plan(profile_report, user_goal)
        yield "Workflow Plan", plan.model_dump_json(indent=2)

        yield "Data Scientist", "Generating Python Code..."
        
        max_retries = 3
        previous_code = None
        error_message = None
        execution_result = ""
        final_code = ""

        for attempt in range(max_retries):
            code_response = self.executor.generate_code(profile_report, plan.model_dump_json(), previous_code, error_message)
            final_code = code_response.python_code
            
            yield f"Generated Code (Attempt {attempt + 1})", final_code
            yield "Sandbox", f"Executing code (Attempt {attempt + 1})..."
            
            execution_result = execute_python(final_code)
            
            if "Errors:\n" in execution_result:
                yield f"Execution Error (Attempt {attempt + 1})", execution_result
                previous_code = final_code
                error_message = execution_result
                continue # Retry
            else:
                yield "Execution Success", execution_result
                break

        yield "Communicator", "Communicating results..."
        final_answer = self.communicator.communicate(user_goal, execution_result)
        yield "Final Answer", final_answer

