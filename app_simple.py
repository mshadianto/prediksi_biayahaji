import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import json

# Page config
st.set_page_config(
    page_title="🕌 Prediksi Biaya Haji Indonesia",
    page_icon="🕌",
    layout="wide"
)

st.title("🕌 RAG Agentic AI - Prediksi Biaya Haji Indonesia")
st.markdown("*Self-contained version - Semua dalam satu file*")

# Configuration
class SimpleConfig:
    def __init__(self):
        self.OPENROUTER_API_KEY = ""
        self.FINNHUB_API_KEY = ""
        self.FIXER_API_KEY = ""

# Knowledge Base
KNOWLEDGE_BASE = {
    "biaya_haji_dasar": {
        "biaya_pendaftaran": 500000,
        "biaya_administrasi": 1000000,
        "transportasi_domestik": 2000000,
        "akomodasi_makkah": 15000000,
        "akomodasi_madinah": 10000000,
        "transportasi_udara": 25000000,
        "visa_dan_dokumen": 3000000,
        "makan_dan_konsumsi": 8000000,
        "perlengkapan_haji": 5000000,
        "dana_darurat": 5000000
    },
    "faktor_ekonomi": {
        "inflasi_tahunan": 0.035,
        "korelasi_emas_haji": 0.7,
        "volatilitas_mata_uang": 0.15
    }
}

# Functions
def get_gold_price_demo():
    """Demo gold price data"""
    return {
        'current_price': 2000.50,
        'change': 15.25,
        'change_percent': 0.77,
        'high': 2010.00,
        'low': 1985.00,
        'open': 1995.00,
        'timestamp': datetime.now()
    }

def calculate_hajj_cost_scenarios(gold_price=2000):
    """Calculate hajj cost scenarios"""
    base_cost = sum(KNOWLEDGE_BASE["biaya_haji_dasar"].values())
    correlation = KNOWLEDGE_BASE["faktor_ekonomi"]["korelasi_emas_haji"]
    
    # Apply gold correlation
    historical_gold = 2000
    gold_change = (gold_price - historical_gold) / historical_gold
    adjustment = base_cost * gold_change * correlation
    
    scenarios = {
        "Konservatif": base_cost + (adjustment * 0.95),
        "Realistis": base_cost + adjustment,
        "Optimistis": base_cost + (adjustment * 1.05)
    }
    
    return scenarios

def create_prediction_chart(scenarios):
    """Create prediction chart"""
    months = list(range(0, 25))
    fig = go.Figure()
    
    colors = {"Konservatif": "green", "Realistis": "blue", "Optimistis": "red"}
    
    for scenario, base_cost in scenarios.items():
        monthly_growth = 0.08 / 12  # 8% annual growth
        costs = [base_cost * (1 + monthly_growth) ** month for month in months]
        
        fig.add_trace(go.Scatter(
            x=months,
            y=costs,
            mode='lines+markers',
            name=f'Skenario {scenario}',
            line=dict(color=colors[scenario], width=3)
        ))
    
    fig.update_layout(
        title="Prediksi Biaya Haji Indonesia (24 Bulan)",
        xaxis_title="Bulan Ke Depan",
        yaxis_title="Biaya (IDR)",
        template='plotly_white',
        height=500
    )
    
    return fig

def generate_ai_response(question):
    """Generate demo AI response"""
    return f"""
**Analisis AI (Demo Mode)** 🤖

Berdasarkan pertanyaan: "{question}"

**📊 Analisis:**
- Biaya haji saat ini: Rp 75-80 juta per jamaah
- Harga emas memiliki korelasi 70% dengan biaya haji
- Inflasi tahunan 3.5% mempengaruhi kenaikan biaya
- Nilai tukar USD/IDR sangat berpengaruh

**📈 Prediksi Trend:**
- Kenaikan biaya tahunan: ~8%
- Faktor musiman: ~5% variasi
- Volatilitas mata uang perlu diperhatikan

**💡 Rekomendasi:**
1. Mulai menabung sedini mungkin
2. Diversifikasi investasi termasuk emas
3. Monitor perkembangan ekonomi global
4. Pertimbangkan asuransi perjalanan

*Note: Gunakan API key untuk analisis AI yang lebih mendalam.*
"""

