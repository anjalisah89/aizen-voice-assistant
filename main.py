import os
import re
import sys
import shutil
import logging
import webbrowser
import pyttsx3
import pyjokes
import speech_recognition as sr
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai 

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found. Please check your .env file or environment variables.")

try:
    # Configure the client library
    genai.configure(api_key=api_key)

    # Create the model instance
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    logging.info("Gemini client initialized successfully.")
    gemini_initialized = True
except Exception as e:
    logging.error(f"Failed to initialize Gemini client: {e}")
    # Set model to None to indicate failure
    # This will prevent any further calls to the model until re-initialized
    model = None
    gemini_initialized = False

# Initialize TTS engine
tts = pyttsx3.init()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Speak helper
def speak(text):
    print("Aizen:", text)
    tts.say(text)
    tts.runAndWait()

# Use Gemini to process unknown commands
def process_with_ai(command):
    if not gemini_initialized or model is None:
         return "Sorry, the AI backend is not available due to an initialization error."
    try:
        # Send the command to the Gemini model
        logging.info(f"Sending command to Gemini: '{command}'")
        response = model.generate_content(command)

        # Extract the text response.
        if response.text:
             logging.info(f"Received response from Gemini: '{response.text}'")
             return response.text
        else:
             # Handle empty or blocked responses
             logging.warning("Gemini response was empty or potentially blocked.")
             print(response.prompt_feedback)
             return "I couldn't get a proper response from the AI. Maybe try rephrasing?"

    except Exception as e:
        logging.error(f"Gemini API error: {e}")
        return "Sorry, I encountered an error while trying to process that with the AI."

# Handle the commands
def process_command(command):
    print(f"Command received: {command}")
    command = command.lower().strip() # Normalize command

    wake_words = ["hello", "hey", "hi", "hii", "yo", "sup", "what's up", "heya", "hiya", "assistant", "hey aizen", "aizen", "listen", "listening", "help", "wake up", "activate", "start", "how are you", "are you there", "are you awake", "are you listening", "aizen are you there", "aizen are you awake", "aizen are you listening"]

    #Terminate Aizen
    if re.search(r'\b(stop|exit|quit|bye|goodbye)\b', command): 
        speak("Goodbye! Have a great day!")
        logging.info("Terminating Aizen.")
        sys.exit()

    elif command in wake_words:
        speak("Hi there! How can I assist you?")
        return True 

    # Open Application or Website
    elif command.startswith('open '):
        target = command.split('open ', 1)[1].strip()
        app_path = shutil.which(target) 

        if app_path:
             # Try to open as a system application
            try:
                os.startfile(app_path) 
                speak(f"Opening {target} application for you.")
            except Exception as e:
                logging.error(f"Failed to open application {target}: {e}")
                speak(f"Sorry, I encountered an error trying to open {target}.")
        else:
            if not '.' in target and ' ' not in target: 
                url = f"https://{target}.com"
                webbrowser.open(url)
                speak(f"Opening {target} website for you.")
            else: # Fallback to Google search
                search_query = target.replace(" ", "+")
                fallback_url = f"https://www.google.com/search?q={search_query}"
                webbrowser.open(fallback_url)
                speak(f"I couldn't find an app or website for '{target}'. Searching it on Google.")

    # Close Application (Windows specific)
    elif command.startswith('close '):
        target = command.split('close ', 1)[1].strip()
        # Adding .exe is often needed for taskkill, but might not always be right.
        if sys.platform == "win32": 
            try:
                # Try closing common variations
                result1 = os.system(f"taskkill /f /im {target}.exe")
                result2 = os.system(f"taskkill /f /im {target}") if result1 != 0 else 0 

                if result1 == 0 or result2 == 0:
                    speak(f"Closing {target} application for you.")
                else:
                     speak(f"Could not find or close the process '{target}'. It might not be running or the name is incorrect.")
            except Exception as e:
                logging.error(f"Error trying to close {target}: {e}")
                speak(f"Sorry, I encountered an error trying to close {target}.")
       
    # Search Web
    elif command.startswith('search for ') or command.startswith('search '):
        query = command.split('search for ', 1)[-1].split('search ', 1)[-1].strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
            speak(f"Searching for {query} on Google.")
        else:
            speak("What would you like me to search for?")

    # Play on YouTube (basic search link)
    elif command.startswith('play '):
        song = command.split('play ', 1)[1].strip()
        if song:
            # Using Youtube URL directly 
            webbrowser.open(f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}")
            speak(f"Searching for {song} on YouTube.")
        else:
            speak("What song would you like me to play?")

    # Get Weather
    elif 'weather in' in command:
        location = command.split('weather in', 1)[1].strip()
        if location:
            webbrowser.open(f"https://www.google.com/search?q=weather+{location.replace(' ', '+')}")
            speak(f"Fetching weather information for {location}.")
        else:
            speak("Which location's weather are you interested in?")
    elif 'weather' in command: 
         speak("Please specify a location for the weather report, like 'weather in London'.")

    # Get Time
    elif "what time is it" in command or command == "time":
        current_time = datetime.now().strftime("%I:%M %p") 
        speak(f"The current time is {current_time}.")

    # Get Date
    elif "what's the date" in command or "today's date" in command or command == "date":
        current_date = datetime.now().strftime("%A, %B %d, %Y") 
        speak(f"Today's date is {current_date}.")

    # Get News
    elif "news" in command:
        webbrowser.open("https://news.google.com")
        speak("Fetching the latest news for you on Google News.")

    # Tell a Joke
    elif "joke" in command or "tell me a joke" in command:
        speak(pyjokes.get_joke())

    # Fallback to Gemini AI
    elif all(phrase not in command for phrase in ["open", "search", "play", "weather", "time", "date", "news", "joke"]):
        # If the command is not recognized, use GeminiAI to process it
        response = process_with_ai(command)
        speak(response)

    else:
        speak("Sorry, I didn't understand that command.")

