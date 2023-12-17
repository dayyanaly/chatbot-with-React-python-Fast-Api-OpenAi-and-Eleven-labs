import requests
from decouple import config

# Use uppercase for constants
ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")

def convert_text_to_speech(message, voice="mTSvIrm2hmcnOvb21nW2"):
    """
    Converts text to speech using the Eleven Labs API.

    Args:
        message (str): The text to be converted to speech.
        voice (str): The ID of the voice to use. Default is "mTSvIrm2hmcnOvb21nW2".

    Returns:
        bytes: The audio content in bytes if successful, None otherwise.
    """
    # Define API endpoint and headers
    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"
    headers = {
        "xi-api-key": ELEVEN_LABS_API_KEY,
        "Content-Type": "application/json",
        "accept": "audio/mpeg"
    }

    # Define voice settings
    voice_settings = {
        "stability": 0,
        "similarity_boost": 0
    }

    # Construct request body
    body = {
        "text": message,
        "voice_settings": voice_settings
    }

    try:
        # Make API request
        response = requests.post(endpoint, json=body, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        # Log and handle errors
        print(f"Error during API request: {e}")
        return None

    if response.status_code == requests.codes.ok:
        # Return audio content if successful
        return response.content
    else:
        # Log and handle errors
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Example usage:
text_to_convert = "Hello, how are you?"
voice_data = convert_text_to_speech(text_to_convert, voice="mTSvIrm2hmcnOvb21nW2")
if voice_data:
    # Save audio content to a file
    output_filename = "output.wav"
    with open(output_filename, "wb") as output_file:
        output_file.write(voice_data)
    print(f"Text converted to speech and saved as {output_filename}")
else:
    print("Text to speech conversion failed.")
