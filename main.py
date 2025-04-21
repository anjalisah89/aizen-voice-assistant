import speech_recognition as sr
import webbrowser
import pyttsx3
import pyjokes
import os
from openai import OpenAI
from dotenv import load_dotenv

api_key = os.getenv("OPENAI_API_KEY")
load_dotenv()  # load from .env file

# Initialize recognizer
ttsx = pyttsx3.init()

def speak(text):
    ttsx.say(text)
    ttsx.runAndWait()

def aiProcess(command):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Aizen that can perform various tasks like Alexa and Google Assistant."},
            {"role": "user", "content": command}
        ],
        max_tokens=100
    )
    return(response.choices[0].message.content)

def processcommand(command):
    print ("Command Received", command)

    if "stop" in command or "exit" in command:
        speak("Goodbye!")
        exit()
    
    elif "open" in command:
        # Extract the website name from the command 
        website = command.split("open")[-1].strip()
        # Open the website in the default web browser 
        webbrowser.open(f"https://{website}.com") 
        speak(f"Opening {website} for you.")

    elif "search" in command:
        # Extract the search query from the command
        query = command.split("search")[-1].strip()
        # Perform a Google search for the query 
        webbrowser.open(f"https://www.google.com/search?q={query}") 
        speak(f"Searching for {query} on Google.")

    elif "play" in command:
        # Extract the song name from the command
        song = command.split("play")[-1].strip()
        # Perform a Youtube search for the song
        webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
        speak(f"Playing {song} on Youtube.")
    
    elif "weather" in command:
        # Extract the location from the command
        location = command.split("weather")[-1].strip()
        # Perform a Foogle Search for the Weather
        webbrowser.open(f"https://www.google.com/search?q=weather+{location}")
        speak(f"Fetching weather information for {location}.")

    elif "time" in command:
        # Get the current time
        from datetime import datetime
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        speak(f"The current time is {current_time}.")

    elif "date" in command:
        # Get the current date
        from datetime import datetime
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        speak(f"Today's date is {current_date}.")
    
    elif "news" in command:
        # Perform a Google search for the news
        webbrowser.open("https://news.google.com")
        speak("Fetching the latest news for you.")

    elif "joke" in command:
        # Get a random joke
        speak(pyjokes.get_joke())

    elif command:
        try:
        # Process the command using OpenAI API
            response = aiProcess(command)
            speak(response)
        except Exception as e:
            print(f"Error: {e}")
            speak("Something went wrong, please try again.")
    
    else:
        speak("Sorry, I didn't understand that command.")     

if __name__ == "__main__":
    # Speak a greeting message
    speak("Initializing Aizen...")
    speak("Hey there, I am Aizen. How can I help you today?")

    #Listen for the wake up word "Hey Aizen"
    while True:
        r = sr.Recognizer()
        
        try:
            with sr.Microphone() as source:
                print("Listening for 'Hey Aizen'...")
                audio = r.listen(source)
            # Recognize speech using Google Web Speech API
            message = r.recognize_google(audio).lower()
            print(f"Message received: {message}")

            if any(greeting in message.lower() for greeting in ["hello", "hey", "hi", "yo", "sup", "what's up", "heya", "hiya", "hey assistant", "hey aizen"]):
                speak("Yeah, I am here.")
                with sr.Microphone() as source:
                    print("Aizen is active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio).lower()
                    processcommand(command)

        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except Exception as e:
            print(f"Could not request results; {e}")
