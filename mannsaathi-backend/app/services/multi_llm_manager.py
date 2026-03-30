"""
Multi-LLM Manager - Orchestrates multiple LLMs for diverse responses
"""

import structlog
import asyncio
from typing import List, Dict, Any, Optional
from enum import Enum
import random

# Import different LLM providers
import openai
import anthropic
import google.generativeai as genai
import cohere
import together
from groq import Groq

logger = structlog.get_logger()

class LLMProvider(Enum):
    GROQ = "groq"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    COHERE = "cohere"
    TOGETHER = "together"

class ResponseStyle(Enum):
    EMPATHETIC = "empathetic"
    PRACTICAL = "practical"
    CULTURAL = "cultural"
    HOLISTIC = "holistic"
    CONCISE = "concise"
    DETAILED = "detailed"

class MultiLLMManager:
    """Manages multiple LLMs for diverse, empathetic responses"""
    
    def __init__(self, config: Dict[str, str]):
        self.config = config
        self.clients = {}
        self.initialize_clients()
        
        # Define provider strengths
        self.provider_strengths = {
            LLMProvider.GROQ: ["speed", "code_mixed", "hinglish", "cost_effective"],
            LLMProvider.OPENAI: ["empathy", "nuance", "creativity", "emotional_depth"],
            LLMProvider.ANTHROPIC: ["safety", "ethics", "harmlessness", "therapeutic"],
            LLMProvider.GEMINI: ["cultural_context", "multilingual", "indian_context"],
            LLMProvider.COHERE: ["generation", "summarization", "classification"],
            LLMProvider.TOGETHER: ["open_source", "customization", "diversity"]
        }
        
        logger.info("Multi-LLM Manager initialized", providers=list(self.clients.keys()))
    
    def initialize_clients(self):
        """Initialize all configured LLM clients"""
        
        # Groq (already have)
        if self.config.get('GROQ_API_KEY'):
            self.clients[LLMProvider.GROQ] = Groq(api_key=self.config['GROQ_API_KEY'])
        
        # OpenAI
        if self.config.get('OPENAI_API_KEY'):
            openai.api_key = self.config['OPENAI_API_KEY']
            self.clients[LLMProvider.OPENAI] = openai
        
        # Anthropic Claude
        if self.config.get('ANTHROPIC_API_KEY'):
            self.clients[LLMProvider.ANTHROPIC] = anthropic.Anthropic(
                api_key=self.config['ANTHROPIC_API_KEY']
            )
        
        # Google Gemini
        if self.config.get('GEMINI_API_KEY'):
            genai.configure(api_key=self.config['GEMINI_API_KEY'])
            self.clients[LLMProvider.GEMINI] = genai
        
        # Cohere
        if self.config.get('COHERE_API_KEY'):
            self.clients[LLMProvider.COHERE] = cohere.Client(
                self.config['COHERE_API_KEY']
            )
        
        # Together AI
        if self.config.get('TOGETHER_API_KEY'):
            together.api_key = self.config['TOGETHER_API_KEY']
            self.clients[LLMProvider.TOGETHER] = together
    
    async def generate_diverse_responses(
        self, 
        user_message: str, 
        emotion: str = None,
        context: str = None,
        num_responses: int = 3
    ) -> List[Dict[str, Any]]:
        """Generate responses from multiple LLMs and return diverse options"""
        
        tasks = []
        providers = list(self.clients.keys())
        
        # Select providers based on strengths
        selected_providers = self.select_providers_for_task(emotion, num_responses)
        
        # Generate responses in parallel
        for provider in selected_providers:
            task = self.generate_with_provider(
                provider, 
                user_message, 
                emotion, 
                context
            )
            tasks.append(task)
        
        # Wait for all responses
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter and format successful responses
        diverse_responses = []
        for provider, response in zip(selected_providers, responses):
            if not isinstance(response, Exception) and response:
                diverse_responses.append({
                    'provider': provider.value,
                    'strengths': self.provider_strengths.get(provider, []),
                    'response': response,
                    'style': self.detect_response_style(response)
                })
        
        # If not enough responses, add fallbacks
        if len(diverse_responses) < num_responses:
            diverse_responses.extend(
                self.get_fallback_responses(user_message, emotion)[:num_responses - len(diverse_responses)]
            )
        
        return diverse_responses
    
    async def generate_with_provider(
        self, 
        provider: LLMProvider, 
        user_message: str, 
        emotion: str = None,
        context: str = None
    ) -> str:
        """Generate response using specific provider"""
        
        try:
            if provider == LLMProvider.GROQ:
                return await self._generate_groq(user_message, emotion, context)
            
            elif provider == LLMProvider.OPENAI:
                return await self._generate_openai(user_message, emotion, context)
            
            elif provider == LLMProvider.ANTHROPIC:
                return await self._generate_anthropic(user_message, emotion, context)
            
            elif provider == LLMProvider.GEMINI:
                return await self._generate_gemini(user_message, emotion, context)
            
            elif provider == LLMProvider.COHERE:
                return await self._generate_cohere(user_message, emotion, context)
            
            elif provider == LLMProvider.TOGETHER:
                return await self._generate_together(user_message, emotion, context)
        
        except Exception as e:
            logger.error(f"Generation failed for {provider.value}", error=str(e))
            return None
    
    async def _generate_groq(self, message: str, emotion: str, context: str) -> str:
        """Generate with Groq (fast, good for Hinglish)"""
        
        prompt = self._build_prompt(message, emotion, context, style="warm_hinglish")
        
        try:
            completion = self.clients[LLMProvider.GROQ].chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=400
            )
            return completion.choices[0].message.content
        except:
            return None
    
    async def _generate_openai(self, message: str, emotion: str, context: str) -> str:
        """Generate with OpenAI GPT-4 (empathetic, nuanced)"""
        
        prompt = self._build_prompt(message, emotion, context, style="empathetic_deep")
        
        try:
            response = self.clients[LLMProvider.OPENAI].chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.85,
                max_tokens=450
            )
            return response.choices[0].message.content
        except:
            return None
    
    async def _generate_anthropic(self, message: str, emotion: str, context: str) -> str:
        """Generate with Claude (safe, therapeutic)"""
        
        prompt = self._build_prompt(message, emotion, context, style="therapeutic_safe")
        
        try:
            response = self.clients[LLMProvider.ANTHROPIC].messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=450,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except:
            return None
    
    async def _generate_gemini(self, message: str, emotion: str, context: str) -> str:
        """Generate with Gemini (cultural context, multilingual)"""
        
        prompt = self._build_prompt(message, emotion, context, style="culturally_adapted")
        
        try:
            model = self.clients[LLMProvider.GEMINI].GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            return response.text
        except:
            return None
    
    async def _generate_cohere(self, message: str, emotion: str, context: str) -> str:
        """Generate with Cohere (creative, generative)"""
        
        prompt = self._build_prompt(message, emotion, context, style="creative_supportive")
        
        try:
            response = self.clients[LLMProvider.COHERE].generate(
                model='command',
                prompt=prompt,
                max_tokens=400,
                temperature=0.9
            )
            return response.generations[0].text
        except:
            return None
    
    async def _generate_together(self, message: str, emotion: str, context: str) -> str:
        """Generate with Together AI (open source models)"""
        
        prompt = self._build_prompt(message, emotion, context, style="diverse_perspective")
        
        try:
            response = self.clients[LLMProvider.TOGETHER].Completion.create(
                model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                prompt=prompt,
                max_tokens=400,
                temperature=0.8
            )
            return response.choices[0].text
        except:
            return None
    
    def select_providers_for_task(self, emotion: str, num_providers: int) -> List[LLMProvider]:
        """Intelligently select providers based on emotion and task"""
        
        available = list(self.clients.keys())
        
        # Prioritize based on emotion
        if emotion in ['sadness', 'grief', 'hopelessness']:
            # Prioritize empathetic providers
            priority = [LLMProvider.ANTHROPIC, LLMProvider.OPENAI, LLMProvider.GEMINI]
        
        elif emotion in ['anger', 'frustration']:
            # Prioritize calming, safe providers
            priority = [LLMProvider.ANTHROPIC, LLMProvider.GROQ, LLMProvider.COHERE]
        
        elif emotion in ['anxiety', 'fear']:
            # Prioritize grounding, practical providers
            priority = [LLMProvider.GROQ, LLMProvider.OPENAI, LLMProvider.ANTHROPIC]
        
        else:
            # General: diversity of perspectives
            priority = [LLMProvider.OPENAI, LLMProvider.GROQ, LLMProvider.GEMINI, 
                       LLMProvider.ANTHROPIC, LLMProvider.TOGETHER]
        
        # Select top N available providers
        selected = [p for p in priority if p in available][:num_providers]
        
        # If not enough, add random others
        if len(selected) < num_providers:
            remaining = [p for p in available if p not in selected]
            selected.extend(random.sample(remaining, min(num_providers - len(selected), len(remaining))))
        
        return selected
    
    def _build_prompt(self, message: str, emotion: str, context: str, style: str) -> str:
        """Build customized prompt for each LLM style"""
        
        base_prompt = f"""You are MannSaathi, a compassionate mental health assistant for Indian users.

User message: {message}
Detected emotion: {emotion if emotion else 'neutral'}
Context: {context if context else 'General support'}

"""
        
        style_prompts = {
            "warm_hinglish": """
Provide a warm, caring response in Hinglish (mix of Hindi and English). 
Be like a supportive friend. Use phrases like:
- "Aap akela nahi hain" (You're not alone)
- "Main samajh sakta hoon" (I understand)
- "Sath hain hum" (We're together)

Keep it conversational and culturally relatable.
""",
            
            "empathetic_deep": """
Provide an deeply empathetic response. Show deep understanding of their emotional state.
Validate their feelings without trying to "fix" them.
Use reflective listening: "It sounds like you're feeling..."
Ask gentle, open-ended questions to help them explore their feelings.
Show genuine care and presence.
""",
            
            "therapeutic_safe": """
Provide a safe, therapeutic response. Use evidence-based techniques like:
- Cognitive reframing
- Grounding exercises
- Validation and normalization
- Gentle psychoeducation

Always prioritize safety and never give medical advice. 
Suggest professional help when appropriate.
""",
            
            "culturally_adapted": """
Provide a culturally-adapted response for Indian users. Consider:
- Family dynamics and values
- Community support systems
- Spiritual and traditional practices
- Language preferences
- Social expectations

Balance modern mental health approaches with cultural sensitivity.
""",
            
            "creative_supportive": """
Provide a creative, supportive response. Use metaphors, analogies, and storytelling.
Make it memorable and inspiring. 
Examples: "Like a river that flows around obstacles, you too can find your path..."
Keep it warm but imaginative.
""",
            
            "diverse_perspective": """
Provide a response that offers a fresh perspective. 
Help them see their situation from different angles.
Offer multiple ways to think about their challenge.
Encourage hope and possibility while being realistic.
"""
        }
        
        return base_prompt + style_prompts.get(style, style_prompts["warm_hinglish"])
    
    def detect_response_style(self, response: str) -> str:
        """Detect the style of generated response"""
        
        styles = []
        
        if any(word in response.lower() for word in ['aap', 'hai', 'hain', 'samajh']):
            styles.append('hinglish')
        
        if any(word in response.lower() for word in ['feel', 'understand', 'validate']):
            styles.append('empathetic')
        
        if any(word in response.lower() for word in ['try', 'exercise', 'practice']):
            styles.append('practical')
        
        if any(word in response.lower() for word in ['family', 'community', 'culture']):
            styles.append('cultural')
        
        return styles[0] if styles else 'general'
    
    def get_fallback_responses(self, user_message: str, emotion: str) -> List[Dict[str, Any]]:
        """Get fallback responses if LLMs fail"""
        
        fallbacks = {
            'sadness': [
                "I hear the heaviness in your words. It's okay to feel this way. Would you like to tell me more about what's making you feel sad? Sometimes sharing can lighten the burden.",
                "Your feelings matter. When we're sad, even small steps can help. Would you like to try a simple breathing exercise together?",
                "Aap akela nahi hain. Sadness is a natural emotion, and it's okay to sit with it. Is there something small that usually brings you comfort?"
            ],
            'anxiety': [
                "I can sense your mind is racing. Let's try to ground ourselves. Take a deep breath with me... Inhale 1-2-3-4, hold, exhale 1-2-3-4-5-6. How does that feel?",
                "Anxiety can feel overwhelming. Remember, you're safe right now. Let's focus on what's in your control. What's one small thing you can do in this moment?",
                "Worry is like a wave - it comes and goes. Let's try to ride it together. What thoughts are coming up for you right now?"
            ],
            'default': [
                "Thank you for trusting me with your feelings. I'm here to listen and support you. What would be most helpful for you right now?",
                "Your courage to share is inspiring. Let's explore this together. What's been on your mind lately?",
                "Main yahan hoon aapke saath. We can take this journey step by step. What would you like to focus on?"
            ]
        }
        
        selected = fallbacks.get(emotion, fallbacks['default'])
        return [
            {
                'provider': 'fallback',
                'strengths': ['reliable', 'warm'],
                'response': resp,
                'style': 'empathetic'
            }
            for resp in selected[:3]
        ]

