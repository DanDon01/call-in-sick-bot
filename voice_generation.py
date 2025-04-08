import os
import random
import json
import tempfile
from dotenv import load_dotenv
import subprocess
import base64

# Load environment variables
load_dotenv()

# Constants
DEFAULT_VOICE = "Sick Man 1"  # Custom voice name
DEFAULT_VOICE_ID = "lsBMTulYfC7cPRgpqMR8"  # The Sick Man 1 voice ID
FALLBACK_VOICE = "Adam"  # Fallback voice if custom voice isn't found
FALLBACK_VOICE_ID = "pNInz6obpgDQGcFmaJgB"  # Adam voice ID
ELEVEN_MODEL = "eleven_turbo_v2"  # Using turbo v2 instead of multilingual

def find_voice_by_name(name: str):
    """
    Find a voice by name in the user's ElevenLabs account.
    
    Args:
        name: The name of the voice to find
        
    Returns:
        The voice ID if found, None otherwise
    """
    try:
        import elevenlabs
        
        # Get API key from environment
        api_key = os.getenv('ELEVENLABS_API_KEY')
        if not api_key:
            print("No API key found, can't look up voice")
            return None
            
        # Create an ElevenLabs client
        client = elevenlabs.ElevenLabs(api_key=api_key)
        
        # Get available voices - properly access the voices from the client
        try:
            # Try various ways to access voices based on the ElevenLabs API versions
            try:
                # For newer versions of the library where voices might be a property
                voices = client.voices
                if not voices:
                    # If voices is empty or None, try the old approach of voice.from_api
                    voices = elevenlabs.voices.from_api()
            except AttributeError:
                try:
                    # For versions of the library where voices are accessed via from_api method
                    voices = elevenlabs.voices.from_api()
                except:
                    # Last resort - try directly with the Voice interface
                    from elevenlabs import Voice
                    voices = Voice.from_api()
            
            print(f"Found {len(voices) if voices else 0} voices")
            
            # Look for voice with the specified name
            for voice in voices:
                # Try to match name accounting for different object structures
                voice_name = getattr(voice, 'name', None)
                if not voice_name and hasattr(voice, '__getitem__'):
                    # If it's a dict-like object
                    voice_name = voice.get('name', '')
                
                # Try to get the voice_id accounting for different object structures
                voice_id = getattr(voice, 'voice_id', None)
                if not voice_id and hasattr(voice, '__getitem__'):
                    # If it's a dict-like object
                    voice_id = voice.get('voice_id', '')
                
                if voice_name and voice_name.lower() == name.lower() and voice_id:
                    print(f"Found voice '{name}' with ID: {voice_id}")
                    return voice_id
                    
            # If we got here, we didn't find the voice
            print(f"Voice '{name}' not found in your account")
            
            # Print available voices to help troubleshooting
            print("Available voices:")
            for voice in voices:
                voice_name = getattr(voice, 'name', None)
                if not voice_name and hasattr(voice, '__getitem__'):
                    voice_name = voice.get('name', 'Unknown')
                print(f" - {voice_name}")
                
            return None
            
        except Exception as e:
            print(f"Error listing voices: {e}")
            return None
    except Exception as e:
        print(f"Error importing elevenlabs or creating client: {e}")
        return None

