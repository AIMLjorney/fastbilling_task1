@REM FastBillingX Complete Setup Script for Windows
@REM This script sets up the entire project for all three tasks

@echo off
cls
echo.
echo ╔════════════════════════════════════════════════╗
echo ║   FastBillingX - Complete Setup Script         ║
echo ║   All 3 Tasks: CV + Backend + Security         ║
echo ╚════════════════════════════════════════════════╝
echo.

REM Check Python version
echo [*] Checking Python version...
python --version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo [✓] Python %python_version% detected
echo.

REM Create virtual environment
echo [*] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo [✓] Virtual environment created
) else (
    echo [✓] Virtual environment already exists
)
echo.

REM Activate venv
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat
echo [✓] Virtual environment activated
echo.

REM Upgrade pip
echo [*] Upgrading pip...
python -m pip install --upgrade pip
echo [✓] pip upgraded
echo.

REM Install requirements
echo [*] Installing dependencies (this may take 2-5 minutes)...
pip install -r requirements.txt
if errorlevel 1 (
    echo [!] Error installing dependencies
    exit /b 1
)
echo [✓] All dependencies installed
echo.

REM Create directories
echo [*] Creating data directories...
if not exist "data\images" mkdir data\images
if not exist "data\videos" mkdir data\videos
if not exist "models\weights" mkdir models\weights
echo [✓] Directories created
echo.

REM Display next steps
echo ╔════════════════════════════════════════════════╗
echo ║           SETUP COMPLETED SUCCESSFULLY!        ║
echo ╚════════════════════════════════════════════════╝
echo.
echo NEXT STEPS:
echo.
echo 1. TASK 1 - Computer Vision Demo (Webcam):
echo    python run_demo.py
echo.
echo 2. TASK 1 - Computer Vision Demo (Video):
echo    python run_demo.py --source video.mp4
echo.
echo 3. TASK 1 - Generate Demo Video:
echo    python create_demo_video.py
echo.
echo 4. TASK 2 - Start Backend API (in separate terminal):
echo    uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
echo.
echo 5. TASK 3 - Read Security Documentation:
echo    type docs\Payments_Security_Concept.md
echo.
echo For more help:
echo    python run_demo.py --help
echo    python create_demo_video.py --help
echo.
pause
