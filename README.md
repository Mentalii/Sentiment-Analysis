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

### Environment Variables
- The `Agent Service` and `Telegram Bot` support environment variable files (`envir.env` and `.env` respectively), but these are commented out in the compose file. If your application requires runtime environment variables, uncomment the relevant `env_file` lines in `docker-compose.yml` and ensure the files exist with the necessary variables.

### Exposed Ports
- **Agent Service:** 8002
- **RAG Service:** 8001
- **Sentiment Tool Service:** 8000
- **Telegram Bot:** (no port exposed; runs as a background process)

### Build and Run Instructions
1. **Clone the repository and ensure Docker and Docker Compose are installed.**
2. **(Optional) Configure environment variables:**
   - If needed, edit `./Agent Service/envir.env` and/or `./telegram Bot/.env` and uncomment the corresponding `env_file` lines in `docker-compose.yml`.
3. **Build and start all services:**
   ```sh
   docker compose up --build
   ```
   This will build all images and start the services with the correct dependencies and networking.

4. **To run containers if images are built:**

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

Refer to the `docker-compose.yml` for further customization or to add environment variables as needed.
