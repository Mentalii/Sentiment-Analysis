'''
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

system_message = """

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
'''


from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
#from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
#from sentiment_tool import sentiment_tool #import from sentiment_tool.py is not needed when we building microservice

from langchain.memory import ConversationBufferWindowMemory


#from RAG_tool import build_rag_tool
from remote_tools import sentiment_tool, rag_tool
#rag_tool = build_rag_tool("student_bio.txt")

import os



load_dotenv(dotenv_path="envir.env")
#load_dotenv()

class AgentResponse(BaseModel):
    FinalAnswer: str
    tools_used: list[str]
    
llm = ChatOpenAI(
    temperature=0,
    model_name="gpt-4o-mini",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)    

memory = ConversationBufferWindowMemory(
    memory_key="chat_history",       # must match your prompt variable
    return_messages=True,            # returns messages in LangChain format
    k=10                             # number of messages to retain
)


parser = PydanticOutputParser(pydantic_object=AgentResponse)



prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are Mike. You play Baseball and you are a student at University of Data Lab. You are friendly and funny.
            Answer the user query and use tools if needed. You have access to chat history(you have memory of last messages) and to two tools:
            1. SentimentClassifier — for analyzing emotional tone.
            2. RAGRetriever — for retrieving factual information from document with bio about 'student' or 'Vitalii Kozak'.
            Use SentimentClassifier only when the user asks about emotions, reactions, sentiment or provides text that clearly needs emotional evaluation.
            Use RAGRetriever only when the user asks for factual information, bio, or document-based answers about student "Vitalii Kozak".
            If the query is general knowledge or conversational and does not require a tool, respond directly.
            Wrap the output in this format and provide no other text\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [sentiment_tool, rag_tool]
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools,
    
)

agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)

#query = input("What can i help you research?")
#raw_response = agent_executor.invoke({"query": query})



def run_agent(user_input_str, agent=agent_executor):
    user_input_dict = {"query": user_input_str}

    response = agent.invoke(user_input_dict)
    #logging.info(f"User: {user_input}\nAgent Raw: {response}\n---")

    try:
        structured_response = parser.parse(response.get("output"))  #[0]["text"] 
        #print(structured_response)
        return structured_response.FinalAnswer
    except Exception as e:
        #print("Error parsing response", e, "Raw Response - ", response)
        error_message = f"Error occurred: {e}. Raw Response - {response}"
        return error_message

  

