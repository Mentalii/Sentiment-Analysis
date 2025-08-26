# AgentRun.py

#from langchain.agents import initialize_agent
#from langchain.agents import AgentType

#from langchain.llms import OpenAI  # or use a dummy LLM if you prefer


import warnings
from langchain_core._api.deprecation import LangChainDeprecationWarning

warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)


# Initialize the agent
# agent_setup.py
#from agent_setup import create_agent
from agent_setup import run_agent
#agent = create_agent()

import time
from colorama import Fore, Style
from rich.console import Console
from rich.panel import Panel

console = Console()

def simulate_typing(text, delay=0.02):
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

while True:
    query = input(Fore.LIGHTRED_EX + "\n🧑 You: " + Style.RESET_ALL)
    if query.lower() in ["exit", "quit", "stop", "bye"]:
        print("👋 Goodbye!")
        break
    #response = agent.run(query)
    #print(Fore.CYAN + "\n🤖 Agent: " + Style.RESET_ALL)
    #simulate_typing(run_agent(agent, query))
    print_agent_response(run_agent(query))
    #print_agent_response(run_agent(agent, query))







#agent.run("What's the sentiment of the tweet: 'I hate this so much 😡'")


