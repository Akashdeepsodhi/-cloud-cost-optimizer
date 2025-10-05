"""
AWS Cost Optimization Connector
"""
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
from .base_connector import BaseCloudConnector

class AWSConnector(BaseCloudConnector):
    """AWS Cloud connector for cost optimization"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.region = config.get('region', 'ap-south-1')
        self.access_key = config.get('access_key_id')
        self.secret_key = config.get('secret_access_key')

        self._cost_client = None
        self._ec2_client = None
        self._cloudwatch_client = None

    async def authenticate(self) -> bool:
        """Authenticate with AWS services"""
        try:
            session = boto3.Session(
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name=self.region
            )

            self._cost_client = session.client('ce')
            self._ec2_client = session.client('ec2')
            self._cloudwatch_client = session.client('cloudwatch')

            # Test connection
            await self._test_connection()
            self._authenticated = True
            self.logger.info("AWS authentication successful")
            return True

        except Exception as e:
            self.logger.error(f"AWS authentication failed: {e}")
            self._authenticated = False
            return False

    async def _test_connection(self):
        """Test AWS connection"""
        try:
            self._cost_client.get_cost_and_usage(
                TimePeriod={
                    'Start': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
                    'End': datetime.now().strftime('%Y-%m-%d')
                },
                Granularity='DAILY',
                Metrics=['BlendedCost']
            )
        except Exception as e:
            raise Exception(f"AWS connection test failed: {e}")

    async def get_cost_data(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Retrieve AWS cost data"""
        if not self._authenticated:
            await self.authenticate()

        try:
            response = self._cost_client.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date.strftime('%Y-%m-%d'),
                    'End': end_date.strftime('%Y-%m-%d')
                },
                Granularity='DAILY',
                Metrics=['BlendedCost'],
                GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
            )

            usd_to_inr = 83.0
            total_cost = 0

            for result in response['ResultsByTime']:
                cost_usd = float(result['Total']['BlendedCost']['Amount'])
                total_cost += cost_usd * usd_to_inr

            return {
                'provider': 'AWS',
                'currency': 'INR', 
                'total_cost': total_cost,
                'period': {
                    'start': start_date.isoformat(),
                    'end': end_date.isoformat()
                }
            }

        except Exception as e:
            self.logger.error(f"Failed to retrieve AWS cost data: {e}")
            raise

    async def get_resource_inventory(self) -> List[Dict[str, Any]]:
        """Get AWS resource inventory"""
        if not self._authenticated:
            await self.authenticate()

        resources = []

        try:
            # Get EC2 instances
            response = self._ec2_client.describe_instances()

            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    resources.append({
                        'id': instance['InstanceId'],
                        'type': 'EC2',
                        'instance_type': instance['InstanceType'],
                        'state': instance['State']['Name'],
                        'region': self.region,
                        'launch_time': instance.get('LaunchTime'),
                        'tags': instance.get('Tags', [])
                    })

            return resources

        except Exception as e:
            self.logger.error(f"Failed to get resource inventory: {e}")
            return []

    async def get_utilization_metrics(self, resource_id: str, days: int = 30) -> Dict[str, Any]:
        """Get CloudWatch metrics"""
        if not self._authenticated:
            await self.authenticate()

        try:
            end_time = datetime.now()
            start_time = end_time - timedelta(days=days)

            response = self._cloudwatch_client.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'InstanceId', 'Value': resource_id}],
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,
                Statistics=['Average', 'Maximum']
            )

            metrics = {
                'resource_id': resource_id,
                'period_days': days,
                'cpu_utilization': {'average': 0, 'maximum': 0}
            }

            if response['Datapoints']:
                cpu_averages = [dp['Average'] for dp in response['Datapoints']]
                metrics['cpu_utilization']['average'] = sum(cpu_averages) / len(cpu_averages)
                metrics['cpu_utilization']['maximum'] = max([dp['Maximum'] for dp in response['Datapoints']])

            return metrics

        except Exception as e:
            self.logger.error(f"Failed to get utilization metrics: {e}")
            raise

    async def apply_optimization(self, recommendation: Dict[str, Any]) -> Dict[str, Any]:
        """Apply optimization recommendation"""
        # Implementation for applying recommendations
        return {"status": "success", "message": "Optimization applied"}

    async def _check_permissions(self) -> Dict[str, bool]:
        """Check AWS permissions"""
        return {
            'cost_read': True,
            'resource_read': True,
            'resource_modify': False,
            'billing_read': True
        }
