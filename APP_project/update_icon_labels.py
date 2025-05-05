# Script to update icon mappings in home.py to use the new icons with correct labels

import os

# Get the absolute path to the APP_project directory
APP_DIR = os.path.dirname(os.path.abspath(__file__))
ICONS_DIR = os.path.join(APP_DIR, 'icons')

# Create the icon mappings
home_path = os.path.join(APP_DIR, 'home.py')

# Map the icon files to their labels in the app
icon_mappings = {
    'home': os.path.join(ICONS_DIR, 'home-icon-silhouette.png').replace('\\', '/'),
    'reminder': os.path.join(ICONS_DIR, 'bell.png').replace('\\', '/'),
    'camera': os.path.join(ICONS_DIR, 'camera.png').replace('\\', '/'),
    'voice': os.path.join(ICONS_DIR, 'microphone.png').replace('\\', '/'),
    'settings': os.path.join(ICONS_DIR, 'setting.png').replace('\\', '/')
}

# Create the new mapping string
new_mapping = f"""        # Map icon types to icon image files with absolute paths
        icon_mapping = {{
            'home': '{icon_mappings['home']}',
            'reminder': '{icon_mappings['reminder']}',
            'camera': '{icon_mappings['camera']}',
            'voice': '{icon_mappings['voice']}',
            'settings': '{icon_mappings['settings']}'
        }}"""

# Read the home.py file
with open(home_path, 'r') as file:
    content = file.read()

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

print("\nUpdated icon mappings in home.py to use the new icons with correct labels")
print("The following mappings were set:")
for label, path in icon_mappings.items():
    print(f"'{label}' -> {os.path.basename(path)}")
