from langchain_openai import ChatOpenAI
from backend.data_ingestion.vector_db import VectorDB

class LLMManager:
    def __init__(self, model="gpt-4o-mini", temperature=0.8, max_tokens=1024):
        self.llm = ChatOpenAI(model=model, temperature=temperature, max_tokens=max_tokens)
        self.vector_db = VectorDB()
        self.retriever = self.vector_db.vector_store.as_retriever()

    def get_llm(self):
        return self.llm

    def get_retriever(self):
        return self.retriever

    def get_vector_db(self):
        return self.vector_db