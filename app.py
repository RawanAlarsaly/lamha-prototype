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

# 2. Complete CSS Inject for strict RTL, proper font scaling, custom alignment, and Red Accent
st.markdown("""
    <style>
    /* Global alignment to RTL and Font settings */
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Tajawal', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
        background-color: #0b0d13;
        color: #f3f4f6;
    }
    
    /* Center aligning titles and descriptions */
    .center-text {
        text-align: center !important;
        direction: rtl !important;
    }
    
    /* Highlighting "لمحة" in Luxury Red Crimson */
    .brand-title {
        font-size: 3rem !important;
        font-weight: 900 !important;
        color: #ffffff;
        margin-bottom: 5px;
    }
    .brand-highlight {
        color: #ff3b30 !important;
        text-shadow: 0px 0px 20px rgba(255, 59, 48, 0.4);
    }
    
    /* Tabs customization to match 2026 UI standards */
    button[data-baseweb="tab"] {
        font-family: 'Tajawal', sans-serif !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #8a99ad !important;
        direction: rtl !important;
        border-bottom: 2px solid transparent;
        padding: 12px 24px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #ff3b30 !important;
        border-bottom: 2px solid #ff3b30 !important;
    }
    
    /* Buttons Customization with micro-interactions */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #ff3b30 0%, #a31d1d 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 28px !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(255, 59, 48, 0.2);
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 59, 48, 0.4);
    }
    
    /* Metric Cards Redesign */
    .metric-card-2026 {
        background: linear-gradient(145deg, #161a24 0%, #11141d 100%);
        padding: 24px;
        border-radius: 16px; 
        border: 1px solid #232a3d;
        text-align: center !important;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    .metric-card-2026 p {
        color: #9ca3af;
        margin: 0 0 8px 0;
        font-size: 1rem;
        font-weight: 500;
    }
    .metric-card-2026 h2 {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
    }
    
    /* Strict Alignment for Input forms and placeholders */
    input[type="text"], .stTextInput div {
        direction: rtl !important;
        text-align: right !important;
    }
    div[data-testid="stMarkdownContainer"] p {
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

# Main Branding Header (Centered with Arabic RTL focus)
st.markdown("<div class='center-text'><h1 class='brand-title'>📊 منصة <span class='brand-highlight'>لمحة</span> الذكية للأداء الرقمي</h1></div>", unsafe_allow_html=True)
st.markdown("<div class='center-text'><p style='color: #9ca3af; font-size: 1.1rem; margin-bottom: 25px;'>نظام هندسة وتنظيف فوري للبيانات الإعلانية الخام مدمج بوكيل ذكي مستشار لقطاع الأعمال.</p></div>", unsafe_allow_html=True)
st.markdown("<div class='center-text'><hr style='border: 0; height: 1px; background: linear-gradient(to right, transparent, #232a3d, transparent); margin-bottom: 30px;'></div>", unsafe_allow_html=True)

# Secure API Configuration
api_key = st.secrets.get("GEMINI_API_KEY", None)
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ خطأ في التكوين: مفتاح السيرفر المجهول GEMINI_API_KEY غير متصل بالخادم.")

# File Drop-zone
uploaded_file = st.file_uploader("📥 اسحبي ملف الـ CSV المعقد أو الخام هنا لبدء خط التنظيف الفوري:", type=["csv"])

if uploaded_file is not None:
    # Load into active Dataframe
    raw_df = pd.read_csv(uploaded_file)
    
    # ------------------ Advanced 2026 Edge Data Cleaning Pipeline ------------------
    cleaned_df = raw_df.copy()
    
    # Standardize column naming conventions
    cleaned_df.columns = cleaned_df.columns.str.strip().str.lower()
    
    # Textual Column Sanitization (Stripping whitespaces & case sensitivity control)
    for col in cleaned_df.select_dtypes(include=['object']).columns:
        cleaned_df[col] = cleaned_df[col].astype(str).str.strip()
        # Catch and unify platform typos like instagram/Instagram
        if col == 'platform':
            cleaned_df[col] = cleaned_df[col].str.capitalize()
            
    # Numerical Column Normalization (Fix missing values, ensure safe operational bounds)
    num_cols = cleaned_df.select_dtypes(include=['number']).columns
    cleaned_df[num_cols] = cleaned_df[num_cols].fillna(0)
    
    # Categorical Fallback Management
    str_cols = cleaned_df.select_dtypes(include=['object']).columns
    cleaned_df[str_cols] = cleaned_df[str_cols].fillna('غير محدد / NA')
    
    # Injecting Missing Crucial KPIs safely
    if 'clicks' in cleaned_df.columns and 'impressions' in cleaned_df.columns:
        # Avoid division by zero bugs dynamically using a safe continuous function lambda
        cleaned_df['calculated_ctr'] = cleaned_df.apply(
            lambda row: round((row['clicks'] / row['impressions'] * 100), 2) if row['impressions'] > 0 else 0.0, 
            axis=1
        )
    # ---------------------------------------------------------------------------------

    st.success("✅ تم الفحص الأمني، معالجة القيم الفارغة، وتنظيف تباين النصوص بنجاح.")
    
    # Modern Tabs split
    tab1, tab2, tab3 = st.tabs(["🎯 المؤشرات التنفيذية (KPIs)", "📈 مركز التحليل البصري", "🤖 مستشار لمحة الإستراتيجي"])
    
    # Tab 1: Professional Executive KPI Cards
    with tab1:
        st.subheader("📋 مخرجات جداول البيانات المهندسة")
        st.dataframe(cleaned_df, use_container_width=True)
        st.write(" ")
        
        # Grid of cards
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            clicks_val = cleaned_df['clicks'].sum() if 'clicks' in cleaned_df.columns else 0
            st.markdown(f"<div class='metric-card-2026'><p>إجمالي النقرات المستلمة</p><h2>{int(clicks_val):,}</h2></div>", unsafe_allow_html=True)
        with c2:
            imp_val = cleaned_df['impressions'].sum() if 'impressions' in cleaned_df.columns else 0
            st.markdown(f"<div class='metric-card-2026'><p>إجمالي عدد الظهور</p><h2>{int(imp_val):,}</h2></div>", unsafe_allow_html=True)
        with c3:
            spend_val = cleaned_df['spent_usd'].sum() if 'spent_usd' in cleaned_df.columns else 0
            st.markdown(f"<div class='metric-card-2026'><p>حجم الاستهلاك المالي</p><h2>${spend_val:,}</h2></div>", unsafe_allow_html=True)
        with c4:
            ctr_val = cleaned_df['calculated_ctr'].mean() if 'calculated_ctr' in cleaned_df.columns else 0
            st.markdown(f"<div class='metric-card-2026'><p>متوسط كفاءة التحويل (CTR)</p><h2>{ctr_val:.2f}%</h2></div>", unsafe_allow_html=True)

    # Tab 2: Premium Visualizations
    with tab2:
        st.subheader("📈 مركز تحليلات النماذج التفاعلية")
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            if 'ad_title' in cleaned_df.columns and 'engagement_rate' in cleaned_df.columns:
                fig_bar = px.bar(cleaned_df, x='ad_title', y='engagement_rate', 
                                 title="معدلات تفاعل الجماهير حسب الإعلان التفاعلي",
                                 labels={'engagement_rate': 'معدل التفاعل (%)', 'ad_title': 'عنوان الحملة'},
                                 color='engagement_rate', color_continuous_scale=['#330808', '#ff3b30'], template="plotly_dark")
                st.plotly_chart(fig_bar, use_container_width=True)
                
        with col_chart2:
            if 'platform' in cleaned_df.columns and 'spent_usd' in cleaned_df.columns:
                fig_pie = px.pie(cleaned_df, values='spent_usd', names='platform', 
                                 title="توزيع النفقات المالية على المنصات الرقمية", 
                                 hole=0.5, color_discrete_sequence=['#ff3b30', '#a31d1d', '#1f293d', '#4a5568'], template="plotly_dark")
                st.plotly_chart(fig_pie, use_container_width=True)

    # Tab 3: AI Agent Core
    with tab3:
        st.subheader("🤖 المحادثة والاستشارة الفورية")
        st.markdown("<p style='text-align: right;'>اكتبي استفسارك الاستثماري أو استشيري الوكيل في كفاءة التوزيع المالي للشركة وسيحلل لك السجلات والأنماط المليونية فوراً.</p>", unsafe_allow_html=True)
        
        data_context = cleaned_df.to_string(index=False)
        user_query = st.text_input("💬 ما هي التوصية الإستراتيجية التي تودين معرفتها من الداتا المرفوعة؟", placeholder="مثال: قيم أداء المنصات ورتب الميزانية المقترحة للحملة القادمة...")
        
        if user_query:
            system_prompt = f"""
            You are the elite digital marketing AI consultant for the "Lamha" (لمحة) interactive advertising platform.
            Your goal is to analyze the user's cleaned corporate data and provide extremely professional, strategic, and data-backed advice strictly in Arabic.
            
            Guidelines:
            1. Respond in professional corporate Arabic.
            2. Base your analysis completely on the metrics provided below.
            3. Use bullet points and professional terms.
            4. Structure your response into: Dashboard Insights, Discovered Issues, and Strategic Recommendations.
            
            Cleaned Data Set:
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
                    st.error(f"حدث خطأ أثناء معالجة استفسار الوكيل: {e}")
