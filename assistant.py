import pyttsx3
import logging
from ai_handler import AIHandler
from command_handler import CommandHandler
import sys 
import re 

class Assistant:
    """The core Assistant class, managing TTS, AI, and command handling."""

    def __init__(self):
        """Initializes the assistant components."""
        logging.info("Initializing Assistant components...")

        # Initialize TTS engine
        try:
            self.tts_engine = pyttsx3.init()
            logging.info("TTS engine initialized.")
        except Exception as e:
            logging.error(f"Failed to initialize TTS engine: {e}")
            self.tts_engine = None 

        # Initialize AI Handler
        self.ai_handler = AIHandler()
        if not self.ai_handler.initialized:
            logging.warning("AI Handler failed to initialize. AI features will be disabled.")

        # Initialize Command Handler, passing necessary dependencies
        self.command_handler = CommandHandler(self.speak, self.ai_handler.process_command)
        logging.info("Command Handler initialized.")

        # Check if core components are ready
        self.is_ready = self.tts_engine is not None 


    def speak(self, text: str):
        """Uses the TTS engine to speak the given text."""
        if self.tts_engine is not None:
            print("Aizen:", text) 
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        else:
            print("Aizen (TTS Failed):", text) 


    def process_input(self, command: str):
        """
        Processes recognized voice input.
        This method is called by the main loop in main.py
        It checks for termination commands and delegates others to the CommandHandler.
        """
        command_lower = command.lower().strip()
        print(f"Input received by Assistant: {command_lower}")

        # Check for termination commands
        if re.search(r'\b(stop|exit|quit|bye|goodbye)\b', command_lower):
             self.speak("Goodbye! Have a great day!")
             logging.info("Termination command received. Exiting.")
             sys.exit() # Exit the application

        # This command handler will decide whether to use a specific handler or the AI
        self.command_handler.process_command(command_lower)

# For Testing
if __name__ == "__main__":
     logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
     print("Testing Assistant class...")
     assistant = Assistant()
     if assistant.is_ready:
         assistant.speak("Assistant initialized and ready.")
         assistant.process_input("what time is it")
         assistant.process_input("tell me a joke") 
         assistant.process_input("exit") 