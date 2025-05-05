from kivy.uix.image import Image as KivyImage
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import cv2

class CameraScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)

        # Create a Kivy Image widget for displaying frames
        self.camera_view = KivyImage(
            size_hint=(1, 1),
            allow_stretch=True,
            keep_ratio=True
        )
        self.main_layout.add_widget(self.camera_view)

        # Initialize OpenCV capture on device 0
        try:
            self.capture = cv2.VideoCapture(0)
            if not self.capture.isOpened():
                raise Exception('Could not open video device')
        except Exception as e:
            print(f"Error initializing camera capture: {e}")
            error_label = Label(
                text="Unable to access camera.",
                font_size=dp(18),
                color=(1, 0, 0, 1),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            self.main_layout.add_widget(error_label)
            return

        # Schedule the frame update
        self.event = Clock.schedule_interval(self.update_frame, 1.0 / 30.0)  # 30 FPS

    def update_frame(self, dt):
        # Read frame from OpenCV
        ret, frame = self.capture.read()
        if not ret:
            return

        # Convert BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Flip horizontal (optional)
        frame = cv2.flip(frame, 0)

        # Convert to texture
        texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]),
            colorfmt='rgb'
        )
        texture.blit_buffer(frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')

        # Display image from the texture
        self.camera_view.texture = texture

    def on_leave(self):
        # Stop the scheduled event and release capture
        if hasattr(self, 'event'):
            self.event.cancel()
        if hasattr(self, 'capture') and self.capture.isOpened():
            self.capture.release()
        return super().on_leave()
