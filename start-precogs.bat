@echo off
echo ========================================
echo   OROBOROS PRECOG PIPELINE STARTER
echo   A\ 1272 Hz | UEE-2024 | 12-Strata
echo ========================================
echo.
echo Starting Three Precog Pipeline...
echo   - Writing Precog (Anthropic, Glasswing, X Profile, Breaking News)
echo   - Video Precog (Glasswing, Breaking News)
echo   - Image Precog (All sources with Unsplash photos)
echo.
echo API Server: http://127.0.0.1:8083
echo Endpoints:
echo   - GET /api/precog/feed
echo   - GET /api/precog/writing
echo   - GET /api/precog/video
echo   - GET /api/precog/image
echo   - GET /api/precog/status
echo.
cd /d "%~dp0precogs"
python api_server.py
pause