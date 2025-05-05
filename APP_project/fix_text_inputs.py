# Script to fix text input issues where text appears cut off
import re

def fix_login_text_inputs():
    # Read the loggin.py file
    with open('loggin.py', 'r') as f:
        content = f.read()
    
    # Fix the StyledTextInput class for better text display
    original_class = """class StyledTextInput(TextInput):
    def __init__(self, **kwargs):
        super(StyledTextInput, self).__init__(**kwargs)
        self.background_color = (1, 1, 1, 0.9)
        self.foreground_color = (0, 0, 0, 1)
        self.cursor_color = (0.1, 0.5, 0.9, 1)
        self.font_size = dp(18)
        self.padding = [20, 12]  # Adjusted padding to prevent text cut-off
        self.multiline = False
        # Set text_validate_unfocus to False to keep focus on input after enter key
        self.text_validate_unfocus = False
        # Set write_tab to False to prevent tab character insertion
        self.write_tab = False
        # These properties help ensure text isn't cut off
        self.hint_text_color = (0.5, 0.5, 0.5, 0.5)
        self.cursor_width = '2sp'"""
    
    improved_class = """class StyledTextInput(TextInput):
    def __init__(self, **kwargs):
        super(StyledTextInput, self).__init__(**kwargs)
        self.background_color = (1, 1, 1, 0.9)
        self.foreground_color = (0, 0, 0, 1)
        self.cursor_color = (0.1, 0.5, 0.9, 1)
        self.font_size = dp(18)
        self.padding = [20, 12]  # Adjusted padding to prevent text cut-off
        self.multiline = False
        self.text_validate_unfocus = False  # Keep focus after pressing enter
        self.write_tab = False  # Prevent tab character insertion
        # Added property to ensure text displays properly
        self.line_height = 1.2
        # Set input_filter to None to allow all characters
        self.input_filter = None
        # Add a hint text color that's visible but not distracting
        self.hint_text_color = (0.5, 0.5, 0.5, 0.5)
        # Set a custom cursor width for better visibility
        self.cursor_width = '2sp'"""
    
    # Replace the class definition
    updated_content = content.replace(original_class, improved_class)
    
    # Fix all text input instantiations to increase their height
    pattern_username = r'self\.username = StyledTextInput\(size_hint_y=None, height=dp\(45\)\)'
    replacement_username = 'self.username = StyledTextInput(size_hint_y=None, height=dp(55), hint_text="Enter username")'
    updated_content = re.sub(pattern_username, replacement_username, updated_content)
    
    pattern_password = r'self\.password = StyledTextInput\(password=True, size_hint_y=None, height=dp\(45\)\)'
    replacement_password = 'self.password = StyledTextInput(password=True, size_hint_y=None, height=dp(55), hint_text="Enter password")'
    updated_content = re.sub(pattern_password, replacement_password, updated_content)
    
    # Also fix email input in register screen if it exists
    pattern_email = r'self\.email = StyledTextInput\(size_hint_y=None, height=dp\(45\)\)'
    replacement_email = 'self.email = StyledTextInput(size_hint_y=None, height=dp(55), hint_text="Enter email")'
    updated_content = re.sub(pattern_email, replacement_email, updated_content)
    
    # Write the updated content back to the file
    with open('loggin.py', 'w') as f:
        f.write(updated_content)
    
    print("Fixed text input issues in loggin.py")

if __name__ == "__main__":
    fix_login_text_inputs()
