# MannSaathi Pro 🧠💙

**An Enhanced Culturally-Adaptive Multimodal Mental Health AI for India**

MannSaathi Pro is a comprehensive mental health support system specifically designed for Indian users. It understands code-mixed Hinglish, analyzes emotions from text, voice, and images, and provides culturally appropriate responses with safety-aware crisis detection.

## 🌟 Key Features

### Multimodal Emotion Analysis
- **Text Analysis**: Advanced NLP for 8 Indian languages (Hindi, Hinglish, Tamil, Telugu, Bengali, Marathi, Gujarati, English)
- **Voice Analysis**: Speech emotion recognition from tone and prosody
- **Image Analysis**: Facial expression recognition for emotional state detection
- **Combined Analysis**: Weighted multimodal emotion fusion

### Cultural Adaptation
- Code-mixed language support (Hinglish)
- Indian cultural context awareness (family pressure, academic stress, social stigma)
- Culturally appropriate therapeutic responses
- Regional helpline integration

### Safety Features
- Two-tier crisis detection system
- 8+ Indian mental health helplines
- Automatic intervention for high-risk situations
- Safety planning resources

### Technical Stack
- **Backend**: Flask + Python 3.11
- **AI Models**: Groq LLaMA 3.3-70B, FER, SpeechBrain
- **Database**: SQLite with analytics
- **Deployment**: Docker + Docker Compose + Nginx

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker (optional)
- Groq API key

### Local Development

1. **Clone and setup**
```bash
cd mannsaathi-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

3. **Run the application**
```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Docker Deployment

1. **Build and run**
```bash
docker-compose up --build
```

2. **Access the application**
- API: `http://localhost:5000`
- With Nginx: `http://localhost`

## 📡 API Endpoints

### Chat Endpoints
- `POST /api/chat/message` - Send a message
- `GET /api/chat/history/<session_id>` - Get conversation history
- `DELETE /api/chat/session/<session_id>` - End session
- `POST /api/chat/feedback` - Submit feedback

### Multimodal Endpoints
- `POST /api/multimodal/analyze-image` - Analyze image emotions
- `POST /api/multimodal/analyze-voice` - Analyze voice emotions
- `POST /api/multimodal/combined-analysis` - Combined multimodal analysis
- `POST /api/multimodal/upload-image` - Upload and analyze image
- `POST /api/multimodal/upload-audio` - Upload and analyze audio

### Analytics Endpoints
- `GET /api/analytics/dashboard` - Get dashboard data
- `GET /api/analytics/session/<session_id>` - Get session analytics
- `GET /api/analytics/emotions/distribution` - Get emotion distribution
- `GET /api/analytics/languages/distribution` - Get language distribution
- `GET /api/analytics/crisis/summary` - Get crisis events summary
- `GET /api/analytics/feedback/summary` - Get feedback summary

### Health Endpoints
- `GET /api/health/` - Basic health check
- `GET /api/health/detailed` - Detailed health check
- `GET /api/health/helplines` - Get all helplines
- `GET /api/health/config` - Get public configuration

## 📊 Example Usage

### Send a message
```bash
curl -X POST http://localhost:5000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "mujhe bahut tension ho rahi hai",
    "session_id": "test-session-123"
  }'
```

### Analyze image
```bash
curl -X POST http://localhost:5000/api/multimodal/analyze-image \
  -H "Content-Type: application/json" \
  -d '{
    "image": "base64-encoded-image-data",
    "session_id": "test-session-123"
  }'
```

## 🛡️ Crisis Helplines

The system provides access to these Indian mental health helplines:

| Organization | Number | Hours | Languages |
|-------------|--------|-------|-----------|
| Vandrevala Foundation | 1860-2662-345 | 24/7 | English, Hindi |
| AASRA | 91-22-27546669 | 24/7 | English, Hindi |
| iCall | 022-25521111 | Mon-Sat, 10am-8pm | English, Hindi, Marathi, Gujarati |
| Sneha Foundation | 044-24640050 | 24/7 | English, Tamil |
| Roshni Trust | 040-66202000 | Mon-Sat, 11am-9pm | English, Telugu, Hindi |
| Lifeline Foundation | 033-24637401 | Daily, 10am-10pm | English, Bengali, Hindi |
| Samaritans Mumbai | 91-8422984528 | Daily, 5pm-8pm | English, Hindi, Marathi |
| Kiran Helpline | 1800-599-0019 | 24/7 | English, Hindi, Regional |

## 📁 Project Structure

```
mannsaathi-backend/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── database.py          # Database operations
│   ├── models/
│   │   ├── emotion_analyzer.py    # Text emotion analysis
│   │   ├── image_analyzer.py      # Facial emotion analysis
│   │   └── voice_analyzer.py      # Speech emotion analysis
│   ├── services/
│   │   ├── nlp_preprocessor.py    # Text preprocessing
│   │   ├── crisis_detector.py     # Crisis detection
│   │   └── response_generator.py  # LLM response generation
│   └── routes/
│       ├── chat.py          # Chat endpoints
│       ├── multimodal.py    # Multimodal endpoints
│       ├── analytics.py     # Analytics endpoints
│       └── health.py        # Health check endpoints
├── data/
│   └── emotion_lexicon.py   # Multilingual emotion lexicons
├── app.py                   # Main entry point
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker image
├── docker-compose.yml      # Docker Compose config
├── nginx.conf              # Nginx configuration
└── README.md               # This file
```

## 🔧 Configuration

Environment variables (see `.env.example`):

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Groq API key for LLM | Required |
| `SECRET_KEY` | Flask secret key | Required |
| `FLASK_ENV` | Flask environment | `development` |
| `DATABASE_PATH` | SQLite database path | `mannsaathi.db` |
| `ENABLE_ML_ENHANCEMENT` | Enable ML emotion models | `True` |
| `CRISIS_THRESHOLD` | Crisis detection threshold | `0.7` |

## 📈 Monitoring

The system provides comprehensive analytics:
- Session statistics
- Emotion distribution
- Language usage patterns
- Crisis event tracking
- User feedback analysis

Access analytics via `/api/analytics/dashboard`

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Groq for LLaMA 3.3-70B API
- FER library for facial expression recognition
- SpeechBrain for speech emotion recognition
- All mental health organizations providing helplines

---

**Disclaimer**: MannSaathi Pro is a supportive tool and not a replacement for professional mental health care. In case of emergency, please contact the helplines provided or visit your nearest hospital.
