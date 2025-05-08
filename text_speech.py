import pyttsx3
import os
import time
import threading
import tempfile
import sys

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    print("Google Text-to-Speech not available. Install with: pip install gtts")

class EnhancedTTS:
    def __init__(self):
        """Initialize the enhanced text-to-speech engine"""
        self.engine = pyttsx3.init()
        self.is_speaking = False
        self.paused = False
        self.default_rate = 150
        self.default_volume = 1.0
        self.current_voice = None
        self.voices = self.get_available_voices()
        self.speech_thread = None
        self.stop_requested = False
        
        # Set default voice (first available)
        if self.voices:
            self.current_voice = self.voices[0].id
            self.engine.setProperty('voice', self.current_voice)
    
    def get_available_voices(self):
        """Get all available voices on the system"""
        return self.engine.getProperty('voices')
    
    def list_voices(self):
        """Print all available voices with details and return voice info"""
        voices = self.get_available_voices()
        voice_info = []
        
        print("\nAvailable Voices:")
        print("-" * 50)
        
        for i, voice in enumerate(voices):
            print(f"Voice #{i+1}:")
            print(f"ID: {voice.id}")
            print(f"Name: {voice.name}")
            print(f"Languages: {voice.languages}")
            print("-" * 50)
            
            voice_info.append({
                'id': voice.id,
                'name': voice.name,
                'index': i
            })
            
        return voice_info
    
    def set_voice(self, voice_index=None, voice_id=None):
        """Set voice by index or ID"""
        if voice_index is not None and 0 <= voice_index < len(self.voices):
            self.current_voice = self.voices[voice_index].id
        elif voice_id:
            self.current_voice = voice_id
        else:
            return False
            
        self.engine.setProperty('voice', self.current_voice)
        return True
    
    def speak(self, text, rate=None, volume=None, voice_id=None, blocking=True):
        """Convert text to speech with optional parameters"""
        if self.is_speaking:
            self.stop()
            time.sleep(0.5)  # Give time for previous speech to stop
        
        # Set properties
        self.engine.setProperty('rate', rate if rate is not None else self.default_rate)
        self.engine.setProperty('volume', volume if volume is not None else self.default_volume)
        
        if voice_id:
            self.engine.setProperty('voice', voice_id)
        elif self.current_voice:
            self.engine.setProperty('voice', self.current_voice)
        
        if blocking:
            self.is_speaking = True
            self.engine.say(text)
            self.engine.runAndWait()
            self.is_speaking = False
        else:
            # Non-blocking speech in a separate thread
            self.stop_requested = False
            self.is_speaking = True
            self.speech_thread = threading.Thread(target=self._speak_thread, args=(text,))
            self.speech_thread.daemon = True
            self.speech_thread.start()
    
    def _speak_thread(self, text):
        """Internal method for threaded speech"""
        self.engine.say(text)
        self.engine.runAndWait()
        self.is_speaking = False
    
    def stop(self):
        """Stop the current speech"""
        if self.is_speaking:
            self.stop_requested = True
            self.engine.stop()
            self.is_speaking = False
            self.paused = False
            return True
        return False
    
    def save_to_file(self, text, filename, format_type="wav", rate=None, volume=None, voice_id=None, service="local"):
        """
        Save speech to an audio file
        
        Parameters:
            text (str): Text to convert
            filename (str): Output filename without extension
            format_type (str): 'wav' or 'mp3'
            rate (int): Speech rate
            volume (float): Volume level
            voice_id (str): Voice ID to use
            service (str): 'local' for pyttsx3 or 'google' for Google TTS
        """
        # Add extension if not present
        if not filename.lower().endswith(f'.{format_type}'):
            filename = f"{filename}.{format_type}"
            
        if service == "google":
            if not GTTS_AVAILABLE:
                print("Google TTS not available. Install with: pip install gtts")
                return False
                
            # Use Google's TTS service (only supports MP3)
            try:
                tts = gTTS(text=text, lang='en', slow=False)
                tts.save(filename)
                print(f"File saved successfully: {filename}")
                return True
            except Exception as e:
                print(f"Error saving file with Google TTS: {e}")
                return False
        else:
            # Use local pyttsx3 (only supports WAV)
            if format_type.lower() != "wav" and service == "local":
                print("Local TTS engine only supports WAV format. Saving as WAV.")
                filename = filename.rsplit('.', 1)[0] + '.wav'
                
            try:
                # Configure engine
                engine = pyttsx3.init()
                engine.setProperty('rate', rate if rate is not None else self.default_rate)
                engine.setProperty('volume', volume if volume is not None else self.default_volume)
                
                if voice_id:
                    engine.setProperty('voice', voice_id)
                elif self.current_voice:
                    engine.setProperty('voice', self.current_voice)
                    
                # Save to file
                engine.save_to_file(text, filename)
                engine.runAndWait()
                print(f"File saved successfully: {filename}")
                return True
            except Exception as e:
                print(f"Error saving file with local TTS: {e}")
                return False


