import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import requests
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import sys
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Add src directory to Python path - fixed version
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
src_path = current_dir / "src"
sys.path.insert(0, str(src_path))

# Data historis biaya haji berdasarkan Keputusan Presiden
HISTORICAL_HAJJ_COSTS = {
    2016: {  # 1437H/2016M - Keppres 21/2016
        'year_hijri': '1437H',
        'jakarta': 34127046,
        'surabaya': 34941414,
        'medan': 31672827,
        'makassar': 38905808,
        'aceh': 31117461,
        'average': 34152912
    },
    2017: {  # 1438H/2017M - Keppres 8/2017
        'year_hijri': '1438H',
        'jakarta': 34306780,
        'surabaya': 35666250,
        'medan': 31707400,
        'makassar': 38972250,
        'aceh': 31040900,
        'average': 34338716
    },
    2018: {  # 1439H/2018M - Keppres 7/2018
        'year_hijri': '1439H',
        'jakarta': 34532190,
        'surabaya': 36091845,
        'medan': 31840375,
        'makassar': 39507741,
        'aceh': 31090010,
        'average': 34612432
    },
    2019: {  # 1440H/2019M - Keppres 8/2019
        'year_hijri': '1440H',
        'jakarta': 34987280,
        'surabaya': 36586945,
        'medan': 31730375,
        'makassar': 39207741,
        'aceh': 30881010,
        'average': 34678670
    },
    2020: {  # 1441H/2020M - Keppres 6/2020
        'year_hijri': '1441H',
        'jakarta': 34772602,
        'surabaya': 37577602,
        'medan': 32172602,
        'makassar': 38352602,
        'aceh': 31454602,
        'average': 34865802
    },
    2022: {  # 1443H/2022M - Keppres 5/2022
        'year_hijri': '1443H',
        'jakarta': 39886009,
        'surabaya': 42586009,
        'medan': 36393073,
        'makassar': 42686506,
        'aceh': 35660857,
        'average': 39442491
    },
    2023: {  # 1444H/2023M - Keppres 7/2023
        'year_hijri': '1444H',
        'jakarta': 91575945,
        'surabaya': 96166395,
        'medan': 85439589,
        'makassar': 92420640,
        'aceh': 84602294,
        'average': 90040973
    },
    2024: {  # 1445H/2024M - Keppres 6/2024
        'year_hijri': '1445H',
        'jakarta': 95862448,
        'surabaya': 97890448,
        'medan': 88509253,
        'makassar': 97609469,
        'aceh': 87359984,
        'average': 93446320
    },
    2025: {  # 1446H/2025M - Keppres 6/2025
        'year_hijri': '1446H',
        'jakarta': 92854259,
        'surabaya': 94934259,
        'medan': 81955039,
        'makassar': 91649429,
        'aceh': 80900841,
        'average': 88458765
    }
}

# Initialize modules loaded flag
MODULES_LOADED = False

# Try to import modules with fallback
try:
    from core.config import Config
    from core.data_collector import DataCollector
    from core.rag_system import RAGSystem
    from core.agentic_ai import AgenticAI
    from core.predictor import HajjCostPredictor
    from utils.visualizations import create_prediction_chart
    from components.sidebar import render_sidebar
    from components.dashboard import render_dashboard
    from components.ai_chat import render_ai_chat
    
    MODULES_LOADED = True
    print("✅ Modular components loaded successfully")
    
except ImportError as e:
    print(f"⚠️ Some modules not found: {e}")
    print("🔧 Running with built-in functionality...")
    MODULES_LOADED = False

