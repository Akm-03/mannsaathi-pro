"""
Chat API Routes - Main conversation endpoint
"""

from flask import Blueprint, request, jsonify, current_app
import uuid
import time
from datetime import datetime

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/message', methods=['POST'])
def send_message():
    """Process user message and generate response"""
    start_time = time.time()
    
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        user_message = data['message']
        session_id = data.get('session_id') or str(uuid.uuid4())
        input_mode = data.get('input_mode', 'text')
        
        # Get services from app context
        nlp_preprocessor = current_app.nlp_preprocessor
        emotion_analyzer = current_app.emotion_analyzer
        crisis_detector = current_app.crisis_detector
        response_generator = current_app.response_generator
        
        # Step 1: NLP Preprocessing
        nlp_result = nlp_preprocessor.preprocess(user_message)
        
        # Step 2: Emotion Analysis
        emotion_result = emotion_analyzer.analyze(
            nlp_result['normalized'],
            language=nlp_result['language']['primary']
        )
        
        # Step 3: Get conversation history
        from ..database import Database
        db = Database(current_app.config['DATABASE_PATH'])
        
        # Create session if new
        session = db.get_session(session_id)
        if not session:
            db.create_session(
                session_id,
                user_agent=request.headers.get('User-Agent'),
                ip_address=request.remote_addr
            )
            turn_number = 1
        else:
            turn_number = session['turn_count'] + 1
        
        conversation_history = db.get_conversation_history(session_id, limit=10)
        emotion_history = db.get_emotion_history(session_id, limit=5)
        
        # Step 4: Crisis Detection
        crisis_result = crisis_detector.detect(
            user_message,
            emotion_result,
            emotion_history
        )
        
        # Step 5: Generate Response
        response_text = response_generator.generate_response(
            user_message=user_message,
            emotion=emotion_result.get('dominant_emotion')
        )

        response_result = {
            "response": response_text,
            "model": "default"
        }
        
        # Step 6: Log to database
        db.add_message(
            session_id=session_id,
            turn_number=turn_number,
            role='user',
            content=user_message,
            input_mode=input_mode,
            emotions=emotion_result['emotions'],
            dominant_emotion=emotion_result['dominant_emotion'],
            crisis_flag=crisis_result['is_crisis'],
            language_detected=nlp_result['language']['primary']
        )
        
        db.add_message(
            session_id=session_id,
            turn_number=turn_number,
            role='assistant',
            content=response_result['response'],
            input_mode='text',
            emotions=None,
            response_time_ms=int((time.time() - start_time) * 1000)
        )
        
        # Log emotion record
        db.add_emotion_record(
            session_id=session_id,
            emotions=emotion_result['emotions'],
            dominant_emotion=emotion_result['dominant_emotion'],
            sentiment_polarity=emotion_result['sentiment']['polarity'],
            intensity=emotion_result['intensity']
        )
        
        # Log crisis event if detected
        if crisis_result['is_crisis']:
            db.log_crisis_event(
                session_id=session_id,
                tier=crisis_result['tier'],
                triggered_by=crisis_result['triggered_by'],
                severity=crisis_result['severity'],
                keywords=[k['keyword'] for k in 
                         crisis_result['details'].get('detected_keywords', [])],
                intervention_provided=True
            )
        
        response_time_ms = int((time.time() - start_time) * 1000)
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'turn_number': turn_number,
            'response': response_result['response'],
            'model': response_result['model'],
            'emotion_analysis': {
                'emotions': emotion_result['emotions'],
                'dominant_emotion': emotion_result['dominant_emotion'],
                'confidence': emotion_result['confidence'],
                'intensity': emotion_result['intensity'],
                'sentiment': emotion_result['sentiment']
            },
            'language': {
                'detected': nlp_result['language']['primary'],
                'is_code_mixed': nlp_result['is_code_mixed'],
                'hindi_ratio': nlp_result['hindi_ratio'],
                'english_ratio': nlp_result['english_ratio']
            },
            'crisis': crisis_result,
            'cultural_context': emotion_result.get('cultural_context', {}),
            'response_time_ms': response_time_ms
        })
        
    except Exception as e:
        current_app.logger.error(f"Error in send_message: {str(e)}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@chat_bp.route('/history/<session_id>', methods=['GET'])
def get_history(session_id):
    """Get conversation history for a session"""
    try:
        from ..database import Database
        db = Database(current_app.config['DATABASE_PATH'])
        
        history = db.get_conversation_history(session_id, limit=50)
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'history': history
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@chat_bp.route('/session/<session_id>', methods=['DELETE'])
def end_session(session_id):
    """End a chat session"""
    try:
        from ..database import Database
        db = Database(current_app.config['DATABASE_PATH'])
        
        # Get session stats
        session = db.get_session(session_id)
        
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'stats': {
                'turn_count': session['turn_count'],
                'crisis_count': session['crisis_count'],
                'created_at': session['created_at'],
                'duration': 'Session ended'
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@chat_bp.route('/feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback"""
    try:
        data = request.get_json()
        
        session_id = data.get('session_id')
        rating = data.get('rating')
        feedback_text = data.get('feedback_text')
        helpful = data.get('helpful')
        
        if not session_id or not rating:
            return jsonify({'error': 'Session ID and rating are required'}), 400
        
        from ..database import Database
        db = Database(current_app.config['DATABASE_PATH'])
        
        success = db.add_feedback(session_id, rating, feedback_text, helpful)
        
        if success:
            return jsonify({'success': True, 'message': 'Feedback submitted'})
        else:
            return jsonify({'error': 'Failed to submit feedback'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