if __name__ == "__main__":
    # Initialize the speech recognizer
    if not gemini_initialized:
        speak("Warning: AI features are disabled due to an initialization error. Please check the logs and API key.")
    speak("Initializing Aizen...")
    speak("Hey there, I am Aizen. How can I help you today?")

    recognizer = sr.Recognizer()
    active_mode = False

    while True:
        try:
            with sr.Microphone() as source:

                if not active_mode:
                    print("Listening for wake word ('Aizen', 'Hey Aizen', etc.)...")
                else:
                    print("Listening for your command...")

                try:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                except sr.WaitTimeoutError:
                    # No speech detected within the timeout period
                    if active_mode:
                        print("No command detected, going back to sleep.")
                        active_mode = False
                    continue # Go back to the start of the loop

                print("Recognizing...")
                # Recognize speech using Google Web Speech API
                message = recognizer.recognize_google(audio).lower().strip()
                print(f"You said: {message}")

                if not active_mode:
                    # Check if the recognized message contains any wake word
                    wake_words_check = ["hello", "hey", "hi", "hii", "yo", "sup", "what's up", "heya", "hiya", "assistant", "hey aizen", "aizen", "listen", "listening", "help", "wake up", "activate", "start", "how are you", "are you there", "are you awake", "are you listening", "aizen are you there", "aizen are you awake", "aizen are you listening"]
                    if any(word in message for word in wake_words_check):
                        speak("Yeah, I'm here!")
                        active_mode = True  # Activate the assistant
                    
                else:
                    process_command(message)
                    if re.search(r'\b(stop|exit|bye|goodbye)\b', message):
                        active_mode = False  # Deactivate mode after "stop" or "exit"

        except sr.UnknownValueError:
            if active_mode: 
                logging.warning("Speech Recognition could not understand audio.")
                # speak("Sorry, I didn't catch that.") 
            else:
                # Don't report if just listening for wake word and heard nothing understandable
                pass

        except sr.RequestError as e:
             logging.error(f"Could not request results from Google Speech Recognition service; {e}")
             speak("Sorry, I'm having trouble connecting to the speech recognition service.")
             active_mode = False # Deactivate on connection error

        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            speak("Sorry, an unexpected error occurred.")
            active_mode = False # Deactivate on unexpected error
