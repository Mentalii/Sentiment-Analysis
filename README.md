## AI Agent with Sentiment Analysis and RAG

This project is a modular AI agent system built with LangChain, FastAPI, and Telegram integration. It uses **tool-aware orchestration** to route user queries to the appropriate microservice — either a **Sentiment Classifier** or a **RAG Retriever** — and responds contextually with memory and personality.

The agent is accessible via:
- 🖥️ Terminal interface
- 📱 Telegram bot
- 🌐 FastAPI `/chat` endpoint - http://localhost:8002/chat (MCP-compliant)

Each tool is wrapped as a LangChain `Tool` with a clear usage policy:
- Sentiment tool is only used when emotional analysis is requested
- RAG tool is used for factual queries about "Vitalii Kozak"

1.  **Sentiment Classifier Tool**: This tool analyzes the sentiment of user input, classifying it as positive or negative.

2.  **RAG (Retrieval Augmented Generation) Tool**: This tool enables the agent to retrieve relevant information from a provided `student_bio.txt` file. This allows the agent to answer questions based on a specific knowledge base.

## 🧩 Architecture Overview

Telegram Bot ↔ MCP Agent Service ↔ LangChain Agent ↔ Tools: 1) Sentiment Microservice 2) RAG Microservice

## Project Structure

The project is organized into several services, each responsible for a specific functionality:

-   **Agent Service**: The core AI agent that orchestrates interactions and tool usage.
-   **RAG Service**: Provides the retrieval-augmented generation capabilities, using `student_bio.txt` as its knowledge base.
-   **Sentiment Tool Service**: Offers sentiment analysis functionality.
-   **Telegram Bot**: An interface to interact with the AI agent via Telegram.

## Running the Project with Docker

This project is composed of four main services, each with its own Dockerfile and managed together via `docker-compose.yml`. The services are:
- Agent Service
- RAG Service
- Sentiment Tool Service
- Telegram Bot

### Project-Specific Docker Requirements
- **Python Versions:**
  - Agent, RAG, Sentiment Tool Services: Python 3.12-slim
  - Telegram Bot: Python 3.11-slim
- **System Dependencies:** All services (except Telegram Bot) install `git` for Python package requirements.
- **Virtual Environments:** Each service installs dependencies into a local virtual environment (`.venv`).

### Environment Variables--
- The `Agent Service` and `Telegram Bot` support environment variable file (`.env`). Set your own environmental variables to test the project. Needed: Openai_api_key and telegram bot token from BotFather.

### Exposed Ports
- **Agent Service:** 8002
- **RAG Service:** 8001
- **Sentiment Tool Service:** 8000
- **Telegram Bot:** (no port exposed; runs as a background process)

### Build and Run Instructions
1. **Clone the repository and ensure Docker and Docker Compose are installed.**
2. **Configure environment variables:**
Set up .env with your OpenAI key
Set up your bot token in telegram_bot.py 
   
4. **Build and start all services:**
   ```sh
   docker compose up --build
   ```
   This will build all images and start the services with the correct dependencies and networking.

5. **To run containers if images are built:**

    ```sh
   docker compose up 
   ```
    or to temporary stop containers via terminal:
   ```sh
   Ctrl + C 
   ```
   To run containers on backround(and do not block current terminal) use '-d'(detached mode):
   ```sh
   docker compose up -d
   ```
6. **Telegram Bot**
   Open your telegram Bot which you created using Bot father and indicated with token in your telegram_bot.py. You can chat with it now!

telegram_bot.py
Telegram bot interface using python-telegram-bot. Supports commands:

/start, /help

/sentiment <text> → routes to sentiment tool

/bio <query> → routes to RAG tool

/reset, /memory, /clear_chat confirm

Internally, it builds MCP-compliant payloads and sends them to the agent service.

🧠 This bot gives users a conversational interface with tool-aware routing and memory.

6. **Terminal**
   In root folder of your project open terminal and run: pyhon AgentRun.py. After you can chat with agent from terminal.
   
   
   

### Special Configuration Notes
- All services are connected via a custom Docker network (`backend`).
- The Agent Service depends on both the RAG and Sentiment Tool services, and the Telegram Bot depends on the Agent Service.
- If you need to persist or access logs, check the `agent_log.txt` in the Agent Service directory.
- The Telegram Bot does not expose a port; it communicates via the Telegram API. Bot receives user messages from Telegram then using POST requst it calls AI agent.
Telegram user → bot → MCP payload → agent → tool → back to Telegram 
- AI agent comunicate with tools using POST requests. Tools can be accessed only through AI agent.
  

### Summary Table
| Service                  | Build Context                | Exposed Port |
|--------------------------|-----------------------------|--------------|
| Agent Service            | ./Agent Service             | 8002         |
| RAG Service              | ./RAG service               | 8001         |
| Sentiment Tool Service   | ./Sentiment tool Service    | 8000         |
| Telegram Bot             | ./telegram Bot              | (none)       |


### 🛠 Technologies Used
LangChain (agent orchestration)

FastAPI (service exposure)

Python Telegram Bot (chat interface)

Pydantic (schema validation)

Model Context Protocol (agent communication)

Docker (microservice containerization)
----------------------------------------------------------------------------------------------------------------------------

Microservice Architecture was used. As it mentioned before there is 4 main services: 
- Agent Service
- RAG Service
- Sentiment Tool Service
- Telegram Bot
Tools and agent services were made with FastApi, so they could communicate with each other.
Agent awaiting when there will be POST request from user (it can came from Terminal, telgram bot or if you use http://localhost:8002/chat to make request). Then if needed agent will call tools via http POST requests to their services:
1) Sentiment classifier: http://localhost:8000/classify
2) RAG: http://localhost:8001/retrieve

Also MCP was used for communication with Agent through Telegram Bot.

In this project, MCP is used to:

Pass user queries and history from Telegram to the agent

Ensure consistent memory and tool usage

Enable future expansion to other interfaces (web, voice, etc.)

### 🧑‍🎓 About the Agent
Mike is a friendly, funny student who plays baseball and studies at the University of Data Lab. He remembers your last 10 messages and knows when to use tools — and when to just chat.

### 📄 License
Apache 2.0 — free to use, modify, and share.

### 🙌 Credits
Built by Vitalii Kozak.
