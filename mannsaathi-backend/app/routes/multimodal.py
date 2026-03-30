"""
Multimodal API Routes - Image and Voice Analysis
"""

from flask import Blueprint, request, jsonify, current_app
import base64

multimodal_bp = Blueprint('multimodal', __name__)


@multimodal_bp.route('/analyze-image', methods=['POST'])
def analyze_image():
    """Analyze image for facial emotions"""
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({'error': 'Image data is required'}), 400
        
        image_data = data['image']
        session_id = data.get('session_id')
        
        # Get image analyzer
        image_analyzer = current_app.image_analyzer
        
        # Analyze image
        result = image_analyzer.analyze_image(image_data)
        
        # Log to database if session exists
        if session_id and result.get('success'):
            from ..database import Database
            db = Database(current_app.config['DATABASE_PATH'])
            
            db.add_emotion_record(
                session_id=session_id,
                emotions=result.get('faces', [{}])[0].get('emotions', {}),
                dominant_emotion=result.get('dominant_emotion', 'neutral'),
                intensity=result.get('faces', [{}])[0].get('confidence', 0)
            )
        
        return jsonify(result)
        
    except Exception as e:
        current_app.logger.error(f"Error in analyze_image: {str(e)}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@multimodal_bp.route('/analyze-voice', methods=['POST'])
def analyze_voice():
    """Analyze voice/audio for emotion"""
    try:
        data = request.get_json()
        
        if not data or 'audio' not in data:
            return jsonify({'error': 'Audio data is required'}), 400
        
        audio_data = data['audio']
        sample_rate = data.get('sample_rate', 16000)
        session_id = data.get('session_id')
        
        # Get voice analyzer
        voice_analyzer = current_app.voice_analyzer
        
        # Analyze audio
        result = voice_analyzer.analyze_audio(audio_data, sample_rate)
        
        # Log to database if session exists
        if session_id and result.get('success'):
            from ..database import Database
            db = Database(current_app.config['DATABASE_PATH'])
            
            db.add_emotion_record(
                session_id=session_id,
                emotions=result.get('emotions', {}),
                dominant_emotion=result.get('dominant_emotion', 'neutral'),
                intensity=result.get('arousal', 0)
            )
        
        return jsonify(result)
        
    except Exception as e:
        current_app.logger.error(f"Error in analyze_voice: {str(e)}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@multimodal_bp.route('/combined-analysis', methods=['POST'])
def combined_analysis():
    """Combined text, image, and voice analysis"""
    try:
        data = request.get_json()
        
        session_id = data.get('session_id')
        text = data.get('text')
        image_data = data.get('image')
        audio_data = data.get('audio')
        
        results = {
            'success': True,
            'modalities': {},
            'combined_emotion': 'neutral',
            'confidence': 0
        }
        
        # Text analysis
        if text:
            nlp_result = current_app.nlp_preprocessor.preprocess(text)
            emotion_result = current_app.emotion_analyzer.analyze(
                nlp_result['normalized'],
                language=nlp_result['language']['primary']
            )
            results['modalities']['text'] = {
                'emotions': emotion_result['emotions'],
                'dominant_emotion': emotion_result['dominant_emotion'],
                'confidence': emotion_result['confidence']
            }
        
        # Image analysis
        if image_data:
            image_result = current_app.image_analyzer.analyze_image(image_data)
            if image_result.get('success'):
                results['modalities']['image'] = {
                    'faces_detected': image_result.get('faces_detected', 0),
                    'dominant_emotion': image_result.get('dominant_emotion'),
                    'overall_mood': image_result.get('overall_mood'),
                    'confidence': image_result.get('confidence')
                }
        
        # Voice analysis
        if audio_data:
            voice_result = current_app.voice_analyzer.analyze_audio(audio_data)
            if voice_result.get('success'):
                results['modalities']['voice'] = {
                    'emotions': voice_result.get('emotions'),
                    'dominant_emotion': voice_result.get('dominant_emotion'),
                    'confidence': voice_result.get('confidence'),
                    'speech_characteristics': voice_result.get('speech_characteristics')
                }
        
        # Combine emotions (weighted average)
        combined_emotions = {}
        weights = {'text': 0.5, 'image': 0.25, 'voice': 0.25}
        
        for modality, weight in weights.items():
            if modality in results['modalities']:
                emotions = results['modalities'][modality].get('emotions', {})
                for emotion, score in emotions.items():
                    if emotion not in combined_emotions:
                        combined_emotions[emotion] = 0
                    combined_emotions[emotion] += score * weight
        
        # Normalize
        total = sum(combined_emotions.values())
        if total > 0:
            combined_emotions = {k: round(v / total, 3) for k, v in combined_emotions.items()}
        
        if combined_emotions:
            results['combined_emotion'] = max(combined_emotions, key=combined_emotions.get)
            results['combined_emotions'] = combined_emotions
            results['confidence'] = combined_emotions[results['combined_emotion']]
        
        return jsonify(results)
        
    except Exception as e:
        current_app.logger.error(f"Error in combined_analysis: {str(e)}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@multimodal_bp.route('/upload-image', methods=['POST'])
def upload_image():
    """Upload and analyze image file"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        session_id = request.form.get('session_id')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read file
        image_bytes = file.read()
        
        # Convert to base64
        image_b64 = base64.b64encode(image_bytes).decode('utf-8')
        
        # Analyze
        image_analyzer = current_app.image_analyzer
        result = image_analyzer.analyze_image(image_b64)
        
        return jsonify(result)
        
    except Exception as e:
        current_app.logger.error(f"Error in upload_image: {str(e)}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@multimodal_bp.route('/upload-audio', methods=['POST'])
def upload_audio():
    """Upload and analyze audio file"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        file = request.files['audio']
        session_id = request.form.get('session_id')
        sample_rate = int(request.form.get('sample_rate', 16000))
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read file
        audio_bytes = file.read()
        
        # Convert to base64
        audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')
        
        # Analyze
        voice_analyzer = current_app.voice_analyzer
        result = voice_analyzer.analyze_audio(audio_b64, sample_rate)
        
        return jsonify(result)
        
    except Exception as e:
        current_app.logger.error(f"Error in upload_audio: {str(e)}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
