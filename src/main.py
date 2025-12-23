import cv2
import argparse
from src.detector import ProductDetector
from src.cart_manager import CartManager
from src.visualizer import Visualizer
import time


class FastBillingXCheckout:
    def __init__(self, model_path='models/best.pt', conf_threshold=0.5):
        """
        Initialize the computer vision checkout system
        """
        self.detector = ProductDetector(model_path, conf_threshold)
        self.cart_manager = CartManager()
        self.visualizer = Visualizer()
        self.frame_count = 0
        self.fps = 0
        self.start_time = time.time()
        
    def process_frame(self, frame):
        """
        Process a single frame for product detection
        """
        # Detect products in frame
        detections = self.detector.detect(frame)
        
        # Update cart with detected items
        for detection in detections:
            self.cart_manager.add_item(
                name=detection['name'],
                confidence=detection['confidence'],
                bbox=detection['bbox'],
                price=detection.get('price', 1.00)
            )
        
        # Get current cart state
        cart_items = self.cart_manager.get_cart_summary()
        
        # Calculate FPS
        self.frame_count += 1
        if self.frame_count % 30 == 0:
            elapsed = time.time() - self.start_time
            self.fps = self.frame_count / elapsed
        
        # Draw visualizations
        frame = self.visualizer.draw_detections(frame, detections)
        frame = self.visualizer.draw_cart_overlay(frame, cart_items, self.fps)
        
        return frame, cart_items
    
    def run(self, source=0, output_file=None):
        """
        Main loop for video processing
        """
        # Initialize video capture
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            print(f"Error: Cannot open video source {source}")
            return
        
        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Initialize video writer if output file specified
        if output_file:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_file, fourcc, 30.0, (width, height))
        
        print("Starting FastBillingX Checkout System...")
        print("Press 'q' to quit, 'c' to clear cart, 's' to save cart")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process frame
            processed_frame, cart_items = self.process_frame(frame)
            
            # Display frame
            cv2.imshow('FastBillingX - AI Checkout', processed_frame)
            
            # Write to output file if specified
            if output_file:
                out.write(processed_frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('c'):
                self.cart_manager.clear_cart()
                print("Cart cleared!")
            elif key == ord('s'):
                self.cart_manager.save_cart_to_file()
                print("Cart saved to file!")
        
        # Cleanup
        cap.release()
        if output_file:
            out.release()
        cv2.destroyAllWindows()
        
        # Print final cart summary
        print("\n" + "="*50)
        print("FINAL CART SUMMARY")
        print("="*50)
        final_cart = self.cart_manager.get_cart_summary()
        total = 0
        for item, details in final_cart.items():
            price = details.get('price', 0) * details['quantity']
            total += price
            print(f"{item}: {details['quantity']} x ${details.get('price', 0):.2f} = ${price:.2f}")
        print("-"*50)
        print(f"TOTAL: ${total:.2f}")
        print("="*50)


def main():
    parser = argparse.ArgumentParser(description='FastBillingX Computer Vision Checkout System')
    parser.add_argument('--source', type=str, default='0', 
                       help='Video source (0 for webcam, or path to video file)')
    parser.add_argument('--model', type=str, default='models/best.pt',
                       help='Path to YOLOv8 model weights')
    parser.add_argument('--conf', type=float, default=0.5,
                       help='Confidence threshold for detection')
    parser.add_argument('--output', type=str, default=None,
                       help='Output video file path (optional)')
    
    args = parser.parse_args()
    
    # Initialize checkout system
    checkout = FastBillingXCheckout(
        model_path=args.model,
        conf_threshold=args.conf
    )
    
    # Run the system
    checkout.run(
        source=args.source if args.source != '0' else 0,
        output_file=args.output
    )


if __name__ == "__main__":
    main()
