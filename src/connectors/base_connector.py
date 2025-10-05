"""
Base connector class for cloud cost optimization
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging

class BaseCloudConnector(ABC):
    """Abstract base class for all cloud provider connectors"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self._client = None
        self._authenticated = False

    @abstractmethod
    async def authenticate(self) -> bool:
        """Authenticate with the cloud provider"""
        pass

    @abstractmethod
    async def get_cost_data(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Retrieve cost data for the specified date range"""
        pass

    @abstractmethod
    async def get_resource_inventory(self) -> List[Dict[str, Any]]:
        """Get inventory of all resources"""
        pass

    @abstractmethod
    async def get_utilization_metrics(self, resource_id: str, days: int = 30) -> Dict[str, Any]:
        """Get resource utilization metrics"""
        pass

    @abstractmethod
    async def apply_optimization(self, recommendation: Dict[str, Any]) -> Dict[str, Any]:
        """Apply an optimization recommendation"""
        pass

    def is_authenticated(self) -> bool:
        """Check if connector is authenticated"""
        return self._authenticated

    async def validate_permissions(self) -> Dict[str, bool]:
        """Validate required permissions"""
        permissions = {
            'cost_read': False,
            'resource_read': False,
            'resource_modify': False,
            'billing_read': False
        }

        try:
            return await self._check_permissions()
        except Exception as e:
            self.logger.error(f"Permission validation failed: {e}")
            return permissions

    @abstractmethod
    async def _check_permissions(self) -> Dict[str, bool]:
        """Provider-specific permission checks"""
        pass
