"""
Database Module - SQLite for Session Management
Stores conversation history, emotion data, and analytics
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional
from contextlib import contextmanager
import structlog

logger = structlog.get_logger()

# Database schema
SCHEMA = """
-- Sessions table
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_agent TEXT,
    ip_address TEXT,
    turn_count INTEGER DEFAULT 0,
    crisis_count INTEGER DEFAULT 0,
    language_preference TEXT DEFAULT 'hinglish'
);

-- Conversations table
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    turn_number INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role TEXT,  -- 'user' or 'assistant'
    content TEXT,
    input_mode TEXT,  -- 'text', 'voice', 'image'
    emotions TEXT,  -- JSON string
    dominant_emotion TEXT,
    crisis_flag INTEGER DEFAULT 0,
    language_detected TEXT,
    response_time_ms INTEGER,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);

-- Emotion history table
CREATE TABLE IF NOT EXISTS emotion_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    emotions TEXT,  -- JSON string
    dominant_emotion TEXT,
    sentiment_polarity REAL,
    intensity REAL,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);

-- Crisis events table
CREATE TABLE IF NOT EXISTS crisis_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tier INTEGER,
    triggered_by TEXT,
    severity TEXT,
    keywords TEXT,  -- JSON string
    intervention_provided INTEGER DEFAULT 0,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);

-- Analytics table
CREATE TABLE IF NOT EXISTS analytics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT UNIQUE,
    total_sessions INTEGER DEFAULT 0,
    total_messages INTEGER DEFAULT 0,
    crisis_events INTEGER DEFAULT 0,
    avg_session_duration_minutes REAL,
    emotion_distribution TEXT,  -- JSON string
    language_distribution TEXT  -- JSON string
);

-- User feedback table
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    rating INTEGER,  -- 1-5
    feedback_text TEXT,
    helpful INTEGER,  -- 0 or 1
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
);
"""


def init_db(db_path: str = 'mannsaathi.db'):
    """Initialize database with schema"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.executescript(SCHEMA)
        conn.commit()
        conn.close()
        logger.info("Database initialized", path=db_path)
    except Exception as e:
        logger.error("Database initialization failed", error=str(e))
        raise


