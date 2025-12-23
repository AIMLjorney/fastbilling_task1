# FastBillingX Deployment & Testing Guide

## 🎯 Quick Verification Checklist

Run these commands to verify everything is properly implemented:

```bash
# 1. Check all files exist
ls -la src/main.py src/detector.py src/cart_manager.py src/visualizer.py
ls -la run_demo.py create_demo_video.py
ls -la models/train.py models/dataset.yaml
ls -la backend/app/main.py
ls -la docs/API_README.md docs/Payments_Security_Concept.md

# 2. Check Python syntax
python -m py_compile src/main.py
python -m py_compile src/detector.py
python -m py_compile src/cart_manager.py
python -m py_compile src/visualizer.py
python -m py_compile run_demo.py
python -m py_compile create_demo_video.py
python -m py_compile models/train.py

# 3. Verify imports work
python -c "from src.detector import ProductDetector; print('✓ Detector OK')"
python -c "from src.cart_manager import CartManager; print('✓ Cart OK')"
python -c "from src.visualizer import Visualizer; print('✓ Visualizer OK')"
python -c "from src.main import FastBillingXCheckout; print('✓ Main OK')"
```

---

## 📦 Installation Steps

### Windows
```batch
# 1. Open Command Prompt in project directory
cd C:\Users\hp5cd\Desktop\fastblling

# 2. Run setup script
setup.bat

# 3. Activate virtual environment
venv\Scripts\activate
```

### Linux/Mac
```bash
# 1. Navigate to project
cd ~/Desktop/fastblling

# 2. Run setup script
chmod +x setup.sh
./setup.sh

# 3. Activate virtual environment
source venv/bin/activate
```

---

## 🧪 Testing Procedures

### Test 1: Import All Modules
```bash
python -c "
from src.detector import ProductDetector
from src.cart_manager import CartManager
from src.visualizer import Visualizer
from src.main import FastBillingXCheckout
print('✓ All modules imported successfully')
"
```

### Test 2: Create Demo Video (2 minutes)
```bash
# This generates a synthetic demo showing detection workflow
python create_demo_video.py --duration 120 --output test_demo.mp4
# Check: test_demo.mp4 should be ~50-100 MB
```

### Test 3: Run with Webcam (Press 'q' to quit)
```bash
# Quick 10-second demo
timeout 10 python run_demo.py --source 0 --conf 0.5
# Or on Windows: 
# python run_demo.py --source 0 (then press 'q')
```

### Test 4: Process Video File
```bash
# If you have a video file (e.g., shopping.mp4)
python run_demo.py --source shopping.mp4 --output result.mp4 --conf 0.5
```

### Test 5: Backend API Test
```bash
# Terminal 1: Start API
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Test API
curl -X POST http://localhost:8000/api/cart/add \
  -H "Content-Type: application/json" \
  -d '{"session_id":"test_cart","item_name":"apple","price":0.50}'

# Check response
curl http://localhost:8000/api/cart/test_cart
```

### Test 6: Model Training (GPU recommended)
```bash
# This requires a dataset in YOLO format
python models/train.py --epochs 10 --batch 8 --device 0
# Or CPU: --device cpu
```

---

## 📊 Expected Output Examples

### Run Demo Output
```
Starting FastBillingX Checkout System...
Press 'q' to quit, 'c' to clear cart

✓ Added to cart: apple ($0.50) - Confidence: 0.95
✓ Added to cart: milk ($1.50) - Confidence: 0.97
✓ Added to cart: bread ($2.00) - Confidence: 0.93

...window shows real-time detection with cart overlay...

==================================================
FINAL CART SUMMARY
==================================================
apple: 1 x $0.50 = $0.50
milk: 1 x $1.50 = $1.50
bread: 1 x $2.00 = $2.00
--------------------------------------------------
TOTAL: $4.00
==================================================
```

### API Response Example
```json
{
  "session_id": "test_cart",
  "items": [
    {
      "item_id": "uuid-123",
      "name": "apple",
      "price": 0.50,
      "detected_at": "2024-12-23T10:30:00",
      "quantity": 1
    }
  ],
  "total_items": 1,
  "total_amount": 0.50
}
```

---

## 🔍 Troubleshooting

### Problem: "No module named 'ultralytics'"
```bash
pip install --upgrade ultralytics
```

### Problem: "Could not create video writer"
```bash
# Update OpenCV
pip install --upgrade opencv-python
```

