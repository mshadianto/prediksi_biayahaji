"""Configuration management for the application"""
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
