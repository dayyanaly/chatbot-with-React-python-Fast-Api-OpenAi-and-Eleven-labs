import os
import json
import random

DEFAULT_FILE_NAME = "stored_data.json"


def get_learn_instruction():
    """
    Generate a learning instruction for the assistant.
    """
    instructions = [
        "Your response will have some light humor.",
        "Your response will include an interesting new fact about Spain.",
        "Your response will recommend another word to learn."
    ]
    instruction = random.choice(instructions)

    return {
        "role": "system",
        "content": f"You are a my teacher and your name is Rachel, the user is called mr john. Keep responses under 20 words. {instruction}"
    }


def get_recent_messages(file_name=DEFAULT_FILE_NAME, num_messages=5):
    """
    Retrieve recent messages from the stored data file.

    Args:
        file_name (str): Name of the file. Default is "stored_data.json".
        num_messages (int): Number of recent messages to retrieve. Default is 5.

    Returns:
        list: List of recent messages.
    """
    try:
        with open(file_name) as user_file:
            data = json.load(user_file)
            learn_instruction = get_learn_instruction()
            messages = [learn_instruction] + data[-num_messages:]
    except FileNotFoundError:
        messages = [get_learn_instruction()]
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        messages = [get_learn_instruction()]

    return messages


def store_messages(request_message, response_message, file_name=DEFAULT_FILE_NAME):
    """
    Store user and assistant messages in the stored data file.

    Args:
        request_message (str): User's message.
        response_message (str): Assistant's message.
        file_name (str): Name of the file. Default is "stored_data.json".
    """
    messages = get_recent_messages(file_name, num_messages=0)  # Get system message only

    user_message = {"role": "user", "content": request_message}
    assistant_message = {"role": "assistant", "content": response_message}

    messages.extend([user_message, assistant_message])

    with open(file_name, "w") as file:
        json.dump(messages, file)


def reset_messages(file_name=DEFAULT_FILE_NAME):
    """
    Reset stored messages by creating an empty file.

    Args:
        file_name (str): Name of the file. Default is "stored_data.json".
    """
    open(file_name, "w").close()


# Example usage:
# recent_messages = get_recent_messages()
# store_messages("Hello", "Hi there!")
# reset_messages()
