# Aizen Voice Assistant

Aizen is a Python-based voice assistant that listens for commands via your microphone, performs various tasks, and provides spoken responses using text-to-speech. It uses the Google Gemini API to handle unrecognized commands or general queries.

## Features

- **Voice Activation:** Uses wake words (e.g., "Hey Aizen", "Aizen") to start listening for commands.
- **Open Applications & Websites:** Opens installed applications (via system PATH) or specified websites (e.g., "open notepad", "open google.com").
- **Close Applications:** Attempts to close running applications using `taskkill` (Windows only).
- **Web Search:** Performs Google searches (e.g., "search for python tutorials").
- **Youtube:** Opens Youtube results for specified queries (e.g., "play relaxing music").
- **Weather Information:** Fetches weather details for a location via Google search (e.g., "weather in India").
- **Time & Date:** Reports the current time and date.
- **News Headlines:** Opens Google News for the latest headlines.
- **Jokes:** Tells programming jokes using the `pyjokes` library.
- **AI Integration:** Leverages Google Gemini API (`gemini-1.5-flash-latest`) to understand and respond to commands not explicitly programmed.
- **Text-to-Speech:** Provides audible responses to commands and queries.

## Prerequisites

- Python 3.x
- `pip` (Python package installer)
- Git (for cloning the repository)
- A working microphone connected and configured on your system.
- **(Potentially)** System libraries for audio I/O, such as PortAudio (often required by PyAudio). If `pip install PyAudio` fails, search for instructions specific to your OS (Windows/macOS/Linux).

## Setup Instructions

1.  **Clone or Fork the Repository:**

    - Fork this repository on GitHub and clone your fork, OR
    - Clone this repository directly:
      ```bash
      git clone https://github.com/anjalisah89/aizen-voice-assistant.git
      cd aizen-voice-assistant
      ```

2.  **Create and Activate a Virtual Environment:**

    - It's highly recommended to use a virtual environment to manage dependencies.

    - **Windows (PowerShell):**
      ```powershell
      python -m venv .venv
      .\.venv\Scripts\Activate.ps1
      ```
    - **Windows (Command Prompt):**
      ```cmd
      python -m venv .venv
      .\.venv\Scripts\activate.bat
      ```
    - **Linux / macOS (Bash/Zsh):**

      ```bash
      python3 -m venv .venv
      source .venv/bin/activate
      ```

    - **Confirm Activation:** Your terminal prompt should now be prefixed with `(.venv)`, like this:
      ```
      (.venv) PS C:\Users\YourUser\Path\To\Project>
      ```

3.  **Install Dependencies:**

    - Ensure you have a `requirements.txt` file (as shown above) in your project directory.
    - Install the required packages:
      ```bash
      pip install -r requirements.txt
      ```

4.  **Set Up Google Gemini API Key:**
    - Generate a Google Gemini API key. Follow the official instructions: [Google AI Setup Guide](https://ai.google.dev/tutorials/setup)
    - Create a file named `.env` in the root directory of the project.
    - Add your API key to the `.env` file like this:
      ```env
      GEMINI_API_KEY=YOUR_ACTUAL_API_KEY
      ```
    - Replace `YOUR_ACTUAL_API_KEY` with your real key.
    - **Important:** Add `.env` to your `.gitignore` file to avoid accidentally committing your secret key.

## Usage

1.  **Run the Assistant:**

    - Make sure your virtual environment is activated.
    - Navigate to the project directory in your terminal.
    - Run the Python script (assuming your file is named `main.py`, rename if necessary):
      ```bash
      python main.py
      ```
    - You'll be greeted with:
      ```
      Aizen: Initializing Aizen...
      Aizen: Hey there, I am Aizen. How can I help you today?
      ```

2.  **Interact with Aizen:**
    - The script will initialize ("Initializing Aizen...").
    - It will then listen for a wake word ("Listening for wake word...").
    - Say one of the wake words (e.g., "Hey Aizen", "Aizen").
    - Aizen will respond ("Yeah, I'm here!") and start listening for your command ("Listening for your command...").
    - State your command clearly (e.g., "What time is it?", "Open Firefox", "Tell me a joke", "Search for Python tutorials", "Play music", "Weather in Delhi", "Any other Commands").
    - Aizen will process the command and respond. After processing, it will go back to listening for the wake word.
    - To stop the assistant, say "stop", "exit", or "goodbye".

## Platform Notes

- The **"close application"** feature uses the `taskkill` command and is **only functional on Windows**.
- Application opening (`os.startfile`) behavior might differ slightly across operating systems.
- Microphone access and TTS engine performance can vary depending on your OS and hardware setup.
