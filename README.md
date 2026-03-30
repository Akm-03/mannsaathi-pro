# MannSaathi Pro - Mental Health Chatbot

A culturally-adaptive, multi-LLM powered mental health support chatbot for Indian users.

## Features

- 🧠 **Multi-LLM Support**: Uses Groq, OpenAI, Claude, Gemini for diverse responses
- 🌸 **Emotion Detection**: ML-powered emotion analysis
- 🚨 **Crisis Detection**: Automatic helpline suggestions
- 🇮🇳 **Cultural Adaptation**: Hinglish support and Indian context
- 💬 **Human-like Conversations**: Natural, empathetic dialogue
- 🎨 **Beautiful UI**: Modern, responsive interface

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup
\`\`\`bash
cd mannsaathi-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
python app.py
\`\`\`

### Frontend Setup
\`\`\`bash
cd app
npm install
cp .env.example .env
npm run dev
\`\`\`

### Access the App
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000
- Health Check: http://localhost:5000/api/health/

## Environment Variables

See `.env.example` files in backend and frontend folders for required environment variables.

## Tech Stack

### Backend
- Flask (Python)
- Multiple LLM APIs (Groq, OpenAI, Anthropic, Gemini)
- Transformers (Hugging Face)
- SQLite
- LangChain

### Frontend
- React
- Vite
- Framer Motion
- React Markdown

## License

MIT

## Support

For issues or questions, please open an issue.