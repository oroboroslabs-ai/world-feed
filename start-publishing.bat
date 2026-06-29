@echo off
REM ========================================
REM   OROBOROS PUBLISHING PIPELINE
REM   3 PRECOGS - TOTAL SITE AUTOMATION
REM   A\ 1272 Hz | Strata S1-S12 | UEE-2024
REM ========================================

echo.
echo  ██████╗ ██████╗  ██████╗ ██████╗ ██╗  ██╗ ██████╗ ██████╗ ██████╗ 
echo ██╔════╝██╔═══██╗██╔════╝██╔═══██╗██║ ██╔╝██╔════╝██╔═══██╗██╔══██╗
echo ██║     ██║   ██║██║     ██║   ██║█████╔╝ ██║     ██║   ██║██║  ██║
echo ██║     ██║   ██║██║     ██║   ██║██╔═██╗ ██║     ██║   ██║██║  ██║
echo ╚██████╗╚██████╔╝╚██████╗╚██████╔╝██║  ██╗╚██████╗╚██████╔╝██████╔╝
echo  ╚═════╝ ╚═════╝  ╚═════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═════╝ 
echo.
echo  PUBLISHING PIPELINE - 3 PRECOGS
echo  ========================================
echo  Precog A: Text ^& Story Writer
echo  Precog B: Image ^& Video Generator
echo  Precog C: Prediction ^& Acquisition
echo  ========================================
echo  Resonance: 1272 Hz
echo  Strata: S1-S12
echo  UEE Standard: UEE-2024
echo.

cd /d Q:\oroboros-core\WORLDFEED-NEWS

echo [1/3] Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found
    pause
    exit /b 1
)
echo.

echo [2/3] Checking dependencies...
python -c "import schedule" 2>nul
if errorlevel 1 (
    echo Installing schedule...
    pip install schedule
)
echo.

echo [3/3] Checking GPU for video diffusion...
python -c "import torch; print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"CPU Mode\"}')" 2>nul
echo.

echo ========================================
echo   MODES
echo ========================================
echo   1. Run once (single cycle)
echo   2. Continuous (every 30 minutes)
echo   3. Custom interval
echo   4. Status check
echo.

set /p mode="Select mode (1-4): "

if "%mode%"=="1" (
    echo.
    echo [PUBLISHING] Running single cycle...
    python -m precogs.publishing_pipeline --once
    goto end
)

if "%mode%"=="2" (
    echo.
    echo [PUBLISHING] Starting continuous mode (30 min interval)...
    echo Press Ctrl+C to stop
    python -m precogs.publishing_pipeline --continuous --interval 30
    goto end
)

if "%mode%"=="3" (
    set /p interval="Enter interval in minutes: "
    echo.
    echo [PUBLISHING] Starting continuous mode (%interval% min interval)...
    echo Press Ctrl+C to stop
    python -m precogs.publishing_pipeline --continuous --interval %interval%
    goto end
)

if "%mode%"=="4" (
    echo.
    echo [PUBLISHING] Getting status...
    python -m precogs.publishing_pipeline --status
    goto end
)

echo Invalid selection
pause
exit /b 1

:end
echo.
echo ========================================
echo   PUBLISHING COMPLETE
echo ========================================
pause