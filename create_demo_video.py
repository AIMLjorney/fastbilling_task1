#!/usr/bin/env python3
"""
FastBillingX Demo Video Generation Script

Creates a synthetic 2:12 minute demo video showing the AI checkout system
detecting various products and updating the shopping cart in real-time.

This script demonstrates:
- Multi-product detection
- Cart state updates
- Price calculation
- Visual overlays with FPS counter
- Real-time cart summary

Usage:
    python create_demo_video.py                      # Create default 92s video
    python create_demo_video.py --duration 300       # Create 5 minute video
    python create_demo_video.py --output custom.mp4  # Custom output filename
"""

import cv2
import numpy as np
import sys
import os
import argparse
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from src.cart_manager import CartManager
from src.visualizer import Visualizer


def create_synthetic_frame(width, height, frame_num, detections):
    """
    Create a synthetic shopping scene frame
    
    Args:
        width: Frame width
        height: Frame height
        frame_num: Current frame number
        detections: List of product detections
        
    Returns:
        Frame as numpy array
    """
    # Create base frame with gradient background
    frame = np.ones((height, width, 3), dtype=np.uint8) * 200
    
    # Add subtle grid pattern
    for x in range(0, width, 50):
        cv2.line(frame, (x, 0), (x, height), (180, 180, 180), 1)
    for y in range(0, height, 50):
        cv2.line(frame, (0, y), (width, y), (180, 180, 180), 1)
    
    # Add title
    cv2.putText(frame, "FastBillingX Demo - AI Checkout System", 
               (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 200), 2)
    
    # Add timestamp and frame info
    timestamp = datetime.now().strftime("%H:%M:%S")
    cv2.putText(frame, f"Time: {timestamp} | Frame: {frame_num}", 
               (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 50, 50), 1)
    
    # Add detection annotations
    for det in detections:
        x1, y1, x2, y2 = det['bbox']
        name = det['name']
        conf = det['confidence']
        price = det['price']
        
        # Draw bounding box
        color = tuple(np.random.randint(50, 255, 3).tolist())
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        
        # Draw label
        label = f"{name}: ${price:.2f} ({conf:.0%})"
        cv2.putText(frame, label, (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    return frame


def create_demo_video(output_path="fastbillingx_demo.mp4", duration_seconds=132):
    """
    Create a complete demo video showing the checkout system
    
    Args:
        output_path: Output video filename
        duration_seconds: Video duration in seconds
    """
    print("="*70)
    print("FastBillingX Demo Video Generator")
    print("="*70)
    
    # Video parameters
    width, height = 1280, 720
    fps = 30
    total_frames = duration_seconds * fps
    
    print(f"\n[*] Video Configuration:")
    print(f"    Resolution: {width}x{height}")
    print(f"    Frame rate: {fps} FPS")
    print(f"    Duration: {duration_seconds} seconds ({total_frames} frames)")
    print(f"    Output file: {output_path}")
    
    # Initialize components
    print(f"\n[*] Initializing components...")
    cart_manager = CartManager()
    visualizer = Visualizer()
    
    # Video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    if not out.isOpened():
        print("[!] Error: Could not create video writer")
        print("    Try installing: pip install opencv-python")
        return False
    
    print("[✓] Components ready")
    
    # Define product scenarios for different time periods
    scenarios = {
        'intro': {
            'frame_range': (0, 135),
            'title': 'Welcome to FastBillingX',
            'products': []
        },
        'fruits': {
            'frame_range': (135, 900),
            'title': 'Detecting Fruits',
            'products': [
                {'name': 'apple', 'price': 0.50, 'bbox': [200, 200, 300, 300], 'confidence': 0.95},
                {'name': 'banana', 'price': 0.30, 'bbox': [400, 250, 500, 350], 'confidence': 0.92},
                {'name': 'orange', 'price': 0.40, 'bbox': [600, 200, 700, 300], 'confidence': 0.88},
                {'name': 'strawberry', 'price': 0.60, 'bbox': [800, 250, 900, 350], 'confidence': 0.90},
                {'name': 'pineapple', 'price': 1.20, 'bbox': [100, 300, 200, 400], 'confidence': 0.87},
                {'name': 'mango', 'price': 0.80, 'bbox': [300, 350, 400, 450], 'confidence': 0.93},
                {'name': 'tomato', 'price': 0.45, 'bbox': [500, 300, 600, 400], 'confidence': 0.91},
                {'name': 'potato', 'price': 0.35, 'bbox': [700, 350, 800, 450], 'confidence': 0.89},
                {'name': 'onion', 'price': 0.25, 'bbox': [900, 300, 1000, 400], 'confidence': 0.88},
                {'name': 'pepper', 'price': 0.55, 'bbox': [150, 400, 250, 500], 'confidence': 0.92},
                {'name': 'lettuce', 'price': 0.70, 'bbox': [350, 450, 450, 550], 'confidence': 0.94},
                {'name': 'cabbage', 'price': 0.65, 'bbox': [550, 400, 650, 500], 'confidence': 0.90},
                {'name': 'cucumber', 'price': 0.40, 'bbox': [750, 450, 850, 550], 'confidence': 0.91},
                {'name': 'blueberry', 'price': 1.00, 'bbox': [950, 400, 1050, 500], 'confidence': 0.87},
                {'name': 'grape', 'price': 0.75, 'bbox': [200, 500, 300, 600], 'confidence': 0.93},
                {'name': 'watermelon', 'price': 2.50, 'bbox': [400, 550, 500, 650], 'confidence': 0.89},
                {'name': 'lemon', 'price': 0.30, 'bbox': [600, 500, 700, 600], 'confidence': 0.92},
                {'name': 'lime', 'price': 0.35, 'bbox': [800, 550, 900, 650], 'confidence': 0.88},
                {'name': 'avocado', 'price': 0.85, 'bbox': [1000, 500, 1100, 600], 'confidence': 0.91},
                {'name': 'kiwi', 'price': 0.60, 'bbox': [250, 600, 350, 700], 'confidence': 0.90},
                {'name': 'papaya', 'price': 1.50, 'bbox': [450, 650, 550, 750], 'confidence': 0.87},
                {'name': 'peach', 'price': 0.70, 'bbox': [650, 600, 750, 700], 'confidence': 0.93},
                {'name': 'pear', 'price': 0.55, 'bbox': [850, 650, 950, 750], 'confidence': 0.89},
                {'name': 'plum', 'price': 0.45, 'bbox': [1050, 600, 1150, 700], 'confidence': 0.92},
            ]
        },
        'dairy': {
            'frame_range': (900, 1800),
            'title': 'Detecting Dairy Products',
            'products': [
                {'name': 'milk', 'price': 1.50, 'bbox': [300, 200, 400, 300], 'confidence': 0.97},
                {'name': 'yogurt', 'price': 1.80, 'bbox': [500, 220, 600, 320], 'confidence': 0.94},
                {'name': 'cheese', 'price': 2.50, 'bbox': [700, 200, 800, 300], 'confidence': 0.91},
                {'name': 'butter', 'price': 3.00, 'bbox': [900, 220, 1000, 320], 'confidence': 0.93},
                {'name': 'cream', 'price': 2.20, 'bbox': [150, 300, 250, 400], 'confidence': 0.90},
                {'name': 'ice_cream', 'price': 4.50, 'bbox': [350, 320, 450, 420], 'confidence': 0.88},
                {'name': 'sour_cream', 'price': 2.80, 'bbox': [550, 300, 650, 400], 'confidence': 0.92},
                {'name': 'cottage_cheese', 'price': 3.20, 'bbox': [750, 320, 850, 420], 'confidence': 0.89},
                {'name': 'milk_bottle', 'price': 1.60, 'bbox': [950, 300, 1050, 400], 'confidence': 0.91},
                {'name': 'whipped_cream', 'price': 2.50, 'bbox': [200, 400, 300, 500], 'confidence': 0.87},
            ]
        },
        'bakery': {
            'frame_range': (1800, 2700),
            'title': 'Detecting Bakery Items',
            'products': [
                {'name': 'bread', 'price': 2.00, 'bbox': [250, 200, 400, 350], 'confidence': 0.93},
                {'name': 'croissant', 'price': 1.50, 'bbox': [500, 180, 650, 330], 'confidence': 0.90},
                {'name': 'donut', 'price': 0.75, 'bbox': [750, 200, 850, 300], 'confidence': 0.88},
                {'name': 'bagel', 'price': 1.25, 'bbox': [950, 220, 1050, 320], 'confidence': 0.91},
                {'name': 'muffin', 'price': 1.80, 'bbox': [150, 300, 250, 400], 'confidence': 0.89},
                {'name': 'cake', 'price': 3.50, 'bbox': [350, 320, 450, 420], 'confidence': 0.87},
                {'name': 'pie', 'price': 4.00, 'bbox': [550, 300, 650, 400], 'confidence': 0.92},
                {'name': 'cookie', 'price': 0.60, 'bbox': [750, 320, 850, 420], 'confidence': 0.90},
                {'name': 'brownie', 'price': 1.00, 'bbox': [950, 300, 1050, 400], 'confidence': 0.88},
                {'name': 'pancake', 'price': 2.50, 'bbox': [200, 400, 300, 500], 'confidence': 0.93},
                {'name': 'waffle', 'price': 2.75, 'bbox': [400, 420, 500, 520], 'confidence': 0.91},
                {'name': 'tortilla', 'price': 1.20, 'bbox': [600, 400, 700, 500], 'confidence': 0.89},
                {'name': 'naan', 'price': 1.50, 'bbox': [800, 420, 900, 520], 'confidence': 0.87},
                {'name': 'pita', 'price': 1.00, 'bbox': [1000, 400, 1100, 500], 'confidence': 0.92},
            ]
        },
        'checkout': {
            'frame_range': (2700, 3960),
            'title': 'Complete Cart Summary',
            'products': [
                {'name': 'apple', 'price': 0.50, 'bbox': [200, 200, 300, 300], 'confidence': 0.95},
                {'name': 'milk', 'price': 1.50, 'bbox': [300, 200, 400, 300], 'confidence': 0.97},
                {'name': 'bread', 'price': 2.00, 'bbox': [250, 400, 400, 550], 'confidence': 0.93},
                {'name': 'chocolate', 'price': 1.20, 'bbox': [500, 250, 600, 350], 'confidence': 0.89},
                {'name': 'chips', 'price': 1.75, 'bbox': [700, 300, 800, 400], 'confidence': 0.91},
                {'name': 'soda', 'price': 1.25, 'bbox': [900, 250, 1000, 350], 'confidence': 0.92},
                {'name': 'cereal', 'price': 3.50, 'bbox': [150, 450, 250, 550], 'confidence': 0.88},
                {'name': 'juice', 'price': 2.00, 'bbox': [350, 500, 450, 600], 'confidence': 0.90},
            ]
        }
    }
    
    print(f"\n[*] Creating {duration_seconds}s demo video...")
    print("    This may take a minute...\n")
    
    last_add_time = {}  # Track last time each item was added
    
    for frame_idx in range(total_frames):
        # Determine current scenario
        current_scenario = None
        for scenario_name, scenario_data in scenarios.items():
            frame_range = scenario_data['frame_range']
            if frame_range[0] <= frame_idx < frame_range[1]:
                current_scenario = scenario_data
                break
        
        # Get products for current scenario
        products = current_scenario['products'] if current_scenario else []
        
        # Create frame
        frame = create_synthetic_frame(width, height, frame_idx, products)
        
        # Add cart items with deduplication
        current_time = frame_idx / fps
        for product in products:
            name = product['name']
            
            # Simple dedup: add at most once per 5 seconds
            last_time = last_add_time.get(name, -10)
            if current_time - last_time > 5:
                cart_manager.add_item(
                    name=name,
                    confidence=product['confidence'],
                    price=product['price'],
                    bbox=product['bbox']
                )
                last_add_time[name] = current_time
        
        # Get cart summary
        cart_items = cart_manager.get_cart_summary()
        
        # Draw detections
        frame = visualizer.draw_detections(frame, products)
        
        # Draw cart overlay
        fps_display = fps  # Display actual FPS
        frame = visualizer.draw_cart_overlay(frame, cart_items, fps_display)
        
        # Write frame
        out.write(frame)
        
        # Progress bar
        progress = (frame_idx + 1) / total_frames
        progress_str = "#" * int(progress * 40)
        empty_str = "-" * (40 - len(progress_str))
        percent = progress * 100
        
        # Print progress every 30 frames
        if frame_idx % 30 == 0:
            time_remaining = (total_frames - frame_idx) / (fps * 30)
            print(f"    [{progress_str}{empty_str}] {percent:.1f}% - "
                  f"Time: {frame_idx/fps:.1f}s / {duration_seconds}s")
    
    # Release video writer
    out.release()
    
    # Final summary
    print(f"\n[✓] Video creation completed!")
    print(f"\n[*] Final Cart Summary:")
    print(f"    Total items: {cart_manager.get_item_count()}")
    print(f"    Total value: ${cart_manager.get_total():.2f}")
    print(f"\n[✓] Demo video saved to: {output_path}")
    
    # Print receipt
    print(f"\n{cart_manager.generate_receipt()}")
    
    return True


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='FastBillingX Demo Video Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  # Create default 92 second demo video
  python create_demo_video.py
  
  # Create 5 minute demo video
  python create_demo_video.py --duration 300
  
  # Custom output filename
  python create_demo_video.py --output my_demo.mp4
  
  # Create longer demo with custom output
  python create_demo_video.py --duration 180 --output long_demo.mp4
        """
    )
    
    parser.add_argument('--duration', type=int, default=92,
                       help='Video duration in seconds (default: 92)')
    parser.add_argument('--output', type=str, default='fastbillingx_demo.mp4',
                       help='Output video filename (default: fastbillingx_demo.mp4)')
    
    args = parser.parse_args()
    
    # Create directory if needed
    output_dir = os.path.dirname(args.output) or '.'
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    try:
        success = create_demo_video(args.output, args.duration)
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n\n[!] Demo video creation interrupted")
        return 1
    except Exception as e:
        print(f"\n[!] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
