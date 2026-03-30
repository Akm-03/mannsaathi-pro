"""
Health Check API Routes - System status and monitoring
"""

from flask import Blueprint, jsonify, current_app
import time
import os

health_bp = Blueprint('health', __name__)

# Start time for uptime calculation
START_TIME = time.time()


@health_bp.route('/', methods=['GET'])
def health_check():
    """Basic health check"""
    uptime = time.time() - START_TIME
    
    return jsonify({
        'status': 'healthy',
        'service': 'MannSaathi Pro API',
        'version': '2.0.0',
        'uptime_seconds': int(uptime),
        'timestamp': time.time()
    })


@health_bp.route('/detailed', methods=['GET'])
def detailed_health():
    """Detailed health check with component status"""
    uptime = time.time() - START_TIME
    
    # Check components
    components = {
        'database': _check_database(),
        'emotion_analyzer': _check_emotion_analyzer(),
        'response_generator': _check_response_generator(),
        'image_analyzer': _check_image_analyzer(),
        'voice_analyzer': _check_voice_analyzer()
    }
    
    # Overall status
    all_healthy = all(c['status'] == 'ok' for c in components.values())
    
    return jsonify({
        'status': 'healthy' if all_healthy else 'degraded',
        'service': 'MannSaathi Pro API',
        'version': '2.0.0',
        'uptime_seconds': int(uptime),
        'components': components,
        'timestamp': time.time()
    })


@health_bp.route('/helplines', methods=['GET'])
def get_helplines():
    """Get all mental health helplines"""
    try:
        from ..services.crisis_detector import CrisisDetector
        
        detector = CrisisDetector()
        helplines = detector.get_all_helplines()
        
        return jsonify({
            'success': True,
            'helplines': helplines
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@health_bp.route('/config', methods=['GET'])
def get_config():
    """Get public configuration"""
    return jsonify({
        'success': True,
        'config': {
            'supported_languages': [
                'hindi', 'hinglish', 'english', 'tamil', 
                'telugu', 'bengali', 'marathi', 'gujarati'
            ],
            'supported_emotions': [
                'sadness', 'fear', 'anger', 'joy', 'surprise', 'neutral'
            ],
            'input_modes': ['text', 'voice', 'image'],
            'features': {
                'text_emotion': True,
                'voice_emotion': True,
                'image_emotion': True,
                'crisis_detection': True,
                'cultural_adaptation': True,
                'code_mixed_support': True
            },
            'version': '2.0.0'
        }
    })


def _check_database():
    """Check database connection"""
    try:
        from ..database import Database
        db = Database(current_app.config['DATABASE_PATH'])
        
        # Try a simple query
        session = db.get_session('test')
        
        return {'status': 'ok', 'message': 'Database connection successful'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def _check_emotion_analyzer():
    """Check emotion analyzer"""
    try:
        analyzer = current_app.emotion_analyzer
        
        # Test analysis
        result = analyzer.analyze("I am feeling happy today")
        
        return {
            'status': 'ok', 
            'message': 'Emotion analyzer working',
            'ml_enhancement': analyzer.use_ml_enhancement and analyzer.ml_model is not None
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def _check_response_generator():
    """Check response generator"""
    try:
        generator = current_app.response_generator
        
        return {
            'status': 'ok',
            'message': 'Response generator initialized',
            'api_available': generator.client is not None
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def _check_image_analyzer():
    """Check image analyzer"""
    try:
        analyzer = current_app.image_analyzer
        
        return {
            'status': 'ok',
            'message': 'Image analyzer initialized',
            'fer_available': analyzer.fer_model is not None
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def _check_voice_analyzer():
    """Check voice analyzer"""
    try:
        analyzer = current_app.voice_analyzer
        
        return {
            'status': 'ok',
            'message': 'Voice analyzer initialized',
            'model_available': analyzer.emotion_model is not None
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
