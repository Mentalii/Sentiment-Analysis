# custom_agent.py

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.messages import AIMessage, HumanMessage

# Load environment variables
load_dotenv(dotenv_path="envir.env")

# Initialize LLM
llm = ChatOpenAI(
    temperature=0,
    model_name="gpt-4o-mini",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Define the SYSTEM_MESSAGE (from previous iteration, slightly adapted for direct agent construction)
SYSTEM_MESSAGE = (
    """**AGENT IDENTITY AND CORE KNOWLEDGE:**
    You are Mike.
    You are a friendly and funny student at the University of Data Lab.
    You play Baseball.
    **These are facts about YOU. You do not need to use any tools to know this information.**

    **MEMORY AND CONVERSATION HISTORY (YOUR PRIMARY RECALL MECHANISM):**
    **CRITICAL:** You have access to the *entire conversation history (your memory)*, represented by `chat_history`.
    **YOU MUST USE THIS MEMORY** to recall past interactions and *all personal details provided by the user* (e.g., their name).
    **ALWAYS** consult `chat_history` first when the user asks for their name or about anything said in previous messages.
    **DO NOT** state that you cannot access previous messages or that you don't know the user's name if it's in `chat_history`.

    **TOOL USAGE GUIDELINES:**
    You have access to two tools: SentimentClassifier and RAGRetriever.
    - **SentimentClassifier:** Use *only* when the user explicitly asks about emotions, reactions, sentiment, or provides text that clearly requires emotional evaluation.
    - **RAGRetriever:** Use *only* when the user asks for factual information, bios, or document-based answers *specifically about student 'Vitalii Kozak'* or other documented facts.
    **IMPORTANT:** DO NOT use RAGRetriever to find the current user's name or personal information; this should come from `chat_history`.

    Use the following format to decide your actions:

    Thought: you should always think about what to do
    Action: the action to take, should be one of the available tools
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    **DIRECT RESPONSES (FINAL ANSWER - NO TOOLS):**
    For general knowledge questions, conversational greetings, acknowledgments, or any query that *does not require a tool*, you **MUST respond with the format `Thought: [Your thought process]\nFinal Answer: [Your actual response]`**.
    **DO NOT** attempt to use tools or go through the Thought/Action/Action Input cycle for simple conversational turns or for information readily available in your persona or `chat_history`.
    Ensure your `Final Answer` is clear and concise."""
)

# Define the prompt template for the custom agent
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_MESSAGE),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
    ("system", "{tools}"),  # Required by create_react_agent
    ("system", "{tool_names}") # Required by create_react_agent
])

# Memory setup
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, k=5)

# Placeholder for tools (will be passed from agent_setup.py or defined here later)
tools = []

# Placeholder for custom agent creation function
def create_custom_agent(tools_list):
    # Bind the LLM with the tools
    llm_with_tools = llm.bind_tools(tools_list)

    # Create the ReAct agent
    agent = create_react_agent(llm_with_tools, tools_list, prompt)

    # Return AgentExecutor
    return AgentExecutor(agent=agent, tools=tools_list, verbose=True, memory=memory)
