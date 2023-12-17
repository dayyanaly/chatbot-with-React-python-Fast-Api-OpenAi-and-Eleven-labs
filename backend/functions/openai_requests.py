import openai
from decouple import config
from functions.database import get_recent_messages

# Constants
WHISPER_MODEL = "whisper-1"
GPT_MODEL = "gpt-3.5-turbo"

# Retrieve Environment Variables
openai.organization = config("OPEN_AI_ORG")
openai.api_key = config("OPEN_AI_KEY")


def convert_audio_to_text(audio_file_path):
    """
    Convert audio to text using OpenAI's Whisper model.

    Args:
        audio_file_path (str): Path to the audio file.

    Returns:
        str: Transcribed text if successful, None otherwise.
    """
    try:
        transcript = openai.Audio.transcribe(WHISPER_MODEL, audio_file_path)
        message_text = transcript["text"]
        return message_text
    except openai.error.OpenAIError as e:
        # Log the error instead of printing
        print(f"Error during Whisper transcription: {e}")
        return None


def get_chat_response(user_message):
    """
    Get a response from OpenAI's ChatGPT model.

    Args:
        user_message (str): User's message.

    Returns:
        str: Response text if successful, None otherwise.
    """
    messages = get_recent_messages()
    user_message = {"role": "user", "content": user_message + " Only say two or 3 words in Spanish if speaking in Spanish. The remaining words should be in English"}
    messages.append(user_message)

    try:
        response = openai.ChatCompletion.create(model=GPT_MODEL, messages=messages)
        message_text = response["choices"][0]["message"]["content"]
        return message_text
    except openai.error.OpenAIError as e:
        # Log the error instead of printing
        print(f"Error during ChatGPT completion: {e}")
        return None


# Example usage:
# audio_transcription = convert_audio_to_text("path/to/audio/file.wav")
# chat_response = get_chat_response("Hello, how are you?")
