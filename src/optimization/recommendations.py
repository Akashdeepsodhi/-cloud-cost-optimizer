"""
Cost optimization recommendations engine
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class RecommendationEngine:
    """Generate cost optimization recommendations"""

    def __init__(self):
        self.savings_priorities = {
            "high": {"min_savings": 10000, "confidence": 0.9},  # ₹10K+ savings, 90% confidence
            "medium": {"min_savings": 5000, "confidence": 0.7},  # ₹5K+ savings, 70% confidence  
            "low": {"min_savings": 1000, "confidence": 0.5}     # ₹1K+ savings, 50% confidence
        }

    async def generate_recommendations(
        self,
        cost_analysis: Dict[str, Any],
        resource_inventory: List[Dict[str, Any]],
        utilization_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate comprehensive cost optimization recommendations"""

        recommendations = []

        # VM rightsizing recommendations
        vm_recommendations = await self._analyze_vm_rightsizing(resource_inventory, utilization_data)
        recommendations.extend(vm_recommendations)

        # Storage optimization recommendations  
        storage_recommendations = await self._analyze_storage_optimization(resource_inventory)
        recommendations.extend(storage_recommendations)

        # Reserved Instance recommendations
        ri_recommendations = await self._analyze_reserved_instances(cost_analysis, resource_inventory)
        recommendations.extend(ri_recommendations)

        # Sort by potential savings
        recommendations.sort(key=lambda x: x.get("estimated_monthly_savings_inr", 0), reverse=True)

        return recommendations

    async def _analyze_vm_rightsizing(
        self,
        inventory: List[Dict[str, Any]],
        utilization: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Analyze VM rightsizing opportunities"""

        recommendations = []

        for resource in inventory:
            if resource.get("type") == "EC2" and resource.get("state") == "running":
                # Simulate low utilization for demo
                recommendation = {
                    "id": f"rightsize_{resource['id']}",
                    "type": "rightsize",
                    "resource_id": resource["id"],
                    "resource_type": "EC2",
                    "current_instance_type": resource.get("instance_type"),
                    "recommended_instance_type": self._get_smaller_instance_type(resource.get("instance_type")),
                    "reason": "Low CPU utilization (avg: 15%)",
                    "estimated_monthly_savings_inr": 8500,  # ₹8,500 savings
                    "confidence": 0.85,
                    "priority": "high",
                    "implementation_effort": "low",
                    "risk_level": "low",
                    "created_at": datetime.now().isoformat()
                }
                recommendations.append(recommendation)

        return recommendations

    async def _analyze_storage_optimization(self, inventory: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze storage optimization opportunities"""

        recommendations = []

        for resource in inventory:
            if resource.get("type") == "EBS":
                attachments = resource.get("attachments", [])

                if not attachments:  # Unattached volume
                    recommendation = {
                        "id": f"storage_{resource['id']}",
                        "type": "delete_unused_storage",
                        "resource_id": resource["id"],
                        "resource_type": "EBS",
                        "reason": "Unattached EBS volume",
                        "estimated_monthly_savings_inr": 3200,  # ₹3,200 savings
                        "confidence": 0.95,
                        "priority": "high",
                        "implementation_effort": "low",
                        "risk_level": "low",
                        "created_at": datetime.now().isoformat()
                    }
                    recommendations.append(recommendation)

        return recommendations

    async def _analyze_reserved_instances(
        self,
        cost_analysis: Dict[str, Any],
        inventory: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Analyze Reserved Instance opportunities"""

        recommendations = []

        running_instances = [r for r in inventory if r.get("type") == "EC2" and r.get("state") == "running"]

        if len(running_instances) >= 3:  # Minimum for RI benefit
            recommendation = {
                "id": "reserved_instances_001",
                "type": "reserved_instances",
                "resource_count": len(running_instances),
                "resource_type": "EC2",
                "reason": f"{len(running_instances)} running instances suitable for Reserved Instances",
                "estimated_monthly_savings_inr": 15000,  # ₹15,000 savings
                "confidence": 0.8,
                "priority": "medium",
                "implementation_effort": "medium",
                "risk_level": "low",
                "commitment_period": "1 year",
                "created_at": datetime.now().isoformat()
            }
            recommendations.append(recommendation)

        return recommendations

    def _get_smaller_instance_type(self, current_type: str) -> str:
        """Get recommended smaller instance type"""

        # Simple mapping for demo - in production, use more sophisticated logic
        downsize_map = {
            "t3.medium": "t3.small",
            "t3.large": "t3.medium", 
            "m5.large": "t3.medium",
            "m5.xlarge": "m5.large",
            "c5.large": "t3.medium"
        }

        return downsize_map.get(current_type, current_type)

    async def calculate_total_potential_savings(self, recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate total potential savings from all recommendations"""

        total_monthly_savings = sum(r.get("estimated_monthly_savings_inr", 0) for r in recommendations)
        total_annual_savings = total_monthly_savings * 12

        high_priority_count = len([r for r in recommendations if r.get("priority") == "high"])
        medium_priority_count = len([r for r in recommendations if r.get("priority") == "medium"])
        low_priority_count = len([r for r in recommendations if r.get("priority") == "low"])

        return {
            "total_recommendations": len(recommendations),
            "estimated_monthly_savings_inr": total_monthly_savings,
            "estimated_annual_savings_inr": total_annual_savings,
            "priority_breakdown": {
                "high": high_priority_count,
                "medium": medium_priority_count,
                "low": low_priority_count
            },
            "currency": "INR",
            "generated_at": datetime.now().isoformat()
        }
