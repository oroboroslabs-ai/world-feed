@echo off
echo ========================================
echo   OROBOROS PRECOG ENGINE
echo   A\ 1272 Hz | UEE-2024 | 12-Strata
echo ========================================
echo.
echo Starting the 3 Precogs...
echo   - Precog A: Text ^& Story Writer
echo   - Precog B: Image ^& Video Generator
echo   - Precog C: Prediction ^& Acquisition
echo.
echo The Precogs will:
echo   1. Predict content needs
echo   2. Generate text stories
echo   3. Create images and videos
echo   4. Post everything to the site
echo.
echo ========================================
echo.

cd /d "%~dp0precogs"

if "%1"=="--continuous" (
    echo [PRECOG] Running in CONTINUOUS mode
    echo [PRECOG] Content will be generated every 30 minutes
    python precog_engine.py --continuous
) else if "%1"=="--once" (
    echo [PRECOG] Running ONCE and exiting
    python precog_engine.py --once
) else (
    echo [PRECOG] Running once. Use --continuous for continuous mode.
    python precog_engine.py --once
)

echo.
echo ========================================
echo [PRECOG] Cycle complete. Check dip.html for updates.
echo ========================================
pause