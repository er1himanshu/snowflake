"""Pydantic schemas for API request and response validation"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class PolicyInput(BaseModel):
    """Schema for policy input request"""
    policy_type: str = Field(..., description="Type of policy change")
    magnitude: float = Field(..., description="Magnitude of change in percentage")
    duration_months: int = Field(..., description="Duration of policy effect in months")
    affected_sectors: Optional[List[str]] = Field(None, description="List of affected sectors")
    description: Optional[str] = Field("", description="Policy description")


class InflationImpact(BaseModel):
    """Schema for inflation impact response"""
    predicted_inflation_rate: float
    confidence: float
    baseline_inflation: float
    change_from_baseline: float


class SectorImpact(BaseModel):
    """Schema for sector impact analysis"""
    sector_impacts: Dict[str, float]
    most_affected: List[Dict[str, Any]]
    overall_economic_impact: float
    positive_sectors: List[str]
    negative_sectors: List[str]


class SentimentAnalysis(BaseModel):
    """Schema for sentiment analysis response"""
    overall_sentiment_score: float
    positive_ratio: float
    negative_ratio: float
    neutral_ratio: float
    sentiment_category: str
    key_concerns: List[str]
    social_unrest_probability: float
    sample_reactions: List[str]


class RiskComponent(BaseModel):
    """Schema for risk components"""
    economic_risk: float
    sector_disruption_risk: float
    social_unrest_risk: float
    income_inequality_risk: float


class RiskAssessment(BaseModel):
    """Schema for risk assessment response"""
    composite_risk_score: float
    risk_level: str
    components: RiskComponent
    recommendations: List[str]


class SimulationSummary(BaseModel):
    """Schema for simulation summary"""
    quick_stats: Dict[str, Any]
    key_findings: List[str]


class SimulationResult(BaseModel):
    """Schema for complete simulation result"""
    policy_info: Dict[str, Any]
    inflation_impact: Dict[str, Any]
    sector_impacts: Dict[str, Any]
    sentiment_analysis: Dict[str, Any]
    risk_assessment: Dict[str, Any]
    recommendations: List[str]
    summary: Dict[str, Any]


class ScenarioInput(BaseModel):
    """Schema for a single scenario in comparison"""
    name: str = Field(..., description="Scenario name")
    policy_type: str
    magnitude: float
    duration_months: int
    affected_sectors: Optional[List[str]] = None
    description: Optional[str] = ""


class CompareRequest(BaseModel):
    """Schema for scenario comparison request"""
    scenarios: List[ScenarioInput] = Field(..., description="List of scenarios to compare")


class ComparisonResult(BaseModel):
    """Schema for scenario comparison result"""
    scenarios: List[Dict[str, Any]]
    comparison_table: List[Dict[str, Any]]
    best_scenario: str
    recommendation: str


class HealthResponse(BaseModel):
    """Schema for health check response"""
    status: str
    version: str
    models_loaded: bool
