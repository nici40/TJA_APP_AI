from kivy.properties import BooleanProperty
from kivy.metrics import dp
from kivy.event import EventDispatcher
from kivy.app import App

class ThemeManager(EventDispatcher):
    _instance = None
    is_dark_mode = BooleanProperty(False)
    _updating = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ThemeManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            super(ThemeManager, self).__init__()
            self.initialized = True
            self._setup_colors()
    
    def _setup_colors(self):
        # Light theme colors
        self.light_colors = {
            'background': [1, 1, 1, 1],  # White
            'text': [0, 0, 0, 1],  # Black
            'primary': [0.2, 0.6, 1, 1],  # Blue
            'secondary': [0.8, 0.8, 0.8, 1],  # Light Gray
            'input_bg': [0.95, 0.95, 0.95, 1],  # Very Light Gray
            'button_bg': [0.2, 0.6, 1, 1]  # Blue
        }
        
        # Dark theme colors
        self.dark_colors = {
            'background': [0.1, 0.1, 0.1, 1],  # Dark Gray
            'text': [1, 1, 1, 1],  # White
            'primary': [0.2, 0.6, 1, 1],  # Blue
            'secondary': [0.3, 0.3, 0.3, 1],  # Dark Gray
            'input_bg': [0.2, 0.2, 0.2, 1],  # Dark Gray
            'button_bg': [0.2, 0.6, 1, 1]  # Blue
        }
    
    def get_colors(self):
        return self.dark_colors if self.is_dark_mode else self.light_colors
    
    def set_dark_mode(self, value):
        # Prevent recursive updates
        if self._updating:
            return
            
        # Only update if the value is different
        if self.is_dark_mode != value:
            self._updating = True
            try:
                self.is_dark_mode = value
                # Update all screens
                app = App.get_running_app()
                if app:
                    app.update_theme()
            finally:
                self._updating = False
    
    def toggle_theme(self):
        self.set_dark_mode(not self.is_dark_mode)
        return self.is_dark_mode 