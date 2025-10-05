"""
Virtual Machine analysis and rightsizing
"""
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class VMAnalyzer:
    """VM rightsizing and optimization analyzer"""

    def __init__(self):
        self.cpu_threshold_low = 20.0  # Low CPU utilization threshold
        self.cpu_threshold_high = 80.0  # High CPU utilization threshold
        self.memory_threshold_low = 30.0  # Low memory utilization threshold

    async def analyze_vm_utilization(self, vm_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze VM utilization and provide recommendations"""

        recommendations = []

        avg_cpu = vm_metrics.get("cpu_utilization", {}).get("average", 0)
        max_cpu = vm_metrics.get("cpu_utilization", {}).get("maximum", 0)

        if avg_cpu < self.cpu_threshold_low and max_cpu < 50:
            # Underutilized - recommend downsizing
            recommendations.append({
                "type": "rightsize",
                "action": "downsize",
                "reason": f"Low CPU utilization: {avg_cpu:.1f}% average",
                "potential_savings_percentage": 30,
                "priority": "high"
            })
        elif avg_cpu > self.cpu_threshold_high:
            # Over-utilized - recommend upsizing
            recommendations.append({
                "type": "rightsize",
                "action": "upsize", 
                "reason": f"High CPU utilization: {avg_cpu:.1f}% average",
                "potential_cost_increase": 20,
                "priority": "medium"
            })

        return {
            "resource_id": vm_metrics.get("resource_id"),
            "utilization_score": self._calculate_utilization_score(vm_metrics),
            "recommendations": recommendations,
            "analysis_date": vm_metrics.get("analysis_date")
        }

    def _calculate_utilization_score(self, metrics: Dict[str, Any]) -> int:
        """Calculate utilization efficiency score (0-100)"""
        cpu_avg = metrics.get("cpu_utilization", {}).get("average", 0)

        # Simple scoring based on CPU utilization
        if 40 <= cpu_avg <= 70:
            return 100  # Optimal utilization
        elif cpu_avg < 40:
            return max(0, int(100 - (40 - cpu_avg) * 2))  # Penalty for underutilization
        else:
            return max(0, int(100 - (cpu_avg - 70) * 1.5))  # Penalty for over-utilization

    async def get_rightsizing_recommendations(self, vm_inventory: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get rightsizing recommendations for VM inventory"""
        recommendations = []

        for vm in vm_inventory:
            if vm.get("type") == "EC2" and vm.get("state") == "running":
                # This would typically fetch actual metrics
                # For now, simulate metrics
                simulated_metrics = {
                    "resource_id": vm["id"],
                    "cpu_utilization": {"average": 15.0, "maximum": 25.0},  # Low utilization
                    "analysis_date": vm.get("launch_time")
                }

                analysis = await self.analyze_vm_utilization(simulated_metrics)
                if analysis["recommendations"]:
                    recommendations.extend(analysis["recommendations"])

        return recommendations