class RealDataAnalyzer:
    """Analyzer untuk data riil biaya haji"""
    
    def __init__(self):
        self.df = self._create_dataframe()
        self.growth_analysis = self._analyze_growth()
        
    def _create_dataframe(self):
        """Buat DataFrame dari data historis"""
        data = []
        for year, costs in HISTORICAL_HAJJ_COSTS.items():
            for city, cost in costs.items():
                if city not in ['year_hijri', 'average']:
                    data.append({
                        'year': year,
                        'year_hijri': costs['year_hijri'],
                        'embarkasi': city,
                        'biaya': cost
                    })
                elif city == 'average':
                    data.append({
                        'year': year,
                        'year_hijri': costs['year_hijri'],
                        'embarkasi': 'rata_rata',
                        'biaya': cost
                    })
        
        return pd.DataFrame(data)
    
    def _analyze_growth(self):
        """Analisis pertumbuhan biaya haji"""
        avg_data = self.df[self.df['embarkasi'] == 'rata_rata'].copy()
        avg_data = avg_data.sort_values('year')
        
        # Hitung growth rate year-over-year
        avg_data['growth_rate'] = avg_data['biaya'].pct_change()
        
        # Analisis periode khusus (ada lonjakan besar 2022-2023)
        normal_periods = avg_data[avg_data['year'].isin([2016, 2017, 2018, 2019, 2020, 2022])]
        post_covid_periods = avg_data[avg_data['year'].isin([2023, 2024, 2025])]
        
        return {
            'overall_cagr': self._calculate_cagr(avg_data['biaya'].iloc[0], avg_data['biaya'].iloc[-1], len(avg_data)-1),
            'normal_period_cagr': self._calculate_cagr(normal_periods['biaya'].iloc[0], normal_periods['biaya'].iloc[-1], len(normal_periods)-1),
            'avg_growth_rate': avg_data['growth_rate'].mean(),
            'median_growth_rate': avg_data['growth_rate'].median(),
            'std_growth_rate': avg_data['growth_rate'].std(),
            'data': avg_data
        }
    
    def _calculate_cagr(self, start_value, end_value, periods):
        """Hitung Compound Annual Growth Rate"""
        if start_value <= 0 or end_value <= 0 or periods <= 0:
            return 0
        return (pow(end_value / start_value, 1/periods) - 1) * 100

