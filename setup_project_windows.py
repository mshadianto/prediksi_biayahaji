#!/usr/bin/env python3
"""
Windows-friendly setup script untuk RAG Agentic AI Hajj Predictor
Tanpa emoji untuk menghindari encoding issues
"""

import os

def create_directory_structure():
    """Buat struktur direktori"""
    directories = [
        "src/core",
        "src/utils", 
        "src/components",
        "src/models",
        "data/raw",
        "data/processed", 
        "data/knowledge_base",
        "config",
        "tests"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        # Buat __init__.py untuk package Python
        if directory.startswith("src/"):
            init_file = os.path.join(directory, "__init__.py")
            with open(init_file, "w", encoding="utf-8") as f:
                f.write(f'"""Package: {directory}"""\n')
    
    print("Struktur direktori berhasil dibuat!")

def create_core_files():
    """Buat file-file core yang diperlukan"""
    
    # src/core/config.py
    config_content = '''"""Configuration management for the application"""
import os
from dataclasses import dataclass

@dataclass
class Config:
    """Application configuration"""
    OPENROUTER_API_KEY: str = ""
    FINNHUB_API_KEY: str = ""
    FIXER_API_KEY: str = ""
    
    OPENROUTER_URL: str = "https://openrouter.ai/api/v1/chat/completions"
    FINNHUB_URL: str = "https://finnhub.io/api/v1"
    FIXER_URL: str = "http://data.fixer.io/api"
    
    def __post_init__(self):
        """Load from environment variables if available"""
        self.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", self.OPENROUTER_API_KEY)
        self.FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", self.FINNHUB_API_KEY)
        self.FIXER_API_KEY = os.getenv("FIXER_API_KEY", self.FIXER_API_KEY)
'''
    
    # src/core/data_collector.py
    data_collector_content = '''"""Data collection from external APIs"""
import requests
import streamlit as st
from datetime import datetime
from typing import Dict, Any

class DataCollector:
    """Class untuk mengumpulkan data dari berbagai sumber"""
    
    def __init__(self, config):
        self.config = config
    
    def get_gold_price(self) -> Dict[str, Any]:
        """Ambil data harga emas dari Finnhub"""
        try:
            if not self.config.FINNHUB_API_KEY:
                return self._get_mock_gold_data()
            
            headers = {'X-Finnhub-Token': self.config.FINNHUB_API_KEY}
            url = f"{self.config.FINNHUB_URL}/quote?symbol=OANDA:XAU_USD"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'current_price': data.get('c', 2000),
                    'change': data.get('d', 0),
                    'change_percent': data.get('dp', 0),
                    'high': data.get('h', 2020),
                    'low': data.get('l', 1980),
                    'open': data.get('o', 2000),
                    'timestamp': datetime.now()
                }
            else:
                return self._get_mock_gold_data()
        except Exception as e:
            st.warning(f"Error fetching gold price, using mock data: {str(e)}")
            return self._get_mock_gold_data()
    
    def get_exchange_rate(self, base: str = "USD", target: str = "IDR") -> float:
        """Ambil nilai tukar mata uang dari Fixer.io"""
        try:
            if not self.config.FIXER_API_KEY:
                return 15000  # Default rate
            
            url = f"{self.config.FIXER_URL}/latest"
            params = {
                'access_key': self.config.FIXER_API_KEY,
                'base': base,
                'symbols': target
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    return data['rates'].get(target, 15000)
            
            return 15000  # Default IDR rate
        except Exception as e:
            st.warning(f"Using default exchange rate: {str(e)}")
            return 15000
    
    def _get_mock_gold_data(self) -> Dict[str, Any]:
        """Return mock gold data for demo purposes"""
        return {
            'current_price': 2000.50,
            'change': 15.25,
            'change_percent': 0.77,
            'high': 2010.00,
            'low': 1985.00,
            'open': 1995.00,
            'timestamp': datetime.now()
        }
'''
    
    # src/core/rag_system.py
    rag_system_content = '''"""RAG (Retrieval Augmented Generation) System"""

class RAGSystem:
    """Retrieval Augmented Generation System untuk konteks haji"""
    
    def __init__(self):
        self.knowledge_base = {
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
            },
            "trend_historis": {
                "kenaikan_tahunan": 0.08,
                "pengaruh_musim": 0.05
            }
        }
    
    def retrieve_context(self, query: str) -> str:
        """Ambil konteks yang relevan berdasarkan query"""
        context = "Konteks Biaya Haji Indonesia:\\n\\n"
        
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["biaya", "harga", "cost"]):
            context += "Komponen Biaya Haji:\\n"
            for item, nilai in self.knowledge_base["biaya_haji_dasar"].items():
                context += f"- {item.replace('_', ' ').title()}: Rp {nilai:,}\\n"
        
        if any(word in query_lower for word in ["emas", "gold", "ekonomi"]):
            context += f"\\nFaktor Ekonomi:\\n"
            econ_factors = self.knowledge_base['faktor_ekonomi']
            context += f"- Korelasi emas dengan biaya haji: {econ_factors['korelasi_emas_haji']}\\n"
            context += f"- Inflasi tahunan rata-rata: {econ_factors['inflasi_tahunan']*100}%\\n"
        
        if any(word in query_lower for word in ["prediksi", "trend", "masa depan"]):
            context += f"\\nTrend Historis:\\n"
            hist_trends = self.knowledge_base['trend_historis']
            context += f"- Kenaikan biaya tahunan: {hist_trends['kenaikan_tahunan']*100}%\\n"
            context += f"- Pengaruh faktor musiman: {hist_trends['pengaruh_musim']*100}%\\n"
        
        return context
'''
    
    # src/core/agentic_ai.py
    agentic_ai_content = '''"""Agentic AI untuk analisis dan prediksi"""
import requests
import streamlit as st

class AgenticAI:
    """Agentic AI untuk analisis dan prediksi biaya haji"""
    
    def __init__(self, config, rag_system):
        self.config = config
        self.rag = rag_system
    
    def generate_response(self, prompt: str, context: str) -> str:
        """Generate response menggunakan Qwen3 via OpenRouter"""
        try:
            if not self.config.OPENROUTER_API_KEY:
                return self._generate_mock_response(prompt, context)
            
            headers = {
                "Authorization": f"Bearer {self.config.OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }
            
            full_prompt = f"""
            Konteks: {context}
            
            Pertanyaan: {prompt}
            
            Sebagai ahli ekonomi syariah dan konsultan haji, berikan analisis yang komprehensif dan prediksi yang akurat berdasarkan data yang tersedia. Sertakan faktor-faktor ekonomi yang mempengaruhi biaya haji.
            """
            
            payload = {
                "model": "qwen/qwen-2.5-72b-instruct",
                "messages": [
                    {
                        "role": "system", 
                        "content": "Anda adalah ahli ekonomi syariah dan konsultan haji yang berpengalaman dalam analisis biaya dan prediksi finansial."
                    },
                    {
                        "role": "user",
                        "content": full_prompt
                    }
                ],
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            response = requests.post(self.config.OPENROUTER_URL, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"Error dalam menggenerate response: {response.status_code}"
                
        except Exception as e:
            return self._generate_mock_response(prompt, context)
    
    def _generate_mock_response(self, prompt: str, context: str) -> str:
        """Generate mock response when API is not available"""
        return f"""
        **Analisis Mock (Demo Mode)**
        
        Berdasarkan pertanyaan Anda: "{prompt}"
        
        **Analisis:**
        - Biaya haji saat ini berkisar Rp 75-80 juta per jamaah
        - Harga emas memiliki korelasi positif dengan biaya haji (70%)
        - Inflasi tahunan rata-rata 3.5% mempengaruhi kenaikan biaya
        
        **Prediksi:**
        - Kenaikan biaya tahunan sekitar 8%
        - Faktor musiman dapat mempengaruhi 5% dari biaya
        - Volatilitas mata uang USD/IDR perlu diperhatikan
        
        **Rekomendasi:**
        - Mulai menabung sedini mungkin
        - Diversifikasi investasi termasuk emas
        - Monitor perkembangan ekonomi global
        
        *Note: Ini adalah respons demo. Masukkan OpenRouter API Key untuk analisis AI yang sesungguhnya.*
        """
'''
    
    # src/core/predictor.py
    predictor_content = '''"""Hajj cost prediction engine"""
from typing import Dict

class HajjCostPredictor:
    """Class utama untuk prediksi biaya haji"""
    
    def __init__(self, data_collector, rag_system):
        self.data_collector = data_collector
        self.rag = rag_system
    
    def calculate_base_cost(self) -> float:
        """Hitung biaya dasar haji"""
        base_costs = self.rag.knowledge_base["biaya_haji_dasar"]
        return sum(base_costs.values())
    
    def apply_gold_correlation(self, base_cost: float, gold_price: float, historical_gold: float = 2000) -> float:
        """Terapkan korelasi dengan harga emas"""
        correlation_factor = self.rag.knowledge_base["faktor_ekonomi"]["korelasi_emas_haji"]
        gold_change = (gold_price - historical_gold) / historical_gold
        cost_adjustment = base_cost * gold_change * correlation_factor
        return base_cost + cost_adjustment
    
    def predict_future_cost(self, months_ahead: int, current_cost: float) -> float:
        """Prediksi biaya di masa depan"""
        annual_growth = self.rag.knowledge_base["trend_historis"]["kenaikan_tahunan"]
        monthly_growth = annual_growth / 12
        future_cost = current_cost * (1 + monthly_growth) ** months_ahead
        return future_cost
    
    def generate_prediction_scenarios(self, gold_price: float, exchange_rate: float) -> Dict[str, float]:
        """Generate berbagai skenario prediksi"""
        base_cost = self.calculate_base_cost()
        
        scenarios = {}
        
        # Skenario konservatif
        conservative_cost = self.apply_gold_correlation(base_cost, gold_price * 0.95)
        scenarios["Konservatif"] = conservative_cost
        
        # Skenario realistis
        realistic_cost = self.apply_gold_correlation(base_cost, gold_price)
        scenarios["Realistis"] = realistic_cost
        
        # Skenario optimistis
        optimistic_cost = self.apply_gold_correlation(base_cost, gold_price * 1.05)
        scenarios["Optimistis"] = optimistic_cost
        
        return scenarios
'''
    
    files_to_create = {
        "src/core/config.py": config_content,
        "src/core/data_collector.py": data_collector_content,
        "src/core/rag_system.py": rag_system_content,
        "src/core/agentic_ai.py": agentic_ai_content,
        "src/core/predictor.py": predictor_content
    }
    
    for file_path, content in files_to_create.items():
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    print("Core files berhasil dibuat!")

def create_component_files():
    """Buat file-file component"""
    
    # src/components/sidebar.py
    sidebar_content = '''"""Sidebar component"""
import streamlit as st

def render_sidebar(config):
    """Render sidebar dengan konfigurasi API"""
    with st.sidebar:
        st.header("Konfigurasi API")
        
        # API Key inputs
        openrouter_key = st.text_input(
            "OpenRouter API Key (Qwen3)", 
            value=config.OPENROUTER_API_KEY,
            type="password",
            help="Untuk fitur AI Analysis"
        )
        
        finnhub_key = st.text_input(
            "Finnhub API Key", 
            value=config.FINNHUB_API_KEY,
            type="password",
            help="Untuk data harga emas real-time"
        )
        
        fixer_key = st.text_input(
            "Fixer.io API Key", 
            value=config.FIXER_API_KEY,
            type="password",
            help="Untuk nilai tukar mata uang"
        )
        
        # Update config if changed
        config_updated = False
        if openrouter_key != config.OPENROUTER_API_KEY:
            config.OPENROUTER_API_KEY = openrouter_key
            config_updated = True
        
        if finnhub_key != config.FINNHUB_API_KEY:
            config.FINNHUB_API_KEY = finnhub_key
            config_updated = True
            
        if fixer_key != config.FIXER_API_KEY:
            config.FIXER_API_KEY = fixer_key
            config_updated = True
        
        st.markdown("---")
        st.header("Parameter Prediksi")
        months_ahead = st.slider("Prediksi Bulan Ke Depan", 1, 36, 24)
        
        st.markdown("---")
        st.header("Informasi")
        st.info("""
        **Demo Mode**: Aplikasi dapat berjalan tanpa API key dengan data mock.
        
        **API Keys Gratis:**
        - Finnhub: 60 calls/minute
        - Fixer.io: 1000 calls/month
        - OpenRouter: Pay per use
        """)
        
        if st.button("Refresh Data"):
            st.rerun()
        
        return config_updated
'''
    
    # src/components/dashboard.py
    dashboard_content = '''"""Main dashboard component"""
import streamlit as st
import pandas as pd
from utils.visualizations import create_prediction_chart

def render_dashboard(data_collector, predictor, rag_system):
    """Render main dashboard"""
    
    # Get real-time data
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Data Real-time")
        
        # Gold price data
        with st.spinner("Mengambil data harga emas..."):
            gold_data = data_collector.get_gold_price()
        
        if gold_data:
            # Display gold metrics
            gold_col1, gold_col2, gold_col3 = st.columns(3)
            
            with gold_col1:
                st.metric(
                    "Harga Emas (USD/oz)",
                    f"${gold_data['current_price']:.2f}",
                    f"{gold_data['change']:+.2f} ({gold_data['change_percent']:+.2f}%)"
                )
            
            with gold_col2:
                st.metric("High", f"${gold_data['high']:.2f}")
            
            with gold_col3:
                st.metric("Low", f"${gold_data['low']:.2f}")
        
        # Exchange rate
        with st.spinner("Mengambil nilai tukar..."):
            exchange_rate = data_collector.get_exchange_rate()
        
        st.info(f"Nilai Tukar USD/IDR: Rp {exchange_rate:,.0f}")
    
    with col2:
        st.header("Prediksi Biaya")
        
        if gold_data:
            scenarios = predictor.generate_prediction_scenarios(
                gold_data['current_price'], 
                exchange_rate
            )
            
            for scenario, cost in scenarios.items():
                st.metric(
                    f"Skenario {scenario}",
                    f"Rp {cost:,.0f}"
                )
    
    # Prediction chart
    if gold_data:
        st.header("Grafik Prediksi Biaya Haji")
        
        scenarios = predictor.generate_prediction_scenarios(
            gold_data['current_price'], 
            exchange_rate
        )
        
        try:
            chart = create_prediction_chart(scenarios, 24)
            st.plotly_chart(chart, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating chart: {e}")
            st.info("Chart visualization sedang dalam pengembangan")
    
    # Cost breakdown
    st.header("Breakdown Biaya Haji")
    
    base_costs = rag_system.knowledge_base["biaya_haji_dasar"]
    
    # Create DataFrame
    df_costs = pd.DataFrame([
        {
            "Komponen": k.replace('_', ' ').title(), 
            "Biaya (IDR)": f"Rp {v:,}",
            "Persentase": f"{(v/sum(base_costs.values()))*100:.1f}%"
        }
        for k, v in base_costs.items()
    ])
    
    st.dataframe(df_costs, use_container_width=True)
    
    # Total cost
    total_cost = sum(base_costs.values())
    st.success(f"**Total Biaya Dasar**: Rp {total_cost:,}")
'''
    
    # src/components/ai_chat.py
    ai_chat_content = '''"""AI Chat component"""
import streamlit as st

def render_ai_chat(agentic_ai, rag_system):
    """Render AI chat interface"""
    
    st.header("Analisis RAG Agentic AI")
    
    # Pre-defined questions
    st.subheader("Pertanyaan Populer")
    
    example_questions = [
        "Bagaimana pengaruh kenaikan harga emas terhadap biaya haji?",
        "Prediksi biaya haji untuk 2 tahun ke depan?",
        "Faktor apa saja yang mempengaruhi biaya haji?",
        "Strategi menabung untuk biaya haji yang efektif?",
        "Kapan waktu terbaik untuk mendaftar haji?"
    ]
    
    for i, question in enumerate(example_questions):
        if st.button(f"Q: {question[:50]}...", key=f"q_{i}"):
            st.session_state['user_question'] = question
    
    # User input
    st.subheader("Ajukan Pertanyaan Anda")
    
    user_query = st.text_area(
        "Pertanyaan:",
        value=st.session_state.get('user_question', ''),
        placeholder="Contoh: Bagaimana pengaruh inflasi terhadap biaya haji tahun depan?",
        height=100
    )
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        analyze_button = st.button("Analisis", type="primary")
    
    with col2:
        if st.button("Clear"):
            st.session_state['user_question'] = ''
            st.rerun()
    
    if analyze_button and user_query:
        with st.spinner("AI sedang menganalisis..."):
            # Retrieve context
            context = rag_system.retrieve_context(user_query)
            
            # Add current data context (simplified for demo)
            current_data_context = """
            Data Real-time Saat Ini:
            - Harga Emas: ~$2000/oz
            - Nilai Tukar USD/IDR: ~Rp 15,000
            - Prediksi Biaya Realistis: ~Rp 75-80 juta
            """
            
            full_context = context + current_data_context
            
            # Generate AI response
            ai_response = agentic_ai.generate_response(user_query, full_context)
            
            # Display response
            st.markdown("### Analisis AI:")
            st.markdown(ai_response)
            
            # Feedback
            st.markdown("---")
            st.markdown("**Apakah analisis ini membantu?**")
            feedback_cols = st.columns(3)
            
            with feedback_cols[0]:
                if st.button("Ya"):
                    st.success("Terima kasih atas feedback Anda!")
            
            with feedback_cols[1]:
                if st.button("Tidak"):
                    st.info("Kami akan terus meningkatkan kualitas analisis")
            
            with feedback_cols[2]:
                if st.button("Saran"):
                    suggestion = st.text_input("Saran perbaikan:")
                    if suggestion:
                        st.success("Saran Anda telah dicatat!")
    
    elif analyze_button and not user_query:
        st.warning("Silakan masukkan pertanyaan terlebih dahulu.")
'''
    
    # src/utils/visualizations.py
    visualizations_content = '''"""Visualization utilities"""
import plotly.graph_objects as go
from typing import Dict

def create_prediction_chart(scenarios: Dict[str, float], months_ahead: int = 24) -> go.Figure:
    """Buat chart prediksi biaya haji"""
    months = list(range(0, months_ahead + 1))
    
    fig = go.Figure()
    
    colors = {"Konservatif": "green", "Realistis": "blue", "Optimistis": "red"}
    
    for scenario, base_cost in scenarios.items():
        annual_growth = 0.08  # 8% pertumbuhan tahunan
        monthly_growth = annual_growth / 12
        
        costs = [base_cost * (1 + monthly_growth) ** month for month in months]
        
        fig.add_trace(go.Scatter(
            x=months,
            y=costs,
            mode='lines+markers',
            name=f'Skenario {scenario}',
            line=dict(color=colors[scenario], width=3),
            hovertemplate=f'<b>{scenario}</b><br>Bulan: %{{x}}<br>Biaya: Rp %{{y:,.0f}}<extra></extra>'
        ))
    
    fig.update_layout(
        title="Prediksi Biaya Haji Indonesia",
        xaxis_title="Bulan Ke Depan",
        yaxis_title="Biaya (IDR)",
        hovermode='x unified',
        template='plotly_white',
        height=500
    )
    
    return fig
'''
    
    files_to_create = {
        "src/components/sidebar.py": sidebar_content,
        "src/components/dashboard.py": dashboard_content,
        "src/components/ai_chat.py": ai_chat_content,
        "src/utils/visualizations.py": visualizations_content
    }
    
    for file_path, content in files_to_create.items():
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    print("Component files berhasil dibuat!")

def main():
    """Main setup function"""
    print("Setting up RAG Agentic AI - Hajj Predictor Project...")
    
    create_directory_structure()
    create_core_files()
    create_component_files()
    
    print()
    print("Setup completed successfully!")
    print()
    print("Next steps:")
    print("1. pip install -r requirements.txt")
    print("2. streamlit run app.py")
    print("3. (Optional) Copy .env.example to .env and add your API keys")
    print()
    print("Enjoy your RAG Agentic AI Hajj Predictor!")

if __name__ == "__main__":
    main()