@contextmanager
def get_db_connection(db_path: str = 'mannsaathi.db'):
    """Context manager for database connections"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


class Database:
    """Database operations for MannSaathi"""
    
    def __init__(self, db_path: str = 'mannsaathi.db'):
        self.db_path = db_path
        self.logger = logger.bind(component="Database")
    
    # Session operations
    def create_session(self, session_id: str, user_agent: str = None, 
                       ip_address: str = None) -> bool:
        """Create a new session"""
        try:
            with get_db_connection(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO sessions (session_id, user_agent, ip_address)
                    VALUES (?, ?, ?)
                """, (session_id, user_agent, ip_address))
                conn.commit()
                self.logger.debug("Session created", session_id=session_id)
                return True
        except Exception as e:
            self.logger.error("Failed to create session", error=str(e))
            return False
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session by ID"""
        try:
            with get_db_connection(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM sessions WHERE session_id = ?
                """, (session_id,))
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            self.logger.error("Failed to get session", error=str(e))
            return None
    
    def update_session(self, session_id: str, **kwargs) -> bool:
        """Update session fields"""
        try:
            with get_db_connection(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Build update query
                fields = []
                values = []
                for key, value in kwargs.items():
                    fields.append(f"{key} = ?")
                    values.append(value)
                
                values.append(session_id)
                
                query = f"""
                    UPDATE sessions 
                    SET {', '.join(fields)}, updated_at = CURRENT_TIMESTAMP
                    WHERE session_id = ?
                """
                
                cursor.execute(query, values)
                conn.commit()
                return True
        except Exception as e:
            self.logger.error("Failed to update session", error=str(e))
            return False
    
    # Conversation operations
    def add_message(self, session_id: str, turn_number: int, role: str,
                    content: str, input_mode: str = 'text',
                    emotions: Dict = None, dominant_emotion: str = None,
                    crisis_flag: bool = False, language_detected: str = None,
                    response_time_ms: int = None) -> bool:
        """Add a message to conversation"""
        try:
            with get_db_connection(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO conversations 
                    (session_id, turn_number, role, content, input_mode, 
                     emotions, dominant_emotion, crisis_flag, language_detected, 
                     response_time_ms)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    session_id, turn_number, role, content, input_mode,
                    json.dumps(emotions) if emotions else None,
                    dominant_emotion, 1 if crisis_flag else 0,
                    language_detected, response_time_ms
                ))
                conn.commit()
                
                # Update session turn count
                cursor.execute("""
                    UPDATE sessions 
                    SET turn_count = turn_count + 1,
                        crisis_count = crisis_count + ?
                    WHERE session_id = ?
                """, (1 if crisis_flag else 0, session_id))
                conn.commit()
                
                return True
        except Exception as e:
            self.logger.error("Failed to add message", error=str(e))
            return False
    
    def get_conversation_history(self, session_id: str, 
                                  limit: int = 20) -> List[Dict]:
        """Get conversation history for a session"""
        try:
            with get_db_connection(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM conversations 
                    WHERE session_id = ?
                    ORDER BY turn_number DESC
                    LIMIT ?
                """, (session_id, limit))
                rows = cursor.fetchall()
                
                history = []
                for row in rows:
                    row_dict = dict(row)
                    if row_dict.get('emotions'):
                        row_dict['emotions'] = json.loads(row_dict['emotions'])
                    history.append(row_dict)
                
                return list(reversed(history))
        except Exception as e:
            self.logger.error("Failed to get conversation history", error=str(e))
            return []
    
    # Emotion history operations
    def add_emotion_record(self, session_id: str, emotions: Dict,
                           dominant_emotion: str, sentiment_polarity: float = 0,
                           intensity: float = 0) -> bool:
        """Add emotion record"""
        try:
            with get_db_connection(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO emotion_history 
                    (session_id, emotions, dominant_emotion, sentiment_polarity, intensity)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    session_id, json.dumps(emotions), dominant_emotion,
                    sentiment_polarity, intensity
                ))
                conn.commit()
                return True
        except Exception as e:
            self.logger.error("Failed to add emotion record", error=str(e))
            return False
    
    def get_emotion_history(self, session_id: str, 
                            limit: int = 10) -> List[Dict]:
        """Get recent emotion history for crisis detection"""
        try:
            with get_db_connection(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM emotion_history 
                    WHERE session_id = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (session_id, limit))
                rows = cursor.fetchall()
                
                history = []
                for row in rows:
                    row_dict = dict(row)
                    if row_dict.get('emotions'):
                        row_dict['emotions'] = json.loads(row_dict['emotions'])
                    history.append(row_dict)
                
                return list(reversed(history))
        except Exception as e:
            self.logger.error("Failed to get emotion history", error=str(e))
            return []
    
    # Crisis event operations
    def log_crisis_event(self, session_id: str, tier: int,
                         triggered_by: str, severity: str,
                         keywords: List[str] = None,
                         intervention_provided: bool = False) -> bool:
        """Log a crisis event"""
        try:
            with get_db_connection(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO crisis_events 
                    (session_id, tier, triggered_by, severity, keywords, intervention_provided)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    session_id, tier, triggered_by, severity,
                    json.dumps(keywords) if keywords else None,
                    1 if intervention_provided else 0
                ))
                conn.commit()
                return True
        except Exception as e:
            self.logger.error("Failed to log crisis event", error=str(e))
            return False
    
    # Analytics operations
    def get_analytics(self, days: int = 7) -> Dict:
        """Get analytics data"""
        try:
            with get_db_connection(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total sessions
                cursor.execute("""
                    SELECT COUNT(*) as total FROM sessions
                    WHERE created_at >= datetime('now', '-{} days')
                """.format(days))
                total_sessions = cursor.fetchone()['total']
                
                # Total messages
                cursor.execute("""
                    SELECT COUNT(*) as total FROM conversations
                    WHERE timestamp >= datetime('now', '-{} days')
                """.format(days))
                total_messages = cursor.fetchone()['total']
                
                # Crisis events
                cursor.execute("""
                    SELECT COUNT(*) as total FROM crisis_events
                    WHERE timestamp >= datetime('now', '-{} days')
                """.format(days))
                crisis_events = cursor.fetchone()['total']
                
                # Emotion distribution
                cursor.execute("""
                    SELECT dominant_emotion, COUNT(*) as count 
                    FROM emotion_history
                    WHERE timestamp >= datetime('now', '-{} days')
                    GROUP BY dominant_emotion
                """.format(days))
                emotion_dist = {row['dominant_emotion']: row['count'] 
                               for row in cursor.fetchall()}
                
                # Language distribution
                cursor.execute("""
                    SELECT language_detected, COUNT(*) as count 
                    FROM conversations
                    WHERE timestamp >= datetime('now', '-{} days')
                    AND language_detected IS NOT NULL
                    GROUP BY language_detected
                """.format(days))
                lang_dist = {row['language_detected']: row['count'] 
                            for row in cursor.fetchall()}
                
                return {
                    'total_sessions': total_sessions,
                    'total_messages': total_messages,
                    'crisis_events': crisis_events,
                    'emotion_distribution': emotion_dist,
                    'language_distribution': lang_dist,
                    'period_days': days
                }
        except Exception as e:
            self.logger.error("Failed to get analytics", error=str(e))
            return {}
    
    # Feedback operations
    def add_feedback(self, session_id: str, rating: int,
                     feedback_text: str = None, helpful: bool = None) -> bool:
        """Add user feedback"""
        try:
            with get_db_connection(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO feedback (session_id, rating, feedback_text, helpful)
                    VALUES (?, ?, ?, ?)
                """, (session_id, rating, feedback_text, 1 if helpful else 0))
                conn.commit()
                return True
        except Exception as e:
            self.logger.error("Failed to add feedback", error=str(e))
            return False
