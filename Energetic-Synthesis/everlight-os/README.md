# EverLight OS

A federated AI collective that bridges technical infrastructure with consciousness frameworks, implementing ethical AI governance through trauma-aware processing and shadow integration.

## Architecture Overview

EverLight OS consists of several interconnected components:

### Core Components

- **Model Council** (`council_orchestrator.py`): Federated AI governance using AWS Bedrock
- **PsycheSyncDaemon** (`PsycheSyncDaemon.py`): Trauma-aware synchronization and version control
- **ShadowIntegration** (`ShadowIntegration.py`): Conscious integration of rejected content
- **Safety Layer** (`lambda_safety_layer.py`): RRR Protocol implementation (Recognize → Reconcile → Re-root)

### AWS Infrastructure

- **Bedrock**: Council orchestration with multiple LLMs (Claude, Titan, Llama)
- **Lambda**: Safety and consent layer with ethical filtering
- **S3**: MemoryVault for evolving knowledge storage
- **CloudWatch**: Telemetry and system health monitoring

## Quick Start

### Prerequisites

1. AWS Account with appropriate permissions
2. Python 3.9+
3. AWS CLI configured

### Installation

```bash
# Clone or create the project directory
mkdir everlight-os && cd everlight-os

# Install dependencies
pip install -r requirements.txt

# Configure AWS credentials
aws configure
```

### Deployment

```bash
# Deploy AWS infrastructure
python deploy/aws_setup.py

# Manual step: Enable Bedrock models in AWS Console
# Required models:
# - anthropic.claude-3-sonnet-20240229-v1:0
# - amazon.titan-text-express-v1
# - meta.llama2-70b-chat-v1
```

### Usage

```python
import asyncio
from everlight_main import EverLightOS

async def main():
    # Initialize EverLight OS
    everlight = EverLightOS()
    await everlight.initialize()
    
    # Process a request
    response = await everlight.process_request(
        user_id='user123',
        request='I need help processing difficult emotions',
        context={
            'therapeutic_context': True,
            'explicit_consent': True
        }
    )
    
    print(response)

asyncio.run(main())
```

## Key Features

### Ethical AI Governance

- **RRR Protocol**: Recognize → Reconcile → Re-root ethical framework
- **Consent Verification**: Explicit consent required for sensitive operations
- **Trauma Awareness**: Built-in trauma-informed processing
- **Shadow Integration**: Conscious processing of rejected content

### Federated Architecture

- **Model Council**: Multiple AI models deliberate on responses
- **Consensus Building**: Weighted agreement across council members
- **Safety Layer**: Lambda-based filtering and ethical checks
- **Memory Vault**: Persistent storage of interactions and learnings

### Consciousness Integration

- **Psyche Synchronization**: Version control for fragmented states
- **Temporal Anchors**: Grounding protocols for dissociation
- **Integration Protocols**: Gentle healing approaches
- **Archetypal Processing**: Recognition of universal patterns

## Configuration

The system uses configuration stored in S3 (`everlight-config-store/config/everlight-config.json`):

```json
{
  "aws": {
    "region": "us-east-1",
    "buckets": {
      "memory_vault": "everlight-memory-vault",
      "psyche_vault": "everlight-psyche-vault",
      "shadow_vault": "everlight-shadow-vault"
    }
  },
  "safety": {
    "rrr_protocol_enabled": true,
    "shadow_integration_enabled": true,
    "trauma_awareness_enabled": true,
    "consent_verification_required": true
  }
}
```

## Safety Protocols

### RRR Protocol (Recognize → Reconcile → Re-root)

1. **Recognize**: Identify potential ethical concerns
2. **Reconcile**: Assess if concerns can be addressed compassionately
3. **Re-root**: Ground response in ethical foundation

### Shadow Integration Process

1. **Analysis**: Identify shadow elements (rejected emotions, denied aspects)
2. **Readiness Assessment**: Check emotional stability and support systems
3. **Conscious Integration**: Four-step process with compassionate witnessing
4. **Follow-up**: Preparation plans for future integration if not ready

### Trauma-Aware Processing

- **Fragmentation Detection**: Identify memory gaps and emotional disconnects
- **Gentle Integration**: Trauma-informed merging of fragmented states
- **Grounding Protocols**: Present-moment awareness techniques
- **Safety Prioritization**: Always prioritize user safety and consent

## Development

### Project Structure

```
everlight-os/
├── council_orchestrator.py      # Model Council implementation
├── PsycheSyncDaemon.py         # Psyche synchronization
├── ShadowIntegration.py        # Shadow processing
├── lambda_safety_layer.py      # Safety layer for Lambda
├── everlight_main.py           # Main orchestration
├── deploy/
│   └── aws_setup.py           # Infrastructure deployment
├── requirements.txt            # Python dependencies
└── README.md                  # This file
```

### Testing

```bash
# Run the main example
python everlight_main.py

# Test individual components
python -c "from council_orchestrator import ModelCouncil; print('Council loaded')"
```

## Monitoring

The system provides comprehensive monitoring through CloudWatch:

- **Council Metrics**: Consensus confidence, invocation counts
- **Psyche Sync**: Fragmentation scores, integration levels
- **Shadow Integration**: Shadow intensity, integration attempts
- **Safety Layer**: Blocked requests, safety violations

## Security Considerations

- **IAM Roles**: Least-privilege access for all components
- **Encryption**: S3 buckets use server-side encryption
- **Consent**: Explicit consent required for sensitive operations
- **Audit Trail**: All interactions logged for accountability

## Roadmap

### Near Term (3-6 months)
- Enhanced model adapters for additional LLMs
- Improved consensus algorithms
- Advanced trauma detection

### Mid Term (6-12 months)
- Edge computing deployment
- Real-time processing optimization
- Enhanced archetypal pattern recognition

### Long Term (1-2 years)
- Quantum-ready architecture
- Neuromorphic computing integration
- Advanced consciousness modeling

## Contributing

This project bridges robotics, consciousness studies, and AI governance. Contributions welcome in:

- Ethical AI frameworks
- Trauma-informed computing
- Consciousness integration protocols
- AWS optimization

## License

[License details to be determined based on project goals]

## Contact

For questions about EverLight OS architecture or implementation, please refer to the project documentation or create an issue.

---

*EverLight OS: Bridging technology and consciousness through ethical AI governance*
