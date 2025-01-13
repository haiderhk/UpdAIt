from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from backend.model.schema import QuestionAnswers
from backend.model.generator import Generator
from backend.data_ingestion.fetch import process_vector_store_metadatas

# Initialize the router
router = APIRouter()
generator = Generator()

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


@router.get("/")
def root():
    return {"message": "Welcome to the DeepLearning.AI InfoHub v2!"}

@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    try:
        result, metadata = await generator.generate_response(request.question)
        return QueryResponse(answer=result, metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/fetch")
def fetch_articles():
    articles = process_vector_store_metadatas()
    return {"articles": articles}

@router.post("/generate-questions", response_model=QuestionAnswers)
def questions(request: QuestionsRequestModel):
    questions = generator.generate_questions(request.article_link)
    return {"questions": questions}