def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_input_with_prompt(prompt):
    """Get input with a styled prompt"""
    print("\n" + "-" * 50)
    print(prompt)
    print("-" * 50)
    return input("> ")


def text_input_menu():
    """Menu for text input options"""
    clear_screen()
    print("\n===== TEXT INPUT OPTIONS =====")
    print("1. Enter text now")
    print("2. Read text from a file")
    print("3. Back to main menu")
    
    choice = get_input_with_prompt("Select an option (1-3)")
    
    if choice == '1':
        print("\nEnter your text (type 'END' on a new line to finish):")
        lines = []
        while True:
            line = input()
            if line.strip() == 'END':
                break
            lines.append(line)
        return '\n'.join(lines)
    
    elif choice == '2':
        file_path = get_input_with_prompt("Enter the path to your text file")
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            input("Press Enter to continue...")
            return None
    
    return None


def voice_selection_menu(tts):
    """Menu for voice selection"""
    clear_screen()
    print("\n===== VOICE SELECTION =====")
    
    voice_info = tts.list_voices()
    
    if not voice_info:
        print("No voices available!")
        input("Press Enter to continue...")
        return None
    
    voice_choice = get_input_with_prompt(f"Select a voice (1-{len(voice_info)})")
    
    try:
        voice_index = int(voice_choice) - 1
        if 0 <= voice_index < len(voice_info):
            tts.set_voice(voice_index=voice_index)
            voice_name = voice_info[voice_index]['name']
            print(f"Voice set to: {voice_name}")
            input("Press Enter to continue...")
            return voice_info[voice_index]['id']
        else:
            print("Invalid selection!")
            input("Press Enter to continue...")
            return None
    except ValueError:
        print("Invalid input! Please enter a number.")
        input("Press Enter to continue...")
        return None


def file_saving_menu(tts, text):
    """Menu for file saving options"""
    if not text:
        print("No text to save!")
        input("Press Enter to continue...")
        return
        
    clear_screen()
    print("\n===== FILE SAVING OPTIONS =====")
    print("1. Save as WAV (Local TTS)")
    if GTTS_AVAILABLE:
        print("2. Save as MP3 (Google TTS - Internet required)")
    print("3. Back to main menu")
    
    choice = get_input_with_prompt("Select an option")
    
    if choice == '1':
        filename = get_input_with_prompt("Enter filename (without extension)")
        tts.save_to_file(text, filename, format_type="wav", service="local")
        input("Press Enter to continue...")
    
    elif choice == '2' and GTTS_AVAILABLE:
        filename = get_input_with_prompt("Enter filename (without extension)")
        tts.save_to_file(text, filename, format_type="mp3", service="google")
        input("Press Enter to continue...")


def main_menu():
    """Main menu for the enhanced TTS tool"""
    tts = EnhancedTTS()
    current_text = ""
    
    while True:
        clear_screen()
        print("\n======================================")
        print("     ENHANCED TEXT-TO-SPEECH TOOL     ")
        print("======================================")
        
        # Show current status
        print("\nCurrent Status:")
        if current_text:
            preview = current_text[:50] + "..." if len(current_text) > 50 else current_text
            print(f"Text: \"{preview}\"")
        else:
            print("Text: None")
        
        current_voice_name = "Default"
        for voice in tts.voices:
            if voice.id == tts.current_voice:
                current_voice_name = voice.name
                break
        
        print(f"Voice: {current_voice_name}")
        print(f"Rate: {tts.default_rate}")
        print(f"Volume: {tts.default_volume}")
        
        # Menu options
        print("\nOptions:")
        print("1. Enter/Load Text")
        print("2. Select Voice")
        print("3. Speak Current Text")
        print("4. Save to File (WAV/MP3)")
        print("5. Adjust Settings")
        print("6. Exit")
        
        choice = get_input_with_prompt("Select an option (1-6)")
        
        if choice == '1':
            result = text_input_menu()
            if result:
                current_text = result
                
        elif choice == '2':
            voice_selection_menu(tts)
            
        elif choice == '3':
            if current_text:
                print("\nSpeaking...")
                tts.speak(current_text)
            else:
                print("\nNo text to speak!")
                input("Press Enter to continue...")
                
        elif choice == '4':
            file_saving_menu(tts, current_text)
            
        elif choice == '5':
            clear_screen()
            print("\n===== ADJUST SETTINGS =====")
            try:
                new_rate = int(get_input_with_prompt("Enter speech rate (50-300, default 150)"))
                new_volume = float(get_input_with_prompt("Enter volume (0.0-1.0, default 1.0)"))
                
                # Validate and set new values
                if 50 <= new_rate <= 300:
                    tts.default_rate = new_rate
                else:
                    print("Invalid rate! Using default.")
                    
                if 0.0 <= new_volume <= 1.0:
                    tts.default_volume = new_volume
                else:
                    print("Invalid volume! Using default.")
                    
            except ValueError:
                print("Invalid input! Settings unchanged.")
                
            input("Press Enter to continue...")
            
        elif choice == '6':
            print("\nExiting program. Goodbye!")
            break
            
        else:
            print("\nInvalid choice. Please try again.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main_menu()