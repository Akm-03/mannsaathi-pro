@echo off
REM MannSaathi Pro - Windows Setup Script
REM Run this in VS Code terminal (PowerShell or CMD)

echo ==========================================
echo    MannSaathi Pro - Setup Script
echo ==========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.11+
    exit /b 1
)
echo [OK] Python found

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found. Please install Node.js 18+
    exit /b 1
)
echo [OK] Node.js found

REM Create project structure
echo.
echo [1/6] Creating project structure...
mkdir mannsaathi-backend 2>nul
mkdir app 2>nul

REM Backend Setup
echo.
echo [2/6] Setting up backend...
cd mannsaathi-backend

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Create requirements.txt
echo Creating requirements.txt...
echo flask==3.0.0 > requirements.txt
echo flask-cors==4.0.0 >> requirements.txt
echo groq==0.4.0 >> requirements.txt
echo numpy==1.26.0 >> requirements.txt
echo pillow==10.1.0 >> requirements.txt
echo opencv-python==4.8.1 >> requirements.txt
echo nltk==3.8.1 >> requirements.txt
echo textblob==0.17.1 >> requirements.txt
echo requests==2.31.0 >> requirements.txt
echo python-dotenv==1.0.0 >> requirements.txt
echo pydantic==2.5.0 >> requirements.txt
echo python-multipart==0.0.6 >> requirements.txt
echo structlog==23.2.0 >> requirements.txt

REM Install dependencies
echo Installing Python dependencies (this may take a few minutes)...
pip install -q -r requirements.txt

REM Download NLTK data
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)"

REM Create .env file
echo Creating .env file...
echo FLASK_ENV=development > .env
echo FLASK_DEBUG=True >> .env
echo SECRET_KEY=your-secret-key-change-this >> .env
echo PORT=5000 >> .env
echo GROQ_API_KEY=your-groq-api-key-here >> .env
echo DATABASE_PATH=mannsaathi.db >> .env
echo UPLOAD_FOLDER=uploads >> .env

echo.
echo [3/6] Backend setup complete!
echo.
cd ..

REM Frontend Setup
echo [4/6] Setting up frontend...

REM Create React app with Vite
echo Creating React app...
call npx create-vite@latest app --template react-ts --force

REM Install frontend dependencies
cd app
echo Installing frontend dependencies (this may take a few minutes)...
call npm install

REM Install additional packages
call npm install uuid @types/uuid sonner lucide-react
call npm install -D tailwindcss postcss autoprefixer

REM Initialize Tailwind
call npx tailwindcss init -p

REM Create .env file
echo Creating frontend .env file...
echo VITE_API_URL=http://localhost:5000/api > .env

echo.
echo [5/6] Frontend setup complete!
echo.
cd ..

REM Create VS Code settings
echo [6/6] Creating VS Code settings...
mkdir .vscode 2>nul
(
echo {
echo   "version": "0.2.0",
echo   "configurations": [
echo     {
echo       "name": "Python: Flask",
echo       "type": "python",
echo       "request": "launch",
echo       "module": "app",
echo       "cwd": "${workspaceFolder}/mannsaathi-backend",
echo       "env": {
echo         "FLASK_APP": "app.py",
echo         "FLASK_DEBUG": "1"
echo       },
echo       "jinja": true
echo     }
echo   ]
echo }
) > .vscode\launch.json

echo.
echo ==========================================
echo    Setup Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Get your Groq API key from https://groq.com
echo 2. Edit mannsaathi-backend/.env and add your GROQ_API_KEY
echo 3. Open VS Code in this folder: code .
echo 4. Open two terminals in VS Code
echo 5. Terminal 1 - Backend:
echo    cd mannsaathi-backend
echo    venv\Scripts\activate
echo    python app.py
echo 6. Terminal 2 - Frontend:
echo    cd app
echo    npm run dev
echo 7. Open http://localhost:5173 in your browser
echo.
pause
