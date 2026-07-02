# Auto Data Analyst 2.0 🚀

A highly autonomous, multi-model AI Data Analyst agent that completely automates data profiling, workflow planning, multi-table joining, code execution, and interactive visualizations. Built as an ultimate showcase for the **AI Agents: Intensive Vibe Coding Capstone Project**.

## 🌟 Key Features (2.0 Upgrades)

- **Multi-Model Factory (New!)**: Seamlessly switch between **OpenAI**, **Anthropic**, **DeepSeek**, and **Google Gemini** by simply changing an environment variable. Features robust JSON extraction and native OpenAI Structured Outputs to entirely eliminate LLM JSON hallucinations.
- **Multi-Table & Multi-Format (New!)**: Simultaneously upload `CSV`, `Excel`, and `JSON` files. The agent will automatically infer schemas and execute complex cross-table operations (e.g., merging an orders CSV with a customers Excel file).
- **Advanced Visualizations (New!)**: Intelligently renders appropriate high-level charts such as **Seaborn Correlation Heatmaps** for high-dimensional data, **WordClouds** for NLP text reviews, and dynamic time-series plots.
- **Autonomous Reflexion (Self-Correcting)**: If the generated Python code throws an error during execution, the agent catches the traceback, debugs itself, and retries the code automatically.
- **Data Privacy Guard (PII Guard)**: Automatically redacts sensitive columns (names, emails, IPs) before sending any metadata to the cloud LLMs, ensuring enterprise-grade data security.
- **Secure Code Sandbox**: Executes all generated Python code inside an isolated, local Model Context Protocol (MCP) server.

## 📦 Test Datasets Included
This repository includes a suite of advanced datasets in the `data/` folder for demonstrating the agent's capabilities:
1. `ecommerce_reviews.csv`: Perfect for testing WordCloud generation on text data.
2. `housing_features.csv`: High-dimensional dataset for testing Correlation Heatmaps.
3. `stock_timeseries.csv`: For testing time-series patching and resampling.
4. `orders.csv` & `customers.xlsx`: For testing cross-format Multi-Table JOIN capabilities.

## 🛠️ Setup & Installation

1. Clone this repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
4. Edit `.env` and choose your preferred AI provider (gemini, openai, anthropic, deepseek) and paste the respective API key.

## 🚀 Usage

Run the Streamlit application:
```bash
streamlit run app.py
```
Upload one or multiple datasets (hold `Ctrl`/`Cmd` to select multiple files), input your business goal (e.g., *"Merge orders and customers by ID and plot the total sales by region"*), and let the AI Data Analyst do the rest!

## 🏗️ Architecture
- `agents/`: Contains the Multi-Model Base Agent and specialized agents (Profiler, Planner, Executor, Communicator).
- `mcp_server/`: Contains the `FastMCP` code interpreter server for sandbox execution.
- `security/`: Contains the PII redaction layer.
