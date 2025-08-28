# remote_tools.py
import requests
from langchain.tools import Tool

SENTIMENT_URL = "http://127.0.0.1:8000/classify"
RAG_URL = "http://127.0.0.1:8001/retrieve"

def remote_sentiment(text: str):
    response = requests.post(SENTIMENT_URL, json={"text": text})
    return response.json()

def remote_rag(query: str):
    try:
        response = requests.post(RAG_URL, json={"query": query})
        data = response.json()
        return data.get("context", "No relevant information found in the document.")
    except Exception as e:
        return f"Error retrieving context: {e}"

sentiment_tool = Tool(
    name="SentimentClassifier",
    func=remote_sentiment,
    description="Use this tool to analyze the sentiment of a given text  via the Sentiment microservice. Only use when sentiment is explicitly requested or implied. Otherwise, respond directly without using this tool."
)

rag_tool = Tool(
    name="RAGRetriever",
    func=remote_rag,
    description="Use this tool to answer factual questions about the student 'Vitalii Kozak' strictly from retrieved context in document 'student_bio.txt'. Only use when the user asks for knowledge, bio, or explanation about student.If no relevant context is found, respond with 'No relevant information found in the document.'"
)