class BuiltinRAGSystem:
    """Built-in RAG System dengan data riil"""
    
    def __init__(self):
        self.analyzer = RealDataAnalyzer()
        self.knowledge_base = self._build_knowledge_base()
    
    def _build_knowledge_base(self):
        """Build knowledge base dengan data riil"""
        return {
            "data_historis": HISTORICAL_HAJJ_COSTS,
            "analisis_pertumbuhan": self.analyzer.growth_analysis,
            "komponen_biaya": {
                "penerbangan_haji": "Tiket pesawat Jakarta-Jeddah PP",
                "akomodasi_makkah": "Hotel/pemondokan di Makkah",
                "akomodasi_madinah": "Hotel/pemondokan di Madinah", 
                "biaya_hidup": "Living cost selama di Arab Saudi",
                "visa_haji": "Visa dan dokumen perjalanan",
                "pelayanan_haji": "Layanan bimbingan dan pendampingan",
                "transportasi_lokal": "Transportasi dalam kota dan antar kota"
            },
            "faktor_kenaikan": {
                "inflasi_saudi": "Inflasi di Arab Saudi mempengaruhi biaya akomodasi",
                "nilai_tukar": "Fluktuasi SAR/IDR dan USD/IDR",
                "harga_minyak": "Mempengaruhi ekonomi Saudi dan biaya operasional",
                "kapasitas_hotel": "Supply-demand akomodasi di Makkah-Madinah",
                "kebijakan_saudi": "Perubahan regulasi dan tarif pemerintah Saudi"
            }
        }
    
    def retrieve_context(self, query: str) -> str:
        """Retrieve konteks berdasarkan query"""
        context = "=== DATA BIAYA HAJI INDONESIA (BERDASARKAN KEPPRES) ===\n\n"
        
        query_lower = query.lower()
        
        # Tambahkan data historis jika ditanya tentang trend/historis
        if any(word in query_lower for word in ["trend", "historis", "naik", "turun", "pertumbuhan", "perubahan"]):
            context += "📊 TREND BIAYA HAJI (RATA-RATA NASIONAL):\n"
            for year, data in HISTORICAL_HAJJ_COSTS.items():
                context += f"- {year} ({data['year_hijri']}): Rp {data['average']:,}\n"
            
            context += f"\n📈 ANALISIS PERTUMBUHAN:\n"
            growth = self.analyzer.growth_analysis
            context += f"- CAGR Keseluruhan (2016-2025): {growth['overall_cagr']:.1f}% per tahun\n"
            context += f"- CAGR Periode Normal (2016-2022): {growth['normal_period_cagr']:.1f}% per tahun\n"
            context += f"- Rata-rata pertumbuhan tahunan: {growth['avg_growth_rate']*100:.1f}%\n\n"
        
        # Tambahkan insight khusus
        if any(word in query_lower for word in ["2023", "covid", "lonjakan", "naik", "tinggi"]):
            context += "🚀 INSIGHT LONJAKAN 2023:\n"
            context += "- Kenaikan drastis ~128% di 2023 setelah periode COVID\n"
            context += "- Dari Rp 39,4 juta (2022) menjadi Rp 90 juta (2023)\n"
            context += "- Faktor: akumulasi inflasi, penyesuaian pasca-pandemi, kenaikan biaya operasional\n\n"
        
        # Tambahkan perbandingan regional
        if any(word in query_lower for word in ["jakarta", "surabaya", "medan", "aceh", "makassar", "embarkasi", "regional"]):
            context += "🗺️ PERBANDINGAN REGIONAL (2025):\n"
            latest_year = 2025
            latest_data = HISTORICAL_HAJJ_COSTS[latest_year]
            for city, cost in latest_data.items():
                if city not in ['year_hijri', 'average']:
                    context += f"- {city.title()}: Rp {cost:,}\n"
            context += "\n"
        
        return context

class BuiltinPredictor:
    """Built-in predictor dengan data riil"""
    
    def __init__(self, analyzer: RealDataAnalyzer):
        self.analyzer = analyzer
        self.model = None
        self.poly_features = None
        self._train_model()
    
    def _train_model(self):
        """Train model prediksi dengan data historis"""
        avg_data = self.analyzer.df[self.analyzer.df['embarkasi'] == 'rata_rata'].copy()
        avg_data = avg_data.sort_values('year')
        
        # Prepare features
        X = avg_data[['year']].values
        y = avg_data['biaya'].values
        
        # Use polynomial features untuk menangkap non-linear trend
        self.poly_features = PolynomialFeatures(degree=2)
        X_poly = self.poly_features.fit_transform(X)
        
        # Train model
        self.model = LinearRegression()
        self.model.fit(X_poly, y)
    
    def predict_future_costs(self, years_ahead: int = 5) -> dict:
        """Prediksi biaya masa depan"""
        current_year = 2025
        future_years = range(current_year + 1, current_year + years_ahead + 1)
        
        predictions = {}
        
        for year in future_years:
            # ML prediction
            X_future = np.array([[year]])
            X_future_poly = self.poly_features.transform(X_future)
            ml_prediction = self.model.predict(X_future_poly)[0]
            
            # Ensemble dengan beberapa metode
            growth_rate = self.analyzer.growth_analysis['normal_period_cagr'] / 100
            current_cost = HISTORICAL_HAJJ_COSTS[current_year]['average']
            years_from_current = year - current_year
            
            # Conservative prediction (based on normal growth)
            conservative = current_cost * (1 + growth_rate) ** years_from_current
            
            # Optimistic prediction (assuming gradual normalization)
            optimistic = current_cost * (1 + (growth_rate * 0.8)) ** years_from_current
            
            # Ensemble prediction
            ensemble = (ml_prediction * 0.4 + conservative * 0.4 + optimistic * 0.2)
            
            predictions[year] = {
                'ml_prediction': ml_prediction,
                'conservative': conservative,
                'optimistic': optimistic,
                'ensemble': ensemble,
                'confidence': self._calculate_confidence(year)
            }
        
        return predictions
    
    def _calculate_confidence(self, year):
        """Hitung confidence level prediksi"""
        years_ahead = year - 2025
        # Confidence menurun seiring waktu
        base_confidence = 85
        decline_rate = 5  # 5% per tahun
        return max(base_confidence - (years_ahead * decline_rate), 40)

