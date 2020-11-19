import os

from dotenv import load_dotenv

from src.base import LoliChan

load_dotenv()

# Load env
TOKEN = os.getenv('DISCORD_TOKEN')

client = LoliChan(verbose=True)

client.run(TOKEN)