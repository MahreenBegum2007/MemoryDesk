import os
from pathlib import Path

from dotenv import load_dotenv
from hindsight_client import Hindsight


# Load .env from the MemoryDesk project folder
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

HINDSIGHT_URL = os.getenv("HINDSIGHT_URL")
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")

print("Hindsight URL found:", bool(HINDSIGHT_URL))
print("Hindsight API key found:", bool(HINDSIGHT_API_KEY))

client = Hindsight(
    base_url=HINDSIGHT_URL,
    api_key=HINDSIGHT_API_KEY
    
)

BANK_ID = "memorydesk-support"

try:
    print("Connecting to Hindsight...")

    client.retain(
        bank_id=BANK_ID,
        content="Customer Sarah prefers UPI payments and previously experienced two payment failures."
    )

    print("Memory stored successfully!")

    result = client.recall(
        bank_id=BANK_ID,
        query="What payment method does Sarah prefer and what happened with her payments?"
    )

    print("\nMemories recalled:")

    for memory in result.results:
        print("-", memory.text)

except Exception as e:
    print("\nERROR:")
    print(e)

finally:
    client.close()