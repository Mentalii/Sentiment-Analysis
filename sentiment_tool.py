from transformers import pipeline
from langchain.tools import Tool


# Load your fine-tuned model
classifier = pipeline(
    "text-classification", 
    model="Mentalii/sentiment-tweets-pos-neg-epoch3"
)

def classify_sentiment(text):
    result = classifier(text)[0]
    print(f"🧠 Sentiment Analysis → Label: {result['label']}, Score: {result['score']:.4f}")
    return result

# Wrap it as a LangChain Tool
sentiment_tool = Tool(
    name="SentimentClassifier",
    func=classify_sentiment,
    description="Use this tool to analyze the sentiment of a given text. Only use when sentiment is explicitly requested or implied. Otherwise, respond directly without using this tool."
)
