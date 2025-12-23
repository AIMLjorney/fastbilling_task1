#!/usr/bin/env python3
"""
FastBillingX Quick Start Demo Script

This is the main entry point for running the AI checkout system.
It provides an interactive interface for:
- Webcam real-time detection
- Video file processing
- Custom model loading
- Output video generation

Usage:
    python run_demo.py                          # Webcam demo with default model
    python run_demo.py --source video.mp4       # Process video file
    python run_demo.py --model custom.pt        # Use custom model
    python run_demo.py --output result.mp4      # Save output video
    python run_demo.py --source 0 --conf 0.45   # Adjust confidence threshold
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

import argparse
from pathlib import Path


def print_banner():
    """Print welcome banner"""
    banner = """
    
    print(banner)


def check_dependencies():
    """Check if required packages are installed"""
    print("\n[*] Checking dependencies...")
    
    required_packages = [
        ('cv2', 'opencv-python'),
        ('ultralytics', 'ultralytics'),
        ('numpy', 'numpy'),
        ('torch', 'torch')
    ]
    
    missing = []
    for module_name, package_name in required_packages:
        try:
            __import__(module_name)
            print(f"    ✓ {package_name}")
        except ImportError:
            print(f"    ✗ {package_name} (MISSING)")
            missing.append(package_name)
    
    if missing:
        print("\n[!] Missing packages. Install with:")
        print(f"    pip install {' '.join(missing)}")
        return False
    
    print("\n[✓] All dependencies satisfied!\n")
    return True


def check_model(model_path):
    """Check if model file exists"""
    if os.path.exists(model_path):
        size_mb = os.path.getsize(model_path) / (1024 * 1024)
        print(f"[✓] Model found: {model_path} ({size_mb:.1f} MB)")
        return True
    else:
        print(f"[!] Model not found: {model_path}")
        print("\n    Downloading pretrained YOLOv8 Nano model...")
        print("    This will download ~25MB on first run")
        print("    (ultralytics will auto-download if internet available)\n")
        return False  # Will auto-download on first use


def main():
    """Main entry point"""
    print_banner()
    
    # Parse arguments
    parser = argparse.ArgumentParser(
        description='FastBillingX Computer Vision Checkout Demo',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  # Run with webcam
  python run_demo.py
  
  # Process video file
  python run_demo.py --source shopping_video.mp4
  
  # Use custom trained model
  python run_demo.py --model models/custom.pt
  
  # Save output video
  python run_demo.py --output result.mp4
  
  # Lower confidence threshold for more detections
  python run_demo.py --conf 0.35
  
  # All options combined
  python run_demo.py --source video.mp4 --model models/best.pt --output result.mp4 --conf 0.45

CONTROLS (during demo):
  q - Quit the application
  c - Clear shopping cart
  s - Save cart to JSON file
        """
    )
    
    parser.add_argument('--source', type=str, default='0',
                       help='Video source: 0 for webcam, or path to video file (default: 0)')
    parser.add_argument('--model', type=str, default='models/best.pt',
                       help='Path to YOLOv8 model weights (default: models/best.pt)')
    parser.add_argument('--conf', type=float, default=0.5,
                       help='Confidence threshold for detections (default: 0.5)')
    parser.add_argument('--output', type=str, default=None,
                       help='Output video file path (optional)')
    parser.add_argument('--skip-check', action='store_true',
                       help='Skip dependency check')
    
    args = parser.parse_args()
    
    # Check dependencies
    if not args.skip_check and not check_dependencies():
        print("\n[!] Please install missing dependencies first")
        return 1
    
    # Check model
    print("[*] Checking model...")
    check_model(args.model)
    
    # Display configuration
    print("[*] Configuration:")
    print(f"    Source: {args.source if args.source != '0' else 'Webcam (0)'}")
    print(f"    Model: {args.model}")
    print(f"    Confidence threshold: {args.conf}")
    print(f"    Output video: {args.output if args.output else 'No (display only)'}")
    
    # Import and run
    print("\n[*] Initializing FastBillingX Checkout System...")
    try:
        from src.main import FastBillingXCheckout
        
        # Create checkout instance
        checkout = FastBillingXCheckout(
            model_path=args.model,
            conf_threshold=args.conf
        )
        
        print("[✓] System initialized!\n")
        print("[*] Starting video processing...")
        print("    Press any key in the window to see controls\n")
        
        # Run the demo
        checkout.run(
            source=args.source if args.source != '0' else 0,
            output_file=args.output
        )
        
        print("\n[✓] Demo completed successfully!")
        return 0
        
    except Exception as e:
        print(f"\n[!] Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check if model file exists")
        print("2. Ensure video source is available")
        print("3. Check for sufficient disk space (if saving output)")
        print("4. Try: pip install --upgrade ultralytics")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n[!] Demo interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Unexpected error: {str(e)}")
        sys.exit(1)
