# Call-in-Sick Bot Masterplan

## Project Overview

The Call-in-Sick Bot is a voice-activated AI web application that helps a user generate a realistic "calling in sick" audio message. The user will speak their sick-day excuse, and the app will respond with a generated audio message that sounds convincingly ill (including coughs, sniffles, and a hoarse tone).

This is achieved by transcribing the user's speech to text and then using ElevenLabs' Model Context Protocol (MCP) (specifically, ElevenLabs' advanced text-to-speech API) to produce a lifelike voice output with the desired sickly effects.

### Key Features and Flow

1. The user records a voice message (their spoken excuse) through the app.
2. The app uses speech-to-text (STT) (powered by Whisper) to transcribe the audio into text.
3. The transcribed text is augmented with "sick" effects in text form (e.g. adding "cough ... sniff" cues).
4. ElevenLabs' text-to-speech (TTS) API (MCP) generates an audio clip from the augmented text, using a natural voice that sounds congested or hoarse.
5. The resulting audio message is played back to the user (which they could use as an excuse recording).

This masterplan outlines the project structure, required tools, and step-by-step implementation guidance. It is written for an AI coding agent (Claude 3.5 in GitHub Copilot Agent via VS Code) to follow and build the project from an empty repository. Each part of the implementation is explained with clarity, emphasizing correct usage of ElevenLabs MCP and good development practices.

## Tech Stack and Tools

### Programming Language & Platform

- **Python 3.x** – Main language for backend logic.
- **Flask** – Python web framework to create a local web server (serves a webpage and API endpoints).

### AI/ML Components

#### Whisper (OpenAI)
Used for Speech-to-Text (STT) transcription of the user's spoken input. We will use the open-source Whisper model (preferably a smaller model for local use) to avoid external API calls for transcription.

#### ElevenLabs API (Model Context Protocol)
Used for Text-to-Speech (TTS) generation. The ElevenLabs MCP will be accessed via their API/SDK to convert text into a realistic voice audio. We will ensure the workflow aligns with ElevenLabs' recommended usage:

- Using an ElevenLabs API key for authentication.
- Selecting an appropriate voice (pre-existing voice or a custom clone if available).
- Using the correct model (e.g. eleven_multilingual_v2 for expressive speech) and settings for natural output.
- Generating audio and handling the binary audio output (MP3/WAV).

> **Note:** ElevenLabs also supports voice cloning and other audio tools via MCP, but for this project we primarily use text-to-speech.

### Frontend

- **HTML5 + JavaScript** – for a simple web page that lets the user record their voice and listen to the result.
  - Will utilize browser APIs for audio recording (e.g. MediaRecorder via getUserMedia).
  - HTML `<audio>` element for playback.
- **Bootstrap CSS** (optional) – for basic styling (not required, but could use for quick UI styling if needed).

### Additional Libraries and Tools

- **Python elevenlabs SDK** – Official ElevenLabs Python package to simplify API calls.
  ```bash
  pip install elevenlabs
  ```
  Provides convenient functions like `generate()` for TTS and handles API endpoints internally.

- **Python whisper or openai-whisper** – Whisper ASR library.
  ```bash
  pip install openai-whisper
  ```
  This may also require installing ffmpeg for audio processing.

- **Python pyaudio** (optional) – Not strictly needed if using browser recording.
  ```bash
  pip install pyaudio  # Optional
  ```
  - Used if capturing microphone audio via Python is needed.
  - Browser handles recording in our implementation.
  - The ElevenLabs SDK mentions a pyaudio extra for audio I/O if needed.

- **python-dotenv** – For loading environment variables from a .env file.
  ```bash
  pip install python-dotenv
  ```

- **Requests/HTTP Clients** – Only needed if not using the SDK.
  ```bash
  pip install requests  # Not needed if using elevenlabs SDK
  ```

- **Git** – for version control, following GitHub best practices (frequent commits, .gitignore usage, etc.).

## Project Structure

We will organize the repository for clarity and maintainability:

```
call-in-sick-bot/
├── app.py                  # Flask application (entry point)
├── requirements.txt        # Python dependencies
├── .env.example            # Example environment variables file (for API keys, etc.)
├── .gitignore              # Git ignore file (to exclude .env, __pycache__, etc.)
├── static/
│   ├── script.js           # Frontend JS for audio recording and handling
│   └── style.css           # (Optional) CSS for styling the page
├── templates/
│   └── index.html          # HTML template for the main interface
├── speech_recognition.py   # Module: handles audio transcription with Whisper
├── voice_generation.py     # Module: handles text augmentation and TTS generation with ElevenLabs
└── (maybe tests/ or sample_audio/ for future tests or assets if needed)
```

### Notes on Structure

- The Flask app (`app.py`) will tie everything together: it will provide routes for the frontend page and an API endpoint to receive audio and return the generated sick-voice audio.
- The logic is separated into two helper modules:
  - `speech_recognition.py` – contains functions to load the Whisper model and transcribe audio input.
  - `voice_generation.py` – contains functions to prepare the text (insert coughs/sniffs) and to call ElevenLabs API to get the speech audio.
- **Static files:** `index.html` will be served to the user. It will include `script.js` for recording functionality. The recorded audio will likely be sent to the backend as a blob (e.g. via a form upload or AJAX).
- **Configuration:** `.env` (not committed to repo) will store sensitive keys like `ELEVENLABS_API_KEY`. The `.env.example` will document what variables are needed without the actual values.
- **Dependencies:** `requirements.txt` will include Flask, elevenlabs, openai-whisper, python-dotenv, etc., to allow easy installation.

### GitHub Best Practices

- Use a `.gitignore` to exclude environment files and other unnecessary files (like compiled Python files, potential audio outputs, etc.).
- Keep secrets out of code (use environment variables).
- Write clear commit messages at each step, and possibly include a `README.md` (which could be adapted from this plan) to explain usage.

## Step-by-Step Implementation Plan

We will proceed in incremental steps, verifying functionality at each stage:

### Step 1: Repository Setup and Initial Configuration

#### Tasks

1. Initialize a new git repository (if not already done) and create the basic directory structure.
2. Create a `requirements.txt` with initial dependencies:
   - List at least: Flask, elevenlabs, openai-whisper (or whisper), python-dotenv. (We will update this as needed.)
3. Create a `.gitignore`:
   - Include typical Python ignores (`__pycache__/`, `*.pyc`, etc.).
   - Include `.env` to prevent committing secrets.
   - Include any output files (like `static/output.mp3` if we plan to generate output audio files) so they don’t clutter the repo.
4. Create a `.env.example` file:
   - Document required environment variables, e.g.:
     ```
     ELEVENLABS_API_KEY=<your ElevenLabs API key here>
     # (Add others if any, like VOICE_ID or MODEL_ID if we let those be configurable)
     ```
     We won’t include the actual key here, just a placeholder and instructions.
5. Create an empty Flask app in `app.py` with a basic structure:
   ```python
   from flask import Flask

   app = Flask(__name__)

   # Basic test route
   @app.route("/hello")
   def hello():
       return "Call-in-Sick Bot server is running."

   if __name__ == "__main__":
       app.run(debug=True)
   ```
   This is just to ensure the server can start. Use `debug=True` for easier local development (auto-reload).

#### Testing Step 1

Start the Flask server:
- Run `pip install -r requirements.txt` to install Flask.
- Run `python app.py` and navigate to `http://localhost:5000/hello` to see the test message. This confirms the environment is set up correctly.

**Commit:** “Initial project structure and Flask setup.”

### Step 2: Environment Variables and API Key Configuration

#### Tasks

Before implementing functionality, set up configuration handling:
1. Install `python-dotenv` (should be in requirements already). In `app.py`, load environment variables at startup:
   ```python
   from dotenv import load_dotenv
   import os

   load_dotenv()  # this will read .env file and load variables
   ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
   ```
   Ensure that the `ELEVENLABS_API_KEY` is accessed in our code through this variable (or passed to the ElevenLabs SDK). Do not hard-code the API key.
2. Create a placeholder for the ElevenLabs voice we will use. For example, in `voice_generation.py` we might define:
   ```python
   DEFAULT_VOICE = "Bella"  # Example voice name; can be changed to any available voice or voice ID
   ELEVEN_MODEL = "eleven_multilingual_v2"  # The TTS model to use for generation
   ```
   We will use these in the TTS function later.
3. (Optional) If we anticipate running the app in different environments, ensure that the Flask app reads configuration from env as needed (for example, a secret key for Flask if needed, or debug mode).

#### Testing Step 2

No direct testing needed for this step aside from ensuring no errors on startup. If `ELEVENLABS_API_KEY` is not set yet, that's fine; we just want to ensure our code can load it when present.

**Commit:** “Add environment variable support and load API key from .env.”

### Step 3: Implement Speech-to-Text Module (Whisper)

#### Tasks

Now, implement the module to handle audio transcription using Whisper.

1. Install Whisper. (Ensure `openai-whisper` is in `requirements.txt`. If the package name is different or if it requires PyTorch, ensure those get installed. The `openai-whisper` package will bring in `torch` as a dependency.)
2. In `speech_recognition.py`, implement the following:
   - Load the Whisper model (ideally once, to reuse for multiple transcriptions). For local development, we can use a smaller model to balance speed and accuracy. Whisper has models like `tiny`, `base`, `small`, `medium`, `large`. We will use "small" by default for reasonably good accuracy.
     ```python
     import whisper

     # Load model globally on module import (so it loads at server startup)
     model_name = os.getenv("WHISPER_MODEL", "small")
     STT_MODEL = whisper.load_model(model_name)
     ```
     This loads the model (which might take a few seconds). We allow an optional env var `WHISPER_MODEL` to override model size if needed.
   - Write a function `transcribe_audio(file_path: str) -> str` that takes a path to an audio file and returns the transcribed text:
     ```python
     def transcribe_audio(file_path: str) -> str:
         """
         Transcribe the audio at file_path to text using Whisper.
         Returns the recognized text.
         """
         # Use the loaded model to transcribe
         result = STT_MODEL.transcribe(file_path)
         text = result.get("text", "").strip()
         return text
     ```
     Whisper’s `transcribe` will handle audio loading (requires ffmpeg for formats other than WAV). We strip the text to clean up whitespace.

#### Testing STT

We should test this function with a sample audio file. Since this is a local project, you (the developer) can provide a short WAV or MP3 of someone saying a simple phrase (e.g. "I'm feeling very sick today").

Place a sample audio file in the project (not necessarily committed) or record one through the microphone.

Temporarily, you can create a small script or use the Python shell:
```python
from speech_recognition import transcribe_audio
text = transcribe_audio("path/to/sample_sick_excuse.wav")
print("Transcribed text:", text)
```

Run this test to ensure Whisper model is working and the output text is sensible.

**Commit:** “Add Whisper speech_recognition module with transcribe_audio function.”

### Step 4: Text Augmentation for "Sick" Effects

#### Tasks

After we get the raw transcribed text of what the user said, we want to augment or modify it to include cues that will make the synthesized voice sound ill (coughs, sniffles, etc.). We will implement this in the `voice_generation.py` module as a helper function.

1. In `voice_generation.py`, create a function `augment_text_with_sickness(text: str) -> str` that inserts some cough/sniff onomatopoeic cues into the text. This will be a simple heuristic-based implementation:
   - For example, we can prepend a cough at the beginning and append a sniffle at the end of the sentence.
   - Also, if the text is long or has multiple sentences, we might insert a cough in between or after a pause.
   - We should ensure we don't add too many to overdo it.

#### Example Approach

```python
import random

def augment_text_with_sickness(text: str) -> str:
    # Trim whitespace
    text = text.strip()
    if not text:
        return text  # nothing to augment

    sick_text = text

    # Prefix a cough at the start
    sick_text = "*cough* " + sick_text

    # Optionally insert a sniffle or cough in the middle for longer text
    # e.g., after a comma or between clauses
    if len(sick_text.split()) > 7:
        # insert a sniff somewhere in the middle
        words = sick_text.split()
        mid = len(words)//2
        words.insert(mid, "*sniff*")
        sick_text = " ".join(words)

    # Suffix a cough or sniff at the end
    if not sick_text.endswith("*cough*") and not sick_text.endswith("*sniff*"):
        sick_text = sick_text + " *cough*"

    return sick_text
```

The above is a simple logic: always start with a cough, maybe insert a sniff in the middle if the sentence is long enough, and end with a cough. This ensures at least a couple of "sick sounds" in the speech.

#### Testing Text Augmentation

Write some test cases for `augment_text_with_sickness`:
```python
print(augment_text_with_sickness("I have a fever and a sore throat."))
# Expected output might be: "*cough* I have a fever and a *sniff* sore throat. *cough*"
print(augment_text_with_sickness("I'm not feeling well today"))
# "*cough* I'm not feeling well today *cough*"
```

Ensure the function handles empty string and doesn’t produce weird spacing. We can refine the strategy based on output.

**Commit:** “Add text augmentation for sick effects (coughs/sniffs) in voice_generation module.”

### Step 5: Text-to-Speech Generation with ElevenLabs (MCP)

#### Tasks

With the text prepared, the core of the project is to convert this augmented text into spoken audio using ElevenLabs. We will use the ElevenLabs API via their Python SDK to do this. This step is crucial to do correctly in line with ElevenLabs MCP usage guidelines.

1. In `voice_generation.py`, implement the function to call ElevenLabs:
   ```python
   import elevenlabs

   # Ensure API key is set for ElevenLabs SDK (from environment)
   ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
   if ELEVENLABS_API_KEY:
       elevenlabs.set_api_key(ELEVENLABS_API_KEY)
   else:
       # It's okay if this is not set yet; but the TTS function will require it
       print("Warning: ELEVENLABS_API_KEY not set. Voice generation will not work without an API key.")
   ```

We set the API key at import time so that the `elevenlabs` library knows our credentials.

Now create a function `generate_sick_voice_audio(text: str, voice: str = DEFAULT_VOICE) -> str` which:
- Calls `augment_text_with_sickness` on the input text to get the "sick" version.
- Calls ElevenLabs TTS to generate audio from the sick text.
- Saves the audio to a file and returns the filename (or returns the binary data, to be decided).

#### Example Implementation

```python
def generate_sick_voice_audio(text: str, voice: str = DEFAULT_VOICE) -> str:
    """
    Generate an audio file for the given text with a sick voice effect.
    Returns the filepath of the saved audio.
    """
    if not text or text.isspace():
        raise ValueError("No text provided for TTS")

    # 1. Augment text with sick effects
    sick_text = augment_text_with_sickness(text)
    
    # 2. Use ElevenLabs to generate audio
    try:
        audio = elevenlabs.generate(
            text = sick_text,
            voice = voice,
            model = ELEVEN_MODEL   # e.g. "eleven_multilingual_v2"
            # We could also adjust stability/similarity settings if desired by creating a Voice object
        )
    except Exception as e:
        # If the API call fails, propagate the error or handle it
        raise

    # 3. Save the audio to a file
    output_path = "static/output.mp3"
    elevenlabs.save(audio, output_path)
    return output_path
```

#### Notes on Implementation

- We call our earlier `augment_text_with_sickness` to insert the cues.
- We use `elevenlabs.generate` with parameters:
  - `text`: The final text to speak.
  - `voice`: The voice name or ID. (We're using a default voice; the ElevenLabs SDK can accept voice names for known pre-made voices like "Bella", "Antoni", etc. Alternatively, a voice ID string for a custom voice could be used. Using the name is convenient for known default voices. Ensure the name matches one on the ElevenLabs account associated with the API key. The free tier usually has a few premade voices.)
  - `model`: Specify the model. `eleven_multilingual_v2` is recommended for the most natural and expressive output (it supports English and other languages with improved quality). Using v2 should also allow the model to handle the non-verbal cues better.

#### Testing TTS

This part requires the ElevenLabs API key to be set and internet access. If available, we can do a quick dry run:
```python
from voice_generation import generate_sick_voice_audio
test_text = "I won't be able to come in today, I'm feeling awful."
audio_file = generate_sick_voice_audio(test_text)
print("Audio saved to", audio_file)
```

Running this should produce an `output.mp3` file. You can manually listen to it (outside of the Python process) to verify the voice sounds as expected (with coughs/sniffs). This confirms the ElevenLabs integration works.

**Commit:** “Implement ElevenLabs TTS generation in voice_generation module.”

### Step 6: Integrate into Flask Backend (API Endpoints)

#### Tasks

With core functionality in place (transcription and voice generation), we now connect everything in the Flask app to create the interactive experience. We need two main routes:
1. A route to serve the web interface (HTML page with the recorder).
2. A route to handle the uploaded audio from the user, process it (STT -> augment -> TTS), and return the generated audio.

#### Frontend Page Route

In `app.py`, import our modules:
```python
from flask import Flask, request, render_template, send_file, jsonify
from speech_recognition import transcribe_audio
from voice_generation import generate_sick_voice_audio
```

Set up the frontend page route:
```python
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
```

This will serve `templates/index.html` which we will create next.

#### HTML Template

Create the HTML template `templates/index.html`:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Call-in-Sick Bot</title>
  <!-- (Optional Bootstrap CDN for styling) -->
</head>
<body>
  <h1>Call-in-Sick Bot</h1>
  <p>Click "Record" and speak your sick-day message, then click "Stop". The app will generate a sick-sounding audio message for you.</p>
  
  <button id="recordBtn">Record</button>
  <button id="stopBtn" disabled>Stop</button>
  <br/>
  <p id="statusMsg"></p>
  
  <!-- Audio player for result -->
  <audio id="resultAudio" controls style="display:none; margin-top: 20px;"></audio>
  
  <script src="{{ url_for('static', filename='script.js') }}"></script>
</body>
</html>
```

We'll style and improve it later if needed, but this is the basic structure.

#### Static Script

Implement `static/script.js` for recording and sending audio:
```javascript
const recordBtn = document.getElementById('recordBtn');
const stopBtn = document.getElementById('stopBtn');
const statusMsg = document.getElementById('statusMsg');
const resultAudio = document.getElementById('resultAudio');
let mediaRecorder;
let audioChunks = [];

recordBtn.addEventListener('click', async () => {
  // Request microphone permission and start recording
  audioChunks = [];
  statusMsg.textContent = "Recording... (speak now)";
  resultAudio.style.display = "none";
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();
    recordBtn.disabled = true;
    stopBtn.disabled = false;

    mediaRecorder.ondataavailable = e => {
      if (e.data.size > 0) {
        audioChunks.push(e.data);
      }
    };

    mediaRecorder.onstop = async () => {
      // When recording stops, combine chunks into a blob
      const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
      statusMsg.textContent = "Processing your audio...";
      // Send the blob to the server
      let formData = new FormData();
      formData.append('audio_file', audioBlob, 'recording.webm');
      try {
        const response = await fetch('/process-audio', {
          method: 'POST',
          body: formData
        });
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(errorText || "Server error");
        }
        // Expect the server to respond with the audio data (MP3) or a JSON with path
        const audioBlobResponse = await response.blob();
        // Create a URL for the blob and set it to the audio element
        const audioURL = URL.createObjectURL(audioBlobResponse);
        resultAudio.src = audioURL;
        resultAudio.style.display = "block";
        resultAudio.play();
        statusMsg.textContent = "Here's your sick note message:";
      } catch (err) {
        console.error("Error:", err);
        statusMsg.textContent = "Error: " + err.message;
      } finally {
        // Re-enable record button for another try
        recordBtn.disabled = false;
        stopBtn.disabled = true;
      }
    };
  } catch (err) {
    console.error('Recording failed:', err);
    statusMsg.textContent = "Could not access microphone: " + err;
  }
});

