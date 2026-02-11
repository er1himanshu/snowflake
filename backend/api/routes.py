"""API route definitions"""
from fastapi import APIRouter, HTTPException
from typing import List
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from api.schemas import (
    PolicyInput,
    SimulationResult,
    CompareRequest,
    ComparisonResult,
    HealthResponse
)
from services.policy_simulator import get_policy_simulator
from services.scenario_comparator import get_scenario_comparator
from services.data_service import DataService
from config import SECTORS, POLICY_TYPES

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "models_loaded": True
    }


@router.post("/simulate", response_model=SimulationResult)
async def simulate_policy(policy_input: PolicyInput):
    """
    Run a single policy simulation
    
    Args:
        policy_input: Policy parameters
    
    Returns:
        Comprehensive simulation results
    """
    try:
        simulator = get_policy_simulator()
        
        result = simulator.simulate_policy(
            policy_type=policy_input.policy_type,
            magnitude=policy_input.magnitude,
            duration_months=policy_input.duration_months,
            affected_sectors=policy_input.affected_sectors,
            description=policy_input.description
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/compare", response_model=ComparisonResult)
async def compare_scenarios(compare_request: CompareRequest):
    """
    Compare multiple policy scenarios
    
    Args:
        compare_request: List of scenarios to compare
    
    Returns:
        Comparative analysis with rankings
    """
    try:
        if len(compare_request.scenarios) < 2:
            raise HTTPException(
                status_code=400,
                detail="At least 2 scenarios required for comparison"
            )
        
        comparator = get_scenario_comparator()
        
        # Convert Pydantic models to dicts
        scenarios = [s.dict() for s in compare_request.scenarios]
        
        result = comparator.compare_scenarios(scenarios)
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sectors")
async def get_sectors():
    """
    Get list of available sectors and their weights
    
    Returns:
        Sector information
    """
    try:
        data_service = DataService()
        sector_data = data_service.load_sector_weights()
        
        return {
            "sectors": SECTORS,
            "weights": sector_data['weights'],
            "interdependencies": sector_data['interdependencies']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/policy-types")
async def get_policy_types():
    """
    Get list of available policy types
    
    Returns:
        List of policy types
    """
    return {
        "policy_types": POLICY_TYPES
    }


@router.get("/history")
async def get_simulation_history(limit: int = 10):
    """
    Get recent simulation history
    
    Args:
        limit: Number of recent simulations to return
    
    Returns:
        List of recent simulations
    """
    try:
        simulator = get_policy_simulator()
        history = simulator.get_simulation_history(limit)
        
        return {
            "count": len(history),
            "simulations": history
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/economic-indicators")
async def get_economic_indicators():
    """
    Get latest economic indicators
    
    Returns:
        Current economic indicators
    """
    try:
        data_service = DataService()
        indicators = data_service.get_latest_economic_indicators()
        
        return indicators
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
