from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv
import os
import tempfile
import base64
import sys
import subprocess
import json

# Import our voice generation module
from voice_generation import generate_sick_voice_audio

# Load environment variables
load_dotenv()

# Simple API key check
api_key = os.getenv('ELEVENLABS_API_KEY')
if not api_key or api_key == 'your_api_key_here':
    print("API key not properly loaded or is set to default value")
    # Try to read from .env file directly if needed
    try:
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    if line.strip() and not line.strip().startswith('#'):
                        if 'ELEVENLABS_API_KEY=' in line:
                            key_value = line.strip().split('ELEVENLABS_API_KEY=')[1]
                            os.environ['ELEVENLABS_API_KEY'] = key_value
                            api_key = key_value
                            print("Loaded API key from .env file")
                            break
    except Exception as e:
        print(f"Error reading .env file: {e}")

# Check if ElevenLabs MCP is installed
def check_mcp_installation():
    try:
        subprocess.run(
            [sys.executable, "-m", "elevenlabs_mcp", "--version"],
            capture_output=True,
            text=True
        )
        return True
    except Exception:
        return False

# Simplified API key validation
def validate_api_key(api_key):
    if not api_key:
        return False
    
    if api_key == 'your_api_key_here':
        return False
    
    # Basic format check for ElevenLabs API keys
    if not api_key.startswith('sk_'):
        return False
    
    return True

app = Flask(__name__)

@app.route('/')
def home():
    # Check if MCP is installed and warn user if not
    mcp_installed = check_mcp_installation()
    
    # Check API key
    api_key = os.getenv('ELEVENLABS_API_KEY')
    api_key_valid = validate_api_key(api_key) if api_key else False
    
    return render_template('index.html', 
                          mcp_installed=mcp_installed,
                          api_key_valid=api_key_valid)

@app.route('/generate-from-text', methods=['POST'])
def generate_from_text():
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({
            'success': False,
            'error': 'No text provided'
        }), 400
    
    # Simple API key check
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key or api_key == 'your_api_key_here':
        return jsonify({
            'success': False,
            'error': 'Please set your ElevenLabs API key in the .env file'
        }), 401
    
    try:
        print(f"Generating audio from text: {text[:30]}...")
        # Generate audio using our voice generation module with MCP
        # Using None for voice parameter will trigger the lookup for the custom "Sick Man 1" voice
        audio, augmented_text = generate_sick_voice_audio(text, voice=None)
        
        # Save the audio file
        os.makedirs('static', exist_ok=True)  # Ensure static directory exists
        audio_path = os.path.join('static', 'sick_call.mp3')
        with open(audio_path, 'wb') as f:
            f.write(audio)
            
        print(f"Audio generated successfully and saved to {audio_path}")
        
        return jsonify({
            'success': True,
            'text': augmented_text,
            'audio_url': '/static/sick_call.mp3'
        })
    
    except Exception as e:
        error_message = str(e)
        print(f"Error generating audio: {error_message}")
        
        if 'invalid_api_key' in error_message.lower() or 'api key' in error_message.lower():
            error_message = f'There was a problem with your ElevenLabs API key. Please check if it is valid and has sufficient credits. Error: {error_message}'
        elif 'No module named' in error_message:
            error_message = 'The ElevenLabs MCP module is not installed correctly. Please run: pip install elevenlabs-mcp'
        elif 'connection' in error_message.lower() or 'network' in error_message.lower():
            error_message = f'Network connection error while communicating with ElevenLabs API: {error_message}'
        
        return jsonify({
            'success': False,
            'error': error_message
        }), 500

