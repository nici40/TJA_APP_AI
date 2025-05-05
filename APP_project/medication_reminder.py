import json
import os
import datetime
from datetime import datetime, timedelta
import uuid
from kivy.event import EventDispatcher
from kivy.properties import ListProperty
from kivy.clock import Clock
from plyer import notification

class MedicationReminder(EventDispatcher):
    reminders = ListProperty([])
    
    def __init__(self, **kwargs):
        super(MedicationReminder, self).__init__(**kwargs)
        self.reminders_file = 'medication_reminders.json'
        self.load_reminders()
        
        # Start the reminder checking scheduler
        Clock.schedule_interval(self.check_reminders, 30)  # Check every 30 seconds
    
    def load_reminders(self):
        """Load reminders from file"""
        if os.path.exists(self.reminders_file):
            try:
                with open(self.reminders_file, 'r') as f:
                    data = json.load(f)
                    
                    # Convert string dates back to datetime objects
                    for reminder in data:
                        if 'next_time' in reminder and reminder['next_time']:
                            reminder['next_time'] = datetime.fromisoformat(reminder['next_time'])
                        if 'end_date' in reminder and reminder['end_date']:
                            reminder['end_date'] = datetime.fromisoformat(reminder['end_date'])
                        if 'times' in reminder:
                            reminder['times'] = [datetime.fromisoformat(t) if isinstance(t, str) else t for t in reminder['times']]
                    
                    self.reminders = data
            except Exception as e:
                print(f"Error loading reminders: {str(e)}")
                self.reminders = []
        else:
            self.reminders = []
    
    def save_reminders(self):
        """Save reminders to file"""
        try:
            # Convert datetime objects to strings for JSON serialization
            serializable_reminders = []
            for reminder in self.reminders:
                reminder_copy = reminder.copy()
                if 'next_time' in reminder_copy and isinstance(reminder_copy['next_time'], datetime):
                    reminder_copy['next_time'] = reminder_copy['next_time'].isoformat()
                if 'end_date' in reminder_copy and isinstance(reminder_copy['end_date'], datetime):
                    reminder_copy['end_date'] = reminder_copy['end_date'].isoformat()
                if 'times' in reminder_copy:
                    reminder_copy['times'] = [t.isoformat() if isinstance(t, datetime) else t for t in reminder_copy['times']]
                serializable_reminders.append(reminder_copy)
            
            with open(self.reminders_file, 'w') as f:
                json.dump(serializable_reminders, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving reminders: {str(e)}")
            return False
    
    def add_reminder(self, medication_name, dosage, frequency, duration, start_time=None, notes=None):
        """Add a new medication reminder"""
        if not start_time:
            start_time = datetime.now()
        
        # Calculate end date based on duration (in days)
        end_date = None
        if duration and int(duration) > 0:
            end_date = datetime.now() + timedelta(days=int(duration))
        
        # Generate schedule based on frequency
        times = self._generate_schedule(frequency, start_time, end_date)
        
        reminder = {
            'id': str(uuid.uuid4()),
            'medication_name': medication_name,
            'dosage': dosage,
            'frequency': frequency,
            'duration': duration,
            'times': times,
            'next_time': times[0] if times else None,
            'end_date': end_date,
            'notes': notes,
            'created_at': datetime.now().isoformat(),
            'active': True
        }
        
        self.reminders.append(reminder)
        self.save_reminders()
        return reminder['id']
    
    def _generate_schedule(self, frequency, start_time, end_date):
        """Generate schedule of times based on frequency"""
        times = []
        current_time = start_time
        
        # Convert frequency to hours
        hours = self._frequency_to_hours(frequency)
        if not hours:
            return times
        
        # Generate times until end date
        while not end_date or current_time <= end_date:
            times.append(current_time)
            current_time += timedelta(hours=hours)
            
            # Stop if we've generated too many (safety)
            if len(times) > 100:
                break
        
        return times
    
    def _frequency_to_hours(self, frequency):
        """Convert frequency string to hours interval"""
        frequency = frequency.lower()
        
        if 'once daily' in frequency or 'once a day' in frequency or 'daily' in frequency:
            return 24
        elif 'twice daily' in frequency or 'twice a day' in frequency or 'bid' in frequency:
            return 12
        elif 'three times daily' in frequency or 'three times a day' in frequency or 'tid' in frequency:
            return 8
        elif 'four times daily' in frequency or 'four times a day' in frequency or 'qid' in frequency:
            return 6
        elif 'every 6 hours' in frequency:
            return 6
        elif 'every 8 hours' in frequency:
            return 8
        elif 'every 12 hours' in frequency:
            return 12
        else:
            # Default to once daily if unknown
            return 24
    
    def update_reminder(self, reminder_id, **kwargs):
        """Update an existing reminder"""
        for i, reminder in enumerate(self.reminders):
            if reminder['id'] == reminder_id:
                # If frequency or duration changed, regenerate schedule
                regenerate_schedule = False
                if 'frequency' in kwargs and kwargs['frequency'] != reminder['frequency']:
                    regenerate_schedule = True
                
                if 'duration' in kwargs:
                    regenerate_schedule = True
                    if kwargs['duration'] and int(kwargs['duration']) > 0:
                        kwargs['end_date'] = datetime.now() + timedelta(days=int(kwargs['duration']))
                
                # Update the reminder with new values
                for key, value in kwargs.items():
                    reminder[key] = value
                
                # Regenerate schedule if needed
                if regenerate_schedule:
                    start_time = datetime.now()
                    reminder['times'] = self._generate_schedule(
                        reminder['frequency'], 
                        start_time, 
                        reminder['end_date']
                    )
                    reminder['next_time'] = reminder['times'][0] if reminder['times'] else None
                
                self.reminders[i] = reminder
                self.save_reminders()
                return True
        return False
    
    def delete_reminder(self, reminder_id):
        """Delete a reminder"""
        for i, reminder in enumerate(self.reminders):
            if reminder['id'] == reminder_id:
                self.reminders.pop(i)
                self.save_reminders()
                return True
        return False
    
    def get_reminder(self, reminder_id):
        """Get a specific reminder"""
        for reminder in self.reminders:
            if reminder['id'] == reminder_id:
                return reminder
        return None
    
    def get_active_reminders(self):
        """Get all active reminders"""
        now = datetime.now()
        active_reminders = []
        
        for reminder in self.reminders:
            # Skip if not active
            if not reminder.get('active', True):
                continue
                
            # Skip if end date has passed
            if 'end_date' in reminder and reminder['end_date'] and reminder['end_date'] < now:
                continue
                
            active_reminders.append(reminder)
        
        return active_reminders
    
    def check_reminders(self, dt=None):
        """Check for due reminders and send notifications"""
        now = datetime.now()
        updated = False
        
        for i, reminder in enumerate(self.reminders):
            # Skip inactive reminders
            if not reminder.get('active', True):
                continue
                
            # Skip if no next time
            if not reminder.get('next_time'):
                continue
                
            # Check if reminder is due (within last 5 minutes)
            if isinstance(reminder['next_time'], datetime) and reminder['next_time'] <= now and \
               reminder['next_time'] >= now - timedelta(minutes=5):
                # Send notification
                self._send_notification(reminder)
                
                # Update next time
                times = reminder.get('times', [])
                if times:
                    # Find the next future time
                    future_times = [t for t in times if isinstance(t, datetime) and t > now]
                    if future_times:
                        reminder['next_time'] = min(future_times)
                    else:
                        reminder['next_time'] = None
                else:
                    reminder['next_time'] = None
                
                # Mark as updated
                updated = True
                self.reminders[i] = reminder
        
        # Save if any reminders were updated
        if updated:
            self.save_reminders()
    
    def _send_notification(self, reminder):
        """Send a system notification for a medication reminder"""
        try:
            title = f"Medication Reminder: {reminder['medication_name']}"
            message = f"Time to take {reminder['dosage']} of {reminder['medication_name']}."
            if reminder.get('notes'):
                message += f" Note: {reminder['notes']}"
                
            notification.notify(
                title=title,
                message=message,
                app_name="Antibiotic Reminder",
                timeout=10
            )
        except Exception as e:
            print(f"Error sending notification: {str(e)}")
    
    def check_antibiotic_name(self, name):
        """Check if the provided name is a known antibiotic"""
        common_antibiotics = [
            'amoxicillin', 'penicillin', 'azithromycin', 'ciprofloxacin', 
            'doxycycline', 'metronidazole', 'clindamycin', 'erythromycin',
            'trimethoprim', 'cephalexin', 'sulfamethoxazole', 'tetracycline',
            'levofloxacin', 'clarithromycin', 'vancomycin', 'minocycline',
            'nitrofurantoin', 'ampicillin', 'cefdinir', 'ceftriaxone'
        ]
        
        # Check if the name contains any common antibiotic
        name_lower = name.lower()
        for antibiotic in common_antibiotics:
            if antibiotic in name_lower:
                return True, antibiotic
        
        # If no match, return false
        return False, None
    
    def get_usage_advice(self, antibiotic_name):
        """Get basic usage advice for common antibiotics"""
        advice = {
            'amoxicillin': "Take with or without food. Complete the full course as prescribed.",
            'penicillin': "Take on an empty stomach, 1 hour before or 2 hours after meals.",
            'azithromycin': "Take with or without food. If stomach upset occurs, take with food.",
            'ciprofloxacin': "Take with plenty of water. Avoid antacids, dairy products, and calcium-rich foods.",
            'doxycycline': "Take with food or milk to prevent stomach upset. Avoid sun exposure.",
            'metronidazole': "Take with food to reduce stomach upset. Avoid alcohol.",
            'clindamycin': "Take with a full glass of water to prevent throat irritation.",
            'erythromycin': "Take with meals to reduce stomach upset.",
            'trimethoprim': "Take with plenty of fluids.",
            'cephalexin': "Take with or without food."
        }
        
        antibiotic_name = antibiotic_name.lower()
        
        # Try to find a match
        for key, value in advice.items():
            if key in antibiotic_name:
                return value
        
        # General advice if no specific advice found
        return "Take as prescribed by your healthcare provider. Complete the full course even if you feel better. Contact your healthcare provider if you experience severe side effects."
