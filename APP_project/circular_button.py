from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse
from kivy.metrics import dp

class CircularButton(Button):
    """A simple circular button that ensures the entire circle is clickable"""
    
    def __init__(self, **kwargs):
        # Extract custom properties
        bg_color = kwargs.pop('bg_color', (0.2, 0.7, 0.3, 1))  # Default green
        
        # Make sure we have a square button for perfect circle
        kwargs['size_hint'] = (None, None)
        
        # Initialize with a transparent background
        kwargs['background_normal'] = ''
        kwargs['background_color'] = (0, 0, 0, 0)  # Transparent
        
        super(CircularButton, self).__init__(**kwargs)
        
        # Store color for reuse
        self.bg_color = bg_color
        
        # Draw the circle
        self.redraw()
        
        # Bind to size and pos changes to keep circle updated
        self.bind(size=self.redraw)
        self.bind(pos=self.redraw)
    
    def redraw(self, *args):
        """Redraw the circle whenever size or position changes"""
        # Clear existing canvas
        self.canvas.before.clear()
        
        # Draw the circle background
        with self.canvas.before:
            Color(*self.bg_color)
            self.circle = Ellipse(pos=self.pos, size=self.size)
