"""
NLP Preprocessor for Code-Mixed Indian Languages
Handles Hinglish, Devanagari, and mixed script text
"""

import re
import unicodedata
from typing import Dict, List, Tuple
import structlog

logger = structlog.get_logger()


class NLPPreprocessor:
    """
    Preprocess code-mixed text for Indian languages
    Handles Unicode detection, tokenization, and normalization
    """
    
    # Unicode ranges for Indian scripts
    UNICODE_RANGES = {
        'devanagari': (0x0900, 0x097F),
        'tamil': (0x0B80, 0x0BFF),
        'telugu': (0x0C00, 0x0C7F),
        'bengali': (0x0980, 0x09FF),
        'gujarati': (0x0A80, 0x0AFF),
        'kannada': (0x0C80, 0x0CFF),
        'malayalam': (0x0D00, 0x0D7F),
        'oriya': (0x0B00, 0x0B7F),
        'punjabi': (0x0A00, 0x0A7F),
    }
    
    # Common Hinglish words (Roman script Hindi)
    HINGLISH_WORDS = {
        'main', 'hoon', 'hai', 'hain', 'tha', 'thi', 'the', 'nahin', 'nahi', 'nai',
        'kya', 'kaun', 'kaise', 'kyun', 'kyon', 'kahan', 'kidhar', 'kab', 'kitna',
        'mujhe', 'tujhe', 'usko', 'unhe', 'isko', 'inhe', 'sabko',
        'mera', 'tera', 'uska', 'unka', 'iska', 'inka',
        'meri', 'teri', 'uski', 'unki', 'iski', 'inki',
        'mere', 'tere', 'uske', 'unke', 'iske', 'inke',
        'mein', 'par', 'se', 'ko', 'ka', 'ki', 'ke', 'ne', 'bhi',
        'aur', 'ya', 'lekin', 'magar', 'parantu', 'kyunki', 'kyonki',
        'bahut', 'bohot', 'jyada', 'zyada', 'thora', 'thoda', 'kam', 'kum',
        'acha', 'accha', 'bura', 'ganda', 'sundar', 'badiya', 'badhiya',
        'din', 'raat', 'subah', 'shaam', 'kal', 'aaj', 'abhi',
        'ghar', 'school', 'college', 'kaam', 'naukri', 'paise',
        'dost', 'yaar', 'dosti', 'pyaar', 'pyar', 'mohabbat', 'ishq',
        'maa', 'papa', 'mummy', 'dad', 'mom', 'bhai', 'behen', 'didi', 'bhabhi',
        'khana', 'peena', 'sona', 'uthna', 'baithna', 'chalna',
        'khush', 'udaas', 'gussa', 'dar', 'dard', 'pareshan', 'tension',
        'maza', 'masti', 'fun', 'timepass', 'bakwaas', 'jhakaas',
        'han', 'haan', 'hmm', 'acha', 'theek', 'sahi', 'bas', 'chalo'
    }
    
    def __init__(self):
        self.logger = logger.bind(component="NLPPreprocessor")
        self.logger.info("NLPPreprocessor initialized")
    
    def preprocess(self, text: str) -> Dict:
        """
        Preprocess text for analysis
        
        Returns:
            Dict with normalized text, language info, and tokens
        """
        if not text or not text.strip():
            return self._get_empty_result()
        
        # Clean text
        cleaned = self._clean_text(text)
        
        # Detect scripts
        script_info = self._detect_scripts(cleaned)
        
        # Detect language
        language_info = self._detect_language(cleaned, script_info)
        
        # Tokenize
        tokens = self._tokenize(cleaned, language_info['primary'])
        
        # Normalize
        normalized = self._normalize(cleaned, language_info['primary'])
        
        return {
            'original': text,
            'cleaned': cleaned,
            'normalized': normalized,
            'tokens': tokens,
            'language': language_info,
            'scripts': script_info,
            'is_code_mixed': language_info.get('is_code_mixed', False),
            'hindi_ratio': script_info.get('hindi_ratio', 0),
            'english_ratio': script_info.get('english_ratio', 0)
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Normalize Unicode
        text = unicodedata.normalize('NFKC', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove mentions and hashtags (keep the text)
        text = re.sub(r'[@#]', '', text)
        
        # Normalize repeated characters (e.g., "sooooo" -> "soo")
        text = re.sub(r'(.)\1{3,}', r'\1\1', text)
        
        return text.strip()
    
    def _detect_scripts(self, text: str) -> Dict:
        """Detect scripts used in text"""
        scripts = {'ascii': 0, 'devanagari': 0, 'other': 0}
        total_chars = 0
        
        for char in text:
            if char.isspace():
                continue
            
            total_chars += 1
            code_point = ord(char)
            
            # Check Devanagari
            if self.UNICODE_RANGES['devanagari'][0] <= code_point <= self.UNICODE_RANGES['devanagari'][1]:
                scripts['devanagari'] += 1
            # Check ASCII (English)
            elif code_point < 128:
                scripts['ascii'] += 1
            else:
                scripts['other'] += 1
        
        if total_chars == 0:
            return {'ascii': 1.0, 'devanagari': 0, 'other': 0}
        
        # Calculate ratios
        scripts['hindi_ratio'] = scripts['devanagari'] / total_chars
        scripts['english_ratio'] = scripts['ascii'] / total_chars
        scripts['other_ratio'] = scripts['other'] / total_chars
        
        return scripts
    
    def _detect_language(self, text: str, script_info: Dict) -> Dict:
        """Detect primary language and code-mixing"""
        text_lower = text.lower()
        words = set(re.findall(r'\b\w+\b', text_lower))
        
        # Count Hinglish words
        hinglish_count = len(words.intersection(self.HINGLISH_WORDS))
        total_words = len(words)
        
        if total_words == 0:
            return {'primary': 'english', 'is_code_mixed': False}
        
        hinglish_ratio = hinglish_count / total_words
        
        # Determine language
        if script_info['hindi_ratio'] > 0.3:
            primary = 'hindi'
            is_code_mixed = script_info['english_ratio'] > 0.1 or hinglish_ratio > 0.2
        elif hinglish_ratio > 0.2:
            primary = 'hinglish'
            is_code_mixed = script_info['english_ratio'] > 0.3
        else:
            primary = 'english'
            is_code_mixed = hinglish_ratio > 0.1
        
        return {
            'primary': primary,
            'is_code_mixed': is_code_mixed,
            'hinglish_ratio': hinglish_ratio,
            'detected_words': hinglish_count
        }
    
    def _tokenize(self, text: str, language: str) -> List[str]:
        """Tokenize text based on language"""
        if language == 'hindi':
            # Simple tokenization for Hindi (space-based with some rules)
            tokens = re.findall(r'\b\w+\b', text)
        else:
            # Standard tokenization
            tokens = re.findall(r'\b\w+\b', text.lower())
        
        return tokens
    
    def _normalize(self, text: str, language: str) -> str:
        """Normalize text for processing"""
        # Convert to lowercase for non-Devanagari
        if language != 'hindi':
            text = text.lower()
        
        # Normalize common variations
        replacements = {
            'nahi': 'nahin',
            'nai': 'nahin',
            'bohot': 'bahut',
            'bhot': 'bahut',
            'thora': 'thoda',
            'zyada': 'jyada',
            'accha': 'acha',
            'theek': 'thik',
        }
        
        for old, new in replacements.items():
            text = re.sub(r'\b' + old + r'\b', new, text, flags=re.IGNORECASE)
        
        return text
    
    def _get_empty_result(self) -> Dict:
        """Return empty result"""
        return {
            'original': '',
            'cleaned': '',
            'normalized': '',
            'tokens': [],
            'language': {'primary': 'unknown', 'is_code_mixed': False},
            'scripts': {'ascii': 0, 'devanagari': 0, 'other': 0},
            'is_code_mixed': False,
            'hindi_ratio': 0,
            'english_ratio': 0
        }
    
    def detect_sentiment_indicators(self, text: str) -> Dict:
        """Detect sentiment indicators in text"""
        text_lower = text.lower()
        
        positive_indicators = ['acha', 'accha', 'badhiya', 'badiya', 'maza', 
                              'khush', 'anand', 'sukoon', 'theek', 'sahi']
        negative_indicators = ['bura', 'ganda', 'pareshan', 'tension', 'dard',
                              'udaas', 'gussa', 'dar', 'bekar', 'problem']
        
        positive_count = sum(1 for word in positive_indicators if word in text_lower)
        negative_count = sum(1 for word in negative_indicators if word in text_lower)
        
        return {
            'positive_indicators': positive_count,
            'negative_indicators': negative_count,
            'sentiment_hint': 'positive' if positive_count > negative_count else 
                            'negative' if negative_count > positive_count else 'neutral'
        }
