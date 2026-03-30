"""
Image Emotion Analyzer - Facial Expression Detection
Uses FER (Facial Expression Recognition) and custom models
"""

import numpy as np
from PIL import Image
import cv2
import io
import base64
from typing import Dict, List, Optional, Tuple
import structlog

logger = structlog.get_logger()


class ImageAnalyzer:
    """
    Analyze emotions from facial expressions in images
    Supports multiple faces and provides confidence scores
    """
    
    EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
    
    def __init__(self):
        self.logger = logger.bind(component="ImageAnalyzer")
        self.face_cascade = None
        self.fer_model = None
        self._init_models()
    
    def _init_models(self):
        """Initialize face detection and emotion recognition models"""
        try:
            # Initialize OpenCV face detector
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            
            # Try to load FER model
            try:
                from fer import FER
                self.fer_model = FER(mtcnn=True)
                self.logger.info("FER model loaded successfully")
            except Exception as e:
                self.logger.warning("FER model not available, using fallback", 
                                  error=str(e))
                self.fer_model = None
            
            self.logger.info("ImageAnalyzer initialized")
            
        except Exception as e:
            self.logger.error("Failed to initialize image analyzer", error=str(e))
            raise
    
    def analyze_image(self, image_data: bytes or str) -> Dict:
        """
        Analyze emotions from image
        
        Args:
            image_data: Raw image bytes or base64 encoded string
        
        Returns:
            Dict with detected faces, emotions, and confidence scores
        """
        try:
            # Decode image
            img = self._decode_image(image_data)
            if img is None:
                return self._get_error_result("Could not decode image")
            
            # Detect faces
            faces = self._detect_faces(img)
            
            if not faces:
                return {
                    'success': True,
                    'faces_detected': 0,
                    'faces': [],
                    'dominant_emotion': 'neutral',
                    'overall_mood': 'neutral',
                    'message': 'No faces detected in image'
                }
            
            # Analyze each face
            face_analyses = []
            for face in faces:
                analysis = self._analyze_face(img, face)
                face_analyses.append(analysis)
            
            # Calculate overall mood
            overall_mood = self._calculate_overall_mood(face_analyses)
            
            return {
                'success': True,
                'faces_detected': len(faces),
                'faces': face_analyses,
                'dominant_emotion': overall_mood['dominant'],
                'overall_mood': overall_mood['label'],
                'confidence': overall_mood['confidence'],
                'valence': overall_mood['valence']
            }
            
        except Exception as e:
            self.logger.error("Image analysis failed", error=str(e))
            return self._get_error_result(str(e))
    
    def _decode_image(self, image_data) -> Optional[np.ndarray]:
        """Decode image from bytes or base64 string"""
        try:
            if isinstance(image_data, str):
                # Remove data URL prefix if present
                if ',' in image_data:
                    image_data = image_data.split(',')[1]
                image_bytes = base64.b64decode(image_data)
            else:
                image_bytes = image_data
            
            # Convert to numpy array
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            return img
            
        except Exception as e:
            self.logger.error("Image decoding failed", error=str(e))
            return None
    
    def _detect_faces(self, img: np.ndarray) -> List[Tuple]:
        """Detect faces in image"""
        if self.face_cascade is None:
            return []
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(48, 48)
        )
        
        return faces
    
    def _analyze_face(self, img: np.ndarray, face_rect: Tuple) -> Dict:
        """Analyze emotions for a single face"""
        x, y, w, h = face_rect
        
        # Extract face ROI
        face_img = img[y:y+h, x:x+w]
        
        # Use FER if available
        if self.fer_model:
            return self._analyze_with_fer(face_img, face_rect)
        else:
            return self._analyze_fallback(face_img, face_rect)
    
    def _analyze_with_fer(self, face_img: np.ndarray, face_rect: Tuple) -> Dict:
        """Analyze face using FER model"""
        try:
            result = self.fer_model.detect_emotions(face_img)
            
            if result and len(result) > 0:
                emotions = result[0]['emotions']
                
                # Map FER emotions to our format
                emotion_map = {
                    'angry': 'anger',
                    'disgust': 'anger',
                    'fear': 'fear',
                    'happy': 'joy',
                    'sad': 'sadness',
                    'surprise': 'surprise',
                    'neutral': 'neutral'
                }
                
                mapped_emotions = {}
                for fer_emotion, score in emotions.items():
                    mapped = emotion_map.get(fer_emotion, 'neutral')
                    if mapped in mapped_emotions:
                        mapped_emotions[mapped] = max(mapped_emotions[mapped], score)
                    else:
                        mapped_emotions[mapped] = score
                
                dominant = max(mapped_emotions, key=mapped_emotions.get)
                
                return {
                    'bbox': list(face_rect),
                    'emotions': mapped_emotions,
                    'dominant_emotion': dominant,
                    'confidence': mapped_emotions[dominant],
                    'valence': self._calculate_valence(mapped_emotions)
                }
            
        except Exception as e:
            self.logger.warning("FER analysis failed, using fallback", error=str(e))
        
        return self._analyze_fallback(face_img, face_rect)
    
    def _analyze_fallback(self, face_img: np.ndarray, face_rect: Tuple) -> Dict:
        """Fallback analysis using simple heuristics"""
        # Convert to grayscale
        gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        
        # Simple heuristic based on brightness and contrast
        mean_brightness = np.mean(gray)
        std_brightness = np.std(gray)
        
        # Rough emotion estimation
        emotions = {
            'neutral': 0.4,
            'joy': 0.2,
            'sadness': 0.15,
            'anger': 0.1,
            'fear': 0.1,
            'surprise': 0.05
        }
        
        # Adjust based on brightness
        if mean_brightness > 150:
            emotions['joy'] += 0.2
            emotions['neutral'] -= 0.1
        elif mean_brightness < 80:
            emotions['sadness'] += 0.2
            emotions['neutral'] -= 0.1
        
        dominant = max(emotions, key=emotions.get)
        
        return {
            'bbox': list(face_rect),
            'emotions': emotions,
            'dominant_emotion': dominant,
            'confidence': emotions[dominant],
            'valence': self._calculate_valence(emotions),
            'note': 'fallback_analysis'
        }
    
    def _calculate_valence(self, emotions: Dict) -> float:
        """Calculate emotional valence (-1 to 1)"""
        positive = emotions.get('joy', 0) + emotions.get('surprise', 0) * 0.5
        negative = (emotions.get('sadness', 0) + emotions.get('anger', 0) +
                   emotions.get('fear', 0))
        
        valence = positive - negative
        return round(valence, 3)
    
    def _calculate_overall_mood(self, face_analyses: List[Dict]) -> Dict:
        """Calculate overall mood from multiple faces"""
        if not face_analyses:
            return {'dominant': 'neutral', 'label': 'neutral', 'confidence': 0}
        
        # Average emotions across all faces
        avg_emotions = {}
        for emotion in ['joy', 'sadness', 'anger', 'fear', 'surprise', 'neutral']:
            scores = [f['emotions'].get(emotion, 0) for f in face_analyses]
            avg_emotions[emotion] = np.mean(scores)
        
        dominant = max(avg_emotions, key=avg_emotions.get)
        confidence = avg_emotions[dominant]
        
        # Map to mood label
        mood_labels = {
            'joy': 'positive',
            'surprise': 'neutral-positive',
            'neutral': 'neutral',
            'sadness': 'negative',
            'anger': 'negative',
            'fear': 'negative'
        }
        
        return {
            'dominant': dominant,
            'label': mood_labels.get(dominant, 'neutral'),
            'confidence': round(confidence, 3),
            'valence': self._calculate_valence(avg_emotions)
        }
    
    def _get_error_result(self, message: str) -> Dict:
        """Return error result"""
        return {
            'success': False,
            'error': message,
            'faces_detected': 0,
            'faces': [],
            'dominant_emotion': 'neutral',
            'overall_mood': 'unknown'
        }
    
    def analyze_batch(self, images: List[bytes]) -> List[Dict]:
        """Analyze multiple images"""
        return [self.analyze_image(img) for img in images]
