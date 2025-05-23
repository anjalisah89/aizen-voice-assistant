import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv

class AIHandler:
    """Handles interaction with the Gemini AI model."""

    def __init__(self):
        load_dotenv() 
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            logging.error("Gemini API key not found. Please check your .env file.")
            self.model = None
            self.initialized = False
            return

        try:
            genai.configure(api_key=api_key)
            # Use a specific model name 
            self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
            logging.info("Gemini client initialized successfully.")
            self.initialized = True
        except Exception as e:
            logging.error(f"Failed to initialize Gemini client: {e}")
            self.model = None
            self.initialized = False

    def process_command(self, command: str) -> str:
        """Sends a command to the AI model and returns the response."""
        if not self.initialized or self.model is None:
            return "Sorry, the AI backend is not available due to an initialization error."

        try:
            logging.info(f"Sending command to Gemini: '{command}'")
            # The generate_content method returns a Response object
            response = self.model.generate_content(command)

            if response and response.text:
                logging.info(f"Received response from Gemini: '{response.text}'")
                return response.text
            else:
                 # Handle cases where response might be empty or blocked
                 logging.warning("Gemini response was empty or potentially blocked.")
                 print(response.prompt_feedback) 
                 return "I couldn't get a proper response from the AI. Maybe try rephrasing?"

        except Exception as e:
            logging.error(f"Gemini API error during content generation: {e}")
            return "Sorry, I encountered an error while trying to process that with the AI."

# For Testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    ai_handler = AIHandler()
    if ai_handler.initialized:
        print("AI initialized.")
        response = ai_handler.process_command("What is the capital of India?")
        print(f"AI Response: {response}")
    else:
        print("AI failed to initialize.")