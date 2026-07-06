import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai

# 1. Advanced Page Configuration for an Elite Dashboard 2026 Layout
st.set_page_config(
    page_title="منصة لمحة الذكية | Lamha AI Analytics", 
    page_icon="📊", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Language Selector in Sidebar (Default to Arabic)
st.sidebar.markdown("### 🌐 Language / اللغة")
lang = st.sidebar.selectbox("Choose Interface Language", ["العربية", "English"])

# 3. Dynamic Dictionary for Dual-Language Support
strings = {
    "العربية": {
        "title": "📊 منصة <span class='brand-highlight'>لمحة</span> الذكية للأداء الرقمي",
        "subtitle": "نظام هندسة وتنظيف فوري للبيانات الإعلانية الخام مدمج بوكيل ذكي مستشار لقطاع الأعمال.",
        "uploader_label": "📥 اسحب ملف الـ CSV المعقد أو الخام هنا لبدء خط التنظيف الفوري:",
        "success_msg": "✅ تم الفحص الأمني، معالجة القيم الفارغة، وتنظيف تباين النصوص بنجاح.",
        "tab1": "🎯 المؤشرات التنفيذية (KPIs)",
        "tab2": "📈 مركز التحليل البصري",
        "tab3": "🤖 مستشار لمحة الذكي (Live Agent)",
        "table_title": "📋 مخرجات جداول البيانات المهندسة",
        "card1": "إجمالي النقرات المستلمة",
        "card2": "إجمالي عدد الظهور",
        "card3": "حجم الاستهلاك المالي",
        "card4": "متوسط كفاءة التحويل (CTR)",
        "chart_title": "📈 مركز تحليلات النماذج التفاعلية",
        "chart1_label": "معدلات تفاعل الجماهير حسب الإعلان التفاعلي",
        "chart1_x": "عنوان الحملة",
        "chart1_y": "معدل التفاعل (%)",
        "chart2_label": "توزيع النفقات المالية على المنصات الرقمية",
        "ai_title": "🤖 المحادثة والاستشارة الفورية",
        "ai_subtitle": "اكتب استفسارك الاستثماري أو استشر الوكيل في كفاءة التوزيع المالي للشركة وسيحلل السجلات والأنماط فوراً.",
        "input_placeholder": "مثال: قيم أداء المنصات ورتب الميزانية المقترحة للحملة القادمة...",
        "input_label": "💬 ما هي التوصية الإستراتيجية التي تود معرفتها من الداتا المرفوعة؟",
        "system_gender_prompt": "Answer the user neutrally and professionally, addressing them in a general/gender-neutral format in Arabic (مخاطبة بصيغة الجمع أو المفرد المحايد العام لقطاع الأعمال)."
    },
    "English": {
        "title": "📊 <span class='brand-highlight'>Lamha</span> Smart Digital Performance Platform",
        "subtitle": "Instant data engineering & cleaning pipeline for raw ad data integrated with an enterprise AI consultant.",
        "uploader_label": "📥 Drop your raw or complex CSV file here to start instant cleaning:",
        "success_msg": "✅ Security check passed, null values handled, and text inconsistencies sanitized successfully.",
        "tab1": "🎯 Executive KPIs",
        "tab2": "📈 Visual Analytics Center",
        "tab3": "🤖 Lamha Strategic Consultant (Live Agent)",
        "table_title": "📋 Engineered Data Table Outputs",
        "card1": "Total Clicks Received",
        "card2": "Total Impressions",
        "card3": "Financial Budget Spent",
        "card4": "Average Conversion Rate (CTR)",
        "chart_title": "📈 Interactive Analytics Hub",
        "chart1_label": "Audience Engagement Rates per Interactive Ad",
        "chart1_x": "Campaign Title",
        "chart1_y": "Engagement Rate (%)",
        "chart2_label": "Financial Budget Distribution across Digital Platforms",
        "ai_title": "🤖 Real-Time Chat & Consultation",
        "ai_subtitle": "Type your investment inquiry or consult the agent regarding the company's financial distribution to analyze trends instantly.",
        "input_placeholder": "e.g., Evaluate platform performance and suggest the optimal budget for the next campaign...",
        "input_label": "💬 What strategic insight would you like to extract from the uploaded data?",
        "system_gender_prompt": "Answer the user neutrally and professionally in professional business Arabic, ensuring all verbs and pronouns are completely gender-neutral and general."
    }
}

current_str = strings[lang]
direction = "rtl" if lang == "العربية" else "ltr"
align = "right" if lang == "العربية" else "left"

# 4. Complete CSS Inject for strict RTL/LTR toggling, font scaling, and Red Accent
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {{
        font-family: 'Tajawal', sans-serif !important;
        direction: {direction} !important;
        text-align: {align} !important;
        background-color: #0b0d13;
        color: #f3f4f6;
    }}
    
    .center-text {{
        text-align: center !important;
        direction: {direction} !important;
    }}
    
    .brand-title {{
        font-size: 3rem !important;
        font-weight: 900 !important;
        color: #ffffff;
        margin-bottom: 5px;
    }}
    .brand-highlight {{
        color: #ff3b30 !important;
        text-shadow: 0px 0px 20px rgba(255, 59, 48, 0.4);
    }}
    
    button[data-baseweb="tab"] {{
        font-family: 'Tajawal', sans-serif !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #8a99ad !important;
        padding: 12px 24px !important;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        color: #ff3b30 !important;
        border-bottom: 2px solid #ff3b30 !important;
    }}
    
    div.stButton > button:first-child {{
        background: linear-gradient(135deg, #ff3b30 0%, #a31d1d 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 28px !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(255, 59, 48, 0.2);
    }}
    
    .metric-card-2026 {{
        background: linear-gradient(145deg, #161a24 0%, #11141d 100%);
        padding: 24px;
        border-radius: 16px; 
        border: 1px solid #232a3d;
        text-align: center !important;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }}
    .metric-card-2026 p {{ color: #9ca3af; margin: 0 0 8px 0; font-size: 1rem; font-weight: 500; }}
    .metric-card-2026 h2 {{ color: #ffffff; font-size: 2.2rem; font-weight: 800; margin: 0; }}
    
    input[type="text"], .stTextInput div {{
        direction: {direction} !important;
        text-align: {align} !important;
    }}
    div[data-testid="stMarkdownContainer"] p {{
        text-align: {align} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# Main Branding Header
st.markdown(f"<div class='center-text'><h1 class='brand-title'>{current_str['title']}</h1></div>", unsafe_allow_html=True)
st.markdown(f"<div class='center-text'><p style='color: #9ca3af; font-size: 1.1rem; margin-bottom: 25px;'>{current_str['subtitle']}</p></div>", unsafe_allow_html=True)
st.markdown("<div class='center-text'><hr style='border: 0; height: 1px; background: linear-gradient(to right, transparent, #232a3d, transparent); margin-bottom: 30px;'></div>", unsafe_allow_html=True)

# Secure API Configuration
api_key = st.secrets.get("GEMINI_API_KEY", None)
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ Configuration Error: GEMINI_API_KEY missing in server settings.")

# File Drop-zone
uploaded_file = st.file_uploader(current_str['uploader_label'], type=["csv"])

if uploaded_file is not None:
    raw_df = pd.read_csv(uploaded_file)
    
    # ------------------ Advanced Data Cleaning Pipeline ------------------
    cleaned_df = raw_df.copy()
    cleaned_df.columns = cleaned_df.columns.str.strip().str.lower()
    
    for col in cleaned_df.select_dtypes(include=['object']).columns:
        cleaned_df[col] = cleaned_df[col].astype(str).str.strip()
        if col == 'platform':
            cleaned_df[col] = cleaned_df[col].str.capitalize()
            
    num_cols = cleaned_df.select_dtypes(include=['number']).columns
    cleaned_df[num_cols] = cleaned_df[num_cols].fillna(0)
    
    str_cols = cleaned_df.select_dtypes(include=['object']).columns
    cleaned_df[str_cols] = cleaned_df[str_cols].fillna('N/A')
    
    if 'clicks' in cleaned_df.columns and 'impressions' in cleaned_df.columns:
        cleaned_df['calculated_ctr'] = cleaned_df.apply(
            lambda row: round((row['clicks'] / row['impressions'] * 100), 2) if row['impressions'] > 0 else 0.0, 
            axis=1
        )
    # ---------------------------------------------------------------------------------

    st.success(current_str['success_msg'])
    
    # Modern Tabs split
    tab1, tab2, tab3 = st.tabs([current_str['tab1'], current_str['tab2'], current_str['tab3']])
    
    # Tab 1: Professional Executive KPI Cards
    with tab1:
        st.subheader(current_str['table_title'])
        st.dataframe(cleaned_df, use_container_width=True)
        st.write(" ")
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            clicks_val = cleaned_df['clicks'].sum() if 'clicks' in cleaned_df.columns else 0
            st.markdown(f"<div class='metric-card-2026'><p>{current_str['card1']}</p><h2>{int(clicks_val):,}</h2></div>", unsafe_allow_html=True)
        with c2:
            imp_val = cleaned_df['impressions'].sum() if 'impressions' in cleaned_df.columns else 0
            st.markdown(f"<div class='metric-card-2026'><p>{current_str['card2']}</p><h2>{int(imp_val):,}</h2></div>", unsafe_allow_html=True)
        with c3:
            spend_val = cleaned_df['spent_usd'].sum() if 'spent_usd' in cleaned_df.columns else 0
            st.markdown(f"<div class='metric-card-2026'><p>{current_str['card3']}</p><h2>${spend_val:,}</h2></div>", unsafe_allow_html=True)
        with c4:
            ctr_val = cleaned_df['calculated_ctr'].mean() if 'calculated_ctr' in cleaned_df.columns else 0
            st.markdown(f"<div class='metric-card-2026'><p>{current_str['card4']}</p><h2>{ctr_val:.2f}%</h2></div>", unsafe_allow_html=True)

    # Tab 2: Premium Visualizations
    with tab2:
        st.subheader(current_str['chart_title'])
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            if 'ad_title' in cleaned_df.columns and 'engagement_rate' in cleaned_df.columns:
                fig_bar = px.bar(cleaned_df, x='ad_title', y='engagement_rate', 
                                 title=current_str['chart1_label'],
                                 labels={'engagement_rate': current_str['chart1_y'], 'ad_title': current_str['chart1_x']},
                                 color='engagement_rate', color_continuous_scale=['#330808', '#ff3b30'], template="plotly_dark")
                st.plotly_chart(fig_bar, use_container_width=True)
                
        with col_chart2:
            if 'platform' in cleaned_df.columns and 'spent_usd' in cleaned_df.columns:
                fig_pie = px.pie(cleaned_df, values='spent_usd', names='platform', 
                                 title=current_str['chart2_label'], 
                                 hole=0.5, color_discrete_sequence=['#ff3b30', '#a31d1d', '#1f293d', '#4a5568'], template="plotly_dark")
                st.plotly_chart(fig_pie, use_container_width=True)

    # Tab 3: AI Agent Core
    with tab3:
        st.subheader(current_str['ai_title'])
        st.markdown(f"<p>{current_str['ai_subtitle']}</p>", unsafe_allow_html=True)
        
        data_context = cleaned_df.to_string(index=False)
        user_query = st.text_input(current_str['input_label'], placeholder=current_str['input_placeholder'])
        
        if user_query:
            system_prompt = f"""
            You are the elite digital marketing AI consultant for the "Lamha" (لمحة) interactive advertising platform.
            Your goal is to analyze the user's cleaned data and provide strategic, data-backed advice strictly in Arabic.
            
            Strict Guidelines:
            1. Respond in professional corporate Arabic.
            2. {current_str['system_gender_prompt']} DO NOT address the user as female specifically. Use general business terminology (e.g., 'عملائنا الأعزاء', 'يمكنكم ملاحظة', 'نوصي بـ').
            3. Use bullet points and professional marketing terms.
            4. Structure your response into: Dashboard Insights, Discovered Issues, and Strategic Recommendations.
            
            Data Set:
            {data_context}
            
            User Query: {user_query}
            """
            
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    response = model.generate_content(system_prompt)
                    message_placeholder.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
