# MannSaathi Pro - Quick Start Guide

## 🚀 Fastest Way to Get Started

### Option 1: Automated Setup (Recommended)

#### Windows:
```powershell
# 1. Create a folder for your project
mkdir mannsaathi-pro
cd mannsaathi-pro

# 2. Download the setup script (or copy it from this folder)
# Save setup.bat in this folder

# 3. Run the setup script
.\setup.bat
```

#### Mac/Linux:
```bash
# 1. Create a folder for your project
mkdir mannsaathi-pro
cd mannsaathi-pro

# 2. Download the setup script
# Save setup.sh in this folder

# 3. Run the setup script
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup (More Control)

Follow the detailed guide in `VS_CODE_SETUP_GUIDE.md`

---

## ⚡ Quick Commands Reference

### Start Backend
```bash
cd mannsaathi-backend
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

python app.py
```
Backend runs at: http://localhost:5000

### Start Frontend
```bash
cd app
npm run dev
```
Frontend runs at: http://localhost:5173

---

## 🔑 Get Your Groq API Key

1. Go to https://groq.com
2. Sign up for an account
3. Get your API key from the dashboard
4. Add it to `mannsaathi-backend/.env`:
```
GROQ_API_KEY=gsk_your_actual_api_key_here
```

---

## 📁 File Structure After Setup

```
mannsaathi-pro/
├── mannsaathi-backend/          # Flask API
│   ├── venv/                    # Python virtual environment
│   ├── app/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── models/
│   │   ├── services/
│   │   └── routes/
│   ├── app.py                   # Main entry point
│   ├── requirements.txt
│   ├── .env                     # Your API keys here
│   └── mannsaathi.db            # SQLite database
│
├── app/                         # React Frontend
│   ├── node_modules/
│   ├── src/
│   │   └── App.tsx
│   ├── .env                     # API URL config
│   └── package.json
│
├── .vscode/                     # VS Code settings
│   └── launch.json
│
├── setup.bat                    # Windows setup script
├── setup.sh                     # Mac/Linux setup script
├── VS_CODE_SETUP_GUIDE.md       # Detailed guide
└── QUICK_START.md               # This file
```

---

## 🧪 Test Your Setup

### Test Backend
```bash
# In browser or using curl
curl http://localhost:5000/api/health/

# Should return:
# {"status": "healthy", "service": "MannSaathi Pro API"}
```

### Test Chat API
```bash
curl -X POST http://localhost:5000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "hello", "session_id": "test123"}'
```

### Test Frontend
Open http://localhost:5173 and type a message!

---

## 🐛 Common Issues

| Problem | Solution |
|---------|----------|
| `pip not found` | Use `python -m pip` instead |
| `npm not found` | Reinstall Node.js from nodejs.org |
| `Port 5000 in use` | Change PORT in `.env` to 5001 |
| `CORS error` | Make sure backend is running |
| `Module not found` | Run `pip install -r requirements.txt` |

---

## 📚 Documentation

- **Detailed Setup**: `VS_CODE_SETUP_GUIDE.md`
- **Enhancements**: `MANNSAATHI_PRO_ENHANCEMENTS.md`
- **Backend README**: `mannsaathi-backend/README.md`

---

## 🎉 You're Ready!

Once both backend and frontend are running:
1. Open http://localhost:5173
2. Type your message in Hinglish, Hindi, or English
3. The AI will respond with emotion analysis!

For crisis support, the system will automatically show helpline numbers.

---

**Built with 💙 for India's mental health**
