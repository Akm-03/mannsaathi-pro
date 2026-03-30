"""
Voice Emotion Analyzer - Speech Emotion Recognition
Analyzes tone, pitch, and spectral features for emotion detection
"""

import numpy as np
import librosa
import io
import base64
from typing import Dict, List, Optional, Tuple
import structlog

logger = structlog.get_logger()


class VoiceAnalyzer:
    """
    Analyze emotions from voice/audio
    Extracts prosodic and spectral features for emotion recognition
    """
    
    EMOTIONS = ['neutral', 'joy', 'sadness', 'anger', 'fear', 'surprise']
    
    def __init__(self):
        self.logger = logger.bind(component="VoiceAnalyzer")
        self.sample_rate = 16000
        self._init_model()
    
    def _init_model(self):
        """Initialize speech emotion recognition model"""
        try:
            # Try to load SpeechBrain emotion model
            try:
                from speechbrain.pretrained import EncoderClassifier
                self.emotion_model = EncoderClassifier.from_hparams(
                    source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP"
                )
                self.logger.info("SpeechBrain emotion model loaded")
            except Exception as e:
                self.logger.warning("SpeechBrain model not available", error=str(e))
                self.emotion_model = None
            
            self.logger.info("VoiceAnalyzer initialized")
            
        except Exception as e:
            self.logger.error("Failed to initialize voice analyzer", error=str(e))
            self.emotion_model = None
    
    def analyze_audio(self, audio_data: bytes or str, 
                     sample_rate: int = 16000) -> Dict:
        """
        Analyze emotions from audio
        
        Args:
            audio_data: Raw audio bytes or base64 encoded string
            sample_rate: Audio sample rate
        
        Returns:
            Dict with emotion scores and audio features
        """
        try:
            # Decode audio
            y = self._decode_audio(audio_data, sample_rate)
            if y is None:
                return self._get_error_result("Could not decode audio")
            
            # Extract features
            features = self._extract_features(y, sample_rate)
            
            # Analyze emotions
            emotion_scores = self._analyze_emotions(y, sample_rate)
            
            # Detect speech characteristics
            speech_chars = self._analyze_speech_characteristics(y, sample_rate)
            
            # Determine dominant emotion
            dominant_emotion, confidence = self._get_dominant_emotion(emotion_scores)
            
            return {
                'success': True,
                'emotions': emotion_scores,
                'dominant_emotion': dominant_emotion,
                'confidence': confidence,
                'features': features,
                'speech_characteristics': speech_chars,
                'valence': self._calculate_valence(emotion_scores),
                'arousal': self._calculate_arousal(emotion_scores, features)
            }
            
        except Exception as e:
            self.logger.error("Audio analysis failed", error=str(e))
            return self._get_error_result(str(e))
    
    def _decode_audio(self, audio_data, sample_rate: int) -> Optional[np.ndarray]:
        """Decode audio from bytes or base64 string"""
        try:
            if isinstance(audio_data, str):
                # Remove data URL prefix if present
                if ',' in audio_data:
                    audio_data = audio_data.split(',')[1]
                audio_bytes = base64.b64decode(audio_data)
            else:
                audio_bytes = audio_data
            
            # Load audio with librosa
            y, sr = librosa.load(io.BytesIO(audio_bytes), sr=sample_rate)
            
            return y
            
        except Exception as e:
            self.logger.error("Audio decoding failed", error=str(e))
            return None
    
    def _extract_features(self, y: np.ndarray, sr: int) -> Dict:
        """Extract audio features"""
        features = {}
        
        try:
            # Basic features
            features['duration'] = len(y) / sr
            features['rms_energy'] = float(np.sqrt(np.mean(y**2)))
            
            # Spectral features
            features['spectral_centroid'] = float(np.mean(
                librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            ))
            features['spectral_rolloff'] = float(np.mean(
                librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
            ))
            features['spectral_bandwidth'] = float(np.mean(
                librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
            ))
            
            # Zero crossing rate
            features['zcr'] = float(np.mean(librosa.feature.zero_crossing_rate(y)[0]))
            
            # MFCCs
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            features['mfcc_mean'] = float(np.mean(mfccs))
            features['mfcc_std'] = float(np.std(mfccs))
            
            # Pitch features
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
            pitches_nonzero = pitches[pitches > 0]
            if len(pitches_nonzero) > 0:
                features['pitch_mean'] = float(np.mean(pitches_nonzero))
                features['pitch_std'] = float(np.std(pitches_nonzero))
            else:
                features['pitch_mean'] = 0
                features['pitch_std'] = 0
            
            # Tempo
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            features['tempo'] = float(tempo)
            
        except Exception as e:
            self.logger.warning("Feature extraction failed", error=str(e))
        
        return features
    
    def _analyze_emotions(self, y: np.ndarray, sr: int) -> Dict[str, float]:
        """Analyze emotions from audio"""
        emotions = {emotion: 0.0 for emotion in self.EMOTIONS}
        
        # Use ML model if available
        if self.emotion_model:
            try:
                # Save temporary file for model
                import tempfile
                import os
                
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
                    import soundfile as sf
                    sf.write(tmp.name, y, sr)
                    tmp_path = tmp.name
                
                # Predict emotions
                prediction = self.emotion_model.classify_file(tmp_path)
                
                # Parse prediction
                if isinstance(prediction, tuple):
                    pred_labels = prediction[3]  # Get emotion labels
                    pred_scores = prediction[1]  # Get scores
                    
                    for label, score in zip(pred_labels, pred_scores):
                        emotion_map = {
                            'neu': 'neutral',
                            'hap': 'joy',
                            'sad': 'sadness',
                            'ang': 'anger',
                            'fea': 'fear',
                            'sur': 'surprise'
                        }
                        mapped = emotion_map.get(label, 'neutral')
                        emotions[mapped] = float(score)
                
                # Clean up
                os.unlink(tmp_path)
                
            except Exception as e:
                self.logger.warning("ML emotion analysis failed", error=str(e))
        
        # Fallback: heuristic-based analysis
        if all(v == 0 for v in emotions.values()):
            emotions = self._heuristic_emotion_analysis(y, sr)
        
        # Normalize
        total = sum(emotions.values())
        if total > 0:
            emotions = {k: round(v / total, 3) for k, v in emotions.items()}
        
        return emotions
    
    def _heuristic_emotion_analysis(self, y: np.ndarray, sr: int) -> Dict[str, float]:
        """Heuristic-based emotion analysis using audio features"""
        emotions = {emotion: 0.2 for emotion in self.EMOTIONS}
        
        try:
            # Extract key features
            rms = np.sqrt(np.mean(y**2))
            zcr = np.mean(librosa.feature.zero_crossing_rate(y)[0])
            
            pitches, _ = librosa.piptrack(y=y, sr=sr)
            pitches_nonzero = pitches[pitches > 0]
            pitch_mean = np.mean(pitches_nonzero) if len(pitches_nonzero) > 0 else 0
            pitch_std = np.std(pitches_nonzero) if len(pitches_nonzero) > 0 else 0
            
            # High energy + high ZCR = anger or excitement
            if rms > 0.1 and zcr > 0.1:
                emotions['anger'] += 0.3
                emotions['surprise'] += 0.2
            
            # Low energy + low pitch = sadness
            elif rms < 0.05 and pitch_mean < 150:
                emotions['sadness'] += 0.4
                emotions['neutral'] += 0.1
            
            # High pitch variation = fear or surprise
            elif pitch_std > 50:
                emotions['fear'] += 0.3
                emotions['surprise'] += 0.2
            
            # Moderate energy + stable pitch = joy or neutral
            else:
                emotions['joy'] += 0.3
                emotions['neutral'] += 0.2
            
        except Exception as e:
            self.logger.warning("Heuristic analysis failed", error=str(e))
        
        return emotions
    
    def _analyze_speech_characteristics(self, y: np.ndarray, sr: int) -> Dict:
        """Analyze speech characteristics"""
        chars = {}
        
        try:
            # Speech rate estimation
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            chars['speech_rate'] = 'fast' if tempo > 130 else 'slow' if tempo < 90 else 'normal'
            
            # Volume/loudness
            rms = np.sqrt(np.mean(y**2))
            chars['volume'] = 'loud' if rms > 0.1 else 'quiet' if rms < 0.03 else 'normal'
            
            # Pitch variation
            pitches, _ = librosa.piptrack(y=y, sr=sr)
            pitches_nonzero = pitches[pitches > 0]
            if len(pitches_nonzero) > 0:
                pitch_std = np.std(pitches_nonzero)
                chars['pitch_variation'] = 'high' if pitch_std > 50 else 'low' if pitch_std < 20 else 'normal'
            else:
                chars['pitch_variation'] = 'unknown'
            
            # Voice quality
            zcr = np.mean(librosa.feature.zero_crossing_rate(y)[0])
            chars['voice_quality'] = 'breathy' if zcr < 0.05 else 'tense' if zcr > 0.15 else 'normal'
            
        except Exception as e:
            self.logger.warning("Speech characteristics analysis failed", error=str(e))
        
        return chars
    
    def _get_dominant_emotion(self, emotions: Dict) -> Tuple[str, float]:
        """Get dominant emotion and confidence"""
        if not emotions:
            return 'neutral', 0.0
        
        dominant = max(emotions, key=emotions.get)
        confidence = emotions[dominant]
        
        return dominant, round(confidence, 3)
    
    def _calculate_valence(self, emotions: Dict) -> float:
        """Calculate emotional valence (-1 to 1)"""
        positive = emotions.get('joy', 0) + emotions.get('surprise', 0) * 0.3
        negative = (emotions.get('sadness', 0) + emotions.get('anger', 0) +
                   emotions.get('fear', 0))
        
        return round(positive - negative, 3)
    
    def _calculate_arousal(self, emotions: Dict, features: Dict) -> float:
        """Calculate emotional arousal (0 to 1)"""
        # High arousal emotions
        high_arousal = emotions.get('anger', 0) + emotions.get('fear', 0) + emotions.get('surprise', 0)
        
        # Low arousal emotions
        low_arousal = emotions.get('sadness', 0) + emotions.get('neutral', 0)
        
        # Adjust based on audio features
        energy_factor = min(features.get('rms_energy', 0.05) * 5, 1)
        
        arousal = (high_arousal * 0.7 + energy_factor * 0.3) - (low_arousal * 0.3)
        
        return round(max(0, min(1, arousal)), 3)
    
    def _get_error_result(self, message: str) -> Dict:
        """Return error result"""
        return {
            'success': False,
            'error': message,
            'emotions': {e: 0.0 for e in self.EMOTIONS},
            'dominant_emotion': 'neutral',
            'confidence': 0.0
        }
    
    def analyze_text_sentiment_from_audio(self, text: str, 
                                          audio_analysis: Dict) -> Dict:
        """Combine text and audio sentiment for multimodal analysis"""
        # Get text sentiment (would be passed from text analyzer)
        # Here we just combine with audio emotions
        
        audio_emotions = audio_analysis.get('emotions', {})
        
        # Weight: 60% text, 40% audio (text more reliable for content)
        combined = {
            'multimodal_emotion': audio_analysis.get('dominant_emotion', 'neutral'),
            'audio_confidence': audio_analysis.get('confidence', 0),
            'valence': audio_analysis.get('valence', 0),
            'arousal': audio_analysis.get('arousal', 0.5),
            'speech_characteristics': audio_analysis.get('speech_characteristics', {})
        }
        
        return combined
