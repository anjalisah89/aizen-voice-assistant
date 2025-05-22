import webbrowser
import os
import sys
import shutil
import pyjokes
from datetime import datetime
import logging

class CommandHandler:
    """Handles processing specific, known voice commands."""

    def __init__(self, assistant_speaker, ai_processor):
        """
        Initializes the command handler with references to speaking and AI processing functions.
        :param assistant_speaker: A function that takes text and makes the assistant speak.
        :param ai_processor: A function that takes text and processes it using the AI model.
        """
        self.speak = assistant_speaker
        self.process_with_ai = ai_processor
        # Dictionary mapping keywords/patterns to handler methods
        self._commands = {
            'open': self._handle_open,
            'close': self._handle_close, # Windows specific currently
            'search for': self._handle_search, # More specific
            'search': self._handle_search,       # Less specific
            'play': self._handle_play,
            'weather in': self._handle_weather,  # Specific location
            'weather': self._handle_weather,     # General weather, will prompt for location
            'time': self._handle_time,
            "what time is it": self._handle_time,
            'date': self._handle_date,
            "today's date": self._handle_date,
            "what's the date": self._handle_date,
            'news': self._handle_news,
            'joke': self._handle_joke,
            "tell me a joke": self._handle_joke,
        }

    def process_command(self, command: str):
        """
        Processes the given command string.
        Checks for known commands first, then falls back to AI.
        """
        print(f"Processing command: {command}")
        command_lower = command.lower().strip()

        # This simple loop works for exact matches or simple contains checks
        handled = False
        for keyword, handler_func in self._commands.items():
            # Check if the keyword is in the command
            if keyword in command_lower:
                # Attempt to extract the argument after the keyword
                try:
                    # Split at the first occurrence of the keyword + space
                    parts = command_lower.split(keyword, 1)
                    argument = parts[1].strip() if len(parts) > 1 else '' 
                    handler_func(argument, command_lower) 
                    handled = True
                    break 
                except Exception as e:
                    logging.error(f"Error handling command '{command_lower}' with keyword '{keyword}': {e}")
                    self.speak(f"Sorry, I had trouble executing that command.")
                    handled = True
                    break 

        if not handled:
            # If no specific command was matched, use the AI fallback
            logging.info(f"No specific command handler found for '{command_lower}'. Using AI.")
            response = self.process_with_ai(command_lower) # Call AI handler
            self.speak(response)


    # --- Command Handler Methods ---

    def _handle_open(self, target: str):
        """Handles the 'open' command."""
        if not target:
            self.speak("What application or website would you like me to open?")
            return

        app_path = shutil.which(target) # Try finding as a system application

        if app_path:
            # Try to open as a system application
            try:
                # os.startfile is Windows specific
                if sys.platform == "win32":
                    os.startfile(app_path)
                    self.speak(f"Opening {target} application for you.")
            except Exception as e:
                 logging.error(f"Failed to open application {target}: {e}")
                 self.speak(f"Sorry, I encountered an error trying to open {target}.")
        else:
            # If not found as an app, try opening as a website
            if '.' in target and ' ' not in target: # e.g., google.com, youtube.com
                 url = f"https://{target}" 
                 try:
                     webbrowser.open(url)
                     self.speak(f"Opening {target} website for you.")
                 except Exception as e:
                     logging.error(f"Failed to open website {url}: {e}")
                     self.speak(f"Sorry, I had trouble opening the website {target}.")
            else: # Fallback to Google search
                 search_query = target.replace(" ", "+")
                 fallback_url = f"https://www.google.com/search?q={search_query}"
                 webbrowser.open(fallback_url)
                 self.speak(f"I couldn't find an app or direct website for '{target}'. Searching it on Google.")


    def _handle_close(self, target: str, full_command: str):
        """Handles the 'close' command (currently Windows specific)."""
        if not target:
            self.speak("Which application would you like me to close?")
            return

        if sys.platform == "win32":
            try:
                # Using taskkill command (Windows)
                result_exe = os.system(f"taskkill /f /im {target}.exe")
                if result_exe != 0: # If .exe didn't work, try without
                    result_no_exe = os.system(f"taskkill /f /im {target}")
                    final_result = result_no_exe
                else:
                    final_result = result_exe

                # os.system returns 0 for success on Windows taskkill
                if final_result == 0:
                    self.speak(f"Closing {target} application for you.")
                else:
                     # taskkill return codes can indicate why it failed
                     self.speak(f"Could not find or close the process '{target}'. It might not be running or the name is incorrect.")

            except Exception as e:
                logging.error(f"Error trying to close {target} using taskkill: {e}")
                self.speak(f"Sorry, I encountered an error trying to close {target}.")


    def _handle_search(self, query: str, full_command: str):
        """Handles the 'search' command."""
        # This handler is called for 'search for' and 'search'
        # The 'argument' will be the text *after* the matched keyword ('for ' or ' ')
        if not query:
            # If the original command was just "search", the argument is empty
            if full_command.strip() in ['search', 'search for']: 
                self.speak("What would you like me to search for?")
            else: # This case might happen if the parsing was imperfect but a keyword matched
                 logging.warning(f"Search handler called with empty query for command: {full_command}")
                 self.speak("What would you like me to search for?")
            return

        webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        self.speak(f"Searching for {query} on Google.")


    def _handle_play(self, song_query: str, full_command: str):
        """Handles the 'play' command (attempts Youtube)."""
        if not song_query:
            self.speak("What song or video would you like me to play?")
            return

        # Search for songs on youtube.
        Youtube_url = f"https://www.youtube.com/results?search_query={song_query.replace(' ', '+')}"

        try:
            webbrowser.open(Youtube_url)
            self.speak(f"Searching for {song_query} on YouTube.")
        except Exception as e:
            logging.error(f"Failed to open Youtube for '{song_query}': {e}")
            self.speak(f"Sorry, I had trouble searching for {song_query} on YouTube.")


    def _handle_weather(self, location: str, full_command: str):
        """Handles the 'weather' command."""
        # 'location' will be text after 'weather in ' or 'weather '
        if not location:
            # If the original command was just "weather", prompt for location
             if full_command.strip() == 'weather':
                self.speak("Which location's weather are you interested in? Like 'weather in London'.")
                return
             # If the original command was "weather in", and location is empty, something is wrong with parsing
             logging.warning(f"Weather handler called with empty location for command: {full_command}")
             self.speak("Please specify a location for the weather report.")
             return


        # Simple search for weather in location
        webbrowser.open(f"https://www.google.com/search?q=weather+{location.replace(' ', '+')}")
        self.speak(f"Fetching weather information for {location}.")


    def _handle_time(self):
        """Handles the 'time' command."""
        current_time = datetime.now().strftime("%I:%M %p")
        self.speak(f"The current time is {current_time}.")


    def _handle_date(self):
        """Handles the 'date' command."""
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        self.speak(f"Today's date is {current_date}.")


    def _handle_news(self):
        """Handles the 'news' command."""
        webbrowser.open("https://news.google.com")
        self.speak("Fetching the latest news for you on Google News.")


    def _handle_joke(self):
        """Handles the 'joke' command."""
        self.speak(pyjokes.get_joke())


# For testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def dummy_speak(text):
        print(f"Assistant Speak (Dummy): {text}")

    def dummy_ai_processor(command):
        print(f"AI Processing (Dummy): {command}")
        return f"Dummy AI response for: {command}"

    print("Testing CommandHandler...")
    cmd_handler = CommandHandler(dummy_speak, dummy_ai_processor)

    cmd_handler.process_command("open notepad")
    cmd_handler.process_command("search for cats")
    cmd_handler.process_command("play despacito") 
    cmd_handler.process_command("weather in Bengaluru")
    cmd_handler.process_command("what time is it")
    cmd_handler.process_command("tell me a joke")
    cmd_handler.process_command("tell me about the another name of universe in one word") 
    cmd_handler.process_command("search") 
    cmd_handler.process_command("weather in") 
    cmd_handler.process_command("close chrome") 