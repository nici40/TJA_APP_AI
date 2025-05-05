from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.metrics import dp
from theme_manager import ThemeManager
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, RoundedRectangle

Builder.load_string('''
<SettingsScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(10)
        
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(50)
            spacing: dp(10)
            
            Button:
                text: '<'
                font_size: dp(24)
                size_hint_x: None
                width: dp(50)
                background_normal: ''
                background_color: (0.85, 0.82, 0.78, 1) if not root.theme_manager.is_dark_mode else (0.3, 0.3, 0.3, 1)
                color: (0.1, 0.1, 0.1, 1) if not root.theme_manager.is_dark_mode else (0.9, 0.9, 0.9, 1)
                on_press: root.go_back()
            
            Label:
                text: 'Settings'
                font_size: dp(24)
                color: root.theme_manager.get_colors()['text']
                size_hint_x: 0.8
            
            Button:
                text: 'Logout'
                font_size: dp(16)
                size_hint_x: None
                width: dp(80)
                background_normal: ''
                background_color: (0.85, 0.82, 0.78, 1) if not root.theme_manager.is_dark_mode else (0.3, 0.3, 0.3, 1)
                color: (0.1, 0.1, 0.1, 1) if not root.theme_manager.is_dark_mode else (0.9, 0.9, 0.9, 1)
                on_press: root.logout()
        
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(50)
            padding: [dp(10), 0]
            
            Label:
                text: 'Dark Mode'
                color: root.theme_manager.get_colors()['text']
                size_hint_x: 0.7
            
            Switch:
                id: dark_mode_switch
                active: root.theme_manager.is_dark_mode
                on_active: root.toggle_dark_mode(self.active)
                size_hint_x: 0.3
        
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(50)
            padding: [dp(10), 0]
            
            Label:
                text: 'Notifications'
                color: root.theme_manager.get_colors()['text']
                size_hint_x: 0.7
            
            Switch:
                id: notifications_switch
                active: True
                size_hint_x: 0.3
        
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(50)
            padding: [dp(10), 0]
            
            Label:
                text: 'Sound Effects'
                color: root.theme_manager.get_colors()['text']
                size_hint_x: 0.7
            
            Switch:
                id: sound_switch
                active: True
                size_hint_x: 0.3
''')

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        self.theme_manager = ThemeManager()
        super(SettingsScreen, self).__init__(**kwargs)
        self.setup_ui()
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.update_theme()
    
    def setup_ui(self):
        # Main layout
        self.layout = BoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(10)
        )
        
        # Header with back button and title
        header_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10)
        )
        
        self.back_button = Button(
            text='<',
            font_size=dp(24),
            size_hint_x=None,
            width=dp(50),
            background_normal=''
        )
        self.back_button.bind(on_press=self.go_back)
        
        self.title = Label(
            text='Settings',
            font_size=dp(24),
            size_hint_x=0.8
        )
        
        self.logout_button = Button(
            text='Logout',
            font_size=dp(16),
            size_hint_x=None,
            width=dp(80),
            background_normal=''
        )
        self.logout_button.bind(on_press=self.logout)
        
        header_layout.add_widget(self.back_button)
        header_layout.add_widget(self.title)
        header_layout.add_widget(self.logout_button)
        self.layout.add_widget(header_layout)
        
        # Dark Mode Setting
        dark_mode_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            padding=[dp(10), 0]
        )
        
        self.dark_mode_label = Label(
            text='Dark Mode',
            size_hint_x=0.7
        )
        
        self.dark_mode_switch = Switch(
            active=self.theme_manager.is_dark_mode,
            size_hint_x=0.3
        )
        self.dark_mode_switch.bind(active=self.toggle_dark_mode)
        
        dark_mode_layout.add_widget(self.dark_mode_label)
        dark_mode_layout.add_widget(self.dark_mode_switch)
        self.layout.add_widget(dark_mode_layout)
        
        # Notifications Setting
        notifications_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            padding=[dp(10), 0]
        )
        
        self.notifications_label = Label(
            text='Notifications',
            size_hint_x=0.7
        )
        
        notifications_switch = Switch(
            active=True,
            size_hint_x=0.3
        )
        
        notifications_layout.add_widget(self.notifications_label)
        notifications_layout.add_widget(notifications_switch)
        self.layout.add_widget(notifications_layout)
        
        # Sound Effects Setting
        sound_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            padding=[dp(10), 0]
        )
        
        self.sound_label = Label(
            text='Sound Effects',
            size_hint_x=0.7
        )
        
        sound_switch = Switch(
            active=True,
            size_hint_x=0.3
        )
        
        sound_layout.add_widget(self.sound_label)
        sound_layout.add_widget(sound_switch)
        self.layout.add_widget(sound_layout)
        
        # Add the main layout to the screen
        self.add_widget(self.layout)
        
        # Set up the background canvas
        with self.canvas.before:
            self.bg_color = Color(1, 1, 1, 1)  # Default to white
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
    
    def update_rect(self, *args):
        """Update the background rectangle position and size"""
        if hasattr(self, 'bg_rect'):
            self.bg_rect.pos = self.pos
            self.bg_rect.size = self.size
    
    def update_theme(self):
        """Update the theme colors"""
        colors = self.theme_manager.get_colors()
        
        # Update background color
        if hasattr(self, 'bg_color'):
            self.bg_color.rgba = colors['background']
        
        # Update text colors
        if hasattr(self, 'title'):
            self.title.color = colors['text']
            # Set button colors based on theme
            if self.theme_manager.is_dark_mode:
                self.back_button.background_color = (0.3, 0.3, 0.3, 1)
                self.logout_button.background_color = (0.3, 0.3, 0.3, 1)
                self.back_button.color = (0.9, 0.9, 0.9, 1)
                self.logout_button.color = (0.9, 0.9, 0.9, 1)
            else:
                self.back_button.background_color = (0.85, 0.82, 0.78, 1)
                self.logout_button.background_color = (0.85, 0.82, 0.78, 1)
                self.back_button.color = (0.1, 0.1, 0.1, 1)
                self.logout_button.color = (0.1, 0.1, 0.1, 1)
            
            self.dark_mode_label.color = colors['text']
            self.notifications_label.color = colors['text']
            self.sound_label.color = colors['text']
    
    def toggle_dark_mode(self, instance=None, value=None):
        """Toggle dark mode and update the theme"""
        if value is None:
            value = not self.theme_manager.is_dark_mode
        self.theme_manager.set_dark_mode(value)
        self.update_theme()
    
    def go_back(self, *args):
        """Navigate back to the previous screen"""
        self.manager.current = 'home'
    
    def logout(self, *args):
        """Handle logout action"""
        app = App.get_running_app()
        app.current_user = None
        self.manager.current = 'login' 