import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Modell
OPENAI_MODEL = "gpt-4.1-mini"

# Databas
DATABASE_FILE = "memory.db"

# Hur många tidigare meddelanden AI ska läsa
MEMORY_MESSAGES = 15

# Max antal svarstokens
MAX_TOKENS = 1200

# Temperatur
TEMPERATURE = 0.8