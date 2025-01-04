from model import generate_response

import asyncio
from typing import List
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
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