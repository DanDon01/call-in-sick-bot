# Call-in-Sick Bot

AI-powered web application that helps generate a realistic "calling in sick" audio message. The app takes your excuse and transforms it to sound convincingly ill with coughs, sniffles, and a hoarse tone using ElevenLabs' text-to-speech API.

## Features

- Input your excuse by typing or voice recording
- Automatically adds realistic sick effects (coughs, sniffles, etc.) to your message
- Generates natural-sounding voice audio using ElevenLabs' Text-to-Speech
- Simple, intuitive web interface
- One-click download of your generated audio

## Getting Started

### Prerequisites

- Python 3.7 or higher
- ElevenLabs API key (get one from [ElevenLabs](https://elevenlabs.io))

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/call-in-sick-bot.git
   cd call-in-sick-bot
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   - Create a `.env` file in the project root
   - Add your ElevenLabs API key:
     ```
     ELEVENLABS_API_KEY=your_api_key_here
     ```

### ElevenLabs Model Context Protocol (MCP)

This application uses the ElevenLabs Model Context Protocol (MCP) to access ElevenLabs' Text-to-Speech capabilities. The MCP allows for more advanced interactions with the ElevenLabs API.

To ensure MCP works properly:

1. Make sure your ElevenLabs API key is set in the `.env` file
2. The application will automatically check if the MCP is installed
3. If you see a warning about MCP not being installed, run:
   ```
   pip install elevenlabs-mcp
   ```
4. Restart the application after installing

For more information about MCP, see the [ElevenLabs MCP documentation](https://github.com/elevenlabs/elevenlabs-mcp).

### Running the Application

1. Start the Flask development server:
   ```
   python app.py
   ```

2. Open your web browser and go to:
   ```
   http://localhost:5000
   ```

3. Use the application:
   - Type your excuse or record it using your microphone
   - Click "Generate Sick Call"
   - Listen to the generated audio and download if desired

## How It Works

1. The user provides an excuse message (text or voice)
2. The text is augmented with "sick effects" like coughs and sniffles
3. ElevenLabs TTS API generates realistic sick-sounding audio
4. The audio is played back to the user and available for download

## Project Structure

- `app.py` - Flask application (main entry point)
- `voice_generation.py` - Module for text augmentation and TTS generation
- `templates/` - HTML templates for the web interface
- `static/` - Static files (CSS, JavaScript, generated audio)

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **AI/ML**: ElevenLabs API for Text-to-Speech
- **Dependencies**: elevenlabs, python-dotenv

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [ElevenLabs](https://elevenlabs.io) for their incredible Text-to-Speech API
- [Cursor](https://cursor.sh) - The AI-powered code editor used to build this project
