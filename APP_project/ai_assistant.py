import speech_recognition as sr
import pyttsx3
import threading
import json
import os
from openai import OpenAI
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty
from kivy.event import EventDispatcher
from config import OPENAI_API_KEY, AI_MODEL

class AIAssistant(EventDispatcher):
    response_text = StringProperty('')
    recognized_text = StringProperty('')
    is_listening = BooleanProperty(False)
    is_speaking = BooleanProperty(False)
    is_processing = BooleanProperty(False)
    
    def __init__(self, api_key=None):
        super(AIAssistant, self).__init__()
        # Initialize OpenAI with API key if provided
        self.api_key = api_key or OPENAI_API_KEY
        # Create OpenAI client
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        
        # Initialize speech recognition and text-to-speech engines
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        
        # Set properties for voice
        voices = self.engine.getProperty('voices')
        # Choose a female voice if available
        for voice in voices:
            if 'female' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        # Set voice rate and volume
        self.engine.setProperty('rate', 175)  # Speed of speech
        self.engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        
        # System context for the AI assistant
        self.system_context = """
        You are a medical assistant specializing in medication management. 
        Your primary role is to help users track their antibiotic medications, 
        ensure they take them on schedule, and provide relevant medical advice. 
        
        When asked about antibiotics, provide accurate information about proper usage, 
        including the importance of completing the full course even if symptoms improve. 
        
        For medication reminders:
        1. Ask for medication name, dosage, frequency, and duration
        2. Suggest setting up specific time-based reminders
        3. Emphasize the importance of taking antibiotics exactly as prescribed
        
        You can also provide general health information but clarify that your 
        advice does not replace consultation with healthcare professionals.
        
        Always be helpful, clear, and accurate in your responses.
        """
        
        # Message history
        self.messages = [
            {"role": "system", "content": self.system_context}
        ]
    
    def process_text_input(self, user_input):
        """Process text input and generate AI response"""
        self.is_processing = True
        
        # Add user message to history
        self.messages.append({"role": "user", "content": user_input})
        
        # Process in a separate thread to avoid blocking UI
        threading.Thread(target=self._process_with_ai, args=(user_input,)).start()
    
    def _process_with_ai(self, user_input):
        """Process text with AI and update response"""
        try:
            if not self.api_key:
                # Simulate response if no API key
                response = self._simulate_ai_response(user_input)
            else:
                # Use OpenAI API with new client format
                completion = self.client.chat.completions.create(
                    model=AI_MODEL,
                    messages=self.messages
                )
                response = completion.choices[0].message.content
            
            # Add assistant response to history
            self.messages.append({"role": "assistant", "content": response})
            
            # Update the response text property (needs to be on the main thread)
            Clock.schedule_once(lambda dt: self._update_response(response), 0)
            
        except Exception as e:
            error_msg = f"Error processing request: {str(e)}"
            Clock.schedule_once(lambda dt: self._update_response(error_msg), 0)
        finally:
            Clock.schedule_once(lambda dt: setattr(self, 'is_processing', False), 0)
    
    def _update_response(self, text):
        """Update the response text property"""
        self.response_text = text
    
    def start_voice_input(self):
        """Start listening for voice input"""
        self.is_listening = True
        threading.Thread(target=self._listen_for_speech).start()
    
    def _listen_for_speech(self):
        """Listen for speech and convert to text"""
        with sr.Microphone() as source:
            # Adjust for ambient noise
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            try:
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                # Convert speech to text
                user_input = self.recognizer.recognize_google(audio)
                
                # Process the recognized text
                Clock.schedule_once(lambda dt: self._handle_recognized_text(user_input), 0)
                
            except sr.WaitTimeoutError:
                Clock.schedule_once(lambda dt: self._handle_listening_timeout(), 0)
            except sr.UnknownValueError:
                Clock.schedule_once(lambda dt: self._handle_unrecognized_speech(), 0)
            except Exception as e:
                Clock.schedule_once(lambda dt: self._handle_listening_error(str(e)), 0)
            finally:
                Clock.schedule_once(lambda dt: setattr(self, 'is_listening', False), 0)
    
    def _handle_recognized_text(self, text):
        """Handle recognized text from speech"""
        # Store the recognized text
        self.recognized_text = text
        # Process the text input
        self.process_text_input(text)
    
    def _handle_listening_timeout(self):
        """Handle timeout when listening for speech"""
        self.response_text = "I didn't hear anything. Please try again."
    
    def _handle_unrecognized_speech(self):
        """Handle unrecognized speech"""
        self.response_text = "I couldn't understand what you said. Please try again."
    
    def _handle_listening_error(self, error_msg):
        """Handle error during speech recognition"""
        self.response_text = f"Error during speech recognition: {error_msg}"
    
    def speak_response(self):
        """Convert response text to speech"""
        if not self.response_text:
            return
        
        self.is_speaking = True
        threading.Thread(target=self._text_to_speech).start()
    
    def _text_to_speech(self):
        """Convert text to speech and play it"""
        try:
            self.engine.say(self.response_text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error during text-to-speech: {str(e)}")
        finally:
            Clock.schedule_once(lambda dt: setattr(self, 'is_speaking', False), 0)
    
    def _simulate_ai_response(self, user_input):
        """Simulate AI response when no API key is available"""
        user_input = user_input.lower()
        
        # Check for reminder-related keywords
        if any(word in user_input for word in ['remind', 'reminder', 'schedule', 'set', 'alarm']):
            return "I can help you set a reminder for your antibiotics. Please tell me the name of the medication, dosage, and how often you need to take it."
        
        # Check for antibiotic-related questions
        elif any(word in user_input for word in ['antibiotic', 'medicine', 'medication', 'amoxicillin', 'penicillin']):
            return "Antibiotics are medications used to treat bacterial infections. It's important to complete the full course of antibiotics as prescribed, even if you start feeling better. Would you like me to set up a reminder for your medication?"
        
        # Check for general greeting
        elif any(word in user_input for word in ['hello', 'hi', 'hey', 'greetings']):
            return "Hello! I'm your medication assistant. I can help you manage your antibiotic schedule and answer questions about your medication. How can I assist you today?"
        
        # Default response
        else:
            return "I'm your antibiotic medication assistant. I can help you set reminders, track your medication schedule, or answer questions about your antibiotics. What would you like help with?"
    
    def save_conversation(self, filename='conversation_history.json'):
        """Save the conversation history to a file"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.messages, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving conversation: {str(e)}")
            return False
    
    def load_conversation(self, filename='conversation_history.json'):
        """Load conversation history from a file"""
        try:
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    self.messages = json.load(f)
                return True
            return False
        except Exception as e:
            print(f"Error loading conversation: {str(e)}")
            return False
