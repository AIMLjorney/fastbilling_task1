"""
FastBillingX YOLOv8 Model Training Script

This script trains a YOLOv8 model for product detection with 5310+ items.
Requires: ultralytics, torch, torchvision

Usage:
    python models/train.py
    python models/train.py --epochs 100 --batch 32
    python models/train.py --model yolov8l.pt  # Use larger model
"""

import os
import argparse
from pathlib import Path
from ultralytics import YOLO


def train_model(args):
    """
    Train YOLOv8 model on FastBillingX product dataset
    
    Args:
        args: Command line arguments
    """
    print("="*60)
    print("FastBillingX YOLOv8 Product Detection Training")
    print("="*60)
    
    # Initialize model
    print(f"\n1. Loading base model: {args.model}")
    model = YOLO(args.model)  # load a pretrained model
    
    # Check if dataset exists
    dataset_path = Path(args.dataset)
    if not dataset_path.exists():
        print(f"\nWarning: Dataset path {dataset_path} not found!")
        print("To use this script, prepare your dataset in YOLO format:")
        print("  data/")
        print("    ├── images/")
        print("    │   ├── train/")
        print("    │   ├── val/")
        print("    │   └── test/")
        print("    └── labels/")
        print("        ├── train/")
        print("        ├── val/")
        print("        └── test/")
        print("\nYAML annotation format example:")
        print("  0 0.5 0.5 0.3 0.4  # class_id center_x center_y width height")
    
    print(f"\n2. Training parameters:")
    print(f"   - Model: {args.model}")
    print(f"   - Epochs: {args.epochs}")
    print(f"   - Batch size: {args.batch}")
    print(f"   - Image size: {args.imgsz}")
    print(f"   - Device: {args.device}")
    print(f"   - Dataset: {args.dataset}")
    print(f"   - Project: {args.project}")
    
    # Training configuration
    training_params = {
        'data': args.dataset,
        'epochs': args.epochs,
        'imgsz': args.imgsz,
        'batch': args.batch,
        'workers': args.workers,
        'device': args.device,
        'project': args.project,
        'name': args.name,
        'save': True,
        'save_period': 10,
        'cache': 'disk',  # Cache images to disk
        'pretrained': True,
        'optimizer': 'AdamW',
        'lr0': 0.001,
        'lrf': 0.01,
        'momentum': 0.937,
        'weight_decay': 0.0005,
        'warmup_epochs': 3,
        'warmup_momentum': 0.8,
        'box': 7.5,
        'cls': 0.5,
        'dfl': 1.5,
        'fl_gamma': 0.0,
        'label_smoothing': 0.0,
        'nbs': 64,
        'hsv_h': 0.015,
        'hsv_s': 0.7,
        'hsv_v': 0.4,
        'degrees': 0.0,
        'translate': 0.1,
        'scale': 0.5,
        'shear': 0.0,
        'perspective': 0.0,
        'flipud': 0.0,
        'fliplr': 0.5,
        'mosaic': 1.0,
        'mixup': 0.0,
        'copy_paste': 0.0,
        'patience': 20,  # Early stopping patience
        'verbose': True
    }
    
    print(f"\n3. Starting training...")
    print("   This may take several hours depending on dataset size and hardware")
    print("-"*60)
    
    try:
        # Train the model
        results = model.train(**training_params)
        
        print("-"*60)
        print("\n4. Training completed!")
        print(f"   Results saved to: {results.save_dir}")
        
        # Validate the model
        print(f"\n5. Running validation...")
        metrics = model.val()
        
        print(f"   Validation Results:")
        print(f"   - mAP50: {metrics.box.map50:.4f}")
        print(f"   - mAP50-95: {metrics.box.map:.4f}")
        print(f"   - Precision: {metrics.box.mp:.4f}")
        print(f"   - Recall: {metrics.box.mr:.4f}")
        
        # Test on test set if available
        print(f"\n6. Testing model on test set...")
        test_results = model.val(data=args.dataset, split='test')
        print("   Test completed")
        
        # Export to different formats
        print(f"\n7. Exporting model to different formats...")
        
        export_formats = {
            'onnx': 'ONNX (PyTorch)',
            'torchscript': 'TorchScript',
            'engine': 'TensorRT (requires CUDA)',
            'coreml': 'CoreML (macOS/iOS)',
            'pb': 'TensorFlow SavedModel',
            'tflite': 'TensorFlow Lite'
        }
        
        for fmt, description in export_formats.items():
            try:
                print(f"   - Exporting to {description}...", end=" ")
                model.export(format=fmt, imgsz=args.imgsz)
                print("✓")
            except Exception as e:
                print(f"✗ ({str(e)[:30]})")
        
        print("\n" + "="*60)
        print("Training and export completed successfully!")
        print("="*60)
        print("\nNext steps:")
        print("1. Review training results in:")
        print(f"   {results.save_dir}")
        print("\n2. Use the trained model with:")
        print("   python edge_app/main.py --model <path_to_best.pt>")
        print("\n3. For production deployment:")
        print("   - Use the TensorRT engine for Jetson Nano")
        print("   - Use the ONNX format for cross-platform deployment")
        
        return model
        
    except Exception as e:
        print(f"\nError during training: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Ensure dataset exists at:", args.dataset)
        print("2. Check YAML format is correct")
        print("3. Verify sufficient GPU memory (recommended: 6GB+)")
        print("4. Try reducing batch size if out of memory")
        raise


def main():
    parser = argparse.ArgumentParser(
        description='FastBillingX YOLOv8 Model Training Script',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Train with default settings (nano model, 80 epochs)
  python models/train.py
  
  # Train with custom batch size and epochs
  python models/train.py --epochs 200 --batch 32
  
  # Train with larger model for better accuracy
  python models/train.py --model yolov8l.pt --epochs 150
  
  # Multi-GPU training
  python models/train.py --device 0,1 --batch 64
        """
    )
    
    parser.add_argument('--model', type=str, default='yolov8n.pt',
                       help='Model to use (yolov8n/s/m/l/x) [default: yolov8n.pt]')
    parser.add_argument('--epochs', type=int, default=100,
                       help='Number of training epochs [default: 100]')
    parser.add_argument('--batch', type=int, default=16,
                       help='Batch size [default: 16]')
    parser.add_argument('--imgsz', type=int, default=640,
                       help='Image size [default: 640]')
    parser.add_argument('--device', type=str, default='0',
                       help='Device to use (0 for GPU, cpu for CPU) [default: 0]')
    parser.add_argument('--workers', type=int, default=8,
                       help='Number of workers [default: 8]')
    parser.add_argument('--dataset', type=str, default='models/dataset.yaml',
                       help='Dataset YAML path [default: models/dataset.yaml]')
    parser.add_argument('--project', type=str, default='fastbillingx_models',
                       help='Project name [default: fastbillingx_models]')
    parser.add_argument('--name', type=str, default='product_detector_v1',
                       help='Experiment name [default: product_detector_v1]')
    
    args = parser.parse_args()
    
    train_model(args)


if __name__ == "__main__":
    main()
