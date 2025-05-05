from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, PushMatrix, PopMatrix, Translate, Rotate, Rectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.core.text import Label as CoreLabel
import math
from kivy.metrics import dp

class RoundButtonArea(ButtonBehavior, Widget):
    """A specialized button that reliably detects touches within a circular area"""
    
    def __init__(self, **kwargs):
        # Get background color for the circle
        self.bg_color = kwargs.pop('bg_color', kwargs.pop('color', (0.2, 0.7, 0.3, 1)))  # Default green
        self.fg_color = kwargs.pop('fg_color', (1, 1, 1, 1))  # Default white
        self.text = kwargs.pop('text', '+')
        self.font_size = kwargs.pop('font_size', 24)
        self.bold = kwargs.pop('bold', False)
        
        # Initialize as widget first
        super(RoundButtonArea, self).__init__(**kwargs)
        
        # Draw the circle in the canvas
        with self.canvas:
            # Background circle
            Color(*self.bg_color)
            self.circle = Ellipse(pos=self.pos, size=self.size)
            
            # Create a label for the text
            self.label = CoreLabel(text=self.text, font_size=self.font_size, bold=self.bold)
            self.label.refresh()
            
            # Text in the center
            Color(*self.fg_color)
            
            # Calculate text position - center perfectly
            text_width, text_height = self.label.texture.size
            text_x = self.center_x - text_width / 2
            text_y = self.center_y - text_height / 2
            
            # Draw the text
            self.text_rect = Rectangle(
                pos=(text_x, text_y),
                size=self.label.texture.size,
                texture=self.label.texture
            )
            
        # Update circle and text when position or size changes
        self.bind(pos=self._update_graphics, size=self._update_graphics)
    
    def _update_graphics(self, *args):
        """Update all graphical elements when position or size changes"""
        # Update circle
        self.circle.pos = self.pos
        self.circle.size = self.size
        
        # Update text - ensure it's always centered
        self.label = CoreLabel(text=self.text, font_size=self.font_size, bold=self.bold)
        self.label.refresh()
        
        text_width, text_height = self.label.texture.size
        text_x = self.center_x - text_width / 2
        text_y = self.center_y - text_height / 2
        
        self.text_rect.texture = self.label.texture
        self.text_rect.size = self.label.texture.size
        self.text_rect.pos = (text_x, text_y)
    
    def collide_point(self, x, y):
        """Check if a point is within the circular area"""
        center_x = self.center_x
        center_y = self.center_y
        radius = min(self.width, self.height) / 2
        return math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2) <= radius

# Define a simpler alias for backwards compatibility
RoundButton = RoundButtonArea

class RoundButton(Button):
    def __init__(self, **kwargs):
        # Extract our custom properties
        self.bg_color = kwargs.pop('bg_color', (0.2, 0.7, 0.3, 1))  # Default green
        self.fg_color = kwargs.pop('fg_color', (1, 1, 1, 1))  # Default white
        
        super(RoundButton, self).__init__(**kwargs)
        
        # Set up button properties
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)  # Transparent
        self.color = self.fg_color  # Text color
        
        # Bind to size and pos changes
        self.bind(size=self._update_canvas, pos=self._update_canvas)
    
    def _update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg_color)
            Ellipse(pos=self.pos, size=self.size)
    
    def collide_point(self, x, y):
        # Check if the point is inside the circle
        center_x = self.center_x
        center_y = self.center_y
        radius = min(self.width, self.height) / 2
        
        # Calculate distance from center
        distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
        
        return distance <= radius
