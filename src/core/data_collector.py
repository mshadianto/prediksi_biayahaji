"""Data collection from external APIs"""
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
