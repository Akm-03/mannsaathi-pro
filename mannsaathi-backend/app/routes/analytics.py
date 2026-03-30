"""
Analytics API Routes - Dashboard and statistics
"""

from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta

analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    """Get analytics dashboard data"""
    try:
        days = request.args.get('days', 7, type=int)
        
        from ..database import Database
        db = Database(current_app.config['DATABASE_PATH'])
        
        analytics = db.get_analytics(days=days)
        
        return jsonify({
            'success': True,
            'period_days': days,
            'data': analytics,
            'generated_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        current_app.logger.error(f"Error in get_dashboard: {str(e)}")
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/session/<session_id>', methods=['GET'])
def get_session_analytics(session_id):
    """Get analytics for a specific session"""
    try:
        from ..database import Database
        db = Database(current_app.config['DATABASE_PATH'])
        
        session = db.get_session(session_id)
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        history = db.get_conversation_history(session_id, limit=100)
        emotion_history = db.get_emotion_history(session_id, limit=50)
        
        # Calculate emotion trend
        emotion_trend = []
        for record in emotion_history:
            emotion_trend.append({
                'timestamp': record.get('timestamp'),
                'dominant_emotion': record.get('dominant_emotion'),
                'intensity': record.get('intensity')
            })
        
        # Calculate sentiment trend
        sentiment_scores = [h.get('sentiment_polarity', 0) for h in emotion_history]
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'session_info': {
                'created_at': session['created_at'],
                'updated_at': session['updated_at'],
                'turn_count': session['turn_count'],
                'crisis_count': session['crisis_count']
            },
            'emotion_trend': emotion_trend,
            'sentiment_analysis': {
                'average_sentiment': round(avg_sentiment, 3),
                'trend': 'improving' if avg_sentiment > 0.1 else 
                        'declining' if avg_sentiment < -0.1 else 'stable'
            },
            'conversation_summary': {
                'total_messages': len(history),
                'user_messages': len([h for h in history if h['role'] == 'user']),
                'assistant_messages': len([h for h in history if h['role'] == 'assistant'])
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/emotions/distribution', methods=['GET'])
def get_emotion_distribution():
    """Get emotion distribution across all sessions"""
    try:
        days = request.args.get('days', 7, type=int)
        
        from ..database import Database
        db = Database(current_app.config['DATABASE_PATH'])
        
        analytics = db.get_analytics(days=days)
        
        emotion_dist = analytics.get('emotion_distribution', {})
        
        # Calculate percentages
        total = sum(emotion_dist.values()) if emotion_dist else 0
        percentages = {}
        if total > 0:
            percentages = {k: round(v / total * 100, 2) 
                          for k, v in emotion_dist.items()}
        
        return jsonify({
            'success': True,
            'period_days': days,
            'distribution': emotion_dist,
            'percentages': percentages,
            'total_records': total
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/languages/distribution', methods=['GET'])
def get_language_distribution():
    """Get language distribution across all sessions"""
    try:
        days = request.args.get('days', 7, type=int)
        
        from ..database import Database
        db = Database(current_app.config['DATABASE_PATH'])
        
        analytics = db.get_analytics(days=days)
        
        lang_dist = analytics.get('language_distribution', {})
        
        # Calculate percentages
        total = sum(lang_dist.values()) if lang_dist else 0
        percentages = {}
        if total > 0:
            percentages = {k: round(v / total * 100, 2) 
                          for k, v in lang_dist.items()}
        
        return jsonify({
            'success': True,
            'period_days': days,
            'distribution': lang_dist,
            'percentages': percentages,
            'total_records': total
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/crisis/summary', methods=['GET'])
def get_crisis_summary():
    """Get crisis events summary"""
    try:
        days = request.args.get('days', 7, type=int)
        
        from ..database import Database
        import sqlite3
        
        db_path = current_app.config['DATABASE_PATH']
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get crisis events
        cursor.execute("""
            SELECT * FROM crisis_events
            WHERE timestamp >= datetime('now', '-{} days')
            ORDER BY timestamp DESC
        """.format(days))
        
        events = [dict(row) for row in cursor.fetchall()]
        
        # Get summary by severity
        cursor.execute("""
            SELECT severity, COUNT(*) as count 
            FROM crisis_events
            WHERE timestamp >= datetime('now', '-{} days')
            GROUP BY severity
        """.format(days))
        
        severity_summary = {row['severity']: row['count'] 
                           for row in cursor.fetchall()}
        
        # Get summary by tier
        cursor.execute("""
            SELECT tier, COUNT(*) as count 
            FROM crisis_events
            WHERE timestamp >= datetime('now', '-{} days')
            GROUP BY tier
        """.format(days))
        
        tier_summary = {f"tier_{row['tier']}": row['count'] 
                       for row in cursor.fetchall()}
        
        conn.close()
        
        return jsonify({
            'success': True,
            'period_days': days,
            'total_crisis_events': len(events),
            'severity_breakdown': severity_summary,
            'tier_breakdown': tier_summary,
            'recent_events': events[:10]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/feedback/summary', methods=['GET'])
def get_feedback_summary():
    """Get user feedback summary"""
    try:
        days = request.args.get('days', 30, type=int)
        
        import sqlite3
        
        db_path = current_app.config['DATABASE_PATH']
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get average rating
        cursor.execute("""
            SELECT AVG(rating) as avg_rating, COUNT(*) as total
            FROM feedback
            WHERE timestamp >= datetime('now', '-{} days')
        """.format(days))
        
        row = cursor.fetchone()
        avg_rating = row['avg_rating'] if row['avg_rating'] else 0
        total_feedback = row['total']
        
        # Get rating distribution
        cursor.execute("""
            SELECT rating, COUNT(*) as count 
            FROM feedback
            WHERE timestamp >= datetime('now', '-{} days')
            GROUP BY rating
        """.format(days))
        
        rating_dist = {row['rating']: row['count'] 
                      for row in cursor.fetchall()}
        
        # Get helpful percentage
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN helpful = 1 THEN 1 ELSE 0 END) as helpful_count,
                COUNT(*) as total
            FROM feedback
            WHERE timestamp >= datetime('now', '-{} days')
        """.format(days))
        
        row = cursor.fetchone()
        helpful_pct = (row['helpful_count'] / row['total'] * 100) if row['total'] > 0 else 0
        
        conn.close()
        
        return jsonify({
            'success': True,
            'period_days': days,
            'average_rating': round(avg_rating, 2),
            'total_feedback': total_feedback,
            'rating_distribution': rating_dist,
            'helpful_percentage': round(helpful_pct, 2)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
