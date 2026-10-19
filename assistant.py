from openai import OpenAI

from config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    MAX_TOKENS,
    TEMPERATURE,
)

from prompts import SYSTEM_PROMPT
from memory import (
    remember_user_message,
    remember_ai_message,
    load_memory,
)

client = OpenAI(api_key=OPENAI_API_KEY)


def ask_ai(user_id, username, message):

    history = load_memory(user_id)

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": message
        }
    )

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )

    answer = response.choices[0].message.content

    remember_user_message(
        user_id,
        username,
        message
    )

    remember_ai_message(
        user_id,
        username,
        answer
    )

    return answer