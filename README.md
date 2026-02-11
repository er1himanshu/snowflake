"# ❄️ Snowflake - AI Policy Impact Simulator

<div align="center">

![VIT Vellore Hackathon 2026](https://img.shields.io/badge/VIT%20Vellore-Hackathon%202026-purple?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green?style=for-the-badge&logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Predictive Governance for Smarter Decision-Making**

*An AI-driven platform that enables policymakers to simulate policy changes and predict their economic, social, and sectoral impacts before implementation.*

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [API Docs](#-api-documentation) • [Architecture](#-architecture)

</div>

---

## 🌟 Problem Statement

Policymakers often lack predictive tools to assess the comprehensive impact of proposed policies before implementation. **Snowflake** bridges this gap by providing:

- **Real-time simulation** of policy changes (fuel prices, taxes, subsidies, wages, regulations, tariffs)
- **Multi-dimensional impact analysis** across inflation, sectors, public sentiment, and risk
- **Data-driven recommendations** to minimize negative impacts and maximize benefits
- **Comparative scenario analysis** to choose the best policy option

---

## ✨ Features

### 🎯 Core Capabilities

- **📊 Inflation Prediction** - ML-powered forecasting using Gradient Boosting Regressor
- **🏭 Sector Impact Analysis** - Simplified Leontief input-output model for 8 key sectors
- **💭 Sentiment Analysis** - NLP-based public sentiment prediction using TextBlob
- **⚠️ Risk Assessment** - Composite risk index (0-100 scale) with 4 components
- **📈 Scenario Comparison** - Compare multiple policy options side-by-side
- **🎨 Interactive Dashboard** - Modern dark-themed UI with real-time charts

### 🔬 Technical Highlights

- **Machine Learning Models**: scikit-learn (Gradient Boosting)
- **NLP Sentiment Analysis**: TextBlob with synthetic reaction generation
- **Economic Modeling**: Sector interdependencies and ripple effect calculations
- **Risk Quantification**: Multi-factor composite scoring system
- **RESTful API**: FastAPI with OpenAPI documentation
- **Modern Frontend**: Vanilla JS with Chart.js visualizations

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **scikit-learn** - Machine learning models
- **pandas & numpy** - Data processing
- **TextBlob** - Natural language processing
- **Pydantic** - Data validation

### Frontend
- **HTML5/CSS3** - Modern responsive design
- **Vanilla JavaScript** - No framework dependencies
- **Chart.js** - Interactive data visualizations
- **Glass-morphism UI** - Dark theme with backdrop blur effects

### Data & Models
- **Synthetic Economic Data** - 40+ quarters of realistic Indian economic indicators
- **Sector Interdependency Matrix** - 8 sectors with weighted relationships
- **Sentiment Templates** - Policy-specific reaction patterns

---

## 📦 Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/er1himanshu/snowflake.git
cd snowflake
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Download NLTK data (for TextBlob and sentiment analysis)**
```bash
python -c "import nltk; nltk.download('brown'); nltk.download('punkt'); nltk.download('wordnet'); nltk.download('omw-1.4')"
```

4. **Set up environment variables (optional)**
```bash
cp .env.example .env
# Edit .env if you want to change PORT or other settings
```

5. **Run the application**
```bash
python backend/app.py
```

6. **Open your browser**
```
http://localhost:8000
```

The API documentation is available at: `http://localhost:8000/api/docs`

---

## 🚀 Usage

### Single Policy Simulation

1. Select a **policy type** (e.g., Fuel Price Change)
2. Set the **magnitude** of change (e.g., +15%)
3. Choose **duration** in months (e.g., 12)
4. Select **affected sectors** (e.g., Transport, Energy)
5. Add an optional **description**
6. Click **"🚀 Run Simulation"**

The dashboard will display:
- **Inflation Impact** - Predicted rate with confidence level
- **Risk Assessment** - Composite score with component breakdown
- **Sector Analysis** - Impact on each economic sector
- **Public Sentiment** - Positive/negative/neutral distribution
- **Recommendations** - Actionable insights

### Scenario Comparison

1. Switch to **"📈 Compare Scenarios"** tab
2. Click **"➕ Add Scenario"** for each option
3. Fill in parameters for 2+ scenarios
4. Click **"📈 Compare Scenarios"**

View:
- **Ranking table** - Sorted by risk score
- **Comparison chart** - Visual side-by-side analysis
- **Recommendation** - Best option with justification

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Endpoints

#### 1. Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "models_loaded": true
}
```

#### 2. Simulate Policy
```http
POST /api/simulate
Content-Type: application/json

{
  "policy_type": "Fuel Price Change",
  "magnitude": 15.0,
  "duration_months": 12,
  "affected_sectors": ["Transport", "Energy"],
  "description": "15% fuel price increase over 12 months"
}
```

**Response:** Comprehensive simulation result with inflation impact, sector analysis, sentiment, and risk assessment.

#### 3. Compare Scenarios
```http
POST /api/compare
Content-Type: application/json

{
  "scenarios": [
    {
      "name": "Option A",
      "policy_type": "Tax Reform",
      "magnitude": 10,
      "duration_months": 12
    },
    {
      "name": "Option B",
      "policy_type": "Subsidy Change",
      "magnitude": -15,
      "duration_months": 6
    }
  ]
}
```

**Response:** Ranked comparison with recommendation.

#### 4. Get Sectors
```http
GET /api/sectors
```

Returns list of sectors, weights, and interdependencies.

#### 5. Get Policy Types
```http
GET /api/policy-types
```

Returns available policy types.

#### 6. Get Simulation History
```http
GET /api/history?limit=10
```

Returns recent simulation history.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Browser)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Dashboard   │  │   Charts.js  │  │  API Client  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────┬───────────────────────────────┘
                              │ HTTP/JSON
┌─────────────────────────────▼───────────────────────────────┐
│                    Backend (FastAPI)                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              API Routes & Schemas                     │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │                                      │
│  ┌────────────────────▼─────────────────────────────────┐  │
│  │           Policy Simulator (Orchestrator)             │  │
│  └──┬──────────────┬──────────────┬───────────────┬─────┘  │
│     │              │              │               │          │
│  ┌──▼────┐  ┌─────▼────┐  ┌─────▼─────┐  ┌──────▼──────┐ │
│  │Inflation│ │  Sector  │  │ Sentiment │  │    Risk     │ │
│  │  Model  │ │  Impact  │  │  Analyzer │  │    Index    │ │
│  │  (ML)   │ │  Model   │  │   (NLP)   │  │  Calculator │ │
│  └─────────┘ └──────────┘  └───────────┘  └─────────────┘ │
│                       │                                      │
│  ┌────────────────────▼─────────────────────────────────┐  │
│  │         Data Service (CSV/JSON Loaders)               │  │
│  └───────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### Directory Structure

```
snowflake/
├── backend/
│   ├── models/          # ML models (inflation, sector, sentiment, risk)
│   ├── services/        # Business logic (simulator, analyzers)
│   ├── api/             # API routes and schemas
│   ├── data/            # Sample datasets (CSV, JSON)
│   ├── app.py           # FastAPI application
│   └── config.py        # Configuration settings
├── frontend/
│   ├── index.html       # Main dashboard
│   ├── css/styles.css   # Dark theme styling
│   ├── js/              # JavaScript modules
│   └── assets/logo.svg  # Snowflake logo
├── tests/               # Unit tests (pytest)
├── notebooks/           # Jupyter notebooks (demos)
└── requirements.txt     # Python dependencies
```

---

## 🧪 Testing

Run unit tests:

```bash
pytest tests/ -v
```

Test coverage:
- Inflation model predictions
- Sector impact calculations
- Sentiment analysis
- Risk index computation

---

## 📊 Sample Results

### Example: Fuel Price Increase (+20%)

**Inflation Impact:**
- Predicted Rate: 7.8%
- Baseline: 5.5%
- Change: +2.3%
- Confidence: 87%

**Risk Assessment:**
- Composite Score: 62.5 (High)
- Economic Risk: 68
- Sector Disruption: 55
- Social Unrest: 71
- Inequality Impact: 48

**Most Affected Sectors:**
1. Transport (-0.65)
2. Energy (-0.58)
3. Manufacturing (-0.42)

**Public Sentiment:**
- Overall: Negative (-0.42)
- Negative Reactions: 68%
- Key Concerns: burden, inflation, expensive

**Recommendations:**
- ⚠️ HIGH RISK: Implement strong mitigation measures
- 🏭 Provide targeted support to heavily affected sectors
- 👥 Enhance public communication and stakeholder engagement
- ⚖️ Include compensatory measures for vulnerable groups

---

## 🎯 Key Algorithms

### 1. Inflation Prediction Model
- **Algorithm:** Gradient Boosting Regressor
- **Features:** fuel_price_change, tax_rate_change, subsidy_change, interest_rate, money_supply_growth
- **Training:** Historical economic data (40+ quarters)
- **Output:** Predicted inflation rate with confidence interval

### 2. Sector Impact Model
- **Approach:** Simplified Leontief input-output model
- **Method:** Direct impact + indirect ripple effects via interdependency matrix
- **Sectors:** Agriculture, Manufacturing, Services, Transport, Energy, Healthcare, Education, IT
- **Output:** Impact scores (-1 to +1) for each sector

### 3. Sentiment Analysis
- **Library:** TextBlob (NLP)
- **Process:** Generate synthetic reactions → Analyze polarity → Calculate sentiment distribution
- **Output:** Overall sentiment score, positive/negative/neutral ratios, unrest probability

### 4. Risk Index Calculator
- **Components:** 
  - Economic Risk (35% weight)
  - Sector Disruption (25%)
  - Social Unrest (25%)
  - Income Inequality (15%)
- **Scale:** 0-100
- **Categories:** Low (0-25), Moderate (26-50), High (51-75), Critical (76-100)

---

## 🤝 Contributing

This is a hackathon project, but contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Team

**Team Name:** [Your Team Name Here]

Built for **VIT Vellore Hackathon 2026**

---

## 🙏 Acknowledgments

- VIT Vellore for organizing the hackathon
- Open-source community for amazing libraries
- Economic policy research for domain knowledge
- Chart.js for beautiful visualizations

---

## 📞 Contact

For questions or feedback:
- GitHub Issues: [er1himanshu/snowflake](https://github.com/er1himanshu/snowflake/issues)
- Repository: [https://github.com/er1himanshu/snowflake](https://github.com/er1himanshu/snowflake)

---

<div align="center">

**Built with ❤️ using Python, FastAPI, and Machine Learning**

⭐ Star this repo if you find it useful!

</div>" 
