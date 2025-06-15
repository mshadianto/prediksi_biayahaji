"""Sidebar component"""
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
