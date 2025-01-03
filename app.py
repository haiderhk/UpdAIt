from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from langchain_openai import ChatOpenAI
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain

from data_ingestion.ingestion import get_vector_store
from dotenv import load_dotenv

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

app = FastAPI()

load_dotenv()

llm = ChatOpenAI(model = "gpt-4o-mini", temperature=0.5, max_tokens = 256)
vector_store = get_vector_store()
retriever = vector_store.as_retriever()
chain = RetrievalQAWithSourcesChain.from_llm(llm = llm, retriever = retriever)


@app.get('/')
def root():
    return {"message": "Welcome to the DeepLearning.AI InfoHub v2!"}

@app.post('/query', response_model=QueryResponse)
def query(request: QueryRequest):
    try:
        result = chain.invoke({"question": request.question}, return_only_outputs = True)
        return QueryResponse(answer=result['answer'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))











# from utils.utils import get_website_html, save_all_articles_text
# from data_ingestion.vector_db import get_vector_store, add_articles_to_vector_db
# from data_ingestion.scraper import get_featured_article_link, get_articles_links, get_article_titles

# THE_BATCH_URL = "https://www.deeplearning.ai/the-batch/"

# llm = ChatOpenAI(model = "gpt-4o-mini", max_tokens = 256, temperature=0.5)
# vector_store = get_vector_store()

# home_page_html = get_website_html(THE_BATCH_URL)
# unfeatured_articles_links = get_articles_links(home_page_html)
# featured_article_link = get_featured_article_link(home_page_html)
# all_articles_links = [featured_article_link] + unfeatured_articles_links
# all_articles_titles = get_article_titles(home_page_html)

# print(f"Successfully retrieved {len(all_articles_links)} article(s) and {len(all_articles_titles)} title(s)\n")

# dir_name="saved_articles"
# save_all_articles_text(all_articles_links, dir_name)
# add_articles_to_vector_db(dir_name, vector_store, all_articles_links, all_articles_titles)
# print("Articles Successfully ingested to vector db.")


# query = input("What would you like to know? ")
# chain = RetrievalQAWithSourcesChain.from_llm(llm = llm, retriever = vector_store.as_retriever())

# results = chain.invoke({"question": query}, return_only_outputs = True)

# print(results['answer'])


#---------------------#
#                     #
#     STUFF TO DO     #
#                     #
#---------------------#

# 1. Check on user given input.
# 2. On every python app.py it shouldn't scrape. Perhaps it should check the directory first.
# 3. Or ask GPT for better ideas related to production as CRON jobs might be a thing later when putting into production.
# 3. Create a Flask application
# 4. SwiftUI time.