def augment_text_with_sickness(text: str) -> str:
    """
    Augment the given text with sick effects like coughs, sniffles, etc.
    to make the spoken voice sound more convincingly ill.
    
    Args:
        text: The original text to augment
        
    Returns:
        The augmented text with sick effects
    """
    # Trim whitespace
    text = text.strip()
    if not text:
        return text  # nothing to augment

    # Using more clearly English phonetic spellings for sick sounds
    sick_effects = [
        "a-khuhm",  # light cough
        "ahem khm",  # throat clearing
        "koff koff",  # classic cough
        "sniff",  # sniff
        "a-hem",  # throat clearing
        "*wheezy breath*",  # wheeze
        "huh-chm",  # suppressed cough
    ]
    
    # Start with a cough sound
    sick_text = f"{random.choice(['a-khuhm ', 'koff ', 'ahem '])}"
    
    # Split text into sentences for better insertion points
    sentences = text.split('.')
    augmented_sentences = []
    
    for i, sentence in enumerate(sentences):
        if not sentence.strip():
            continue
            
        # Clean up the sentence
        sentence = sentence.strip()
        
        # For longer sentences, insert sick effects in the middle
        words = sentence.split()
        if len(words) > 5:
            # Insert effect at approximately 1/3 or 2/3 through the sentence
            insert_pos = random.choice([len(words) // 3, 2 * len(words) // 3])
            words.insert(insert_pos, f" {random.choice(sick_effects)} ")
        
        augmented_sentences.append(" ".join(words))
    
    # Join sentences back together
    sick_text += ". ".join(augmented_sentences)
    
    # Add a sniff or cough at the end if it doesn't already end with one
    if not any(effect in sick_text[-15:] for effect in sick_effects):
        sick_text += f" {random.choice(['sniff', 'koff', 'a-khuhm'])}"
    
    # If the text is very short, ensure we have at least one sick effect
    if len(sick_text.split()) < 5 and not any(effect in sick_text for effect in sick_effects):
        sick_text += f" {random.choice(sick_effects)}"
    
    return sick_text


def generate_sick_voice_audio(text: str, voice: str = None) -> tuple:
    """
    Generate sick-sounding voice audio from the given text using ElevenLabs API.
    
    Args:
        text: The original text to convert to sick-sounding speech
        voice: The ElevenLabs voice to use (name or ID). If None, tries to use the custom voice
        
    Returns:
        A tuple of (audio_data, augmented_text)
    """
    # If no specific voice is provided, try to find the custom voice
    if voice is None:
        # If we have a direct voice ID, use it
        if DEFAULT_VOICE_ID:
            voice = DEFAULT_VOICE_ID
            print(f"Using direct voice ID for '{DEFAULT_VOICE}'")
        else:
            # Try to find the custom voice by name
            custom_voice_id = find_voice_by_name(DEFAULT_VOICE)
            if custom_voice_id:
                voice = custom_voice_id
            else:
                # Fall back to the default voice if custom voice not found
                print(f"Custom voice '{DEFAULT_VOICE}' not found, using fallback voice '{FALLBACK_VOICE}'")
                voice = FALLBACK_VOICE_ID
    
    # Augment the text with sick effects
    sick_text = augment_text_with_sickness(text)
    
    try:
        # Create a temporary file to store the output audio
        fd, output_path = tempfile.mkstemp(suffix=".mp3")
        os.close(fd)
        
        # Get API key from environment
        api_key = os.getenv('ELEVENLABS_API_KEY')
        print(f"Using API key starting with: {api_key[:4]}...")
        
        # Try using the elevenlabs module directly but with updated imports
        try:
            print("Using elevenlabs module directly...")
            
            # Import at runtime to correctly use the elevenlabs library
            import elevenlabs
            from elevenlabs import Voice, VoiceSettings

            # Create an ElevenLabs client
            client = elevenlabs.ElevenLabs(api_key=api_key)
            
            # Generate audio
            print(f"Generating audio with text: {sick_text[:50]}... using voice: {voice}")
            
            # Generate and save audio directly
            audio = client.generate(
                text=sick_text,
                voice=voice,
                model=ELEVEN_MODEL,
                # Use voice settings to make the voice sound more naturally ill
                voice_settings={
                    "stability": 0.3,  # Lower stability for more vocal variation
                    "similarity_boost": 0.75,
                    "style": 0.4,  # Some style emphasis for more expression
                    "speed": 0.9,  # Slightly slower for a tired/sick effect
                }
            )
            
            # Convert generator to bytes if needed
            if hasattr(audio, '__iter__') and not isinstance(audio, (bytes, bytearray)):
                print("Converting generator to bytes...")
                audio_bytes = b''
                for chunk in audio:
                    audio_bytes += chunk
                audio = audio_bytes
            
            # Save audio to file
            with open(output_path, "wb") as f:
                f.write(audio)
                
            print(f"Audio saved to: {output_path}")
            
            # Read the generated audio file
            with open(output_path, 'rb') as audio_file:
                audio_data = audio_file.read()
            
            # Clean up output file
            os.unlink(output_path)
            
            return audio_data, sick_text
            
        except Exception as e1:
            print(f"Direct elevenlabs approach failed: {e1}")
            
            # Fallback approach using direct API call with requests
            import requests
            
            # If we're here and using the custom voice ID, we should try using voice in API call
            # If voice is a name, use the Adam voice ID as fallback
            voice_id = voice
            if isinstance(voice, str) and not voice.startswith("sk_") and not voice.isalnum():
                # If it doesn't look like a voice ID, use Adam's ID
                print(f"Voice '{voice}' doesn't look like a voice ID, using Adam voice ID instead")
                voice_id = "pNInz6obpgDQGcFmaJgB"  # Adam voice ID
            
            print(f"Attempting direct API call as fallback with voice ID: {voice_id}...")
            
            # ElevenLabs API endpoint
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            
            # Request headers with API key
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": api_key
            }
            
            # Request body
            data = {
                "text": sick_text,
                "model_id": ELEVEN_MODEL,
                "voice_settings": {
                    "stability": 0.3,
                    "similarity_boost": 0.75,
                    "style": 0.4,
                    "speed": 0.9
                }
            }
            
            # Make the request
            response = requests.post(url, json=data, headers=headers)
            
            # Check if the request was successful
            if response.status_code == 200:
                # Save the audio
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                print(f"Audio saved to: {output_path}")
                
                # Read the generated audio file
                with open(output_path, 'rb') as audio_file:
                    audio_data = audio_file.read()
                
                # Clean up output file
                os.unlink(output_path)
                
                return audio_data, sick_text
            else:
                raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
    
    except Exception as e:
        print(f"Error in generate_sick_voice_audio: {e}")
        raise Exception(f"Failed to generate audio: {str(e)}")


# For testing only
if __name__ == "__main__":
    test_text = "I won't be able to come in today, I'm feeling awful."
    augmented = augment_text_with_sickness(test_text)
    print(f"Original: {test_text}")
    print(f"Augmented: {augmented}") 