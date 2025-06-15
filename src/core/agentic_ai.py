"""Agentic AI untuk analisis dan prediksi"""
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
