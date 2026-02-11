"""Application configuration settings"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
FRONTEND_DIR = BASE_DIR.parent / "frontend"

# Server configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Model configuration
INFLATION_MODEL_FEATURES = [
    "fuel_price_change",
    "tax_rate_change",
    "subsidy_change",
    "interest_rate",
    "money_supply_growth"
]

# Sectors configuration
SECTORS = [
    "Agriculture",
    "Manufacturing", 
    "Services",
    "Transport",
    "Energy",
    "Healthcare",
    "Education",
    "IT"
]

# Risk index weights
RISK_WEIGHTS = {
    "economic_risk": 0.35,
    "sector_disruption_risk": 0.25,
    "social_unrest_probability": 0.25,
    "income_inequality_impact": 0.15
}

# Policy types
POLICY_TYPES = [
    "Fuel Price Change",
    "Tax Reform",
    "Subsidy Change",
    "Minimum Wage Change",
    "Environmental Regulation",
    "Import/Export Tariff"
]
