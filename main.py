import speech_recognition as sr
import webbrowser
import pyttsx3

# Initialize recognizer
ttsx = pyttsx3.init()

def speak(text):
    ttsx.say(text)
    ttsx.runAndWait()

def processcommand(command):
    print (command)
    if "open" in command:
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
    
    else:
        speak("Sorry, I didn't understand that command.")     
    pass


if __name__ == "__main__":
    # Speak a greeting message
    speak("Initializing Aizen...")
    speak("Hey there, I am Aizen.")

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

            if "hello"or"hey"or"hi" in message:
                speak("how can I help you today?")
                with sr.Microphone() as source:
                    print("Listening for command...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio).lower()
                    processcommand(command)

        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except Exception as e:
            print(f"Could not request results; {e}")
