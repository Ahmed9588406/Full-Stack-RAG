from fastapi import FastAPI
from fastapi.responses import JSONResponse
from rag import get_answer_and_docs
from qdrant import upload_website_to_collection
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(
    title="RAG API",
    description="A simple RAG API",
    version="0.1",
    
)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message:str

@app.get("/",tags=["root"])
async def root():
    return {"message":"Hello World"}

@app.post("/chat",tags=["chat"], description="Chat with the RAG API through this endpoint")
async def chat(message: Message):
    try:
        response = get_answer_and_docs(message.message)
        response_content = {
            "status": "success",
            "data": {
                "question": message.message,
                "answer": response["answer"],
                "documents": [doc.dict() for doc in response["context"]]
            }
        }
        return JSONResponse(content=response_content, status_code=200)
    except Exception as e:
        error_content = {
            "status": "error",
            "message": str(e)
        }
        return JSONResponse(content=error_content, status_code=500)

@app.post("/indexing",tags=["upload-url"],description="Index a website through this endpoints")
def indexing(url:str):
    try:
        response = upload_website_to_collection(url)
        return JSONResponse(content={"response":response},status_code=200)
    
    except Exception as e:
        return JSONResponse(content={"error":str(e)}, status_code=400)