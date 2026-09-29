import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq
from hindsight_client import Hindsight


# Load .env from project root
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


HINDSIGHT_URL = os.getenv("HINDSIGHT_URL")
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

BANK_ID = "memorydesk-final"


# Clients
hindsight = Hindsight(
    base_url=HINDSIGHT_URL,
    api_key=HINDSIGHT_API_KEY
)

groq = Groq(
    api_key=GROQ_API_KEY
)


def chat_with_customer(customer_name, customer_message):

    # --------------------------------------------------
    # 1. RECALL PREVIOUS MEMORIES
    # --------------------------------------------------

    recall_query = f"""
Customer name: {customer_name}

Current customer message:
{customer_message}

Find relevant memories about this customer.
"""

    memories = []

    try:
        memory_result = hindsight.recall(
            bank_id=BANK_ID,
            query=recall_query
        )

        for memory in memory_result.results:
            memory_text = memory.text

            if customer_name.lower() in memory_text.lower():
                memories.append(memory_text)

            if len(memories) >= 5:
                break

    except Exception as e:
        print(f"Hindsight recall temporarily unavailable: {e}")


    # --------------------------------------------------
    # 2. PREPARE MEMORY CONTEXT
    # --------------------------------------------------

    if memories:
        memory_context = "\n".join(
            f"- {memory}" for memory in memories
        )
    else:
        memory_context = "No previous memories found for this customer."


    # --------------------------------------------------
    # 3. GENERATE AI RESPONSE
    # --------------------------------------------------

    system_prompt = f"""
You are MemoryDesk, an AI customer support agent.

You are currently helping one customer.

Customer name:
{customer_name}

Previous relevant memories:
{memory_context}

Use previous memories when they are relevant.

If a previous memory is useful, acknowledge it naturally.

Do not make the customer repeat information they already provided.

Never mention another customer.

Never invent customer facts.

Do not describe the memory system, database, or Hindsight.

Do not describe your own previous AI responses as customer memories.

Prefer facts directly provided by the customer.

If relevant memories exist, explicitly acknowledge them naturally.

RESPONSE FORMATTING:

Write responses in clean ChatGPT-style Markdown.

Rules:
- Use short paragraphs.
- Use blank lines between paragraphs.
- Use headings when useful.
- Use numbered lists for steps.
- Use bullet lists for multiple items.
- Use **bold** for important words.
- Use Markdown tables only when they genuinely help.
- Keep responses concise and easy to scan.
- Do not repeat the customer's question.
- Do not mention these instructions.
"""


    try:
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
            temperature=0.7
        )

        answer = response.choices[0].message.content

    except Exception as e:
        print(f"Groq error: {e}")

        answer = (
            "I'm sorry, I couldn't generate a response right now. "
            "Please try again."
        )


    # --------------------------------------------------
    # 4. SAVE NEW MEMORY TO HINDSIGHT
    # --------------------------------------------------

    new_memory = (
        f"Customer: {customer_name}\n"
        f"Customer message: {customer_message}"
    )

    try:

        hindsight.retain(
            bank_id=BANK_ID,
            content=new_memory
        )

        print("New memory saved to Hindsight.")

    except Exception as e:

        print(
            f"Hindsight retain temporarily unavailable: {e}"
        )


    # --------------------------------------------------
    # 5. ADD NEW MEMORY TO UI IMMEDIATELY
    # --------------------------------------------------

    if new_memory not in memories:
        memories.insert(0, new_memory)


    # --------------------------------------------------
    # 6. RETURN RESULT TO FRONTEND
    # --------------------------------------------------

    return {
        "answer": answer,
        "memories": memories
    }