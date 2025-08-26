
#pip install langchain langchain-community
# agent_setup.py
from langchain.agents import initialize_agent, AgentType
from sentiment_tool import sentiment_tool
#from langchain.chat_models import ChatOpenAI
#from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
#pip install -U langchain-community
 
#from langchain_community.llms import OpenAI
#from :class:`~langchain_openai import ChatOpenAI`
#from langchain.llms import OpenAI


import warnings
from langchain_core._api.deprecation import LangChainDeprecationWarning

warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)

import warnings
from langchain_core._api.deprecation import LangChainDeprecationWarning

warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="envir.env")

llm = ChatOpenAI(
    temperature=0,
    model_name="gpt-4o-mini",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

#from langchain.agents.agent_toolkits import Tool
from langchain_core.tools import Tool

from langchain.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([

    ("system", "You are Mike. You play Baseball and you are a student at University of Data Lab. You are friendly and funny."),
    ("human", "{input}")
])

'''system_message = """

You are a helpful assistant with access to chat history(you have memory of last messages) and to two tools:
1. SentimentClassifier — for analyzing emotional tone.
2. RAGRetriever — for retrieving factual information from documents.

Use SentimentClassifier only when the user asks about emotions, reactions, sentiment or provides text that clearly needs emotional evaluation.
Use RAGRetriever only when the user asks for factual information, bios, or document-based answers about 

student "Vitalii Kozak".
If the query is general knowledge or conversational and does not require a tool, respond directly using this format:
Thought: ...
Final Answer: ...
Do not include 'Action' or 'Action Input' unless you are using a tool.
'''

#Only use it when the user explicitly asks for sentiment analysis
#Otherwise, respond directly using your own reasoning. If you do not need to use a tool, respond with: "Thought: ... Final Answer: ..." Do not include 'Action' or 'Action Input' unless you are using a tool."

from RAG_tool import build_rag_tool

rag_tool = build_rag_tool("student_bio.txt")

tools = [sentiment_tool, rag_tool]

#Only use it when the user explicitly asks for sentiment analysis
#Otherwise, respond directly using your own reasoning. If you do not need to use a tool, respond with: "Thought: ... Final Answer: ..." Do not include 'Action' or 'Action Input' unless you are using a tool."

from RAG_tool import build_rag_tool

rag_tool = build_rag_tool("student_bio.txt")

tools = [sentiment_tool, rag_tool]

from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, k=5)


def create_agent():
    return initialize_agent(
        tools, 
        llm=llm,

agent_type=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,  #OPENAI_FUNCTIONS do not support chat history
        handle_parsing_errors=True,
        #agent_kwargs={"system_message": system_message},
        agent_kwargs={"prompt": prompt},
        memory=memory,
        verbose=False
    )        

import logging
logging.basicConfig(filename="agent_log.txt", level=logging.INFO)

def run_agent(agent, user_input):
    response = agent.invoke(user_input)
    logging.info(f"User: {user_input}\nAgent Raw: {response}\n---")

    # Inspect memory contents (optional, for debugging)
    if hasattr(agent, "memory") and hasattr(agent.memory, "chat_memory"):
        for msg in agent.memory.chat_memory.messages:
            logging.debug(f"{msg.type.upper()}: {msg.content}")

  # Try to extract output safely
    if isinstance(response, dict):
        output = response.get('output') or response.get('answer') or response.get('result')
        if output:
            return output
    elif isinstance(response, str):
        return response
    elif hasattr(response, "get_final_answer"):
        return response.get_final_answer()
    
    return "🤷 Agent did not return a valid response."            
