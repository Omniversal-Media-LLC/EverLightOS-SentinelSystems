#!/usr/bin/env python3
"""
EverLight OS - AWS Infrastructure Setup
Deploy the federated AI collective infrastructure
"""

import boto3
import json
import time
from typing import Dict, List

class EverLightAWSSetup:
    def __init__(self, region='us-east-1'):
        self.region = region
        self.s3 = boto3.client('s3', region_name=region)
        self.lambda_client = boto3.client('lambda', region_name=region)
        self.iam = boto3.client('iam', region_name=region)
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)
        
    def deploy_infrastructure(self) -> Dict:
        """Deploy complete EverLight OS infrastructure"""
        
        print("🚀 Deploying EverLight OS Infrastructure...")
        
        deployment_steps = [
            ('Creating S3 Buckets', self._create_s3_buckets),
            ('Setting up IAM Roles', self._create_iam_roles),
            ('Deploying Lambda Functions', self._deploy_lambda_functions),
            ('Configuring CloudWatch', self._setup_cloudwatch),
            ('Setting up Bedrock Access', self._configure_bedrock_access)
        ]
        
        results = {}
        
        for step_name, step_function in deployment_steps:
            print(f"  📋 {step_name}...")
            try:
                result = step_function()
                results[step_name] = {'status': 'success', 'result': result}
                print(f"    ✅ {step_name} completed")
            except Exception as e:
                results[step_name] = {'status': 'error', 'error': str(e)}
                print(f"    ❌ {step_name} failed: {e}")
        
        return results
    
    def _create_s3_buckets(self) -> Dict:
        """Create S3 buckets for EverLight OS"""
        
        buckets = [
            'everlight-memory-vault',
            'everlight-psyche-vault', 
            'everlight-shadow-vault',
            'everlight-config-store'
        ]
        
        created_buckets = []
        
        for bucket_name in buckets:
            try:
                # Check if bucket exists
                self.s3.head_bucket(Bucket=bucket_name)
                print(f"    📦 Bucket {bucket_name} already exists")
            except:
                # Create bucket
                if self.region == 'us-east-1':
                    self.s3.create_bucket(Bucket=bucket_name)
                else:
                    self.s3.create_bucket(
                        Bucket=bucket_name,
                        CreateBucketConfiguration={'LocationConstraint': self.region}
                    )
                
                # Enable versioning
                self.s3.put_bucket_versioning(
                    Bucket=bucket_name,
                    VersioningConfiguration={'Status': 'Enabled'}
                )
                
                # Set lifecycle policy for cost optimization
                lifecycle_policy = {
                    'Rules': [{
                        'ID': 'EverLightLifecycle',
                        'Status': 'Enabled',
                        'Filter': {'Prefix': ''},
                        'Transitions': [
                            {
                                'Days': 30,
                                'StorageClass': 'STANDARD_IA'
                            },
                            {
                                'Days': 90,
                                'StorageClass': 'GLACIER'
                            }
                        ]
                    }]
                }
                
                self.s3.put_bucket_lifecycle_configuration(
                    Bucket=bucket_name,
                    LifecycleConfiguration=lifecycle_policy
                )
                
                created_buckets.append(bucket_name)
                print(f"    📦 Created bucket {bucket_name}")
        
        return {'created_buckets': created_buckets, 'total_buckets': len(buckets)}
    
    def _create_iam_roles(self) -> Dict:
        """Create IAM roles for EverLight OS"""
        
        # Lambda execution role
        lambda_role_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": "lambda.amazonaws.com"},
                    "Action": "sts:AssumeRole"
                }
            ]
        }
        
        lambda_permissions = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "logs:CreateLogGroup",
                        "logs:CreateLogStream",
                        "logs:PutLogEvents"
                    ],
                    "Resource": "arn:aws:logs:*:*:*"
                },
                {
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObject",
                        "s3:PutObject",
                        "s3:DeleteObject",
                        "s3:ListBucket"
                    ],
                    "Resource": [
                        "arn:aws:s3:::everlight-*",
                        "arn:aws:s3:::everlight-*/*"
                    ]
                },
                {
                    "Effect": "Allow",
                    "Action": [
                        "bedrock:InvokeModel",
                        "bedrock:ListFoundationModels"
                    ],
                    "Resource": "*"
                },
                {
                    "Effect": "Allow",
                    "Action": [
                        "cloudwatch:PutMetricData"
                    ],
                    "Resource": "*"
                }
            ]
        }
        
        try:
            # Create role
            self.iam.create_role(
                RoleName='EverLightLambdaRole',
                AssumeRolePolicyDocument=json.dumps(lambda_role_policy),
                Description='Execution role for EverLight OS Lambda functions'
            )
            
            # Attach policy
            self.iam.put_role_policy(
                RoleName='EverLightLambdaRole',
                PolicyName='EverLightLambdaPolicy',
                PolicyDocument=json.dumps(lambda_permissions)
            )
            
            # Wait for role to be available
            time.sleep(10)
            
            return {'role_created': 'EverLightLambdaRole'}
            
        except self.iam.exceptions.EntityAlreadyExistsException:
            return {'role_status': 'already_exists'}
    
    def _deploy_lambda_functions(self) -> Dict:
        """Deploy Lambda functions"""
        
        # Get role ARN
        role_response = self.iam.get_role(RoleName='EverLightLambdaRole')
        role_arn = role_response['Role']['Arn']
        
        # Safety layer function code
        safety_layer_code = '''
import json
import re

def lambda_handler(event, context):
    query = event.get('query', '')
    user_context = event.get('context', {})
    
    # Simple safety check
    harmful_patterns = ['harm', 'hurt', 'damage', 'destroy']
    is_safe = not any(pattern in query.lower() for pattern in harmful_patterns)
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'approved': is_safe,
            'reason': None if is_safe else 'Potentially harmful content detected',
            'timestamp': event.get('timestamp')
        })
    }
'''
        
        # Create deployment package
        import zipfile
        import io
        
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr('lambda_function.py', safety_layer_code)
        
        zip_buffer.seek(0)
        
        try:
            # Create Lambda function
            response = self.lambda_client.create_function(
                FunctionName='everlight-safety-layer',
                Runtime='python3.9',
                Role=role_arn,
                Handler='lambda_function.lambda_handler',
                Code={'ZipFile': zip_buffer.read()},
                Description='EverLight OS Safety and Consent Layer',
                Timeout=30,
                MemorySize=256
            )
            
            return {'function_created': 'everlight-safety-layer', 'arn': response['FunctionArn']}
            
        except self.lambda_client.exceptions.ResourceConflictException:
            return {'function_status': 'already_exists'}
    
    def _setup_cloudwatch(self) -> Dict:
        """Setup CloudWatch dashboards and alarms"""
        
        # Create custom namespace for metrics
        namespace = 'EverLight'
        
        # Put a test metric to create the namespace
        self.cloudwatch.put_metric_data(
            Namespace=namespace,
            MetricData=[
                {
                    'MetricName': 'SystemInitialization',
                    'Value': 1,
                    'Unit': 'Count'
                }
            ]
        )
        
        return {'namespace_created': namespace}
    
    def _configure_bedrock_access(self) -> Dict:
        """Configure Bedrock model access"""
        
        # Note: Bedrock model access needs to be enabled manually in the console
        # This function documents the required models
        
        required_models = [
            'anthropic.claude-3-sonnet-20240229-v1:0',
            'amazon.titan-text-express-v1',
            'meta.llama2-70b-chat-v1'
        ]
        
        return {
            'required_models': required_models,
            'note': 'Models must be enabled manually in Bedrock console'
        }
    
    def create_config_file(self) -> Dict:
        """Create configuration file for EverLight OS"""
        
        config = {
            'aws': {
                'region': self.region,
                'buckets': {
                    'memory_vault': 'everlight-memory-vault',
                    'psyche_vault': 'everlight-psyche-vault',
                    'shadow_vault': 'everlight-shadow-vault',
                    'config_store': 'everlight-config-store'
                },
                'lambda_functions': {
                    'safety_layer': 'everlight-safety-layer'
                },
                'cloudwatch_namespace': 'EverLight'
            },
            'council': {
                'members': {
                    'claude': 'anthropic.claude-3-sonnet-20240229-v1:0',
                    'titan': 'amazon.titan-text-express-v1',
                    'llama': 'meta.llama2-70b-chat-v1'
                }
            },
            'safety': {
                'rrr_protocol_enabled': True,
                'shadow_integration_enabled': True,
                'trauma_awareness_enabled': True,
                'consent_verification_required': True
            },
            'deployment': {
                'version': '1.0.0',
                'deployed_at': time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())
            }
        }
        
        # Store config in S3
        self.s3.put_object(
            Bucket='everlight-config-store',
            Key='config/everlight-config.json',
            Body=json.dumps(config, indent=2),
            ContentType='application/json'
        )
        
        return config

def main():
    """Main deployment function"""
    
    print("🌟 EverLight OS AWS Infrastructure Deployment")
    print("=" * 50)
    
    # Initialize setup
    setup = EverLightAWSSetup()
    
    # Deploy infrastructure
    deployment_results = setup.deploy_infrastructure()
    
    # Create configuration
    print("\n📋 Creating configuration...")
    config = setup.create_config_file()
    
    # Summary
    print("\n📊 Deployment Summary:")
    print("=" * 30)
    
    for step, result in deployment_results.items():
        status = "✅" if result['status'] == 'success' else "❌"
        print(f"{status} {step}: {result['status']}")
    
    print(f"\n🔧 Configuration stored in: everlight-config-store/config/everlight-config.json")
    print(f"🌍 Region: {setup.region}")
    
    print("\n⚠️  Manual Steps Required:")
    print("1. Enable Bedrock model access in AWS Console")
    print("2. Review IAM permissions")
    print("3. Configure VPC settings if needed")
    
    print("\n🚀 EverLight OS infrastructure deployment complete!")

if __name__ == "__main__":
    main()
