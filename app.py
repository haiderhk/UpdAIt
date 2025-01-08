# import data_ingestion.ingestion
from model.model import generate_response, generate_questions
from model.schema import QuestionAnswers
from data_ingestion.fetch import process_vector_store_metadatas

import uvicorn
import asyncio, os
from typing import List
from pyngrok import ngrok
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
load_dotenv()


class QueryRequest(BaseModel):
    question: str

class Metadata(BaseModel):
    article_link: str
    article_title: str
    chunk_heading: str
    score: float
class QueryResponse(BaseModel):
    answer: str
    metadata: List[Metadata]

class QuestionsRequestModel(BaseModel):
    article_link: str

app = FastAPI()

@app.get('/')
def root():
    return {"message": "Welcome to the DeepLearning.AI InfoHub v2!"}

@app.post('/query', response_model=QueryResponse)
async def query(request: QueryRequest):
    try:
        result, metadata = await generate_response(request.question)
        return QueryResponse(answer=result, metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get('/fetch')
def fetch_articles():
    articles = process_vector_store_metadatas()
    return {"articles": articles}

@app.post('/generate-questions', response_model=QuestionAnswers)
def questions(request: QuestionsRequestModel):
    questions = generate_questions(request.article_link)
    return {"questions": questions}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

if __name__ == "__main__":
    # Configure ngrok
    ngrok.set_auth_token(os.environ.get("NGROK_AUTH_TOKEN"))
    
    # Start ngrok tunnel to port 8000
    public_url = ngrok.connect(8000).public_url
    print(f"ngrok tunnel created at: {public_url}")
    print(f"Public URL for your API: {public_url}")
    
    # Start the FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=8000)