# Sidebar
with st.sidebar:
    st.header("⚙️ Konfigurasi")
    
    config = SimpleConfig()
    config.OPENROUTER_API_KEY = st.text_input("OpenRouter API Key", type="password")
    config.FINNHUB_API_KEY = st.text_input("Finnhub API Key", type="password") 
    config.FIXER_API_KEY = st.text_input("Fixer.io API Key", type="password")
    
    st.markdown("---")
    st.info("💡 **Demo Mode Active**\n\nAplikasi berjalan dengan data demo. Tambahkan API keys untuk data real-time.")
    
    if st.button("🔄 Refresh Data"):
        st.rerun()

# Main content
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🤖 AI Analysis", "📋 Data Details"])

# Tab 1: Dashboard
with tab1:
    st.header("📈 Data Real-time (Demo)")
    
    # Gold price display
    gold_data = get_gold_price_demo()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Harga Emas (USD/oz)",
            f"${gold_data['current_price']:.2f}",
            f"{gold_data['change']:+.2f} ({gold_data['change_percent']:+.2f}%)"
        )
    
    with col2:
        st.metric("High", f"${gold_data['high']:.2f}")
    
    with col3:
        st.metric("Low", f"${gold_data['low']:.2f}")
    
    # Exchange rate
    st.info("💱 Nilai Tukar USD/IDR: Rp 15,000 (Demo)")
    
    # Prediction scenarios
    st.header("🎯 Prediksi Biaya Haji")
    
    scenarios = calculate_hajj_cost_scenarios(gold_data['current_price'])
    
    pred_col1, pred_col2, pred_col3 = st.columns(3)
    
    with pred_col1:
        st.metric("Skenario Konservatif", f"Rp {scenarios['Konservatif']:,.0f}")
    
    with pred_col2:
        st.metric("Skenario Realistis", f"Rp {scenarios['Realistis']:,.0f}")
    
    with pred_col3:
        st.metric("Skenario Optimistis", f"Rp {scenarios['Optimistis']:,.0f}")
    
    # Prediction chart
    st.header("📊 Grafik Prediksi")
    chart = create_prediction_chart(scenarios)
    st.plotly_chart(chart, use_container_width=True)

# Tab 2: AI Analysis
with tab2:
    st.header("🤖 AI Analysis (Demo Mode)")
    
    # Quick questions
    st.subheader("💡 Pertanyaan Populer")
    
    questions = [
        "Pengaruh harga emas terhadap biaya haji?",
        "Prediksi biaya haji 2 tahun ke depan?", 
        "Strategi menabung untuk haji?",
        "Faktor-faktor yang mempengaruhi biaya?",
        "Waktu terbaik untuk mendaftar haji?"
    ]
    
    for i, question in enumerate(questions):
        if st.button(f"❓ {question}", key=f"q_{i}"):
            response = generate_ai_response(question)
            st.markdown(response)
    
    # Custom question
    st.subheader("✍️ Pertanyaan Kustom")
    user_question = st.text_area("Ajukan pertanyaan Anda:")
    
    if st.button("🔍 Analisis"):
        if user_question:
            response = generate_ai_response(user_question)
            st.markdown(response)
        else:
            st.warning("Silakan masukkan pertanyaan!")

# Tab 3: Data Details
with tab3:
    st.header("📋 Detail Komponen Biaya")
    
    # Cost breakdown
    base_costs = KNOWLEDGE_BASE["biaya_haji_dasar"]
    total_cost = sum(base_costs.values())
    
    df_costs = pd.DataFrame([
        {
            "Komponen": k.replace('_', ' ').title(),
            "Biaya (IDR)": f"Rp {v:,}",
            "Persentase": f"{(v/total_cost)*100:.1f}%"
        }
        for k, v in base_costs.items()
    ])
    
    st.dataframe(df_costs, use_container_width=True)
    st.success(f"**Total Biaya Dasar**: Rp {total_cost:,}")
    
    # Economic factors
    st.subheader("📈 Faktor Ekonomi")
    econ_factors = KNOWLEDGE_BASE["faktor_ekonomi"]
    
    for factor, value in econ_factors.items():
        if value < 1:
            display_value = f"{value * 100:.1f}%"
        else:
            display_value = f"{value:.2f}"
        
        st.markdown(f"- **{factor.replace('_', ' ').title()}**: {display_value}")

# Footer
st.markdown("---")
st.markdown("""
**📝 Disclaimer**: Prediksi berdasarkan analisis data historis dan faktor ekonomi.
Biaya aktual dapat berbeda tergantung kondisi pasar dan kebijakan pemerintah.

**🔗 Sumber Data**: Demo data (Finnhub, Fixer.io, OpenRouter untuk versi lengkap)
""")

# Success message
st.success("✅ Aplikasi berjalan sukses! Untuk fitur lengkap, setup project structure dengan setup_project.py")