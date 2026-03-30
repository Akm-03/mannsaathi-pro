"""
Advanced Emotion Analyzer with ML-enhanced detection
Combines rule-based lexicon with transformer models
"""

import numpy as np
import re
from typing import Dict, List, Tuple, Optional
import structlog
from textblob import TextBlob
import nltk
from collections import defaultdict

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

from ..data.emotion_lexicon import (
    ALL_EMOTION_LEXICONS, CRISIS_KEYWORDS, CULTURAL_CONTEXT,
    INTENSITY_MODIFIERS, NEGATION_MARKERS
)

logger = structlog.get_logger()


class EmotionAnalyzer:
    """
    Multilingual emotion analyzer supporting 8 Indian languages
    Combines lexicon-based scoring with ML-enhanced detection
    """
    
    EMOTIONS = ['sadness', 'fear', 'anger', 'joy', 'surprise', 'neutral']
    
    def __init__(self, use_ml_enhancement: bool = True):
        self.logger = logger.bind(component="EmotionAnalyzer")
        self.use_ml_enhancement = use_ml_enhancement
        self.ml_model = None
        
        # Initialize ML model if available
        if use_ml_enhancement:
            self._init_ml_model()
        
        self.logger.info("EmotionAnalyzer initialized", 
                        ml_enhancement=use_ml_enhancement)
    
    def _init_ml_model(self):
        """Initialize transformer-based emotion model"""
        try:
            from transformers import pipeline
            # Use a multilingual emotion model
            self.ml_model = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                top_k=None
            )
            self.logger.info("ML emotion model loaded successfully")
        except Exception as e:
            self.logger.warning("Could not load ML model, using lexicon only", 
                              error=str(e))
            self.ml_model = None
    
    def analyze(self, text: str, language: str = 'auto') -> Dict:
        """
        Analyze emotions in text
        
        Returns:
            Dict with emotion scores, dominant emotion, and confidence
        """
        if not text or not text.strip():
            return self._get_neutral_result()
        
        # Detect language if auto
        if language == 'auto':
            language = self._detect_language(text)
        
        # Get lexicon-based scores
        lexicon_scores = self._lexicon_analysis(text, language)
        
        # Get ML-based scores if available
        ml_scores = {}
        if self.ml_model and self.use_ml_enhancement:
            ml_scores = self._ml_analysis(text)
        
        # Combine scores
        final_scores = self._combine_scores(lexicon_scores, ml_scores)
        
        # Detect crisis indicators
        crisis_indicators = self._detect_crisis_indicators(text)
        
        # Detect cultural context
        cultural_context = self._detect_cultural_context(text)
        
        # Determine dominant emotion
        dominant_emotion, confidence = self._get_dominant_emotion(final_scores)
        
        result = {
            'emotions': final_scores,
            'dominant_emotion': dominant_emotion,
            'confidence': confidence,
            'language': language,
            'crisis_indicators': crisis_indicators,
            'cultural_context': cultural_context,
            'sentiment': self._get_sentiment(text),
            'intensity': self._calculate_intensity(final_scores)
        }
        
        self.logger.debug("Emotion analysis complete", 
                         dominant=dominant_emotion, 
                         confidence=confidence,
                         language=language)
        
        return result
    
    def _detect_language(self, text: str) -> str:
        """Detect the primary language of the text"""
        # Check for Devanagari (Hindi)
        if re.search(r'[\u0900-\u097F]', text):
            return 'hindi'
        
        # Check for Tamil
        if re.search(r'[\u0B80-\u0BFF]', text):
            return 'tamil'
        
        # Check for Telugu
        if re.search(r'[\u0C00-\u0C7F]', text):
            return 'telugu'
        
        # Check for Bengali
        if re.search(r'[\u0980-\u09FF]', text):
            return 'bengali'
        
        # Check for Hinglish (Roman Hindi)
        hinglish_words = ['hai', 'nahi', 'main', 'hoon', 'bahut', 'kya', 
                         'mujhe', 'tum', 'aap', 'mera', 'tera', 'iska']
        text_lower = text.lower()
        hinglish_count = sum(1 for word in hinglish_words if word in text_lower)
        
        if hinglish_count >= 2:
            return 'hinglish'
        
        return 'english'
    
    def _lexicon_analysis(self, text: str, language: str) -> Dict[str, float]:
        """Analyze emotions using lexicon-based approach"""
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        scores = {emotion: 0.0 for emotion in self.EMOTIONS}
        
        # Get appropriate lexicon
        lexicon = ALL_EMOTION_LEXICONS.get(language, ALL_EMOTION_LEXICONS['english'])
        
        # Also check Hinglish for mixed content
        if language in ['hindi', 'hinglish', 'english']:
            lexicon = {**lexicon, **ALL_EMOTION_LEXICONS['hinglish']}
        
        # Score each emotion
        for emotion, keywords in lexicon.items():
            for word in words:
                if word in keywords:
                    scores[emotion] += keywords[word]
        
        # Apply intensity modifiers
        scores = self._apply_intensity_modifiers(text_lower, scores)
        
        # Apply negation handling
        scores = self._apply_negation(text_lower, scores)
        
        # Normalize scores
        total = sum(scores.values())
        if total > 0:
            scores = {k: min(v / total * 2, 1.0) for k, v in scores.items()}
        
        return scores
    
    def _apply_intensity_modifiers(self, text: str, scores: Dict) -> Dict:
        """Apply intensity modifiers to emotion scores"""
        modified_scores = scores.copy()
        
        for modifier, factor in INTENSITY_MODIFIERS['increase'].items():
            if modifier in text:
                # Increase the highest scoring emotion
                max_emotion = max(modified_scores, key=modified_scores.get)
                if modified_scores[max_emotion] > 0:
                    modified_scores[max_emotion] *= factor
        
        for modifier, factor in INTENSITY_MODIFIERS['decrease'].items():
            if modifier in text:
                # Decrease all scores
                for emotion in modified_scores:
                    modified_scores[emotion] *= factor
        
        return modified_scores
    
    def _apply_negation(self, text: str, scores: Dict) -> Dict:
        """Handle negation in text"""
        modified_scores = scores.copy()
        
        for negator in NEGATION_MARKERS:
            if negator in text:
                # Find context after negation
                neg_pos = text.find(negator)
                if neg_pos >= 0:
                    context = text[neg_pos:neg_pos + 50]
                    
                    # Check for emotion words in negated context
                    for emotion in ['joy', 'sadness']:
                        if any(word in context for word in 
                               ALL_EMOTION_LEXICONS['english'].get(emotion, {}).keys()):
                            # Invert the emotion
                            if emotion == 'joy' and modified_scores['joy'] > 0:
                                modified_scores['sadness'] += modified_scores['joy']
                                modified_scores['joy'] = 0
                            elif emotion == 'sadness' and modified_scores['sadness'] > 0:
                                modified_scores['joy'] += modified_scores['sadness'] * 0.5
                                modified_scores['sadness'] *= 0.5
        
        return modified_scores
    
    def _ml_analysis(self, text: str) -> Dict[str, float]:
        """Analyze emotions using ML model"""
        if not self.ml_model:
            return {}
        
        try:
            # Truncate text if too long
            text = text[:512]
            
            result = self.ml_model(text)[0]
            
            # Map model outputs to our emotion categories
            emotion_map = {
                'sadness': 'sadness',
                'fear': 'fear',
                'anger': 'anger',
                'joy': 'joy',
                'surprise': 'surprise',
                'neutral': 'neutral',
                'disgust': 'anger'
            }
            
            scores = {emotion: 0.0 for emotion in self.EMOTIONS}
            
            for item in result:
                emotion_key = emotion_map.get(item['label'], 'neutral')
                scores[emotion_key] = item['score']
            
            return scores
            
        except Exception as e:
            self.logger.warning("ML analysis failed", error=str(e))
            return {}
    
    def _combine_scores(self, lexicon_scores: Dict, ml_scores: Dict) -> Dict[str, float]:
        """Combine lexicon and ML scores"""
        if not ml_scores:
            return lexicon_scores
        
        combined = {}
        for emotion in self.EMOTIONS:
            # Weight: 60% lexicon, 40% ML (lexicon better for Indian languages)
            lex = lexicon_scores.get(emotion, 0)
            ml = ml_scores.get(emotion, 0)
            combined[emotion] = 0.6 * lex + 0.4 * ml
        
        # Normalize
        total = sum(combined.values())
        if total > 0:
            combined = {k: v / total for k, v in combined.items()}
        
        return combined
    
    def _detect_crisis_indicators(self, text: str) -> List[Dict]:
        """Detect crisis-related keywords"""
        text_lower = text.lower()
        indicators = []
        
        for category, keywords in CRISIS_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    indicators.append({
                        'category': category,
                        'keyword': keyword,
                        'severity': 'high' if category == 'suicide' else 'medium'
                    })
        
        return indicators
    
    def _detect_cultural_context(self, text: str) -> Dict[str, float]:
        """Detect Indian cultural context in text"""
        text_lower = text.lower()
        context_scores = {}
        
        for context_type, keywords in CULTURAL_CONTEXT.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                context_scores[context_type] = min(score / 3, 1.0)
        
        return context_scores
    
    def _get_dominant_emotion(self, scores: Dict) -> Tuple[str, float]:
        """Get the dominant emotion and confidence"""
        if not scores or all(v == 0 for v in scores.values()):
            return 'neutral', 1.0
        
        dominant = max(scores, key=scores.get)
        confidence = scores[dominant]
        
        # Boost confidence if there's a clear winner
        sorted_scores = sorted(scores.values(), reverse=True)
        if len(sorted_scores) > 1 and sorted_scores[0] > sorted_scores[1] * 1.5:
            confidence = min(confidence * 1.2, 1.0)
        
        return dominant, round(confidence, 3)
    
    def _get_sentiment(self, text: str) -> Dict:
        """Get sentiment polarity using TextBlob"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            if polarity > 0.1:
                label = 'positive'
            elif polarity < -0.1:
                label = 'negative'
            else:
                label = 'neutral'
            
            return {
                'label': label,
                'polarity': round(polarity, 3),
                'subjectivity': round(subjectivity, 3)
            }
        except Exception:
            return {'label': 'neutral', 'polarity': 0, 'subjectivity': 0}
    
    def _calculate_intensity(self, scores: Dict) -> float:
        """Calculate overall emotional intensity"""
        if not scores:
            return 0.0
        
        # Max score minus neutral
        max_emotion_score = max(
            (v for k, v in scores.items() if k != 'neutral'),
            default=0
        )
        
        return round(max_emotion_score, 3)
    
    def _get_neutral_result(self) -> Dict:
        """Return neutral result for empty input"""
        return {
            'emotions': {emotion: 1.0 if emotion == 'neutral' else 0.0 
                        for emotion in self.EMOTIONS},
            'dominant_emotion': 'neutral',
            'confidence': 1.0,
            'language': 'unknown',
            'crisis_indicators': [],
            'cultural_context': {},
            'sentiment': {'label': 'neutral', 'polarity': 0, 'subjectivity': 0},
            'intensity': 0.0
        }
    
    def analyze_batch(self, texts: List[str]) -> List[Dict]:
        """Analyze multiple texts in batch"""
        return [self.analyze(text) for text in texts]
    
    def get_emotion_trend(self, analyses: List[Dict]) -> Dict:
        """Analyze emotion trend over multiple messages"""
        if not analyses:
            return {'trend': 'stable', 'concern_level': 'low'}
        
        # Track negative emotions over time
        negative_scores = []
        for analysis in analyses:
            neg_score = (analysis['emotions'].get('sadness', 0) +
                        analysis['emotions'].get('fear', 0) +
                        analysis['emotions'].get('anger', 0))
            negative_scores.append(neg_score)
        
        # Detect trend
        if len(negative_scores) >= 3:
            recent = negative_scores[-3:]
            if all(s > 0.5 for s in recent):
                return {'trend': 'worsening', 'concern_level': 'high'}
            elif recent[-1] > recent[0]:
                return {'trend': 'declining', 'concern_level': 'medium'}
        
        return {'trend': 'stable', 'concern_level': 'low'}
