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
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OpenAI API key not found. Please check your .env file.")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Initialize TTS engine
tts = pyttsx3.init()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Speak helper
def speak(text):
    print("Aizen:", text)
    tts.say(text)
    tts.runAndWait()

# Use OpenAI to process unknown commands
def process_with_ai(command):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Aizen that can perform various tasks like Alexa and Google Assistant."},
                {"role": "user", "content": command}
            ],
            max_tokens=100
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"OpenAI error: {e}")
        return "Sorry, something went wrong while processing your request."

# Handle the commands
def process_command(command):
    print(f"Command received: {command}")
    wake_words = ["hello", "hey", "hi", "hii", "yo", "sup", "what's up", "heya", "hiya", "assistant", "hey aizen", "aizen", "listen", "listening", "help", "wake up", "activate", "start", "how are you", "are you there", "are you awake", "are you listening", "aizen are you there", "aizen are you awake", "aizen are you listening"]

    #Terminate Aizen
    if re.search(r'\b(stop|exit|quit|bye)\b', command):
        speak("Goodbye! Have a great day!")
        logging.info("Terminating Aizen.")
        sys.exit()
        
    elif command.strip() in wake_words:
        speak("Hi there! What can I do for you?")
        return

    elif match := re.search(r'open\s+(.+)', command):
        app_or_site = match.group(1).strip().lower()

        # Try to open as a system application
        if shutil.which(app_or_site):            
            os.startfile(app_or_site)
            speak(f"Opening {app_or_site} application for you.")
                
        else:
            words = app_or_site.split()
            if len(words) == 1:
                # Try to open as a website
                site_name = app_or_site.replace(" ", "")
                url = f"https://{site_name}.com"
                webbrowser.open(url)
                speak(f"{app_or_site} application not found. Opening {site_name}.com instead.")
            else:
                # Fallback: search on Google
                search_query = app_or_site.replace(" ", "+")
                fallback_url = f"https://www.google.com/search?q={search_query}"
                webbrowser.open(fallback_url)
                speak(f"I couldn't find an app for {app_or_site}. Searching it on Google.")
                
    elif match := re.search(r'close\s+(.+)', command):
        app_or_site = match.group(1).strip().lower()
        
        # Try to close as a system application
        if shutil.which(app_or_site):
            os.system(f"taskkill /f /im {app_or_site}.exe")
            speak(f"Closing {app_or_site} application for you.")
        else:
            # Closing a website is not straightforward, but we can suggest to the user
            speak(f"I couldn't find an app for {app_or_site}.")
            speak(f"If it's a website, sorry, I can't close it directly. You can close it manually or use a browser extensions.")

    elif match := re.search(r'search\s+(.+)', command):
        query = match.group(1)
        # Perform a Google search for the query
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"Searching for {query} on Google.")

    elif match := re.search(r'play\s+(.+)', command):
        song = match.group(1)
        # Open YouTube and search for the song
        webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
        speak(f"Playing {song} on YouTube.")

    elif match := re.search(r'weather\s+in\s+(.+)', command):
        location = match.group(1)
        # Open Google search for the weather in the specified location
        webbrowser.open(f"https://www.google.com/search?q=weather+{location}")
        speak(f"Fetching weather information for {location}.")

    elif "time" in command:
        # Get the current time
        current_time = datetime.now().strftime("%H:%M")
        speak(f"The current time is {current_time}.")

    elif "date" in command:
        # Get the current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        speak(f"Today's date is {current_date}.")

    elif "news" in command:
        # Open Google News
        webbrowser.open("https://news.google.com")
        speak("Fetching the latest news for you.")

    elif "joke" in command:
        # Tell a random joke
        speak(pyjokes.get_joke())

    elif all(phrase not in command for phrase in ["open", "search", "play", "weather", "time", "date", "news", "joke"]):
        # If the command is not recognized, use OpenAI to process it
        response = process_with_ai(command)
        speak(response)

    else:
        speak("Sorry, I didn't understand that command.")

if __name__ == "__main__":
    # Initialize the speech recognizer
    speak("Initializing Aizen...")
    speak("Hey there, I am Aizen. How can I help you today?")

    recognizer = sr.Recognizer()
    active_mode = False  # Track whether Aizen is actively listening for commands

    while True:
        try:
            with sr.Microphone() as source:
                if not active_mode:
                    print("Listening for \"Hey Aizen\"...")
                else:
                    print("Listening for your command...")

                audio = recognizer.listen(source)
                # Recognize speech using Google Web Speech API
                print("Recognizing...")
                message = recognizer.recognize_google(audio).lower()
                print(f"You said: {message}")
                
                if not active_mode:
                  wake_words = ["hello", "hey", "hi", "hii", "yo", "sup", "what's up", "heya", "hiya", "assistant", "hey aizen", "aizen", "listen", "listening", "help", "wake up", "activate", "start", "how are you", "are you there", "are you awake", "are you listening", "aizen are you there", "aizen are you awake", "aizen are you listening"]
                  if any(word in message for word in wake_words):
                       speak("Yeah, I am here.")
                       active_mode = True  # Activate command mode
                else:
                    process_command(message)
                    if re.search(r'\b(stop|exit|bye)\b', message):
                        active_mode = False  # Deactivate mode after "stop" or "exit"

        except sr.UnknownValueError:
            logging.warning("Speech Recognition could not understand audio.")
        except Exception as e:
            logging.error(f"Error: {e}")

