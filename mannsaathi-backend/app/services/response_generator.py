"""
Enhanced Response Generator with Multi-LLM Support
"""

import structlog
import asyncio
import os
from typing import Dict, Any, Optional
from .multi_llm_manager import MultiLLMManager, ResponseEnsembler
from .knowledge_base import MentalHealthKnowledgeBase

logger = structlog.get_logger()

class ResponseGenerator:
    """Enhanced response generator with multi-LLM support"""
    
    def __init__(self, api_key: str, config: Dict[str, str] = None):
        # Initialize multi-LLM manager
        llm_config = config or {
            'GROQ_API_KEY': api_key,
            # Add other API keys from environment
            'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
            'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY'),
            'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY'),
            'COHERE_API_KEY': os.getenv('COHERE_API_KEY'),
            'TOGETHER_API_KEY': os.getenv('TOGETHER_API_KEY'),
        }
        
        self.llm_manager = MultiLLMManager(llm_config)
        self.ensembler = ResponseEnsembler()
        self.knowledge_base = MentalHealthKnowledgeBase()
        
        logger.info("Enhanced Response Generator initialized with multi-LLM support")
    
    async def generate_response_async(
        self, 
        user_message: str, 
        emotion: str = None,
        context: dict = None
    ) -> Dict[str, Any]:
        """Generate diverse, empathetic responses asynchronously"""
        
        # Check for crisis
        crisis_info = self.knowledge_base.get_crisis_resources(user_message)
        
        if crisis_info['is_crisis']:
            return {
                'response': self._generate_crisis_response(crisis_info),
                'is_crisis': True,
                'helplines': crisis_info['helplines']
            }
        
        # Get relevant context
        relevant_context = self.knowledge_base.get_relevant_context(user_message, k=3)
        context_text = "\n".join(relevant_context) if relevant_context else None
        
        # Generate responses from multiple LLMs
        diverse_responses = await self.llm_manager.generate_diverse_responses(
            user_message=user_message,
            emotion=emotion,
            context=context_text,
            num_responses=3
        )
        
        # Ensemble into final response
        final_response = self.ensembler.ensemble_responses(diverse_responses)
        
        return {
            'response': final_response,
            'is_crisis': False,
            'alternative_responses': diverse_responses[:2] if len(diverse_responses) > 1 else None,
            'emotion': emotion,
            'context_used': bool(relevant_context)
        }
    
    def generate_response(
        self, 
        user_message: str, 
        emotion: str = None,
        context: dict = None
    ) -> str:
        """Synchronous wrapper for response generation"""
        
        try:
            # Run async function in sync context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                self.generate_response_async(user_message, emotion, context)
            )
            loop.close()
            return result['response']
        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            return self._get_fallback_response(emotion, {})
    
    def _generate_crisis_response(self, crisis_info: dict) -> str:
        """Generate immediate crisis response"""
        helplines = crisis_info['helplines']
        
        helpline_text = "\n".join([
            f"📞 {h['name']}: {h['number']} ({h['hours']})" 
            for h in helplines
        ])
        
        return f"""I hear how difficult things are right now. Please know that your feelings are valid and you're not alone.

**Immediate Support Available:**
{helpline_text}

Please reach out to these helplines - trained counselors are available 24/7 to support you. You matter and you deserve help. 💙"""
    
    def _get_fallback_response(self, emotion: str, crisis_info: dict) -> str:
        """Fallback responses when generation fails"""
        
        fallbacks = {
            'sadness': "I hear that you're feeling sad. It's okay to feel this way. Would you like to talk about what's bothering you? Remember, taking small steps can help - even just sharing your feelings is a positive step.",
            
            'anxiety': "I can sense you're feeling anxious. Let's try a simple grounding exercise: take a deep breath, look around and name 5 things you can see, 4 things you can feel, 3 things you can hear. How does that feel?",
            
            'anger': "It sounds like you're feeling frustrated. That's understandable. Sometimes taking a moment to breathe deeply can help. Would you like to share what's making you feel this way?",
            
            'default': "Thank you for sharing that with me. I'm here to listen and support you. Could you tell me more about what you're experiencing?"
        }
        
        return fallbacks.get(emotion, fallbacks['default'])