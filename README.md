# 🧠 MemoryDesk

## AI Customer Support That Remembers Every Customer Interaction

MemoryDesk is an AI-powered customer support agent that uses
**Hindsight** as a persistent memory layer. It recalls relevant customer
context before generating a response and retains new customer
interactions for future conversations.

## Problem

Traditional AI customer-support systems can lose context between
interactions. A customer may explain that they always use UPI and have
already experienced two payment failures, then later report another
failure. The customer should not have to repeat the same information.

## Solution

MemoryDesk creates a memory loop:

``` text
Customer Message
      ↓
Hindsight Recall
      ↓
Relevant Customer Memories
      ↓
Groq LLM
      ↓
Personalized Response
      ↓
Hindsight Retain
      ↓
Future Conversations
```

## Key Features

-   **Persistent customer memory** for previous problems, preferences,
    and relevant context.
-   **Personalized responses** using recalled memories.
-   **Visible memory panel** showing relevant memories used for the
    current response.
-   **Customer-specific filtering** to reduce the risk of using another
    customer's information.
-   **Graceful Hindsight error handling** so temporary memory-service
    failures do not crash the complete application.

## Technology Stack

  Technology            Purpose
  --------------------- ------------------------
  Python                Backend
  FastAPI               API and web backend
  Hindsight             Long-term AI memory
  Groq                  LLM inference
  HTML/CSS/JavaScript   Frontend
  Uvicorn               Development server
  GitHub                Source-code management

## Project Structure

``` text
MemoryDesk/
├── backend/
│   ├── main.py
│   ├── agent.py
│   ├── hindsight.py
│   └── prompts.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── data/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## How It Works

### 1. Customer sends a message

Example:

``` text
Hi, I'm Alex. I always use UPI and my last two payments failed.
```

### 2. Hindsight recall

The backend sends the customer context and current message to Hindsight
and retrieves relevant memories.

### 3. Groq generates the response

The retrieved memories are provided to the LLM as context so the
response can naturally use relevant previous information.

### 4. Hindsight retain

The customer's new interaction is retained for future conversations.

### 5. Memory is visible

The frontend displays up to five relevant memories in the Memory panel.

## Example Demo

**First interaction**

``` text
Customer:
Hi, I'm Alex. I always use UPI and my last two payments failed.
```

**Later interaction**

``` text
Customer:
My payment failed again. What should I do?
```

MemoryDesk can recall context such as:

``` text
Alex's last two UPI payments failed.
Alex experienced two failed UPI payments.
```

This demonstrates the core concept:

``` text
Before: Every interaction starts from scratch.

After: The agent recalls relevant customer context.
```

## Environment Variables

Create `.env` in the project root:

``` env
HINDSIGHT_API_KEY=your_hindsight_api_key
HINDSIGHT_URL=https://api.hindsight.vectorize.io
GROQ_API_KEY=your_groq_api_key
```

Never commit `.env` to GitHub.

Recommended `.gitignore`:

``` text
venv/
.env
__pycache__/
*.pyc
```

## Run Locally

### 1. Create the virtual environment

Windows PowerShell:

``` powershell
py -3.11 -m venv venv
.env\Scripts\Activate.ps1
```

### 2. Install dependencies

``` powershell
pip install -r requirements.txt
```

### 3. Start MemoryDesk

``` powershell
uvicorn backend.main:app --port 8001
```

### 4. Open the application

``` text
http://127.0.0.1:8001
```

## Architecture

``` text
                    ┌─────────────────────┐
                    │      Customer       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    MemoryDesk UI    │
                    │    HTML/CSS/JS      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       FastAPI       │
                    │       Backend       │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
             ┌──────────────┐      ┌──────────────┐
             │   Hindsight  │      │     Groq     │
             │ Recall/Retain│      │     LLM      │
             └──────┬───────┘      └──────┬───────┘
                    │                     │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │ Personalized Reply  │
                    └─────────────────────┘
```

## Hackathon Focus

MemoryDesk keeps **memory central and visible** rather than treating
memory as an invisible add-on. The project focuses on one tight
workflow:

**Customer support + persistent customer memory**

The visible memory panel makes the Hindsight recall step easy to
demonstrate during a live presentation.

## Future Improvements

-   Customer profile summaries
-   Multiple customer accounts
-   Support-ticket integration
-   Order and refund workflows
-   Memory timeline
-   Analytics dashboard
-   Authentication
-   Production deployment

## Project

**MemoryDesk --- AI Customer Support That Remembers**

Built with **FastAPI + Groq + Hindsight**.