### Problem: "Cannot open video source 0 (webcam)"
```bash
# Check if webcam is available
# Try different source: --source 1 or --source 2
# Or use video file instead: --source video.mp4
```

### Problem: "CUDA out of memory"
```bash
# Reduce confidence threshold
python run_demo.py --conf 0.5

# Or limit to CPU
python run_demo.py --device cpu
```

### Problem: "MongoDB connection failed"
```bash
# This is OK - system falls back to in-memory storage
# No MongoDB required for demo
# Set MONGODB_URI only if you have MongoDB running
```

---

## 📈 Performance Monitoring

### Check FPS
Watch the FPS counter in the top-left of the video window.
- Expected: 15-20 FPS on CPU, 30-60 on GPU

### Check Memory Usage
```bash
# Linux/Mac
python -c "import psutil; print(f'Memory: {psutil.virtual_memory().percent}%')"

# Windows PowerShell
Get-Process python | Select ProcessName, @{Name="Memory(MB)";Expression={[math]::Round($_.WS/1MB)}}
```

### Check Inference Time
Look at the detection logs - should be < 100ms per frame

---

## 🚀 Production Deployment

### Deploy to Jetson Nano
```bash
# 1. Install JetPack with PyTorch support
# 2. Clone repo on Jetson
# 3. Run setup script (modify for ARM architecture if needed)
# 4. Export model to TensorRT
python -c "
from ultralytics import YOLO
model = YOLO('models/best.pt')
model.export(format='engine')  # TensorRT
"
# 5. Use exported model
python run_demo.py --model models/best.engine
```

### Deploy Backend to Cloud
```bash
# Option 1: Docker
docker build -t fastbillingx-api backend/
docker run -p 8000:8000 fastbillingx-api

# Option 2: AWS Lambda
# Use serverless framework or AWS SAM

# Option 3: Google Cloud Run
gcloud run deploy fastbillingx --source .
```

---

## 📋 Code Quality Checks

```bash
# Check syntax
python -m py_compile src/*.py
python -m py_compile run_demo.py
python -m py_compile create_demo_video.py
python -m py_compile models/train.py

# Check imports
python -m pylint src/ --disable=all --enable=import-error

# Check style (PEP 8)
pip install flake8
flake8 src/ --max-line-length=100 --ignore=E203,W503
```

---

## 📝 File Size Reference

Expected file sizes after complete installation:

```
src/main.py              ~12 KB
src/detector.py          ~6 KB
src/cart_manager.py      ~8 KB
src/visualizer.py        ~12 KB
run_demo.py              ~8 KB
create_demo_video.py     ~12 KB
models/train.py          ~9 KB
models/best.pt           ~25 MB (auto-downloaded)
backend/app/main.py      ~8 KB
docs/                    ~20 KB

venv/                    ~500 MB (Python packages)

Total: ~600 MB (including all packages)
```

---

## 🔐 Security Testing

```bash
# Check for common vulnerabilities
pip install bandit
bandit -r src/

# Check for outdated packages
pip list --outdated

# Verify no secrets in code
grep -r "password\|api_key\|secret" src/ || echo "✓ No hardcoded secrets"
```

---

## ✅ Sign-Off Checklist

Before final submission, verify:

- ✓ All source files created (src/ directory)
- ✓ All entry points work (run_demo.py, create_demo_video.py)
- ✓ Backend API starts without errors
- ✓ Training script runs (or fails gracefully if no dataset)
- ✓ Documentation is complete (README, API_README, Security)
- ✓ No hardcoded secrets or credentials
- ✓ All imports resolve correctly
- ✓ Code follows PEP 8 style
- ✓ Error handling is comprehensive
- ✓ Performance meets requirements

---

## 📞 Support Commands

```bash
# Show help for main demo
python run_demo.py --help

# Show help for demo video generator
python create_demo_video.py --help

# Show help for training
python models/train.py --help

# Check backend API documentation
# Visit: http://localhost:8000/docs (after starting API)

# View all logs
cat *.log

# Clean up generated files
rm -rf cart_*.json test_demo.mp4 fastbillingx_models/
```

---

## 🎓 Learning Resources

- YOLOv8 Docs: https://docs.ultralytics.com/
- FastAPI: https://fastapi.tiangolo.com/
- OpenCV: https://docs.opencv.org/
- PyTorch: https://pytorch.org/docs/

---

**Last Updated**: December 23, 2025
**Status**: Ready for Testing & Evaluation
