@echo off
REM Oroboros Video Diffusion Pipeline Startup
REM 1272 Hz Resonance | Strata S1-S12 | UEE-2024

echo ========================================
echo   OROBOROS VIDEO DIFFUSION PIPELINE
echo   Q:\video-production-pipeline
echo   1272 Hz Resonance
echo ========================================
echo.

cd /d Q:\video-production-pipeline

echo [1/3] Checking GPU...
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
if errorlevel 1 (
    echo WARNING: No NVIDIA GPU detected or drivers not installed
    echo Video generation will run in CPU mode (slower)
)
echo.

echo [2/3] Checking Python environment...
python --version
if errorlevel 1 (
    echo ERROR: Python not found
    echo Please install Python 3.10+ and add to PATH
    pause
    exit /b 1
)
echo.

echo [3/3] Checking dependencies...
python -c "import torch; print(f'PyTorch: {torch.__version__}')" 2>nul
if errorlevel 1 (
    echo Installing PyTorch...
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
)

python -c "import diffusers; print(f'Diffusers: {diffusers.__version__}')" 2>nul
if errorlevel 1 (
    echo Installing Diffusers...
    pip install diffusers transformers accelerate safetensors
)
echo.

echo ========================================
echo   VIDEO PIPELINE READY
echo ========================================
echo.
echo Available modes:
echo   1. text_to_image       - SDXL text-to-image
echo   2. image_to_video       - SVD image-to-video
echo   3. text_to_video        - CogVideoX direct
echo   4. style_transfer       - IP-Adapter style
echo   5. keyframe_interpolate - FILM interpolation
echo.
echo Usage:
echo   python -c "from pipeline.controller import OroborosVideoPipeline; p = OroborosVideoPipeline(); p.text_to_video('prompt')"
echo.
echo Press any key to start interactive mode...
pause >nul

REM Start interactive Python session
python -i -c "from pipeline.controller import OroborosVideoPipeline; pipeline = OroborosVideoPipeline(); print('Pipeline ready: pipeline.text_to_video(\"your prompt\")')"