stopBtn.addEventListener('click', () => {
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop();
    statusMsg.textContent = "Recording stopped. Generating voice..."; 
    stopBtn.disabled = true;
  }
});
```

#### Audio Processing Route

Back in `app.py`, implement the audio processing route:
```python
import os
from werkzeug.utils import secure_filename

@app.route("/process-audio", methods=["POST"])
def process_audio():
    # Ensure an audio file is in the request
    if 'audio_file' not in request.files:
        return "No audio file provided", 400
    file = request.files['audio_file']
    if file.filename == '':
        return "Empty file", 400

    # Save the uploaded audio file to a temporary location
    filename = secure_filename(file.filename)
    temp_path = os.path.join("static", filename)
    file.save(temp_path)

    try:
        # 1. Transcribe the audio to text
        transcribed_text = transcribe_audio(temp_path)
        if not transcribed_text:
            return "No speech detected in audio", 400

        # 2. Generate sick voice audio using ElevenLabs
        output_path = generate_sick_voice_audio(transcribed_text)
    except Exception as e:
        print("Error during processing:", e)
        return "Error during processing audio", 500
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return send_file(output_path, mimetype="audio/mpeg")
```

#### Testing the Full Pipeline

Start the Flask server (`python app.py`). Open `http://localhost:5000` in a browser.

Try the recording feature:
- Click "Record", say something like "Hi, I'm not feeling well... I think I have a bad cough and can't come in today.", then click "Stop".
- The status text should update to "Processing..." while the app uploads and waits for the response.
- After a few moments, you should see the audio player appear with the generated audio, and it should autoplay.

**Commit:** “Integrate STT and TTS into Flask app, add frontend recording interface.”

### Step 7: Refinements, Best Practices, and Project Documentation

#### Tasks

With a working prototype in place, we do final clean-up and ensure the project adheres to best practices:

1. **Code Quality:** Review the code for clarity and add comments or docstrings where useful, especially in the modules.
2. **Security & Secrets:** Double-check that no API keys or sensitive info are printed or logged.
3. **GitHub Repository Basics:** Update `README.md` with instructions on how to set up and run the project locally.
4. **Environment and Deployability:** Ensure the app can run on different OS.
5. **Optional Enhancements:** Consider future improvements like better frontend UX, realistic effects, voice selection, phone call integration, etc.

**Commit:** “Finalize project with documentation and cleanup.”