@app.route('/generate-from-voice', methods=['POST'])
def generate_from_voice():
    data = request.json
    audio_data = data.get('audio', '')
    
    if not audio_data:
        return jsonify({
            'success': False,
            'error': 'No audio data provided'
        }), 400
    
    # Simple API key check
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key or api_key == 'your_api_key_here':
        return jsonify({
            'success': False,
            'error': 'Please set your ElevenLabs API key in the .env file'
        }), 401
        
    try:
        # For demo purposes, we'll skip the actual voice-to-text step
        # and just use a placeholder text message since we don't have a speech-to-text 
        # API integrated yet
        placeholder_text = "Hello, eh, I'm affriad I'm not feeling very well today, and er, wont be able to come into work today, ill call you in the morning if I'm still not well."
        
        print(f"Generating audio from voice input (using placeholder text)...")
        # Generate audio using our voice generation module with MCP
        # Using None for voice parameter will trigger the lookup for the custom "Sick Man 1" voice
        audio, augmented_text = generate_sick_voice_audio(placeholder_text, voice=None)
        
        # Save the audio file
        os.makedirs('static', exist_ok=True)  # Ensure static directory exists
        audio_path = os.path.join('static', 'sick_call.mp3')
        with open(audio_path, 'wb') as f:
            f.write(audio)
            
        print(f"Audio generated successfully and saved to {audio_path}")
        
        return jsonify({
            'success': True,
            'text': augmented_text,
            'audio_url': '/static/sick_call.mp3'
        })
    
    except Exception as e:
        error_message = str(e)
        print(f"Error generating audio: {error_message}")
        
        if 'invalid_api_key' in error_message.lower() or 'api key' in error_message.lower():
            error_message = f'There was a problem with your ElevenLabs API key. Please check if it is valid and has sufficient credits. Error: {error_message}'
        elif 'No module named' in error_message:
            error_message = 'The ElevenLabs MCP module is not installed correctly. Please run: pip install elevenlabs-mcp'
        elif 'connection' in error_message.lower() or 'network' in error_message.lower():
            error_message = f'Network connection error while communicating with ElevenLabs API: {error_message}'
        
        return jsonify({
            'success': False,
            'error': error_message
        }), 500

@app.route('/test-api-key', methods=['GET'])
def test_api_key():
    """Endpoint for directly testing the API key"""
    api_key = os.getenv('ELEVENLABS_API_KEY')
    results = {
        'key_present': bool(api_key),
        'key_is_default': api_key == 'your_api_key_here' if api_key else False,
        'key_format_valid': api_key.startswith('sk_') if api_key else False,
        'key_length': len(api_key) if api_key else 0,
        'mcp_installed': check_mcp_installation()
    }
    
    # Only test the key if it seems valid
    if results['key_present'] and not results['key_is_default'] and results['mcp_installed']:
        try:
            cmd = [
                sys.executable, "-m", "elevenlabs_mcp", 
                "list_voices",
                "--api-key", api_key
            ]
            process = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True,
                timeout=10  # Add timeout to prevent hanging
            )
            results['key_validation_test'] = process.returncode == 0
            
            if results['key_validation_test']:
                results['validation_message'] = "API key is valid and working!"
            else:
                results['validation_message'] = "API key validation failed."
        except Exception as e:
            results['validation_message'] = f"Error testing API key: {str(e)}"
    
    return jsonify(results)

@app.route('/set-voice-id', methods=['POST'])
def set_voice_id():
    """Allow the user to directly set their voice ID"""
    data = request.json
    voice_id = data.get('voice_id', '')
    
    if not voice_id:
        return jsonify({
            'success': False,
            'error': 'No voice ID provided'
        }), 400
    
    try:
        # Import the voice generation module to set the DEFAULT_VOICE_ID
        import voice_generation
        voice_generation.DEFAULT_VOICE_ID = voice_id
        print(f"Set default voice ID to: {voice_id}")
        
        return jsonify({
            'success': True,
            'message': f"Voice ID set successfully. Your next generations will use this voice ID."
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Failed to set voice ID: {str(e)}"
        }), 500

if __name__ == '__main__':
    if not check_mcp_installation():
        print("WARNING: ElevenLabs MCP not found. Please install it with 'pip install elevenlabs-mcp'")
    app.run(debug=True)