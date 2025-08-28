# agent_service.py
from fastapi import FastAPI, Request
import requests
from pydantic import BaseModel, Field
#from agent_setup import agent_executor, parser
from agent_setup import run_agent

app = FastAPI()

#SENTIMENT_URL = "http://localhost:8000/classify"
#RAG_URL = "http://localhost:8001/retrieve"

SENTIMENT_URL = "http://127.0.0.1:8000/classify"
RAG_URL = "http://127.0.0.1:8001/retrieve"

def call_sentiment(text: str):
    response = requests.post(SENTIMENT_URL, json={"text": text})
    return response.json()

def call_rag(query: str):
    response = requests.post(RAG_URL, json={"query": query})
    return response.json()["context"]


class ChatPayload(BaseModel):
    query: str = Field(
        ...,
        example="Hi, can you summarize what you know about Vitalii?"
    )

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
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data["query"]
    answer = run_agent(user_input)
    return {"answer": answer}
'''
@app.get("/")
def root():
    return {"message": "Agent service is running"}