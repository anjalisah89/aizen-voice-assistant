import sys
import logging
import speech_recognition as sr
from dotenv import load_dotenv 
from assistant import Assistant # 

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """Main function to run the voice assistant."""
    # Load environment variables first
    load_dotenv()
    logging.info(".env file loaded.")

    # Initialize the Assistant core
    assistant = Assistant()

    if not assistant.is_ready:
         logging.error("Assistant failed to initialize properly. Exiting.")
         # Decide if you want to exit immediately or try running without some features
         sys.exit("Assistant initialization failed.")

    # Initial greeting
    assistant.speak("Initializing Aizen...")
    assistant.speak("Hey there, I am Aizen. How can I help you today?")

    # Initialize the speech recognizer
    recognizer = sr.Recognizer()
    active_mode = False 

    # wake_words = ["aizen", "hey aizen"] 
    # Activation phases
    all_activation_phrases = ["hello", "hey", "hi", "hii", "yo", "sup", "what's up", "heya", "hiya", "assistant", "hey aizen", "aizen", "listen", "listening", "help", "wake up", "activate", "start", "how are you", "are you there", "are you awake", "are you listening", "aizen are you there", "aizen are you awake", "aizen are you listening"]


    while True:
        try:
            with sr.Microphone() as source:
                # Adjust for ambient noise before listening
                recognizer.adjust_for_ambient_noise(source, duration=1) # Listen for 1 sec to calibrate noise

                if not active_mode:
                    print("Listening for activation phrase ('Hey Aizen', 'Aizen', etc.)...")
                else:
                    print("Listening for your command...")
                    # Add a shorter pause threshold when active for quicker response
                    recognizer.pause_threshold = 0.8
                    recognizer.energy_threshold = 4000 # Adjust based on environment noise
                    timeout = 8 # Listen for up to 8 seconds of non-speech
                    phrase_time_limit = 15 # Process phrases up to 15 seconds long
                
                try:
                    # Listen for audio
                    audio = recognizer.listen(source, timeout=timeout if active_mode else 5,
                                              phrase_time_limit=phrase_time_limit if active_mode else 10)
                    
                except sr.WaitTimeoutError:
                    # No speech detected within the timeout period
                    if active_mode:
                        print("No command detected, going back to sleep.")
                        active_mode = False 
                    continue # Go back to the start of the loop to listen again

                print("Recognizing...")
                
                # Recognize speech using Google Web Speech API
                try:
                     message = recognizer.recognize_google(audio).lower().strip()
                     print(f"You said: {message}")
                except sr.UnknownValueError:
                    if active_mode:
                         logging.warning("Speech Recognition could not understand audio.")
                    else:
                         # Don't log/speak if it's just background noise during passive listening
                         pass
                    continue # Continue the loop

                # Reset recognizer settings for the next listen cycle
                recognizer.pause_threshold = 0.8 
                recognizer.energy_threshold = 4000


                # --- Main Loop ---
                if not active_mode:
                    # Check if the recognized message contains any activation phrase
                    if any(phrase in message for phrase in all_activation_phrases):
                        assistant.speak("Yeah, I'm here!")
                        active_mode = True  # Activate the assistant
                    else:
                        # If not active and no wake word, ignore the input
                        print("Not in active mode, ignoring input.")
                        pass # Do nothing, go back to listening for wake word

                else:
                    # The Assistant class handles termination commands ('exit', 'stop', etc.)
                    assistant.process_input(message)

                    # Check if the assistant processed a termination command (sys.exit called internally)
                    # if re.search(r'\b(stop|exit|quit|bye|goodbye)\b', message):
                    #     active_mode = False # Deactivate mode after a termination command was likely processed

        except sr.RequestError as e:
             logging.error(f"Could not request results from Google Speech Recognition service; {e}")
             assistant.speak("Sorry, I'm having trouble connecting to the speech recognition service.")
             active_mode = False # Go back to passive mode 

        except Exception as e:
            logging.error(f"An unexpected error occurred in the main loop: {e}")
            assistant.speak("Sorry, an unexpected error occurred.")
            active_mode = False # Go back to passive mode


if __name__ == "__main__":
    main() # Call the main function to start 