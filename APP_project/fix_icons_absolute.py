# Script to fix icon paths in home.py by using absolute paths

import os
from PIL import Image, ImageDraw, ImageFont

# Get the absolute path to the APP_project directory
APP_DIR = os.path.dirname(os.path.abspath(__file__))
ICONS_DIR = os.path.join(APP_DIR, 'icons')

# Make sure the icons directory exists
if not os.path.exists(ICONS_DIR):
    os.makedirs(ICONS_DIR)

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
    position = ((size[0] - w) // 2, (size[1] - h) // 2 - h // 4)  # Adjusted for visual centering
    
    # Draw the letter
    draw.text(position, letter, font=font, fill=fg_color)
    
    # Save the image
    filepath = os.path.join(ICONS_DIR, f"{name}.png")
    img.save(filepath)
    print(f"Created icon: {filepath}")
    return filepath

# Create all the icons
icons = ['home', 'reminder', 'camera', 'microphone', 'settings']
for icon in icons:
    create_icon(icon)

# Create the home.py icon mapping replacements
home_path = os.path.join(APP_DIR, 'home.py')
with open(home_path, 'r') as file:
    content = file.read()

# Get absolute paths for icons in Kivy-friendly format
home_icon = os.path.join(ICONS_DIR, 'home.png').replace('\\', '/')
reminder_icon = os.path.join(ICONS_DIR, 'reminder.png').replace('\\', '/')
camera_icon = os.path.join(ICONS_DIR, 'camera.png').replace('\\', '/')
microphone_icon = os.path.join(ICONS_DIR, 'microphone.png').replace('\\', '/')
settings_icon = os.path.join(ICONS_DIR, 'settings.png').replace('\\', '/')

# Create the new mapping string
new_mapping = f"""        # Map icon types to icon image files with absolute paths
        icon_mapping = {{
            'home': '{home_icon}',
            'reminder': '{reminder_icon}',
            'camera': '{camera_icon}',
            'voice': '{microphone_icon}',
            'settings': '{settings_icon}'
        }}"""

# Update both instances of icon_mapping in the file
lines = content.split('\n')
updated_lines = []
in_mapping_block = False
line_count = 0

for line in lines:
    if '# Map icon types to icon image files' in line:
        in_mapping_block = True
        line_count = 0
        # Add the new mapping block instead
        updated_lines.append(new_mapping)
    elif in_mapping_block:
        line_count += 1
        # Skip the old mapping block lines
        if line_count >= 8:  # After the closing brace line
            in_mapping_block = False
            updated_lines.append(line)  # Keep the line after the block
    else:
        updated_lines.append(line)

# Write the updated content back to the file
with open(home_path, 'w') as file:
    file.write('\n'.join(updated_lines))

print(f"\nUpdated icon mappings in {home_path} to use absolute paths")
print("\nIcons should now display correctly in the app!")
