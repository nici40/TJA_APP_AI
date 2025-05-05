# Antibiotic Reminder App with AI Assistant

## Overview
This application helps users track and manage their antibiotic medications with intelligent reminders and an AI-powered assistant that can provide information about medications and help create reminders.

## Features
- **Medication Reminder System**: Set up reminders for antibiotics with customizable frequency and duration
- **AI Assistant**: Ask questions about antibiotics, get usage advice, and control the app with voice commands
- **Voice Control**: Speak to the app to add reminders or get information
- **Smart Notifications**: Get alerts when it's time to take your medication
- **Beautiful UI**: Modern, intuitive interface designed for ease of use

## Installation

### Dependencies
Install the required dependencies:

```
pip install -r requirements.txt
```

### API Key (Optional)
For full AI functionality, create a file named `openai_api_key.txt` in the root directory containing your OpenAI API key.

## Usage

1. Run the application:
```
python main.py
```

2. Create a user account or log in
3. Navigate to the Reminders section to add antibiotic reminders
4. Use the Voice Assistant to ask questions about your medications

## Modules

- **main.py**: Main application entry point with navigation logic
- **medication_reminder.py**: Handles reminder creation, storage, and notifications
- **ai_assistant.py**: AI conversation and voice recognition capabilities
- **home.py**: UI screens and components
- **loggin.py**: Authentication and user management
