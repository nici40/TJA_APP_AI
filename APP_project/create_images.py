from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os
import math
import random

def create_background():
    """Create a beautiful gradient background with a modern look"""
    # Create a 1000x1600 image (portrait orientation good for mobile apps)
    width, height = 1000, 1600
    background = Image.new('RGB', (width, height), (30, 30, 40))
    
    # Create a gradient from dark blue to purple
    draw = ImageDraw.Draw(background)
    
    # Top color (dark blue) to bottom color (purple)
    top_color = (25, 35, 60)
    bottom_color = (60, 30, 80)
    
    # Draw gradient
    for y in range(height):
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * y / height)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * y / height)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Add some circles for modern look
    for i in range(5):
        # Create circle with gradient
        size = random.randint(200, 500)
        circle = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        circle_draw = ImageDraw.Draw(circle)
        
        # Draw a radial gradient circle
        for r in range(size//2, 0, -1):
            # Decrease opacity as radius increases
            alpha = int(120 * (r / (size/2))) 
            color = (random.randint(100, 200), random.randint(50, 150), random.randint(150, 255), alpha)
            circle_draw.ellipse((size//2-r, size//2-r, size//2+r, size//2+r), fill=color)
        
        # Apply blur
        circle = circle.filter(ImageFilter.GaussianBlur(15))
        
        # Random position
        x = random.randint(-size//2, width-size//2)
        y = random.randint(-size//2, height-size//2)
        
        # Paste the circle on the background
        background.paste(circle, (x, y), circle)
    
    # Apply slight blur for smoothness
    background = background.filter(ImageFilter.GaussianBlur(2))
    
    # Save the result
    background.save('background.jpg', quality=95)
    print("Background created successfully!")

def create_simple_logo():
    """Create a simple logo without using advanced features"""
    # Create a 300x300 image with blue background
    size = 300
    logo = Image.new('RGB', (size, size), (40, 120, 200))
    draw = ImageDraw.Draw(logo)
    
    # Draw a white circle in the middle
    center = size // 2
    circle_radius = 80
    draw.ellipse((center-circle_radius, center-circle_radius, 
                 center+circle_radius, center+circle_radius), 
                 fill=(255, 255, 255))
    
    # Add a smaller red circle
    small_radius = 40
    draw.ellipse((center-small_radius, center-small_radius, 
                 center+small_radius, center+small_radius), 
                 fill=(255, 100, 100))
    
    # Save the result
    logo.save('app_logo.png')
    print("Logo created successfully!")

if __name__ == "__main__":
    # For reproducibility
    random.seed(42)
    
    print("Creating images for the app...")
    create_background()
    try:
        create_simple_logo()
    except Exception as e:
        print(f"Error creating logo: {e}")
        print("Creating simple logo instead...")
        create_simple_logo()
    print("All images created successfully!") 