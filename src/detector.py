from ultralytics import YOLO
import cv2
import numpy as np


class ProductDetector:
    def __init__(self, model_path, conf_threshold=0.5):
        """
        Initialize YOLOv8 model for product detection
        """
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.class_names = self.model.names
        
        # Product price mapping (comprehensive list for demo)
        self.price_map = {
            # Fruits
            'apple': 0.50,
            'banana': 0.30,
            'orange': 0.40,
            'grape': 0.35,
            'mango': 0.75,
            'strawberry': 0.60,
            'blueberry': 0.80,
            'watermelon': 3.50,
            'pineapple': 1.50,
            'lemon': 0.25,
            
            # Vegetables
            'tomato': 0.60,
            'potato': 0.40,
            'onion': 0.35,
            'carrot': 0.45,
            'cucumber': 0.70,
            'pepper': 0.90,
            'lettuce': 1.00,
            'broccoli': 1.20,
            'spinach': 0.80,
            'cabbage': 0.55,
            
            # Dairy
            'milk': 1.50,
            'yogurt': 1.80,
            'cheese': 2.50,
            'butter': 3.00,
            'cream': 2.00,
            'egg': 0.25,
            'eggs': 2.50,
            
            # Bread & Bakery
            'bread': 2.00,
            'croissant': 1.50,
            'donut': 0.75,
            'cake': 3.00,
            'muffin': 1.00,
            
            # Beverages
            'water': 0.80,
            'coffee': 5.00,
            'tea': 3.50,
            'juice': 2.00,
            'cola': 1.50,
            'soda': 1.50,
            'milk_bottle': 1.50,
            
            # Snacks & Sweets
            'chocolate': 1.20,
            'candy': 0.50,
            'chips': 1.00,
            'cookie': 0.75,
            'cereal': 4.00,
            'granola': 3.50,
            'popcorn': 2.50,
            
            # Pantry Items
            'pasta': 1.80,
            'rice': 3.00,
            'flour': 2.50,
            'sugar': 2.00,
            'salt': 1.00,
            'oil': 4.50,
            'canned_beans': 1.20,
            'canned_tuna': 1.80,
            'peanut_butter': 3.00,
            'jam': 2.50,
            
            # Condiments
            'ketchup': 2.00,
            'mustard': 1.50,
            'mayo': 2.50,
            'vinegar': 1.80,
            'soy_sauce': 2.00,
            
            # Frozen Foods
            'frozen_pizza': 5.00,
            'frozen_vegetables': 3.50,
            'ice_cream': 4.00,
            'frozen_fish': 6.00,
            'frozen_chicken': 5.50,
            
            # Household Items
            'soap': 1.50,
            'shampoo': 3.00,
            'toothpaste': 2.00,
            'detergent': 2.50,
            'toilet_paper': 3.00,
            'tissues': 1.00,
            'paper_towels': 1.50,
            
            # Personal Care
            'deodorant': 2.50,
            'lotion': 3.00,
            'sunscreen': 4.00,
            
            # More generic items (for generalization)
            'item': 1.00,
            'product': 1.00,
            'object': 1.00,
        }
    
    def detect(self, image):
        """
        Detect products in the image
        """
        # Run YOLOv8 inference
        results = self.model(image, conf=self.conf_threshold, verbose=False)
        
        detections = []
        
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    try:
                        # Extract detection information
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        confidence = float(box.conf[0])
                        class_id = int(box.cls[0])
                        
                        # Get class name
                        class_name = self.class_names.get(class_id, f"class_{class_id}")
                        
                        # Get price
                        price = self.price_map.get(class_name.lower(), 1.00)
                        
                        # Create detection dictionary
                        detection = {
                            'name': class_name,
                            'confidence': confidence,
                            'bbox': [int(x1), int(y1), int(x2), int(y2)],
                            'price': price
                        }
                        
                        detections.append(detection)
                    except Exception as e:
                        print(f"Error processing detection: {e}")
                        continue
        
        return detections
    
    def get_price(self, product_name):
        """
        Get price for a product
        """
        return self.price_map.get(product_name.lower(), 1.00)
    
    def update_price(self, product_name, price):
        """
        Update price for a product
        """
        self.price_map[product_name.lower()] = price
