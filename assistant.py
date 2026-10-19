from openai import OpenAI

from config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    MAX_TOKENS,
    TEMPERATURE,
)

from prompts import SYSTEM_PROMPT
from memory import memory

client = OpenAI(api_key=OPENAI_API_KEY)


def ask_ai(user_id, username, message):

    # Registrera användaren
    memory.register_user(
        user_id,
        username,
        username,
    )

    # Hämta tidigare konversation
    history = memory.get_recent_conversation(user_id)

    # Hämta långtidsminnen
    memories = memory.get_memories(user_id)

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    # Lägg till minnen om det finns några
    if memories:
        messages.append(
            {
                "role": "system",
                "content": memories,
            }
        )

    # Lägg till tidigare konversation
    messages.extend(history)

    # Nuvarande användarmeddelande
    messages.append(
        {
            "role": "user",
            "content": message,
        }
    )

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )

    answer = response.choices[0].message.content

    # Spara konversationen
    memory.save_message(
        user_id,
        "user",
        message,
    )

    memory.save_message(
        user_id,
        "assistant",
        answer,
    )

    return answer