# AgentRun.py

import warnings
from langchain_core._api.deprecation import LangChainDeprecationWarning

warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)



import time
from colorama import Fore, Style
from rich.console import Console
from rich.panel import Panel

console = Console()

def simulate_typing(text, delay=0.01):
    for char in text:
        print(Fore.GREEN + char + Style.RESET_ALL, end='', flush=True)
        time.sleep(delay)
    print()

from io import StringIO
import sys

def print_agent_response(response_text):
    panel = Panel(response_text, title="🤖 Agent:", expand=False)
    buffer = StringIO()
    console.file = buffer
    console.print(panel)
    console.file = sys.stdout
    simulate_typing(buffer.getvalue())



import requests

conversation_id = "terminal-session-001"
history = []


while True:
    query = input(Fore.LIGHTRED_EX + "\n🧑 You: " + Style.RESET_ALL)
    if query.lower() in ["exit", "quit", "stop", "bye"]:
        print("👋 Goodbye!")
        break

    # Add user message to history
    history.append({"role": "user", "content": query})

    # Build MCP payload
    mcp_payload = {
        "context": {
            "conversation_id": conversation_id,
            "history": history
        },
        "input": {
            "query": query
        }
    }

    # Send to agent
    response = requests.post("http://localhost:8002/chat", json=mcp_payload)
    agent_reply = response.json().get("output", "⚠️ No response")

    
    # Add agent reply to history
    history.append({"role": "assistant", "content": agent_reply["result"]})

    print_agent_response(agent_reply["result"])

