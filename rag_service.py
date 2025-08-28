# rag_service.py
from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from RAG_tool import build_rag_tool

app = FastAPI()


class QueryPayload(BaseModel):
    query: str = Field(
        ...,
        example="Summarize the student's research interests"
    )

rag_tool = build_rag_tool("student_bio.txt")    


'''
@app.post("/retrieve")
async def retrieve(request: Request):
    data = await request.json()
    query = data["query"]
    result = rag_tool.func(query)
    return {"context": result}
'''
# 3. Use the Pydantic model as the function parameter
@app.post("/retrieve")
async def retrieve(payload: QueryPayload):
    context = rag_tool.func(payload.query)
    if not context:
        context = "No relevant information found in the document."
    return {"context": context}
    


# 4. Health check endpoint
@app.get("/")
def root():
    return {"message": "Rag service is running"}
