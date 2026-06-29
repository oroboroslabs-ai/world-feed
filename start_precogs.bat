@echo off
title PreCog Pipeline - Three-AI Engine
color 0a
echo ============================================================
echo            PRECOG PIPELINE - THREE-AI ENGINE
echo                  Anti-Algo News Network
echo                       A\ 1272 Hz
echo ============================================================
echo.
echo [INITIALIZING] Starting PreCog Engine...
echo.

cd /d Q:\oroboros-core\worldfeed-news

echo [STEP 1] Activating Precog A (Tor Feed Writer)...
echo [STEP 2] Activating Precog B (X Feed Writer)...
echo [STEP 3] Activating Precog C (Anthropic/Oroboros Writer)...
echo.

python run_pipeline.py

echo.
echo ============================================================
echo              PIPELINE EXECUTION COMPLETE
echo ============================================================
echo.
pause