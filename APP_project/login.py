from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from theme_manager import ThemeManager

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.theme_manager = ThemeManager()
        self.setup_ui()
        self.update_theme()
    
    def setup_ui(self):
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Logo
        logo = Image(source='icons/logo.png', size_hint=(1, 0.3))
        layout.add_widget(logo)
        
        # Username input
        self.username = TextInput(
            hint_text='Username',
            multiline=False,
            size_hint=(1, None),
            height=50
        )
        layout.add_widget(self.username)
        
        # Password input
        self.password = TextInput(
            hint_text='Password',
            password=True,
            multiline=False,
            size_hint=(1, None),
            height=50
        )
        layout.add_widget(self.password)
        
        # Login button
        login_btn = Button(
            text='Login',
            size_hint=(1, None),
            height=50
        )
        login_btn.bind(on_press=self.login)
        layout.add_widget(login_btn)
        
        # Register link
        register_btn = Button(
            text='Don\'t have an account? Register',
            size_hint=(1, None),
            height=30,
            background_color=(0, 0, 0, 0)
        )
        register_btn.bind(on_press=self.go_to_register)
        layout.add_widget(register_btn)
        
        self.add_widget(layout)
    
    def update_theme(self):
        colors = self.theme_manager.get_colors()
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*colors['background'])
            Rectangle(pos=self.pos, size=self.size)
        
        # Update text colors
        for child in self.children[0].children:
            if isinstance(child, TextInput):
                child.background_color = colors['input_bg']
                child.foreground_color = colors['text']
                child.hint_text_color = colors['text']
            elif isinstance(child, Button):
                child.background_color = colors['button_bg']
                child.color = colors['text']
    
    def login(self, instance):
        # TODO: Implement login logic
        self.manager.current = 'home'
    
    def go_to_register(self, instance):
        self.manager.current = 'register' 