class ResponseEnsembler:
    """Combine responses from multiple LLMs into a final response"""
    
    def __init__(self):
        self.logger = structlog.get_logger()
    
    def ensemble_responses(self, responses: List[Dict[str, Any]]) -> str:
        """Combine multiple LLM responses into one diverse, empathetic response"""
        
        if not responses:
            return "I'm here to support you. Could you tell me more about how you're feeling?"
        
        # If only one response, return it
        if len(responses) == 1:
            return responses[0]['response']
        
        # Extract all responses
        all_texts = [r['response'] for r in responses]
        
        # Create ensemble by combining strengths
        combined = self._combine_by_strength(responses)
        
        return combined
    
    def _combine_by_strength(self, responses: List[Dict[str, Any]]) -> str:
        """Intelligently combine responses based on their strengths"""
        
        combined_parts = []
        
        # Extract key elements from each response
        for resp in responses:
            strengths = resp.get('strengths', [])
            text = resp['response']
            
            # Take different parts based on strengths
            if 'empathy' in strengths or 'empathetic' in strengths:
                # Take empathetic opening
                combined_parts.append(self._extract_empathetic_part(text))
            
            elif 'practical' in strengths or 'cultural' in strengths:
                # Take practical suggestions
                combined_parts.append(self._extract_practical_part(text))
            
            elif 'hinglish' in strengths:
                # Take cultural connection
                combined_parts.append(self._extract_cultural_part(text))
        
        # If we couldn't extract parts, combine full texts with separator
        if not combined_parts:
            combined_parts = [r['response'] for r in responses[:2]]
        
        # Join with a warm transition
        transitions = [
            "Also, something else to consider:",
            "Another way to look at this:",
            "And remember,",
            "What also might help:"
        ]
        
        result = combined_parts[0]
        for i, part in enumerate(combined_parts[1:], 1):
            transition = random.choice(transitions)
            result += f"\n\n{transition} {part}"
        
        return result
    
    def _extract_empathetic_part(self, text: str) -> str:
        """Extract empathetic portion of response"""
        # Simple extraction - can be enhanced with NLP
        sentences = text.split('.')
        if len(sentences) > 3:
            return '.'.join(sentences[:2]) + '.'
        return text
    
    def _extract_practical_part(self, text: str) -> str:
        """Extract practical suggestions portion"""
        # Look for action-oriented sentences
        sentences = text.split('.')
        practical = [s for s in sentences if any(word in s.lower() for word in ['try', 'can', 'step', 'exercise', 'practice'])]
        if practical:
            return '.'.join(practical[:2]) + '.'
        return text
    
    def _extract_cultural_part(self, text: str) -> str:
        """Extract culturally-adapted portion"""
        sentences = text.split('.')
        cultural = [s for s in sentences if any(word in s.lower() for word in ['aap', 'hai', 'indian', 'family', 'community'])]
        if cultural:
            return '.'.join(cultural[:2]) + '.'
        return text
        