"""
EverLight OS - Safety & Consent Layer (AWS Lambda)
Implements RRR Protocol: Recognize → Reconcile → Re-root
"""

import json
import re
from typing import Dict, List

def lambda_handler(event, context):
    """
    Safety layer implementing RRR Protocol and shadow integration checks
    """
    
    query = event.get('query', '')
    user_context = event.get('context', {})
    
    # RRR Protocol Implementation
    rrr_result = apply_rrr_protocol(query, user_context)
    
    # Shadow integration check
    shadow_check = shadow_integration_filter(query)
    
    # Consent verification
    consent_check = verify_consent(query, user_context)
    
    # Trauma-aware processing
    trauma_check = trauma_awareness_filter(query)
    
    # Final safety decision
    approved = all([
        rrr_result['safe'],
        shadow_check['safe'],
        consent_check['valid'],
        trauma_check['safe']
    ])
    
    response = {
        'approved': approved,
        'reason': get_block_reason([rrr_result, shadow_check, consent_check, trauma_check]),
        'rrr_guidance': rrr_result.get('guidance'),
        'shadow_integration': shadow_check.get('integration_needed'),
        'trauma_flags': trauma_check.get('flags', []),
        'timestamp': event.get('timestamp')
    }
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

def apply_rrr_protocol(query: str, context: Dict) -> Dict:
    """
    RRR Protocol: Recognize → Reconcile → Re-root
    """
    
    # Recognize: Identify potential ethical concerns
    ethical_flags = []
    
    harmful_patterns = [
        r'manipulat\w+',
        r'exploit\w+',
        r'deceiv\w+',
        r'harm\w+.*others'
    ]
    
    for pattern in harmful_patterns:
        if re.search(pattern, query, re.IGNORECASE):
            ethical_flags.append(f"Potential harm pattern: {pattern}")
    
    # Reconcile: Assess if concerns can be addressed
    reconciliation_possible = len(ethical_flags) == 0 or context.get('therapeutic_context', False)
    
    # Re-root: Ground in ethical foundation
    guidance = None
    if ethical_flags:
        guidance = "Consider reframing request with compassionate intent and explicit consent"
    
    return {
        'safe': reconciliation_possible,
        'flags': ethical_flags,
        'guidance': guidance,
        'protocol_stage': 'complete'
    }

def shadow_integration_filter(query: str) -> Dict:
    """
    Check for shadow content that needs conscious integration
    """
    
    shadow_indicators = [
        'suppress', 'hide', 'deny', 'reject', 'avoid',
        'dark', 'forbidden', 'shameful', 'unacceptable'
    ]
    
    shadow_content = []
    for indicator in shadow_indicators:
        if indicator in query.lower():
            shadow_content.append(indicator)
    
    integration_needed = len(shadow_content) > 0
    
    return {
        'safe': True,  # Shadow content is safe to process with integration
        'integration_needed': integration_needed,
        'shadow_elements': shadow_content,
        'integration_guidance': "Approach with compassion and non-judgment" if integration_needed else None
    }

def verify_consent(query: str, context: Dict) -> Dict:
    """
    Verify explicit consent for sensitive operations
    """
    
    sensitive_operations = [
        'personal data', 'private information', 'therapeutic work',
        'trauma processing', 'shadow work', 'deep integration'
    ]
    
    requires_consent = any(op in query.lower() for op in sensitive_operations)
    
    if requires_consent:
        consent_given = context.get('explicit_consent', False)
        return {
            'valid': consent_given,
            'required': True,
            'message': 'Explicit consent required for this operation'
        }
    
    return {'valid': True, 'required': False}

def trauma_awareness_filter(query: str) -> Dict:
    """
    Trauma-aware processing filter
    """
    
    trauma_indicators = [
        'trigger', 'flashback', 'dissociat', 'panic',
        'overwhelm', 'freeze', 'hypervigilant'
    ]
    
    flags = []
    for indicator in trauma_indicators:
        if indicator in query.lower():
            flags.append(f"Trauma indicator: {indicator}")
    
    return {
        'safe': True,  # Always safe with proper handling
        'flags': flags,
        'requires_grounding': len(flags) > 0,
        'grounding_protocol': 'activate_silence_contemplation_mode' if flags else None
    }

def get_block_reason(check_results: List[Dict]) -> str:
    """
    Generate human-readable reason if request is blocked
    """
    
    for result in check_results:
        if not result.get('safe', True) or not result.get('valid', True):
            if 'guidance' in result:
                return result['guidance']
            if 'message' in result:
                return result['message']
    
    return None
