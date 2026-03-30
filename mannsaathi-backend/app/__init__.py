"""
MannSaathi Pro - Enhanced Multimodal Mental Health Chatbot
A culturally-adaptive AI system for Indian users with sentiment analysis
"""
# In your app initialization
from app.services.knowledge_base import MentalHealthKnowledgeBase
knowledge_base = MentalHealthKnowledgeBase()
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging
from logging.handlers import RotatingFileHandler
import structlog

# Load environment variables
load_dotenv()

def configure_logging():
    """Configure structured logging"""
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # File handler for logs
    handler = RotatingFileHandler(
        'mannsaathi.log', maxBytes=10000000, backupCount=5
    )
    handler.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    
    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)
    root_logger.addHandler(console_handler)

def create_app(config_name='development'):
    """Application factory pattern"""
    configure_logging()
    
    app = Flask(__name__, 
                static_folder='../static',
                template_folder='../templates')
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
    app.config['DATABASE_PATH'] = os.getenv('DATABASE_PATH', 'mannsaathi.db')
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    app.config['REDIS_URL'] = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # CORS configuration
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://localhost:5173", "*"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "X-Session-ID"]
        }
    })
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register blueprints
    from .routes.chat import chat_bp
    from .routes.analytics import analytics_bp
    from .routes.multimodal import multimodal_bp
    from .routes.health import health_bp
    
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    app.register_blueprint(multimodal_bp, url_prefix='/api/multimodal')
    app.register_blueprint(health_bp, url_prefix='/api/health')
    
    # Initialize database
    from .database import init_db
    init_db(app.config['DATABASE_PATH'])
    
    # Initialize emotion models
    from .models.emotion_analyzer import EmotionAnalyzer
    app.emotion_analyzer = EmotionAnalyzer()
    
    # Initialize image analyzer
    from .models.image_analyzer import ImageAnalyzer
    app.image_analyzer = ImageAnalyzer()
    
    # Initialize voice analyzer
    from .models.voice_analyzer import VoiceAnalyzer
    app.voice_analyzer = VoiceAnalyzer()
    
    # Initialize crisis detector
    from .services.crisis_detector import CrisisDetector
    app.crisis_detector = CrisisDetector()
    
    # In create_app() function, update response generator initialization:

    # Initialize response generator with multi-LLM support
    from .services.response_generator import ResponseGenerator
    app.response_generator = ResponseGenerator(
        api_key=app.config['GROQ_API_KEY'],
        config={
            'GROQ_API_KEY': app.config['GROQ_API_KEY'],
            'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
            
            'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY'),
            'COHERE_API_KEY': os.getenv('COHERE_API_KEY'),
            
        }
    )

    # Initialize NLP preprocessor
    from .services.nlp_preprocessor import NLPPreprocessor
    app.nlp_preprocessor = NLPPreprocessor()
    
    logger = structlog.get_logger()
    logger.info("MannSaathi Pro initialized", 
                version="2.0.0",
                config=config_name)
    
    return app
