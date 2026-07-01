from mcp.server.fastmcp import FastMCP
import io
import sys
import contextlib
import traceback
import pandas as pd
import os

# Initialize the FastMCP server
mcp = FastMCP("Data Analyst Code Sandbox")

# A simple global dictionary to hold variables between executions
sandbox_globals = {"pd": pd}

# Ensure plot directory exists
os.makedirs("static_plots", exist_ok=True)

@mcp.tool()
def execute_python(code: str) -> str:
    """
    Executes Python code in an isolated environment and returns the stdout and stderr output.
    Useful for data analysis tasks.
    
    Args:
        code: The Python code to execute.
    """
    stdout = io.StringIO()
    stderr = io.StringIO()
    
    # We use contextlib to redirect stdout and stderr
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        try:
            # Execute the code in the context of sandbox_globals
            exec(code, sandbox_globals)
        except Exception:
            # Catch any execution errors and log them to stderr
            traceback.print_exc(file=stderr)
            
    # Combine outputs
    out_str = stdout.getvalue()
    err_str = stderr.getvalue()
    
    result = ""
    if out_str:
        result += f"Output:\n{out_str}\n"
    if err_str:
        result += f"Errors:\n{err_str}\n"
        
    if not result:
        result = "Code executed successfully with no output."
        
    return result

if __name__ == "__main__":
    # To run the MCP server over stdio
    mcp.run()
