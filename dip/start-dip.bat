@echo off
echo ============================================================
echo   DIP - Data Interception Proxy
echo   A\ 1272 Hz | UEE Standard | 12-Strata ECC
echo ============================================================
echo.
echo   Starting DIP Server...
echo   Port: 8081
echo   Resonance: 1272 Hz
echo.
echo ============================================================
echo.

cd /d "%~dp0"
python server.py

pause