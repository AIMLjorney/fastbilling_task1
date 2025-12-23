import cv2
import numpy as np


class Visualizer:
    def __init__(self):
        """
        Initialize visualization utilities
        """
        self.colors = [
            (255, 0, 0),       # Blue
            (0, 255, 0),       # Green
            (0, 0, 255),       # Red
            (255, 255, 0),     # Cyan
            (255, 0, 255),     # Magenta
            (0, 255, 255),     # Yellow
            (128, 0, 0),       # Navy
            (0, 128, 0),       # Dark Green
            (0, 0, 128),       # Dark Red
            (128, 128, 0),     # Olive
            (128, 0, 128),     # Purple
            (0, 128, 128),     # Teal
        ]
        
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.6
        self.font_thickness = 2
    
    def draw_detections(self, image, detections):
        """
        Draw bounding boxes and labels on image
        
        Args:
            image: Input image
            detections: List of detection dictionaries
            
        Returns:
            Image with annotations
        """
        for idx, det in enumerate(detections):
            x1, y1, x2, y2 = det['bbox']
            name = det['name']
            confidence = det['confidence']
            price = det.get('price', 0)
            
            # Generate color based on product name hash
            color_idx = hash(name) % len(self.colors)
            color = self.colors[color_idx]
            
            # Draw bounding box
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
            
            # Create label with price and confidence
            label = f"{name}: ${price:.2f} ({confidence:.0%})"
            
            # Calculate text size for background
            (text_width, text_height), baseline = cv2.getTextSize(
                label, self.font, self.font_scale, self.font_thickness
            )
            
            # Draw label background (filled rectangle)
            cv2.rectangle(
                image, 
                (x1, y1 - text_height - 10),
                (x1 + text_width + 5, y1),
                color,
                -1
            )
            
            # Draw label text
            cv2.putText(
                image,
                label,
                (x1 + 3, y1 - 5),
                self.font,
                self.font_scale,
                (255, 255, 255),  # White text
                self.font_thickness,
                cv2.LINE_AA
            )
        
        return image
    
    def draw_cart_overlay(self, image, cart_items, fps=0):
        """
        Draw cart overlay on the right side of the image
        
        Args:
            image: Input image
            cart_items: Dictionary of cart items
            fps: Current FPS counter
            
        Returns:
            Image with cart overlay
        """
        h, w = image.shape[:2]
        overlay_width = 380
        
        # Create semi-transparent overlay
        overlay = image.copy()
        cv2.rectangle(overlay, (w - overlay_width, 0), (w, h), (0, 0, 0), -1)
        image = cv2.addWeighted(overlay, 0.7, image, 0.3, 0)
        
        # Cart header with shopping bag emoji
        y_offset = 40
        header_text = "SHOPPING CART"
        cv2.putText(
            image,
            header_text,
            (w - overlay_width + 20, y_offset),
            self.font,
            0.9,
            (0, 255, 0),
            2,
            cv2.LINE_AA
        )
        
        # FPS counter (top left)
        cv2.putText(
            image,
            f"FPS: {fps:.1f}",
            (20, 30),
            self.font,
            0.7,
            (0, 255, 255),
            2,
            cv2.LINE_AA
        )
        
        # Divider line
        y_offset += 15
        cv2.line(image, (w - overlay_width + 10, y_offset + 10), 
                (w - 10, y_offset + 10), (100, 100, 100), 1)
        
        # Cart items
        y_offset += 40
        total = 0
        
        if not cart_items:
            cv2.putText(
                image,
                "No items detected yet...",
                (w - overlay_width + 15, y_offset),
                self.font,
                0.6,
                (200, 200, 200),
                1,
                cv2.LINE_AA
            )
        else:
            # Show up to 8 items
            items_to_show = list(cart_items.items())[:8]
            
            for item_name, details in items_to_show:
                quantity = details['quantity']
                price = details.get('price', 0)
                item_total = details['total_price']
                confidence = details.get('confidence', 0)
                total += item_total
                
                # Item name (truncated)
                item_display = item_name[:14]
                item_text = f"• {item_display}"
                
                cv2.putText(
                    image,
                    item_text,
                    (w - overlay_width + 15, y_offset),
                    self.font,
                    0.55,
                    (255, 255, 255),
                    1,
                    cv2.LINE_AA
                )
                
                # Quantity
                qty_text = f"x{quantity}"
                cv2.putText(
                    image,
                    qty_text,
                    (w - overlay_width + 200, y_offset),
                    self.font,
                    0.55,
                    (200, 200, 200),
                    1,
                    cv2.LINE_AA
                )
                
                # Item total price
                price_text = f"${item_total:.2f}"
                cv2.putText(
                    image,
                    price_text,
                    (w - 100, y_offset),
                    self.font,
                    0.55,
                    (0, 255, 255),
                    1,
                    cv2.LINE_AA
                )
                
                y_offset += 28
            
            # Show if more items exist
            if len(cart_items) > 8:
                more_text = f"+{len(cart_items) - 8} more items"
                cv2.putText(
                    image,
                    more_text,
                    (w - overlay_width + 15, y_offset),
                    self.font,
                    0.5,
                    (100, 200, 100),
                    1,
                    cv2.LINE_AA
                )
                y_offset += 20
        
        # Separator line
        y_offset += 5
        cv2.line(image, (w - overlay_width + 10, y_offset), 
                (w - 10, y_offset), (100, 100, 100), 2)
        y_offset += 15
        
        # Total price display
        total_text = "TOTAL:"
        cv2.putText(
            image,
            total_text,
            (w - overlay_width + 20, y_offset),
            self.font,
            0.8,
            (255, 255, 0),
            2,
            cv2.LINE_AA
        )
        
        price_display = f"${total:.2f}"
        cv2.putText(
            image,
            price_display,
            (w - 120, y_offset),
            self.font,
            0.9,
            (0, 255, 0),
            3,
            cv2.LINE_AA
        )
        
        # Item count
        y_offset += 30
        item_count = sum(item['quantity'] for item in cart_items.values()) if cart_items else 0
        count_text = f"Items: {item_count}"
        cv2.putText(
            image,
            count_text,
            (w - overlay_width + 20, y_offset),
            self.font,
            0.6,
            (200, 255, 200),
            1,
            cv2.LINE_AA
        )
        
        # Instructions at bottom
        y_offset = h - 100
        instructions = [
            "CONTROLS:",
            "'q' - Quit",
            "'c' - Clear cart",
            "'s' - Save cart"
        ]
        
        for instruction in instructions:
            cv2.putText(
                image,
                instruction,
                (w - overlay_width + 15, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (200, 200, 255),
                1,
                cv2.LINE_AA
            )
            y_offset += 18
        
        return image
    
    def draw_status_bar(self, image, text, color=(0, 255, 0)):
        """
        Draw status bar at bottom of image
        
        Args:
            image: Input image
            text: Status text
            color: Text color (BGR)
            
        Returns:
            Image with status bar
        """
        h, w = image.shape[:2]
        cv2.rectangle(image, (0, h - 40), (w, h), (0, 0, 0), -1)
        cv2.putText(
            image,
            text,
            (20, h - 10),
            self.font,
            0.7,
            color,
            2,
            cv2.LINE_AA
        )
        return image
    
    def draw_info_panel(self, image, title, info_dict, position=(10, 10)):
        """
        Draw an info panel with multiple lines
        
        Args:
            image: Input image
            title: Panel title
            info_dict: Dictionary of key-value pairs to display
            position: (x, y) tuple for top-left corner
            
        Returns:
            Image with info panel
        """
        x, y = position
        line_height = 25
        
        # Draw panel background
        num_lines = len(info_dict) + 1
        panel_height = num_lines * line_height + 10
        cv2.rectangle(image, (x, y), (x + 300, y + panel_height), (0, 0, 0), -1)
        cv2.rectangle(image, (x, y), (x + 300, y + panel_height), (100, 100, 100), 1)
        
        # Draw title
        cv2.putText(image, title, (x + 10, y + 20), self.font, 0.7, (0, 255, 0), 2)
        
        # Draw info lines
        y_offset = y + 45
        for key, value in info_dict.items():
            text = f"{key}: {value}"
            cv2.putText(image, text, (x + 10, y_offset), self.font, 0.6, (255, 255, 255), 1)
            y_offset += line_height
        
        return image
