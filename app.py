import streamlit as st
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Page Config
st.set_page_config(
    page_title="InsightAI",
    page_icon="📈",
    layout="wide"
)

# Title
st.title("📈 InsightAI - AI Business Intelligence Assistant")

st.markdown("""
Upload your business dataset and let Google Gemini generate:

✅ Executive Summary  
✅ Business Insights  
✅ KPI Analysis  
✅ Risk Detection  
✅ Actionable Recommendations  
""")

st.subheader("Powered by Google Gemini AI")

# File Upload
uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    # Read CSV
    df = pd.read_csv(uploaded_file)

    # Display Data
    st.write("## Uploaded Data")
    st.dataframe(df)

    # KPI Cards
    if 'Sales' in df.columns and 'Profit' in df.columns:

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Total Sales",
                f"{df['Sales'].sum():,}"
            )

        with col2:
            st.metric(
                "Total Profit",
                f"{df['Profit'].sum():,}"
            )

        # Charts
        if 'Month' in df.columns:

            st.write("## Sales Trend")
            st.line_chart(
                df.set_index("Month")["Sales"]
            )

            st.write("## Profit Trend")
            st.bar_chart(
                df.set_index("Month")["Profit"]
            )

    # Dataset Summary
    summary = df.describe(include='all').to_string()

    # AI Button
    if st.button("🚀 Generate AI Insights"):

        model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

        prompt = f"""
You are a Senior Analyst.

Analyze this dataset and provide:

1. Executive Summary
2. Key Trends
3. Business Insights
4. Risks
5. Recommendations

Dataset:

{summary}
"""

        with st.spinner("Generating AI Insights..."):
            response = model.generate_content(prompt)

        st.success("AI Insights Generated Successfully!")

        st.write("## AI Insights")
        st.markdown(response.text)