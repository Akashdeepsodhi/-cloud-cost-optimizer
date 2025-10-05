"""
Custom exceptions for Cloud Cost Optimizer
"""

class CloudCostOptimizerException(Exception):
    """Base exception class"""
    pass

class ConnectorException(CloudCostOptimizerException):
    """Exception raised by cloud connectors"""
    pass

class AuthenticationException(ConnectorException):
    """Authentication failed"""
    pass

class PermissionException(ConnectorException):
    """Insufficient permissions"""
    pass

class CostAnalysisException(CloudCostOptimizerException):
    """Exception during cost analysis"""
    pass

class OptimizationException(CloudCostOptimizerException):
    """Exception during optimization"""
    pass

class IndianComplianceException(CloudCostOptimizerException):
    """Exception related to Indian compliance"""
    pass
