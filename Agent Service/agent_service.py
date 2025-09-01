# agent_service.py
from fastapi import FastAPI
import requests
from pydantic import BaseModel, Field
#from agent_setup import agent_executor, parser
from agent_setup import run_agent
from typing import List, Dict, Any

class MCPContext(BaseModel):
    conversation_id: str = ""
    history: List[Dict[str, Any]] = []

class MCPInput(BaseModel):
    query: str

class MCPRequest(BaseModel):
    context: MCPContext
    input: MCPInput

class MCPOutput(BaseModel):
    result: str

class MCPResponse(BaseModel):
    output: MCPOutput

app = FastAPI()

#SENTIMENT_URL = "http://localhost:8000/classify"
#RAG_URL = "http://localhost:8001/retrieve"

SENTIMENT_URL = "http://127.0.0.1:8000/classify"
RAG_URL = "http://127.0.0.1:8001/retrieve"





# We updated this endpoint to match the MCP request/response format

'''
class ChatPayload(BaseModel):
    query: str = Field(
        ...,
        example="Hi, can you summarize what you know about Vitalii?"
    )
'''
''' 
@app.post("/chat")
async def chat(payload: ChatPayload):
    """
    Receives a user query, invokes the agent,
    and returns the agent's answer.
    """
    user_input = payload.query

    # If your run_agent needs the helper functions, you can pass them in:
    answer = run_agent(user_input)

    return {"answer": answer}
'''
@app.post("/chat", response_model=MCPResponse)
async def chat(payload: MCPRequest):
    """
    Receives an MCP request, invokes the agent,
    and returns an MCP response.
    """
    user_input = payload.input.query

    # Optionally, you can use context/history for advanced memory
    answer = run_agent(user_input)

    return MCPResponse(output=MCPOutput(result=answer))


@app.get("/")
def root():
    return {"message": "Agent service is running"}