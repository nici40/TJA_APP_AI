# Script to fix the add button in the ReminderScreen

def fix_reminder_screen():
    # Read home.py file
    with open('home.py', 'r') as f:
        content = f.read()
    
    # Replace the entire section of button creation with a simpler approach
    # that guarantees the entire button area responds to touch
    old_code = """        # Create a round button using the built-in button with background override
        from kivy.uix.button import Button
        
        # Create a simple button with maximum tap area
        circle_btn = Button(
            text='+',
            font_size=dp(42),
            bold=True,
            background_color=(0.2, 0.7, 0.3, 1),  # Green
            background_normal='',  # No background image
            background_down='',  # No pressed image
            color=(1, 1, 1, 1),  # White text
            size_hint=(None, None),
            size=(dp(70), dp(70)),
            border=(0, 0, 0, 0)  # No border - pure color
        )
        
        # Round the corners with maximum radius to create a circle
        circle_btn.radius = [dp(35), dp(35), dp(35), dp(35)]"""
    
    new_code = """        # Create a simple button that's fully responsive
        from kivy.uix.button import Button
        
        # Create a completely flat, solid colored button for maximum touch area
        circle_btn = Button(
            text='+',
            font_size=dp(42),
            bold=True,
            background_color=(0.2, 0.7, 0.3, 1),  # Green color
            background_normal='',  # No background image for clean color
            background_down='',    # No pressed state image 
            color=(1, 1, 1, 1),    # White text color
            size_hint=(None, None),
            size=(dp(70), dp(70)),
            markup=False           # No markup to interfere with touch
        )
        
        # We'll round the corners with custom canvas instructions that won't interfere with touches
        with circle_btn.canvas.before:
            Color(0.2, 0.7, 0.3, 1)  # Match button background color
            self.circle_bg = RoundedRectangle(
                pos=circle_btn.pos, 
                size=circle_btn.size,
                radius=[dp(35), dp(35), dp(35), dp(35)]  # Maximum rounding for a circle
            )
        
        # Make sure our custom drawing follows the button
        def update_circle_bg(instance, value):
            if hasattr(self, 'circle_bg'):
                self.circle_bg.pos = instance.pos
                self.circle_bg.size = instance.size
                
        # Connect position and size updates
        circle_btn.bind(pos=update_circle_bg, size=update_circle_bg)"""
    
    # Replace the button creation code
    updated_content = content.replace(old_code, new_code)
    
    # Remove any troublesome _update_circle method
    old_update_method = """    def _update_circle(self, instance, value):
        """Update all elements of the circular button when position or size changes"""
        # Update all circle elements
        self.circle.pos = instance.pos
        self.circle.size = instance.size
        
        # Update stencil elements
        if hasattr(self, 'circle_clip'):
            self.circle_clip.pos = instance.pos
            self.circle_clip.size = instance.size
            
        if hasattr(self, 'circle_release'):
            self.circle_release.pos = instance.pos
            self.circle_release.size = instance.size"""
    
    new_update_method = """    def _update_circle(self, instance, value):
        """Stub method maintained for compatibility"""
        pass"""
    
    # Replace the update method
    updated_content = updated_content.replace(old_update_method, new_update_method)
    
    # Write the changes back to home.py
    with open('home.py', 'w') as f:
        f.write(updated_content)
    
    print("Fixed the add button in ReminderScreen so the entire circle is clickable.")

if __name__ == "__main__":
    fix_reminder_screen()
