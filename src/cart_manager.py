import json
import time
from collections import defaultdict
from datetime import datetime


class CartManager:
    def __init__(self, dedup_cooldown=2.0):
        """
        Initialize shopping cart manager with deduplication logic
        
        Args:
            dedup_cooldown: Seconds to wait before adding same item again (default: 2.0)
        """
        self.cart = defaultdict(lambda: {
            'quantity': 0, 
            'total_price': 0, 
            'last_detected': None,
            'price': 0,
            'confidence': 0
        })
        self.cart_history = []
        self.session_id = f"cart_{int(time.time())}"
        self.dedup_cooldown = dedup_cooldown
        self.start_time = datetime.now()
        
    def add_item(self, name, confidence, bbox=None, price=1.00):
        """
        Add detected item to cart with deduplication logic
        
        Args:
            name: Product name
            confidence: Detection confidence score
            bbox: Bounding box coordinates [x1, y1, x2, y2]
            price: Product price
            
        Returns:
            True if item was added, False if skipped due to dedup cooldown
        """
        current_time = time.time()
        
        # Deduplication check - prevent duplicate additions within cooldown period
        if name in self.cart:
            last_time = self.cart[name].get('last_detected', 0)
            if current_time - last_time < self.dedup_cooldown:
                return False
        
        # Update cart
        self.cart[name]['quantity'] += 1
        self.cart[name]['total_price'] += price
        self.cart[name]['last_detected'] = current_time
        self.cart[name]['price'] = price
        self.cart[name]['confidence'] = confidence
        
        # Log to history
        cart_entry = {
            'timestamp': datetime.now().isoformat(),
            'item': name,
            'price': price,
            'confidence': confidence,
            'session_id': self.session_id,
            'bbox': bbox
        }
        self.cart_history.append(cart_entry)
        
        print(f"✓ Added to cart: {name} (${price:.2f}) - Confidence: {confidence:.2f}")
        return True
    
    def remove_item(self, name, quantity=1):
        """
        Remove item from cart
        
        Args:
            name: Product name
            quantity: Number of items to remove
            
        Returns:
            Amount removed (total price)
        """
        if name in self.cart:
            current_qty = self.cart[name]['quantity']
            price = self.cart[name].get('price', 0)
            
            if quantity >= current_qty:
                removed_price = self.cart[name]['total_price']
                del self.cart[name]
                print(f"Removed all {name} from cart (${removed_price:.2f})")
                return removed_price
            else:
                self.cart[name]['quantity'] -= quantity
                self.cart[name]['total_price'] -= price * quantity
                removed_price = price * quantity
                print(f"Removed {quantity} {name}(s) from cart (${removed_price:.2f})")
                return removed_price
        return 0
    
    def get_cart_summary(self):
        """
        Get current cart state
        
        Returns:
            Dictionary of cart items with details
        """
        return dict(self.cart)
    
    def get_total(self):
        """
        Calculate total cart value
        
        Returns:
            Total price (float)
        """
        total = sum(item['total_price'] for item in self.cart.values())
        return total
    
    def get_item_count(self):
        """
        Get total number of items in cart
        
        Returns:
            Total item count (int)
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    def clear_cart(self):
        """
        Clear all items from cart
        """
        self.cart.clear()
        print("Cart cleared!")
    
    def save_cart_to_file(self, filename=None):
        """
        Save cart to JSON file
        
        Args:
            filename: Output filename (optional)
            
        Returns:
            Filename where cart was saved
        """
        if filename is None:
            filename = f"cart_{self.session_id}.json"
        
        # Prepare cart data for JSON serialization
        cart_dict = {}
        for item_name, details in self.cart.items():
            cart_dict[item_name] = {
                'quantity': details['quantity'],
                'price': details['price'],
                'total_price': details['total_price'],
                'confidence': details['confidence']
            }
        
        cart_data = {
            'session_id': self.session_id,
            'timestamp': datetime.now().isoformat(),
            'start_time': self.start_time.isoformat(),
            'items': cart_dict,
            'total_items': self.get_item_count(),
            'total_amount': self.get_total(),
            'history': self.cart_history
        }
        
        with open(filename, 'w') as f:
            json.dump(cart_data, f, indent=2)
        
        print(f"Cart saved to {filename}")
        return filename
    
    def generate_receipt(self):
        """
        Generate printable receipt
        
        Returns:
            Receipt string
        """
        receipt_lines = []
        receipt_lines.append("="*50)
        receipt_lines.append("FASTBILLINGX - SMART CHECKOUT RECEIPT")
        receipt_lines.append("="*50)
        receipt_lines.append(f"Session ID: {self.session_id}")
        receipt_lines.append(f"Date & Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        receipt_lines.append(f"Duration: {(datetime.now() - self.start_time).total_seconds():.1f}s")
        receipt_lines.append("-"*50)
        receipt_lines.append(f"{'Item':<25} {'Qty':>5} {'Price':>8} {'Total':>8}")
        receipt_lines.append("-"*50)
        
        for item_name, details in self.cart.items():
            line = f"{item_name[:25]:<25} {details['quantity']:>5} ${details.get('price', 0):>7.2f} ${details['total_price']:>7.2f}"
            receipt_lines.append(line)
        
        receipt_lines.append("-"*50)
        receipt_lines.append(f"Total Items: {self.get_item_count():<35} ${self.get_total():>7.2f}")
        receipt_lines.append("="*50)
        receipt_lines.append("Thank you for shopping with FastBillingX!")
        receipt_lines.append("All items detected via AI Computer Vision")
        receipt_lines.append("="*50)
        
        return "\n".join(receipt_lines)
    
    def export_to_api_format(self):
        """
        Export cart in format suitable for backend API integration
        
        Returns:
            List of items in API format
        """
        items = []
        for item_name, details in self.cart.items():
            for _ in range(details['quantity']):
                items.append({
                    'session_id': self.session_id,
                    'item_name': item_name,
                    'price': details['price'],
                    'confidence': details['confidence'],
                    'timestamp': datetime.now().isoformat()
                })
        return items
