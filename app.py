import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai

# Page configuration for a clean, eye-friendly layout
st.set_page_config(page_title="Lamha - AI Agent", page_icon="✨", layout="wide")

# RTL styling helper for Arabic content inside a clean interface
st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    div.stButton > button:first-child { background-color: #4A90E2; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ Lamha Project - Analytics Dashboard & AI Agent")
st.write("Welcome! This is the prototype for Lamha. Please upload your CSV file to test the system.")

# Safely retrieve the API key from deployment secrets
api_key = st.secrets.get("GEMINI_API_KEY", None)

if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ Error: GEMINI_API_KEY not found in Advanced Settings.")

# File uploader widget for the user or your friends to upload their data
uploaded_file = st.file_uploader("Choose your ads data CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV file and display it cleanly
    df = pd.read_csv(uploaded_file)
    
    st.success("✅ File uploaded successfully! Here is a quick look at your data:")
    st.dataframe(df, use_container_width=True)
    
    # Create two tabs: one for automated charts and one for the AI chat agent
    tab1, tab2 = st.tabs(["📊 Automated Visualizations", "🤖 Ask Lamha AI Consultant"])
    
    with tab1:
        st.subheader("Quick Visual Performance Analysis")
        
        # Simple interactive bar chart: Engagement Rate per Ad
        if 'ad_title' in df.columns and 'engagement_rate' in df.columns:
            fig = px.bar(df, x='ad_title', y='engagement_rate', title="Engagement Rate per Ad (%)", 
                         labels={'engagement_rate':'Engagement Rate', 'ad_title':'Ad Title'},
                         color='engagement_rate', color_continuous_scale=px.colors.sequential.Viridis)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Make sure your CSV contains 'ad_title' and 'engagement_rate' columns to display this chart.")

    with tab2:
        st.subheader("💬 Chat with Your Data (AI Agent)")
        st.write("Type your question in Arabic or English, and the AI will analyze the table and answer instantly.")
        
        # Convert the dataframe to a string format so Gemini can easily read it
        data_context = df.to_string(index=False)
        
        user_query = st.text_input("What would you like to know about your ads? (e.g., Which ad performed best and why?)")
        
        if user_query:
            with st.spinner("🔄 The AI Agent is analyzing your data now..."):
                try:
                    # Provide system instructions and context to the AI model
                    full_prompt = f"""
                    You are a digital marketing expert and a smart advertising consultant for the "Lamha" platform.
                    Your task is to analyze the following data and answer the user's question accurately and professionally in Arabic.
                    
                    Ads Data (CSV):
                    {data_context}
                    
                    User Question: {user_query}
                    """
                    
                    # Call the fast, modern, and cost-effective Gemini 2.5 Flash model
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    response = model.generate_content(full_prompt)
                    
                    # Display the AI's response in a beautifully formatted box
                    st.info(response.text)
                    
                except Exception as e:
                    st.error(f"An error occurred while communicating with Gemini: {e}")
