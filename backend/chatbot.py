from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from fastapi.middleware.cors import CORSMiddleware
from embedding_function import get_embedding_function
import logging

# Initialize FastAPI application
app = FastAPI()

# Add middleware to handle cross-origin requests (CORS configuration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust according to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set logging configuration (Adjust log level and format as needed)
logging.basicConfig(level=logging.INFO)  # Set log level to INFO for normal use, DEBUG for more detailed logs
logger = logging.getLogger(__name__)

# Define the path for the Chroma database (adjust if using a different location or setup)
CHROMA_PATH = "chroma"  # This should point to your Chroma database location

# Template for generating prompt to be sent to the model (modify as per your needs)
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

class QueryRequest(BaseModel):
    query_text: str 

# Function to initialize and return the Chroma database instance
async def get_db() -> Chroma:
    embedding_function = get_embedding_function()  
    return Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function) 

# Function to process the RAG query without caching (can be customized for optimization)
async def query_rag(query_text: str, db: Chroma):
    try:
        # Perform a similarity search in the database to find relevant documents
        search_results = db.similarity_search_with_score(query_text, k=5) 
        # Combine search results into a single context string for the prompt
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in search_results]) 

        # Create the prompt based on the chosen template
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)  
        prompt = prompt_template.format(context=context_text, question=query_text)

        # Generate response using the model
        model = Ollama(model="llama3.1")  
        response_text = model.invoke(prompt) 

        sources = [doc.metadata.get("id", "Unknown ID") for doc, _ in search_results]
        response = {"response": response_text, "sources": sources}

        return response

    except Exception as e:
        logger.error(f"Error during RAG query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error during query processing: {str(e)}")

# Define the endpoint for the FastAPI application
@app.post("/api/v1/query/")
async def handle_query(request: QueryRequest, db: Chroma = Depends(get_db)):
    try:
        # Query the RAG model and return the result
        result = await query_rag(request.query_text, db)
        return result

    except HTTPException as e:
        logger.error(f"HTTP Error: {str(e.detail)}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Unexpected error occurred.")

