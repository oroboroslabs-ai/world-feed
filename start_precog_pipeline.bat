@echo off
REM Start Precog Pipeline - Three AI Content Generation
REM A\ 1272 Hz
REM Oroboros Labs

echo ========================================
echo   PRECOG PIPELINE STARTER
echo   Resonance: 1272 Hz
echo   UEE Standard: UEE-2024
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

echo [INFO] Python found
echo.

REM Install dependencies
echo [INFO] Installing dependencies...
pip install flask flask-cors -q
if errorlevel 1 (
    echo [WARN] Some dependencies may have failed to install
)
echo.

REM Start the Precog API Server
echo [INFO] Starting Precog API Server on port 8082...
echo [INFO] Writing Precog: Active
echo [INFO] Video Precog: Active
echo [INFO] Image Precog: Active
echo.
echo [INFO] Endpoints:
echo   - http://localhost:8082/api/precog/feed
echo   - http://localhost:8082/api/precog/writing
echo   - http://localhost:8082/api/precog/video
echo   - http://localhost:8082/api/precog/image
echo   - http://localhost:8082/api/precog/status
echo.
echo [INFO] User Operations:
echo   - http://localhost:8082/api/user/profile
echo   - http://localhost:8082/api/user/preferences
echo   - http://localhost:8082/api/user/bookmarks
echo.
echo [INFO] Press Ctrl+C to stop
echo ========================================
echo.

python precogs/api_server.py