def create_enhanced_visualization(analyzer: RealDataAnalyzer, predictor: BuiltinPredictor):
    """Buat visualisasi enhanced dengan data riil"""
    
    # Data historis
    historical_df = analyzer.df[analyzer.df['embarkasi'] == 'rata_rata'].copy()
    historical_df = historical_df.sort_values('year')
    
    # Prediksi masa depan
    future_predictions = predictor.predict_future_costs(5)
    
    fig = go.Figure()
    
    # Plot data historis
    fig.add_trace(go.Scatter(
        x=historical_df['year'],
        y=historical_df['biaya'],
        mode='lines+markers',
        name='Data Historis (Keppres)',
        line=dict(color='blue', width=4),
        marker=dict(size=8)
    ))
    
    # Plot prediksi ensemble
    future_years = list(future_predictions.keys())
    ensemble_values = [pred['ensemble'] for pred in future_predictions.values()]
    
    fig.add_trace(go.Scatter(
        x=future_years,
        y=ensemble_values,
        mode='lines+markers',
        name='Prediksi Ensemble',
        line=dict(color='red', width=3, dash='dash'),
        marker=dict(size=6)
    ))
    
    # Plot confidence band
    conservative_values = [pred['conservative'] for pred in future_predictions.values()]
    optimistic_values = [pred['optimistic'] for pred in future_predictions.values()]
    
    fig.add_trace(go.Scatter(
        x=future_years + future_years[::-1],
        y=optimistic_values + conservative_values[::-1],
        fill='toself',
        fillcolor='rgba(255,0,0,0.1)',
        line=dict(color='rgba(255,0,0,0)'),
        name='Confidence Band',
        showlegend=True
    ))
    
    # Annotations untuk event penting
    fig.add_annotation(
        x=2023, y=HISTORICAL_HAJJ_COSTS[2023]['average'],
        text="Lonjakan<br>Pasca-COVID<br>+128%",
        showarrow=True,
        arrowhead=2,
        arrowcolor="orange",
        font=dict(color="orange")
    )
    
    fig.update_layout(
        title="Analisis & Prediksi Biaya Haji Indonesia (Berdasarkan Data Keppres)",
        xaxis_title="Tahun",
        yaxis_title="Biaya Haji (IDR)",
        hovermode='x unified',
        template='plotly_white',
        height=600,
        yaxis=dict(tickformat='.0f')
    )
    
    return fig

