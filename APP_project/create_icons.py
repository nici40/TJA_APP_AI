from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(name, size=(100, 100), bg_color=(240, 240, 240), fg_color=(60, 60, 60)):
    """Create a simple icon with the first letter of the name"""
    # Create a blank image with background color
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to load a font, fall back to default if not available
    try:
        font = ImageFont.truetype("arial.ttf", size[0] // 2)
    except IOError:
        font = ImageFont.load_default()
    
    # Get the first letter of the name
    letter = name[0].upper()
    
    # Calculate position to center the letter
    left, top, right, bottom = font.getbbox(letter)
    w, h = right - left, bottom - top
    position = ((size[0] - w) // 2, (size[1] - h) // 2)
    
    # Draw the letter
    draw.text(position, letter, font=font, fill=fg_color)
    
    # Save the image
    if not os.path.exists('icons'):
        os.makedirs('icons')
    img.save(f'icons/{name}.png')
    print(f"Created icon: icons/{name}.png")

# Create icons for our app
icons = ['home', 'reminder', 'camera', 'microphone', 'settings']

# Create each icon
for icon in icons:
    create_icon(icon)

print("All icons created successfully.")
