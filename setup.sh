#!/bin/bash
# FastBillingX Complete Setup and Installation Script
# This script sets up the entire project for all three tasks

echo "╔════════════════════════════════════════════════╗"
echo "║   FastBillingX - Complete Setup Script         ║"
echo "║   All 3 Tasks: CV + Backend + Security         ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "[*] Checking Python version..."
python --version
python_version=$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [[ $(echo "$python_version >= 3.8" | bc) -eq 0 ]]; then
    echo "[!] Error: Python 3.8+ required, found $python_version"
    exit 1
fi
echo "[✓] Python $python_version detected"
echo ""

# Create virtual environment
echo "[*] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python -m venv venv
    echo "[✓] Virtual environment created"
else
    echo "[✓] Virtual environment already exists"
fi
echo ""

# Activate venv
echo "[*] Activating virtual environment..."
if [ "$OSTYPE" == "msys" ] || [ "$OSTYPE" == "win32" ]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi
echo "[✓] Virtual environment activated"
echo ""

# Upgrade pip
echo "[*] Upgrading pip..."
pip install --upgrade pip
echo "[✓] pip upgraded"
echo ""

# Install requirements
echo "[*] Installing dependencies (this may take 2-5 minutes)..."
pip install -r requirements.txt
echo "[✓] All dependencies installed"
echo ""

# Create necessary directories
echo "[*] Creating data directories..."
mkdir -p data/images
mkdir -p data/videos
mkdir -p models/weights
echo "[✓] Directories created"
echo ""

# Download model weights (if needed)
echo "[*] Checking for YOLOv8 model..."
if [ ! -f "models/best.pt" ]; then
    echo "    Model will auto-download on first run (requires internet)"
else
    echo "[✓] Model found: models/best.pt"
fi
echo ""

# Display next steps
echo "╔════════════════════════════════════════════════╗"
echo "║           SETUP COMPLETED SUCCESSFULLY!        ║"
echo "╚════════════════════════════════════════════════╝"
echo ""
echo "NEXT STEPS:"
echo ""
echo "1. TASK 1 - Computer Vision Demo (Webcam):"
echo "   $ python run_demo.py"
echo ""
echo "2. TASK 1 - Computer Vision Demo (Video):"
echo "   $ python run_demo.py --source video.mp4"
echo ""
echo "3. TASK 1 - Generate Demo Video:"
echo "   $ python create_demo_video.py"
echo ""
echo "4. TASK 2 - Start Backend API (in separate terminal):"
echo "   $ uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "5. TASK 3 - Read Security Documentation:"
echo "   $ cat docs/Payments_Security_Concept.md"
echo ""
echo "For more help:"
echo "   $ python run_demo.py --help"
echo "   $ python create_demo_video.py --help"
echo ""
