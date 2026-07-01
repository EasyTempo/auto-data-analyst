# Auto Data Analyst Agent

A General Data Analysis Expert Agent that automates data profiling, cleaning, workflow planning, and interactive analysis. This project is built for the **AI Agents: Intensive Vibe Coding Capstone Project**.

## Features
- **Multi-agent System**: Utilizes 4 specialized agents (Profiler, Planner, Executor, Communicator) working together.
- **Code Execution Sandbox**: Securely runs generated Python analysis code in an isolated Model Context Protocol (MCP) server.
- **Data Privacy Guard**: Automatically redacts PII (Personally Identifiable Information) before metadata reaches the LLM.
- **Interactive UI**: Built with Streamlit for a great user experience and immediate visualizations.

## Requirements
- Python 3.10+
- A valid Gemini API Key

## Setup
1. Clone this repository.
2. Run `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and insert your API key:
   ```bash
   cp .env.example .env
   # Edit .env with your GEMINI_API_KEY
   ```

## Usage
Run the Streamlit application:
```bash
streamlit run app.py
```
Upload a CSV (you can test with `data/sample_messy_data.csv`) and provide a goal.

## Architecture
- `agents/`: Contains the LLM wrappers using `google-genai` and `pydantic`.
- `mcp_server/`: Contains the `FastMCP` code interpreter server.
- `security/`: Contains the PII redaction layer.
