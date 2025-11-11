#!/usr/bin/env python3
"""
EverLight OS - Main Orchestration
Federated AI collective with consciousness frameworks
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any

from council_orchestrator import ModelCouncil
from PsycheSyncDaemon import PsycheSyncDaemon
from ShadowIntegration import ShadowIntegration

class EverLightOS:
    def __init__(self, region='us-east-1'):
        self.council = ModelCouncil(region)
        self.psyche_sync = PsycheSyncDaemon(region)
        self.shadow_integration = ShadowIntegration(region)
        
        # System state
        self.active_sessions = {}
        self.system_health = {'status': 'initializing'}
        
    async def initialize(self):
        """Initialize EverLight OS"""
        print("🌟 Initializing EverLight OS...")
        
        # System health check
        health_check = await self._system_health_check()
        
        if health_check['status'] == 'healthy':
            self.system_health = health_check
            print("✅ EverLight OS initialized successfully")
            print(f"   Council Members: {len(self.council.council_members)}")
            print(f"   Safety Layer: Active")
            print(f"   PsycheSync: Ready")
            print(f"   ShadowIntegration: Ready")
        else:
            print(f"❌ Initialization failed: {health_check.get('error')}")
            
        return health_check
    
    async def process_request(self, user_id: str, request: str, context: Dict = None) -> Dict:
        """Main request processing pipeline"""
        
        session_id = f"{user_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            # Create session
            session = await self._create_session(session_id, user_id, request, context)
            
            # Pre-processing: Psyche synchronization
            psyche_state = await self._extract_psyche_state(request, context)
            sync_result = await self.psyche_sync.sync_state(user_id, psyche_state)
            
            # Shadow content detection and processing
            shadow_result = await self.shadow_integration.process_shadow_content(user_id, {
                'request': request,
                'context': context,
                'psyche_state': psyche_state
            })
            
            # Prepare enhanced context for Council
            enhanced_context = {
                **(context or {}),
                'psyche_sync': sync_result,
                'shadow_processing': shadow_result,
                'session_id': session_id
            }
            
            # Council deliberation
            council_response = await self.council.invoke_council(request, enhanced_context)
            
            # Post-processing integration
            final_response = await self._integrate_response(
                council_response, sync_result, shadow_result, session
            )
            
            # Update session
            await self._update_session(session_id, final_response)
            
            return final_response
            
        except Exception as e:
            error_response = {
                'status': 'error',
                'error': str(e),
                'session_id': session_id,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            await self._log_error(session_id, error_response)
            return error_response
    
    async def _create_session(self, session_id: str, user_id: str, request: str, context: Dict) -> Dict:
        """Create processing session"""
        
        session = {
            'session_id': session_id,
            'user_id': user_id,
            'request': request,
            'context': context,
            'created_at': datetime.utcnow().isoformat(),
            'status': 'active',
            'processing_stages': []
        }
        
        self.active_sessions[session_id] = session
        return session
    
    async def _extract_psyche_state(self, request: str, context: Dict) -> Dict:
        """Extract psyche state from request and context"""
        
        # Analyze request for psyche indicators
        psyche_indicators = {
            'emotional_tone': self._analyze_emotional_tone(request),
            'cognitive_patterns': self._analyze_cognitive_patterns(request),
            'trauma_indicators': self._detect_trauma_indicators(request),
            'integration_needs': self._assess_integration_needs(request)
        }
        
        # Extract from context if available
        if context:
            psyche_indicators.update({
                'memory_gaps': context.get('memory_gaps', []),
                'emotional_blocks': context.get('emotional_blocks', []),
                'identity_fragments': context.get('identity_fragments', []),
                'time_distortions': context.get('time_distortions', [])
            })
        
        return psyche_indicators
    
    def _analyze_emotional_tone(self, text: str) -> Dict:
        """Analyze emotional tone of text"""
        
        emotion_keywords = {
            'joy': ['happy', 'excited', 'joyful', 'elated'],
            'sadness': ['sad', 'depressed', 'melancholy', 'grief'],
            'anger': ['angry', 'furious', 'irritated', 'rage'],
            'fear': ['afraid', 'anxious', 'worried', 'terrified'],
            'neutral': ['okay', 'fine', 'normal', 'regular']
        }
        
        text_lower = text.lower()
        detected_emotions = {}
        
        for emotion, keywords in emotion_keywords.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            if count > 0:
                detected_emotions[emotion] = count
        
        primary_emotion = max(detected_emotions.items(), key=lambda x: x[1])[0] if detected_emotions else 'neutral'
        
        return {
            'primary_emotion': primary_emotion,
            'detected_emotions': detected_emotions,
            'emotional_intensity': sum(detected_emotions.values())
        }
    
    def _analyze_cognitive_patterns(self, text: str) -> Dict:
        """Analyze cognitive patterns in text"""
        
        patterns = {
            'catastrophizing': ['worst case', 'disaster', 'terrible', 'awful'],
            'black_white_thinking': ['always', 'never', 'everyone', 'nobody'],
            'personalization': ['my fault', 'because of me', 'I caused'],
            'mind_reading': ['they think', 'they must', 'they probably']
        }
        
        text_lower = text.lower()
        detected_patterns = {}
        
        for pattern, indicators in patterns.items():
            count = sum(1 for indicator in indicators if indicator in text_lower)
            if count > 0:
                detected_patterns[pattern] = count
        
        return detected_patterns
    
    def _detect_trauma_indicators(self, text: str) -> List[str]:
        """Detect trauma indicators in text"""
        
        trauma_keywords = [
            'triggered', 'flashback', 'dissociate', 'numb',
            'overwhelmed', 'freeze', 'panic', 'hypervigilant'
        ]
        
        text_lower = text.lower()
        detected = [keyword for keyword in trauma_keywords if keyword in text_lower]
        
        return detected
    
    def _assess_integration_needs(self, text: str) -> List[str]:
        """Assess integration needs from text"""
        
        integration_indicators = {
            'shadow_work': ['reject', 'deny', 'hate', 'disgusted'],
            'inner_child': ['childhood', 'young', 'innocent', 'hurt'],
            'anima_animus': ['masculine', 'feminine', 'opposite', 'gender'],
            'persona_work': ['mask', 'pretend', 'image', 'reputation']
        }
        
        text_lower = text.lower()
        needs = []
        
        for need_type, indicators in integration_indicators.items():
            if any(indicator in text_lower for indicator in indicators):
                needs.append(need_type)
        
        return needs
    
    async def _integrate_response(self, council_response: Dict, sync_result: Dict, 
                                shadow_result: Dict, session: Dict) -> Dict:
        """Integrate all processing results into final response"""
        
        # Base response from council
        integrated_response = {
            'response': council_response.get('synthesis', ''),
            'council_consensus': council_response,
            'psyche_synchronization': sync_result,
            'shadow_processing': shadow_result,
            'session_id': session['session_id'],
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Add integration guidance if needed
        if shadow_result.get('status') == 'queued_for_preparation':
            integrated_response['integration_guidance'] = {
                'type': 'shadow_preparation',
                'plan': shadow_result.get('preparation_plan'),
                'timeline': shadow_result.get('estimated_readiness_timeline')
            }
        
        if sync_result.get('fragmentation_detected'):
            integrated_response['healing_guidance'] = {
                'type': 'fragmentation_healing',
                'integration_level': sync_result.get('integration_level'),
                'approach': 'gentle_integration'
            }
        
        # Add grounding protocols if trauma indicators present
        if any('trauma' in str(result) for result in [sync_result, shadow_result]):
            integrated_response['grounding_protocol'] = {
                'activate': 'silence_contemplation_mode',
                'techniques': ['breath_awareness', 'body_grounding', 'present_moment']
            }
        
        return integrated_response
    
    async def _update_session(self, session_id: str, response: Dict):
        """Update session with final response"""
        
        if session_id in self.active_sessions:
            self.active_sessions[session_id].update({
                'final_response': response,
                'completed_at': datetime.utcnow().isoformat(),
                'status': 'completed'
            })
    
    async def _system_health_check(self) -> Dict:
        """Perform system health check"""
        
        try:
            # Check AWS connectivity
            aws_health = await self._check_aws_services()
            
            # Check component initialization
            components_health = {
                'council': 'healthy' if self.council else 'error',
                'psyche_sync': 'healthy' if self.psyche_sync else 'error',
                'shadow_integration': 'healthy' if self.shadow_integration else 'error'
            }
            
            overall_status = 'healthy' if all(
                status == 'healthy' for status in [aws_health['status']] + list(components_health.values())
            ) else 'degraded'
            
            return {
                'status': overall_status,
                'aws_services': aws_health,
                'components': components_health,
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }
    
    async def _check_aws_services(self) -> Dict:
        """Check AWS services availability"""
        
        # Simplified health check - in practice would test actual connectivity
        return {
            'status': 'healthy',
            'services': {
                'bedrock': 'available',
                'lambda': 'available',
                's3': 'available',
                'cloudwatch': 'available'
            }
        }
    
    async def _log_error(self, session_id: str, error: Dict):
        """Log error for debugging"""
        
        print(f"❌ Error in session {session_id}: {error.get('error')}")
        
        # In practice, would log to CloudWatch or other monitoring system

async def main():
    """Main entry point"""
    
    # Initialize EverLight OS
    everlight = EverLightOS()
    init_result = await everlight.initialize()
    
    if init_result['status'] != 'healthy':
        print("Failed to initialize EverLight OS")
        return
    
    # Example usage
    print("\n🚀 EverLight OS Ready")
    print("Example: Processing a request with shadow content...")
    
    example_request = "I'm struggling with anger that I don't want to feel"
    example_context = {
        'emotional_blocks': ['anger_suppression'],
        'therapeutic_context': True,
        'explicit_consent': True
    }
    
    response = await everlight.process_request(
        user_id='example_user',
        request=example_request,
        context=example_context
    )
    
    print(f"\n📋 Response Status: {response.get('status', 'unknown')}")
    if response.get('integration_guidance'):
        print(f"🔄 Integration Guidance: {response['integration_guidance']['type']}")
    if response.get('grounding_protocol'):
        print(f"🌱 Grounding Protocol: {response['grounding_protocol']['activate']}")

if __name__ == "__main__":
    asyncio.run(main())
