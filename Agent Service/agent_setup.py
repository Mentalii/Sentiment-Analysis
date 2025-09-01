
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
            Use RAGRetriever only when the user asks for factual information, bio, or document-based answers about student "Vitalii Kozak". Each time you use this tool inform about it: write "RAG tool was used".
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

  

