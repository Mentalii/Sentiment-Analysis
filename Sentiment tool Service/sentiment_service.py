# sentiment_service.py
from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from transformers import pipeline

app = FastAPI()
classifier = pipeline(
    "text-classification",
    model="Mentalii/sentiment-tweets-pos-neg-epoch3"
    )

# 1. Define a Pydantic model for the request body
class TextPayload(BaseModel):
    text: str = Field(
        ...,
        example="I absolutely love this!"
    )

# 2. Create a POST endpoint that uses the Pydantic model
@app.post("/classify")
async def classify(payload: TextPayload):
    result = classifier(payload.text)[0]
    return result

@app.get("/")
def root():
    return {"message": "Sentiment service is running"}