#from langchain.vectorstores import FAISS
from langchain_community.vectorstores import FAISS
#from langchain.embeddings import HuggingFaceEmbeddings
#from langchain_community.embeddings import HuggingFaceEmbeddings 
from langchain_huggingface import HuggingFaceEmbeddings
#from langchain.document_loaders import TextLoader
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.tools import Tool

# Step 1: Load and split documents
def load_documents(file_path: str) -> list[Document]:
    loader = TextLoader(file_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(docs)


#import os
#from dotenv import load_dotenv

#load_dotenv(dotenv_path="envir.env")

# Step 2: Embed and store in FAISS
def create_vector_store(docs: list[Document]) -> FAISS:
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2") #We using free embedding model
    return FAISS.from_documents(docs, embeddings)

# Step 3: Define retrieval function
def retrieve_context(query: str, vector_store: FAISS) -> str:
    results = vector_store.similarity_search(query, k=3)
    return "\n---\n".join([doc.page_content for doc in results])

# Step 4: Wrap as LangChain Tool
def build_rag_tool(file_path: str) -> Tool:
    docs = load_documents(file_path)
    store = create_vector_store(docs)

    def rag_function(query: str) -> str:
        context = retrieve_context(query, store)
        return f"Retrieved context:\n{context}"

    return Tool(
        name="RAGRetriever",
        func=rag_function,
        description="Use this tool to answer factual questions about the student 'Vitalii Kozak' strictly from retrieved context in document 'student_bio.txt'. Only use when the user asks for knowledge, bio, or explanation about student.If no relevant context is found, respond with 'No relevant information found in the document.'"
    )

