"""
Cost analysis engine
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class CostAnalyzer:
    """Main cost analysis engine"""

    def __init__(self, connectors: List[Any]):
        self.connectors = connectors
        self.usd_to_inr = 83.0  # Current conversion rate

    async def analyze_costs(
        self,
        start_date: datetime,
        end_date: datetime,
        group_by: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Analyze costs across all connected cloud providers"""

        total_analysis = {
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            },
            "currency": "INR",
            "total_cost_inr": 0.0,
            "providers": {},
            "recommendations": [],
            "potential_savings_inr": 0.0
        }

        for connector in self.connectors:
            if connector.is_authenticated():
                try:
                    provider_costs = await connector.get_cost_data(start_date, end_date)
                    total_analysis["providers"][connector.__class__.__name__] = provider_costs
                    total_analysis["total_cost_inr"] += provider_costs.get("total_cost", 0)
                except Exception as e:
                    logger.error(f"Failed to get costs from {connector.__class__.__name__}: {e}")

        # Calculate potential savings (placeholder logic)
        total_analysis["potential_savings_inr"] = total_analysis["total_cost_inr"] * 0.25  # 25% potential savings

        return total_analysis

    def convert_usd_to_inr(self, usd_amount: float) -> float:
        """Convert USD to INR"""
        return usd_amount * self.usd_to_inr

    async def get_cost_trends(self, days: int = 30) -> Dict[str, Any]:
        """Get cost trends for the specified period"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        return await self.analyze_costs(start_date, end_date)
