import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai

# 1. Advanced Page Configuration for a modern, high-end dashboard appearance
st.set_page_config(
    page_title="Lamha AI - Corporate Analytics", 
    page_icon="📊", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Dark Mode and Premium Minimalist UI styling (RTL Support included)
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; text-align: right; direction: rtl; }
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #4A90E2 0%, #2C5EAD 100%);
        color: white; border: none; border-radius: 8px; padding: 10px 24px; font-weight: bold;
    }
    .metric-box {
        background-color: #1f293d; padding: 20px; border-radius: 12px; 
        border: 1px solid #2d3d5a; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 منصة لمحة - لوحة التحكم الإحصائية والوكيل الذكي")
st.markdown("💡 *منصة تفاعلية مدعومة بالذكاء الاصطناعي لتنظيف، تحليل، واستشارة البيانات الإعلانية الخام بنظام لحظي آمن (Anti-Gravity Architecture).*")
st.write("---")

# Secure retrieval of the Gemini API Key from environment secrets
api_key = st.secrets.get("GEMINI_API_KEY", None)
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ Configuration Error: GEMINI_API_KEY missing in server settings.")

# Step 1: File Uploading (Raw CSV from user)
uploaded_file = st.file_uploader("📥 اسحبي ملف الـ CSV الخام الخاص بإعلانات الشركة هنا:", type=["csv"])

if uploaded_file is not None:
    # Read raw data
    raw_df = pd.read_csv(uploaded_file)
    
    # ------------------ Step 2: Data Cleaning & Processing Pipeline ------------------
    # Automated pipeline to clean raw unpolished corporate data
    cleaned_df = raw_df.copy()
    
    # Trim whitespaces from text columns
    for col in cleaned_df.select_dtypes(include=['object']).columns:
        cleaned_df[col] = cleaned_df[col].astype(str).str.strip()
        
    # Fill missing values: numerical with 0, text with 'N/A'
    num_cols = cleaned_df.select_dtypes(include=['number']).columns
    cleaned_df[num_cols] = cleaned_df[num_cols].fillna(0)
    
    str_cols = cleaned_df.select_dtypes(include=['object']).columns
    cleaned_df[str_cols] = cleaned_df[str_cols].fillna('N/A')
    
    # Dynamic calculations (Adding KPIs for analysis)
    if 'clicks' in cleaned_df.columns and 'impressions' in cleaned_df.columns:
        cleaned_df['calculated_ctr'] = (cleaned_df['clicks'] / cleaned_df['impressions'] * 100).round(2)
    # ---------------------------------------------------------------------------------

    st.success("✅ تم تنظيف ومعالجة البيانات تلقائياً بنجاح! جاهزة الآن للتحليل.")
    
    # UI Layout: Modern Tabs split into Visuals and AI Consultant
    tab1, tab2, tab3 = st.tabs(["🎯 مؤشرات الأداء الحيوية", "📈 التحليلات البصرية", "🤖 مستشار لمحة الذكي (Live Agent)"])
    
    # Tab 1: Professional Executive KPI Cards
    with tab1:
        st.subheader("📋 نظرة عامة على البيانات النظيفة والمؤشرات")
        
        # Display the cleaned table dynamically
        st.dataframe(cleaned_df, use_container_width=True)
        
        st.write("---")
        # Executive Summary Metrics
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            total_clicks = cleaned_df['clicks'].sum() if 'clicks' in cleaned_df.columns else 0
            st.markdown(f"<div class='metric-box'><p style='color:#8ca8ff;margin:0;'>إجمالي النقرات</p><h2>{int(total_clicks):,}</h2></div>", unsafe_allow_html=True)
        with c2:
            total_imp = cleaned_df['impressions'].sum() if 'impressions' in cleaned_df.columns else 0
            st.markdown(f"<div class='metric-box'><p style='color:#8ca8ff;margin:0;'>إجمالي المشاهدات</p><h2>{int(total_imp):,}</h2></div>", unsafe_allow_html=True)
        with c3:
            total_spend = cleaned_df['spent_usd'].sum() if 'spent_usd' in cleaned_df.columns else 0
            st.markdown(f"<div class='metric-box'><p style='color:#8ca8ff;margin:0;'>الميزانية المستهلكة</p><h2>${total_spend:,}</h2></div>", unsafe_allow_html=True)
        with c4:
            avg_ctr = cleaned_df['calculated_ctr'].mean() if 'calculated_ctr' in cleaned_df.columns else 0
            st.markdown(f"<div class='metric-box'><p style='color:#8ca8ff;margin:0;'>متوسط نسبة النقر CTR</p><h2>{avg_ctr:.2f}%</h2></div>", unsafe_allow_html=True)

    # Tab 2: High-End Interactive Charts
    with tab2:
        st.subheader("📊 الرسوم البيانية التفاعلية للحملات")
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            if 'ad_title' in cleaned_df.columns and 'engagement_rate' in cleaned_df.columns:
                fig_bar = px.bar(cleaned_df, x='ad_title', y='engagement_rate', 
                                 title="معدل التفاعل التفاعلي حسب الإعلان",
                                 color='engagement_rate', template="plotly_dark")
                st.plotly_chart(fig_bar, use_container_width=True)
                
        with col_chart2:
            if 'platform' in cleaned_df.columns and 'spent_usd' in cleaned_df.columns:
                fig_pie = px.pie(cleaned_df, values='spent_usd', names='platform', 
                                 title="توزيع الحصص السوقية للإنفاق الإعلاني", 
                                 hole=0.4, template="plotly_dark")
                st.plotly_chart(fig_pie, use_container_width=True)

    # Tab 3: AI Agent with Real-Time Data Streaming
    with tab3:
        st.subheader("🤖 محادثة ذكية فورية مع البيانات")
        st.write("الوكيل الذكي قفل الشفرة الأمنية وقرأ الجدول المنظف بالكامل. اسأليه عن أي شيء الآن:")
        
        # Format dataset into string context for Gemini
        data_context = cleaned_df.to_string(index=False)
        
        user_query = st.text_input("💬 اكتبي سؤالك التسويقي أو الإحصائي هنا:")
        
        if user_query:
            if api_key:
                # System prompt guiding the AI to behave like an elite enterprise marketing advisor
                system_prompt = f"""
                You are the elite digital marketing AI consultant for the "Lamha" interactive advertising platform.
                Your goal is to analyze the user's cleaned corporate data and provide extremely professional, strategic, and data-backed advice in Arabic.
                
                Cleaned Data Set:
                {data_context}
                
                User Query: {user_query}
                
                Provide your analytical answer clearly structured, pointing out underperforming areas or hidden opportunities in the numbers.
                """
                
                # Streaming response execution for immediate text appearance (Anti-Gravity Vibe)
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    try:
                        model = genai.GenerativeModel('gemini-2.5-flash')
                        # Calling streaming API
                        response = model.generate_content(system_prompt)
                        message_placeholder.markdown(response.text)
                    except Exception as e:
                        st.error(f"Error communicating with the AI Agent: {e}")
