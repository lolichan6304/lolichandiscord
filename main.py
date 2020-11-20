import os

from dotenv import load_dotenv

from src.base import LoliChan

load_dotenv()

# Load env
TOKEN = os.getenv('DISCORD_TOKEN')
if os.environ.get('TAGS_NHENTAI') is None:
    os.environ['TAGS_NHENTAI'] = ""
if os.environ.get('ALLOWED_ROLES') is None:
    os.environ['ALLOWED_ROLES'] = ""

client = LoliChan(verbose=False)

client.run(TOKEN)