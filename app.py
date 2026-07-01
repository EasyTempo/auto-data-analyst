import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

from agents.coordinator import AutoDataAnalyst

st.set_page_config(page_title="Auto Data Analyst", page_icon="📊", layout="wide")

st.title("📊 Auto Data Analyst Agent")
st.markdown("Upload a CSV file and tell me what you want to analyze!")

# API Key check
if not os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY") == "your_api_key_here":
    st.warning("Please set your GEMINI_API_KEY in the `.env` file to use the agent.")

uploaded_files = st.file_uploader("Choose Data Files (CSV, Excel, JSON)", type=["csv", "xlsx", "xls", "json"], accept_multiple_files=True)
user_goal = st.text_input("What is your analysis goal? (e.g. 'Merge the tables, clean the data and show me a summary of sales')")

if st.button("Run Analysis"):
    if uploaded_files and user_goal:
        try:
            dfs = {}
            st.write("### Data Preview")
            for f in uploaded_files:
                if f.name.endswith('.csv'):
                    df = pd.read_csv(f)
                elif f.name.endswith('.json'):
                    df = pd.read_json(f)
                else:
                    df = pd.read_excel(f)
                dfs[f.name] = df
                with st.expander(f"Preview of `{f.name}`", expanded=False):
                    st.dataframe(df.head())
            
            # Clear static plots
            if os.path.exists("static_plots"):
                for f in os.listdir("static_plots"):
                    os.remove(os.path.join("static_plots", f))
            
            # Run the agent pipeline
            st.write("### Agent Working Process")
            analyst = AutoDataAnalyst()
            
            final_conclusion = ""
            for step_name, content in analyst.process_data(dfs, user_goal):
                with st.expander(f"🔄 {step_name}", expanded=False):
                    if "Code" in step_name and "Attempt" in step_name:
                        st.code(content, language="python")
                    elif "Error" in step_name:
                        st.error(content)
                    elif "Plan" in step_name:
                        try:
                            st.json(content)
                        except:
                            st.write(content)
                    else:
                        st.write(content)
                if step_name == "Final Answer":
                    final_conclusion = content
                
            st.success("Analysis Complete!")
            st.write("### Analyst Conclusion")
            st.write(final_conclusion)
            
            # Show any plots generated
            if os.path.exists("static_plots") and os.listdir("static_plots"):
                st.write("### Generated Visualizations")
                for img_file in os.listdir("static_plots"):
                    if img_file.endswith(".png") or img_file.endswith(".jpg"):
                        st.image(os.path.join("static_plots", img_file))
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please upload a file and specify a goal.")
