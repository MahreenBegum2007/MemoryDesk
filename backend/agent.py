import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq
from hindsight_client import Hindsight


# Load .env from project root
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


# API keys
HINDSIGHT_URL = os.getenv("HINDSIGHT_URL")
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# Hindsight memory bank
BANK_ID = "memorydesk-final"


# Clients
hindsight = Hindsight(
    base_url=HINDSIGHT_URL,
    api_key=HINDSIGHT_API_KEY,
)

groq = Groq(
    api_key=GROQ_API_KEY
)


def chat_with_customer(customer_name: str, customer_message: str):

    # --------------------------------------------------
    # 1. RECALL PREVIOUS CUSTOMER MEMORIES
    # --------------------------------------------------

    recall_query = f"""
Customer name: {customer_name}

Customer's current message:
{customer_message}

Find only memories that are clearly related to this customer.
Ignore memories belonging to other customers.
"""

    memories = []

    try:

        memory_result = hindsight.recall(
            bank_id=BANK_ID,
            query=recall_query,
        )

        for memory in memory_result.results:

            memory_text = memory.text

            if customer_name.lower() in memory_text.lower():
                memories.append(memory_text)

            if len(memories) >= 5:
                break

    except Exception as e:

        print(
            f"Hindsight recall temporarily unavailable: {e}"
        )

    # --------------------------------------------------
    # 2. PREPARE MEMORY CONTEXT
    # --------------------------------------------------

    if memories:

        memory_text = "\n".join(
            f"- {memory}"
            for memory in memories
        )

    else:

        memory_text = (
            "No previous memories found for this customer."
        )


    # --------------------------------------------------
    # 3. AI SYSTEM PROMPT
    # --------------------------------------------------

    system_prompt = f"""
You are MemoryDesk, an AI customer support agent.

You are currently helping ONE customer.

Customer name:
{customer_name}

Your job is to provide helpful, polite and personalized
customer support.

IMPORTANT MEMORY RULES:

1. Use previous memories when they are relevant.

2. When a previous memory is clearly useful,
   naturally acknowledge it in your response.

3. If the customer previously mentioned a preference,
   problem, or repeated issue, do not make them repeat
   that information unnecessarily.

4. For repeated problems, explain that you remember
   the earlier interaction and use that context.

5. NEVER mention another customer's name.

6. NEVER use information belonging to another customer.

7. NEVER invent customer-specific facts.

8. If a detail is not present in the memories,
   do not pretend that you remember it.

9. Do not say that you are reading a database
   or memory system.

10. Keep the response focused on the current customer.

11. Prefer remembering facts provided by the customer,
    such as preferences, previous problems, or
    important context.

12. Do NOT describe your own previous AI responses
    as customer memories.

13. If relevant memories exist, explicitly acknowledge
    the remembered information naturally.

14. Never invent information that is not present
    in memory.

Previous memories for {customer_name}:

{memory_text}
"""


    # --------------------------------------------------
    # 4. GENERATE AI RESPONSE
    # --------------------------------------------------

    response = groq.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[

            {
                "role": "system",
                "content": system_prompt
            },

            {
                "role": "user",
                "content": customer_message
            }

        ],
    )


    answer = response.choices[0].message.content


    # --------------------------------------------------
    # 5. SAVE CUSTOMER INTERACTION TO HINDSIGHT
    # --------------------------------------------------

    try:

        hindsight.retain(

            bank_id=BANK_ID,

            content=f"""
Customer: {customer_name}

Customer message:
{customer_message}
""",

        )

    except Exception as e:

        print(
            f"Hindsight retain temporarily unavailable: {e}"
        )


    # --------------------------------------------------
    # 6. RETURN RESULT TO FRONTEND
    # --------------------------------------------------

    return {

        "answer": answer,

        "memories": memories,

    }