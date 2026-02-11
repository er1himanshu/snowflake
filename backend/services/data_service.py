"""Data loading and preprocessing service"""
import pandas as pd
import json
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import DATA_DIR


class DataService:
    """Service for loading and managing data"""
    
    @staticmethod
    def load_economic_data():
        """Load historical economic data"""
        data_path = DATA_DIR / "sample_economic_data.csv"
        return pd.read_csv(data_path)
    
    @staticmethod
    def load_sector_weights():
        """Load sector weights and interdependencies"""
        data_path = DATA_DIR / "sector_weights.json"
        with open(data_path, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def load_sentiment_data():
        """Load sentiment templates"""
        data_path = DATA_DIR / "sample_sentiment_data.json"
        with open(data_path, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def get_latest_economic_indicators():
        """Get the latest economic indicators"""
        df = DataService.load_economic_data()
        latest = df.iloc[-1].to_dict()
        
        return {
            "fuel_price_index": float(latest['fuel_price_index']),
            "tax_rate": float(latest['tax_rate']),
            "subsidy_amount_billions": float(latest['subsidy_amount_billions']),
            "interest_rate": float(latest['interest_rate']),
            "money_supply_growth": float(latest['money_supply_growth']),
            "gdp_growth": float(latest['gdp_growth']),
            "inflation_rate": float(latest['inflation_rate']),
            "unemployment_rate": float(latest['unemployment_rate']),
            "consumer_confidence_index": float(latest['consumer_confidence_index'])
        }
