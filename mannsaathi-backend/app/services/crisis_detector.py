"""
Crisis Detection Module - Two-Tier Safety System
Detects mental health crises and provides appropriate interventions
"""

import re
from typing import Dict, List, Optional, Tuple
from collections import deque
import structlog
from datetime import datetime

logger = structlog.get_logger()


class CrisisDetector:
    """
    Two-tier crisis detection system for mental health emergencies
    Tier 1: Keyword-based detection
    Tier 2: Emotion pattern analysis over multiple turns
    """
    
    # Comprehensive crisis keywords
    CRISIS_KEYWORDS = {
        'suicide': {
            'severity': 'critical',
            'keywords': [
                # English
                'suicide', 'suicidal', 'kill myself', 'end my life', 'want to die',
                'better off dead', 'not worth living', 'end it all', 'take my life',
                'self harm', 'self-harm', 'cutting', 'overdose', 'jump off',
                'hang myself', 'shoot myself', 'slit', 'wrists', 'pills',
                'no reason to live', 'cant go on', 'cannot go on',
                # Hinglish
                'aatma hatya', 'aatmahatya', 'khudkushi', 'khud khushi',
                'mar jaana', 'marjaana', 'mar jana', 'marjana', 'jeena nahi',
                'jeenanahi', 'jeena mushkil', 'sab khatam', 'sabkhatam',
                'khatam karna', 'khatamkarna', 'khatam kar', 'khatamkar',
                'khatam kardu', 'khatamkardu', 'khatam hai', 'khatamhai',
                'zindagi khatam', 'zindagikhatam', 'life khatam', 'lifekhatam',
                'marne ka', 'marneka', 'marna hai', 'marnahai', 'mar jau',
                'marjau', 'mar jaun', 'marjaun', 'khatam karu', 'khatamkaru',
                'apni jaan', 'apnijaan', 'jaan de', 'jaande', 'jaan dedu',
                # Hindi (Devanagari)
                'आत्महत्या', 'खुदकुशी', 'मर जाना', 'जीना नहीं', 'सब खतम',
                'खत्म करना', 'खत्म कर दूं', 'जिंदगी खत्म', 'मरने का',
                'अपनी जान', 'जान दे', 'जान दे दूं',
            ]
        },
        'self_harm': {
            'severity': 'high',
            'keywords': [
                'self harm', 'self-harm', 'cutting', 'cutter', 'blade', 'razor',
                'hurt myself', 'hurt me', 'pain makes me feel', 'burn myself',
                'scratch', 'pinch', 'hit myself', 'punish myself',
                'apnu nuksan', 'apne aap ko hurt', 'khud ko dard', 'blade se',
                'chaku se', 'kaatna', 'khud ko kaat', 'zakhm', 'chot',
                'खुद को चोट', 'चाकू से', 'ब्लेड से', 'खुद को दर्द'
            ]
        },
        'hopelessness': {
            'severity': 'high',
            'keywords': [
                'no hope', 'hopeless', 'no point', 'no reason', 'give up',
                'cant go on', 'cannot go on', 'nothing matters', 'nobody cares',
                'everyone hates me', 'alone forever', 'never get better',
                'koi ummeed nahi', 'ummeed nahi', 'koi fayda nahi', 'fayda nahi',
                'chhod do', 'haar maan li', 'sab bekar', 'koi nahi poochta',
                'koi nahi samajhta', 'kabhi nahi sudhrega', 'kabhi theek nahi hoga',
                'कोई उम्मीद नहीं', 'हार मान ली', 'सब बेकार', 'कोई नहीं समझता',
                'कभी ठीक नहीं होगा'
            ]
        },
        'severe_distress': {
            'severity': 'medium',
            'keywords': [
                'cant take it', 'cannot take it', 'breaking down', 'falling apart',
                'losing control', 'going crazy', 'mental breakdown',
                'pagal ho raha', 'pagalhoraha', 'control nahi', 'sambhal nahi raha',
                'बेकाबू', 'कंट्रोल नहीं', 'पागल हो रहा', 'संभल नहीं रहा'
            ]
        }
    }
    
    # Indian Mental Health Helplines
    HELPLINES = {
        'national': [
            {
                'name': 'Vandrevala Foundation',
                'number': '1860-2662-345',
                'hours': '24/7',
                'languages': ['English', 'Hindi'],
                'services': ['Crisis Support', 'Counseling'],
                'website': 'https://www.vandrevalafoundation.com'
            },
            {
                'name': 'AASRA',
                'number': '91-22-27546669',
                'hours': '24/7',
                'languages': ['English', 'Hindi'],
                'services': ['Suicide Prevention', 'Crisis Support'],
                'website': 'http://www.aasra.info'
            },
            {
                'name': 'iCall',
                'number': '022-25521111',
                'hours': 'Mon-Sat, 10am-8pm',
                'languages': ['English', 'Hindi', 'Marathi', 'Gujarati'],
                'services': ['Counseling', 'Mental Health Support'],
                'website': 'https://icallhelpline.org'
            },
            {
                'name': 'Sneha Foundation',
                'number': '044-24640050',
                'hours': '24/7',
                'languages': ['English', 'Tamil'],
                'services': ['Suicide Prevention', 'Crisis Support'],
                'website': 'http://snehaindia.org'
            },
            {
                'name': 'Roshni Trust',
                'number': '040-66202000',
                'hours': 'Mon-Sat, 11am-9pm',
                'languages': ['English', 'Telugu', 'Hindi'],
                'services': ['Counseling', 'Crisis Support'],
                'website': 'http://roshnitrust.org'
            },
            {
                'name': 'Lifeline Foundation',
                'number': '033-24637401',
                'hours': 'Daily, 10am-10pm',
                'languages': ['English', 'Bengali', 'Hindi'],
                'services': ['Crisis Support', 'Counseling'],
                'website': 'http://www.lifelinefoundation.in'
            },
            {
                'name': 'Samaritans Mumbai',
                'number': '91-8422984528',
                'hours': 'Daily, 5pm-8pm',
                'languages': ['English', 'Hindi', 'Marathi'],
                'services': ['Emotional Support', 'Crisis Support'],
                'website': 'http://samaritansmumbai.com'
            },
            {
                'name': 'Kiran Helpline',
                'number': '1800-599-0019',
                'hours': '24/7',
                'languages': ['English', 'Hindi', 'Regional'],
                'services': ['Mental Health Support', 'Crisis Intervention'],
                'website': 'https://kiran.mohfw.gov.in'
            }
        ],
        'emergency': [
            {
                'name': 'Emergency Services',
                'number': '112',
                'type': 'national_emergency'
            },
            {
                'name': 'Police',
                'number': '100',
                'type': 'police'
            },
            {
                'name': 'Ambulance',
                'number': '108',
                'type': 'medical'
            }
        ]
    }
    
    def __init__(self, emotion_history_size: int = 10):
        self.logger = logger.bind(component="CrisisDetector")
        self.emotion_history = deque(maxlen=emotion_history_size)
        self.tier2_threshold = 0.7
        self.tier2_consecutive_turns = 3
        self.logger.info("CrisisDetector initialized")
    
    def detect(self, text: str, emotion_analysis: Dict, 
               session_history: List[Dict] = None) -> Dict:
        """
        Detect crisis using two-tier approach
        
        Args:
            text: User message
            emotion_analysis: Emotion analysis result
            session_history: Previous conversation turns
        
        Returns:
            Dict with crisis status, tier, and intervention info
        """
        # Tier 1: Keyword-based detection
        tier1_result = self._tier1_detection(text)
        
        if tier1_result['is_crisis']:
            return self._build_crisis_response(
                tier=1,
                triggered_by='keyword',
                details=tier1_result,
                emotion_analysis=emotion_analysis
            )
        
        # Tier 2: Emotion pattern detection
        tier2_result = self._tier2_detection(emotion_analysis, session_history)
        
        if tier2_result['is_crisis']:
            return self._build_crisis_response(
                tier=2,
                triggered_by='emotion_pattern',
                details=tier2_result,
                emotion_analysis=emotion_analysis
            )
        
        # No crisis detected
        return {
            'is_crisis': False,
            'tier': None,
            'concern_level': tier2_result.get('concern_level', 'low'),
            'message': 'No crisis indicators detected'
        }
    
    def _tier1_detection(self, text: str) -> Dict:
        """Tier 1: Keyword-based crisis detection"""
        text_lower = text.lower()
        
        detected_keywords = []
        highest_severity = 'low'
        
        for category, data in self.CRISIS_KEYWORDS.items():
            for keyword in data['keywords']:
                if keyword in text_lower:
                    detected_keywords.append({
                        'keyword': keyword,
                        'category': category,
                        'severity': data['severity']
                    })
                    
                    # Track highest severity
                    if data['severity'] == 'critical':
                        highest_severity = 'critical'
                    elif data['severity'] == 'high' and highest_severity != 'critical':
                        highest_severity = 'high'
        
        is_crisis = len(detected_keywords) > 0
        
        return {
            'is_crisis': is_crisis,
            'detected_keywords': detected_keywords,
            'severity': highest_severity,
            'keyword_count': len(detected_keywords)
        }
    
    def _tier2_detection(self, emotion_analysis: Dict, 
                         session_history: List[Dict] = None) -> Dict:
        """Tier 2: Emotion pattern-based detection"""
        emotions = emotion_analysis.get('emotions', {})
        
        # Check current emotion scores
        sadness = emotions.get('sadness', 0)
        fear = emotions.get('fear', 0)
        anger = emotions.get('anger', 0)
        
        # High negative emotion in current turn
        current_high_negative = (sadness > self.tier2_threshold or 
                                  fear > self.tier2_threshold)
        
        if not session_history or len(session_history) < self.tier2_consecutive_turns:
            return {
                'is_crisis': False,
                'concern_level': 'high' if current_high_negative else 'low',
                'consecutive_high': 1 if current_high_negative else 0
            }
        
        # Check consecutive high negative emotions
        recent_history = session_history[-self.tier2_consecutive_turns:]
        consecutive_count = 0
        
        for turn in recent_history:
            turn_emotions = turn.get('emotions', {})
            turn_sadness = turn_emotions.get('sadness', 0)
            turn_fear = turn_emotions.get('fear', 0)
            
            if turn_sadness > self.tier2_threshold or turn_fear > self.tier2_threshold:
                consecutive_count += 1
            else:
                consecutive_count = 0
        
        is_crisis = consecutive_count >= self.tier2_consecutive_turns
        
        return {
            'is_crisis': is_crisis,
            'concern_level': 'high' if consecutive_count >= 2 else 'medium' if consecutive_count >= 1 else 'low',
            'consecutive_high': consecutive_count
        }
    
    def _build_crisis_response(self, tier: int, triggered_by: str,
                               details: Dict, emotion_analysis: Dict) -> Dict:
        """Build crisis response with intervention info"""
        severity = details.get('severity', 'high')
        
        # Select appropriate helplines
        helplines = self._select_helplines(severity)
        
        # Generate intervention message
        intervention_message = self._generate_intervention_message(
            tier, severity, emotion_analysis
        )
        
        return {
            'is_crisis': True,
            'tier': tier,
            'triggered_by': triggered_by,
            'severity': severity,
            'details': details,
            'intervention': {
                'message': intervention_message,
                'helplines': helplines,
                'immediate_actions': self._get_immediate_actions(severity),
                'safety_plan': self._get_safety_plan()
            },
            'timestamp': datetime.now().isoformat()
        }
    
    def _select_helplines(self, severity: str) -> List[Dict]:
        """Select appropriate helplines based on severity"""
        if severity == 'critical':
            # Include emergency services for critical cases
            return self.HELPLINES['national'][:4] + self.HELPLINES['emergency'][:2]
        elif severity == 'high':
            return self.HELPLINES['national'][:3]
        else:
            return self.HELPLINES['national'][:2]
    
    def _generate_intervention_message(self, tier: int, severity: str,
                                       emotion_analysis: Dict) -> str:
        """Generate culturally appropriate intervention message"""
        dominant_emotion = emotion_analysis.get('dominant_emotion', 'distress')
        
        messages = {
            'critical': [
                "Main samajh sakta/sakti hoon ki aap bahut mushkil waqt se guzar rahe hain. "
                "Aapki jaan bahut keemti hai. Kripya turant madad len:",
                "Aapki feelings valid hain, lekin akele mat rahein. "
                "In helpline numbers par call karein - woh aapki madad karenge:"
            ],
            'high': [
                "Mujhe lagta hai ki aap bahut pareshan hain. "
                "Aapki madad ke liye yeh resources hain:",
                "Aapki feelings important hain. "
                "Kripya in trained professionals se baat karein:"
            ],
            'medium': [
                "Main dekh sakta/sakti hoon ki aap stressed hain. "
                "Agar aapko baat karni ho, toh yeh helplines available hain:"
            ]
        }
        
        return messages.get(severity, messages['medium'])[0]
    
    def _get_immediate_actions(self, severity: str) -> List[str]:
        """Get immediate action recommendations"""
        actions = {
            'critical': [
                'Call a trusted friend or family member immediately',
                'Go to a safe place (hospital, police station, or trusted person\'s home)',
                'Remove any means of self-harm from your vicinity',
                'Call emergency services (112) if in immediate danger'
            ],
            'high': [
                'Reach out to someone you trust',
                'Try grounding techniques (deep breathing, 5-4-3-2-1 method)',
                'Move to a safe, comfortable environment',
                'Consider calling a helpline for support'
            ],
            'medium': [
                'Take a break and practice self-care',
                'Talk to a friend or family member',
                'Engage in a calming activity',
                'Consider professional support if feelings persist'
            ]
        }
        
        return actions.get(severity, actions['medium'])
    
    def _get_safety_plan(self) -> Dict:
        """Get safety planning information"""
        return {
            'warning_signs': [
                'Feeling hopeless or trapped',
                'Increased substance use',
                'Withdrawing from friends and family',
                'Extreme mood swings'
            ],
            'coping_strategies': [
                'Talk to someone you trust',
                'Engage in physical activity',
                'Practice mindfulness or meditation',
                'Write down your feelings',
                'Listen to calming music'
            ],
            'support_contacts': [
                'A trusted friend or family member',
                'Your therapist or counselor',
                'Crisis helplines'
            ],
            'safe_places': [
                'Your home',
                'A friend\'s or relative\'s house',
                'Hospital emergency department',
                'Police station'
            ]
        }
    
    def get_all_helplines(self) -> Dict:
        """Get all available helplines"""
        return self.HELPLINES
    
    def add_emotion_to_history(self, emotion_analysis: Dict):
        """Add emotion analysis to history for tier 2 detection"""
        self.emotion_history.append({
            'timestamp': datetime.now().isoformat(),
            'emotions': emotion_analysis.get('emotions', {}),
            'dominant': emotion_analysis.get('dominant_emotion', 'neutral')
        })