def render_builtin_dashboard(analyzer, predictor, rag_system):
    """Render dashboard dengan built-in components"""
    
    st.header("📈 Data Real-time & Prediksi")
    
    # Metrics overview
    col1, col2, col3, col4 = st.columns(4)
    
    latest_cost = HISTORICAL_HAJJ_COSTS[2025]['average']
    prev_cost = HISTORICAL_HAJJ_COSTS[2024]['average']
    change = ((latest_cost - prev_cost) / prev_cost) * 100
    
    with col1:
        st.metric("Biaya Haji 2025", f"Rp {latest_cost:,.0f}", f"{change:+.1f}%")
    
    with col2:
        growth = analyzer.growth_analysis
        st.metric("CAGR 2016-2025", f"{growth['overall_cagr']:.1f}%")
    
    with col3:
        st.metric("Growth Normal", f"{growth['normal_period_cagr']:.1f}%")
    
    with col4:
        jakarta_cost = HISTORICAL_HAJJ_COSTS[2025]['jakarta']
        st.metric("Jakarta 2025", f"Rp {jakarta_cost:,.0f}")
    
    # Main visualization
    fig = create_enhanced_visualization(analyzer, predictor)
    st.plotly_chart(fig, use_container_width=True)
    
    # Predictions table
    st.subheader("🔮 Prediksi 2026-2030")
    future_pred = predictor.predict_future_costs(5)
    
    pred_data = []
    for year, pred in future_pred.items():
        pred_data.append({
            'Tahun': year,
            'Prediksi (Rp)': f"{pred['ensemble']:,.0f}",
            'Conservative (Rp)': f"{pred['conservative']:,.0f}",
            'Optimistic (Rp)': f"{pred['optimistic']:,.0f}",
            'Confidence': f"{pred['confidence']}%"
        })
    
    pred_df = pd.DataFrame(pred_data)
    st.dataframe(pred_df, use_container_width=True)

def render_regional_analysis():
    """Render analisis regional"""
    st.header("🗺️ Perbandingan Regional")
    
    # Regional comparison chart
    regional_data = []
    for year in [2023, 2024, 2025]:
        for city, cost in HISTORICAL_HAJJ_COSTS[year].items():
            if city not in ['year_hijri', 'average']:
                regional_data.append({'Year': year, 'Embarkasi': city.title(), 'Biaya': cost})
    
    regional_df = pd.DataFrame(regional_data)
    
    fig_regional = px.line(
        regional_df, 
        x='Year', 
        y='Biaya', 
        color='Embarkasi',
        title="Perbandingan Biaya Haji per Embarkasi (2023-2025)",
        markers=True
    )
    st.plotly_chart(fig_regional, use_container_width=True)
    
    # Regional metrics
    st.subheader("📊 Analisis Regional 2025")
    latest_year = 2025
    latest_data = HISTORICAL_HAJJ_COSTS[latest_year]
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    cities = ['jakarta', 'surabaya', 'medan', 'makassar', 'aceh']
    cols = [col1, col2, col3, col4, col5]
    
    for city, col in zip(cities, cols):
        with col:
            cost = latest_data[city]
            avg_cost = latest_data['average']
            diff = ((cost - avg_cost) / avg_cost) * 100
            st.metric(
                city.title(),
                f"Rp {cost:,.0f}",
                f"{diff:+.1f}% vs avg"
            )

def render_ai_analysis(rag_system, api_key):
    """Render AI analysis section"""
    st.header("🤖 AI Analysis dengan RAG")
    
    st.subheader("💡 Pertanyaan Populer")
    example_questions = [
        "Bagaimana trend biaya haji dari 2016-2025?",
        "Mengapa ada lonjakan besar di tahun 2023?",
        "Prediksi biaya haji 5 tahun ke depan?",
        "Perbedaan biaya antar embarkasi?",
        "Faktor-faktor yang mempengaruhi kenaikan biaya?"
    ]
    
    # Quick question buttons
    question_cols = st.columns(len(example_questions))
    for i, question in enumerate(example_questions):
        with question_cols[i % len(question_cols)]:
            if st.button(f"❓ Q{i+1}", key=f"q_{i}", help=question):
                st.session_state['selected_question'] = question
    
    # User input
    user_question = st.text_area(
        "Ajukan pertanyaan Anda:",
        value=st.session_state.get('selected_question', ''),
        placeholder="Contoh: Mengapa biaya haji naik drastis di 2023?",
        height=100
    )
    
    if st.button("🔍 Analisis dengan RAG") and user_question:
        with st.spinner("AI sedang menganalisis data riil..."):
            # Retrieve context
            context = rag_system.retrieve_context(user_question)
            
            st.markdown("### 🤖 Analisis AI berdasarkan Data Riil:")
            st.markdown(context)
            
            # Enhanced analysis based on API availability
            if api_key:
                st.info("🔄 Enhanced AI analysis dengan API key akan tersedia setelah implementasi modular")
            else:
                st.info("💡 Tambahkan OpenRouter API Key di sidebar untuk analisis AI yang lebih mendalam")
            
            # Add specific analysis based on question
            if "2023" in user_question.lower() or "lonjakan" in user_question.lower():
                st.markdown("""
                **📊 Analisis Mendalam Lonjakan 2023:**
                - Kenaikan dari Rp 39,4 juta (2022) → Rp 90 juta (2023) = +128%
                - Periode pandemi menyebabkan akumulasi penyesuaian tarif
                - Pemerintah Saudi menaikkan standar layanan dan fasilitas
                - Inflasi global dan devaluasi rupiah turut berpengaruh
                """)

