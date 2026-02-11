"""Scenario comparison service"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from services.policy_simulator import get_policy_simulator


class ScenarioComparator:
    """Service for comparing multiple policy scenarios"""
    
    def __init__(self):
        self.simulator = get_policy_simulator()
    
    def compare_scenarios(self, scenarios):
        """
        Compare multiple policy scenarios
        
        Args:
            scenarios: List of scenario dicts, each containing:
                - name: Scenario name
                - policy_type: Type of policy
                - magnitude: Magnitude of change
                - duration_months: Duration
                - affected_sectors: List of sectors (optional)
                - description: Text description (optional)
        
        Returns:
            dict: Comparative analysis with rankings
        """
        results = []
        
        # Simulate each scenario
        for scenario in scenarios:
            simulation = self.simulator.simulate_policy(
                policy_type=scenario['policy_type'],
                magnitude=scenario['magnitude'],
                duration_months=scenario['duration_months'],
                affected_sectors=scenario.get('affected_sectors'),
                description=scenario.get('description', '')
            )
            
            results.append({
                "scenario_name": scenario.get('name', f"Scenario {len(results)+1}"),
                "simulation": simulation
            })
        
        # Rank scenarios by risk score (lower is better)
        ranked_scenarios = sorted(
            results,
            key=lambda x: x['simulation']['risk_assessment']['composite_risk_score']
        )
        
        # Add rankings
        for idx, scenario in enumerate(ranked_scenarios):
            scenario['rank'] = idx + 1
        
        # Generate comparison table
        comparison_table = self._generate_comparison_table(ranked_scenarios)
        
        # Generate recommendation
        best_scenario = ranked_scenarios[0]
        recommendation = self._generate_recommendation(ranked_scenarios)
        
        return {
            "scenarios": ranked_scenarios,
            "comparison_table": comparison_table,
            "best_scenario": best_scenario['scenario_name'],
            "recommendation": recommendation
        }
    
    def _generate_comparison_table(self, ranked_scenarios):
        """Generate comparison table data"""
        table = []
        
        for scenario in ranked_scenarios:
            sim = scenario['simulation']
            table.append({
                "rank": scenario['rank'],
                "name": scenario['scenario_name'],
                "inflation_rate": sim['inflation_impact']['predicted_inflation_rate'],
                "risk_score": sim['risk_assessment']['composite_risk_score'],
                "risk_level": sim['risk_assessment']['risk_level'],
                "sentiment": sim['sentiment_analysis']['sentiment_category'],
                "negative_sentiment_pct": sim['sentiment_analysis']['negative_ratio']
            })
        
        return table
    
    def _generate_recommendation(self, ranked_scenarios):
        """Generate comparative recommendation"""
        if not ranked_scenarios:
            return "No scenarios to compare."
        
        best = ranked_scenarios[0]
        worst = ranked_scenarios[-1]
        
        best_name = best['scenario_name']
        worst_name = worst['scenario_name']
        
        best_risk = best['simulation']['risk_assessment']['composite_risk_score']
        worst_risk = worst['simulation']['risk_assessment']['composite_risk_score']
        
        recommendation = f"**Recommended Option: {best_name}**\n\n"
        recommendation += f"This scenario has the lowest risk score ({best_risk:.1f}) "
        recommendation += f"compared to {worst_name} ({worst_risk:.1f}).\n\n"
        
        # Add key differentiators
        best_inflation = best['simulation']['inflation_impact']['predicted_inflation_rate']
        best_sentiment = best['simulation']['sentiment_analysis']['sentiment_category']
        
        recommendation += f"Key advantages:\n"
        recommendation += f"- Lower predicted inflation ({best_inflation}%)\n"
        recommendation += f"- {best_sentiment} public sentiment\n"
        recommendation += f"- Better overall risk profile\n"
        
        return recommendation


# Singleton instance
_scenario_comparator_instance = None

def get_scenario_comparator():
    """Get or create the scenario comparator instance"""
    global _scenario_comparator_instance
    if _scenario_comparator_instance is None:
        _scenario_comparator_instance = ScenarioComparator()
    return _scenario_comparator_instance