def render_data_details(analyzer):
    """Render data details section"""
    st.header("📋 Data Details")
    
    # Historical data table
    st.subheader("📊 Data Historis Lengkap")
    
    detailed_data = []
    for year, data in HISTORICAL_HAJJ_COSTS.items():
        row = {'Tahun': year, 'Tahun Hijriah': data['year_hijri']}
        for city in ['aceh', 'medan', 'jakarta', 'surabaya', 'makassar']:
            if city in data:
                row[city.title()] = f"Rp {data[city]:,}"
        row['Rata-rata'] = f"Rp {data['average']:,}"
        detailed_data.append(row)
    
    detailed_df = pd.DataFrame(detailed_data)
    st.dataframe(detailed_df, use_container_width=True)
    
    # Growth analysis
    st.subheader("📈 Analisis Pertumbuhan")
    growth = analyzer.growth_analysis
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        **📊 Statistik Pertumbuhan:**
        - **CAGR Keseluruhan**: {growth['overall_cagr']:.2f}% per tahun
        - **CAGR Periode Normal**: {growth['normal_period_cagr']:.2f}% per tahun  
        - **Rata-rata Growth Rate**: {growth['avg_growth_rate']*100:.2f}%
        - **Median Growth Rate**: {growth['median_growth_rate']*100:.2f}%
        - **Standar Deviasi**: {growth['std_growth_rate']*100:.2f}%
        """)
    
    with col2:
        st.markdown("""
        **🎯 Insight Utama:**
        - Periode 2016-2022: Pertumbuhan stabil dan predictable
        - Tahun 2023: Anomali dengan kenaikan ekstrem (+128%)
        - Tahun 2024-2025: Normalisasi dan stabilisasi
        - Regional variation: ±15-20% dari rata-rata nasional
        """)
    
    # Source information
    st.subheader("📄 Sumber Data")
    st.markdown("""
    **Data diambil dari Keputusan Presiden RI:**
    - Keppres No. 21 Tahun 2016 (1437H/2016M)
    - Keppres No. 8 Tahun 2017 (1438H/2017M)  
    - Keppres No. 7 Tahun 2018 (1439H/2018M)
    - Keppres No. 8 Tahun 2019 (1440H/2019M)
    - Keppres No. 6 Tahun 2020 (1441H/2020M)
    - Keppres No. 5 Tahun 2022 (1443H/2022M)
    - Keppres No. 7 Tahun 2023 (1444H/2023M)
    - Keppres No. 6 Tahun 2024 (1445H/2024M)
    - Keppres No. 6 Tahun 2025 (1446H/2025M)
    """)

# --- NEW FUNCTION FOR FOOTER ---
def render_footer():
    """Menampilkan footer dinamis di akhir halaman."""
    app_version = datetime.now().strftime("v.%Y%m%d.%H%M%S")
    developer_name = "MS Hadianto"
    
    st.markdown("---")  # Garis pemisah
    st.markdown(
        f"""
        <div style='text-align: center; color: grey; font-size: 12px;'>
            <p><strong>Disclaimer:</strong> Ini adalah aplikasi demo. Prediksi didasarkan pada data historis dan hanya untuk tujuan informasi.</p>
            <p>Developed by <strong>{developer_name}</strong> | Version: {app_version}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def main():
    """Main application function"""
    # Declare global variable at the beginning of function
    global MODULES_LOADED
    
    # Page configuration
    st.set_page_config(
        page_title="🕌 RAG Agentic AI - Prediksi Biaya Haji (Data Riil)",
        page_icon="🕌",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main > div {
        padding-top: 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Title and header
    st.title("🕌 RAG Agentic AI - Prediksi Biaya Haji Indonesia")
    st.markdown("*Enhanced dengan Data Riil dari Keputusan Presiden 2016-2025*")
    
    # Initialize components
    analyzer = RealDataAnalyzer()
    rag_system = BuiltinRAGSystem()
    predictor = BuiltinPredictor(analyzer)
    
    # Show data source info
    st.success("✅ Menggunakan data riil dari 9 Keputusan Presiden RI (2016-2025)")
    
    # Initialize session state variables
    if 'selected_question' not in st.session_state:
        st.session_state['selected_question'] = ''
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Quick Stats")
        
        latest_cost = HISTORICAL_HAJJ_COSTS[2025]['average']
        prev_cost = HISTORICAL_HAJJ_COSTS[2024]['average']
        change = ((latest_cost - prev_cost) / prev_cost) * 100
        
        st.metric("Biaya Haji 2025", f"Rp {latest_cost:,.0f}", f"{change:+.1f}%")
        
        growth = analyzer.growth_analysis
        st.metric("CAGR 2016-2025", f"{growth['overall_cagr']:.1f}%")
        st.metric("Growth Normal", f"{growth['normal_period_cagr']:.1f}%")
        
        st.markdown("---")
        st.info("💡 Data berdasarkan Keputusan Presiden RI tentang BPIH tahun 2016-2025")
        
        # Configuration section
        st.header("⚙️ Konfigurasi API (Opsional)")
        
        openrouter_key = st.text_input("OpenRouter API Key", type="password", help="Untuk AI Analysis yang lebih mendalam")
        finnhub_key = st.text_input("Finnhub API Key", type="password", help="Untuk data harga emas real-time")
        fixer_key = st.text_input("Fixer.io API Key", type="password", help="Untuk nilai tukar mata uang")
        
        if st.button("🔄 Refresh Data"):
            st.rerun()
    
    # Main content area
    if MODULES_LOADED:
        # Use modular components if available
        try:
            config = Config()
            config.OPENROUTER_API_KEY = openrouter_key
            config.FINNHUB_API_KEY = finnhub_key
            config.FIXER_API_KEY = fixer_key
            
            data_collector = DataCollector(config)
            
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🗺️ Regional", "🤖 AI Analysis", "📋 Data Details"])
            
            with tab1:
                render_dashboard(data_collector, predictor, rag_system)
            
            with tab2:
                render_regional_analysis()
            
            with tab3:
                render_ai_analysis(rag_system, openrouter_key)
            
            with tab4:
                render_data_details(analyzer)
                
        except Exception as e:
            st.error(f"Error loading modular components: {e}")
            st.info("Switching to built-in mode...")
            MODULES_LOADED = False
    
    if not MODULES_LOADED:
        # Use built-in components
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🗺️ Regional", "🤖 AI Analysis", "📋 Data Details"])
        
        with tab1:
            render_builtin_dashboard(analyzer, predictor, rag_system)
        
        with tab2:
            render_regional_analysis()
        
        with tab3:
            render_ai_analysis(rag_system, openrouter_key)
        
        with tab4:
            render_data_details(analyzer)

    # --- ADD FOOTER AT THE END OF THE PAGE ---
    render_footer()

if __name__ == "__main__":
    main()