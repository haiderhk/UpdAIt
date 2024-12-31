import re, os, time
from bs4 import BeautifulSoup
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from dotenv import load_dotenv

load_dotenv()

from utils import get_website_html, save_all_articles_text, get_article_chunks, parse_article_index, create_metadata
from scraper import get_featured_article_link, get_articles_links, get_article_titles, get_formatted_article_text

BASE_URL = "https://www.deeplearning.ai"
THE_BATCH_URL = "https://www.deeplearning.ai/the-batch/"

llm = ChatOpenAI(model = "gpt-4o-mini", max_tokens = 256, temperature=0.5)
embeddings = OpenAIEmbeddings(model = "text-embedding-3-small")

vector_store = Chroma(collection_name="articles_collection", embedding_function=embeddings)

home_page_html = get_website_html(THE_BATCH_URL)

unfeatured_articles_links = get_articles_links(home_page_html)
featured_article_link = get_featured_article_link(home_page_html)

all_articles_links = [featured_article_link] + unfeatured_articles_links
all_articles_titles = get_article_titles(home_page_html)
print(f"Successfully retrieved {len(all_articles_links)} article(s) and {len(all_articles_titles)} title(s)\n")

dir_name="saved_articles"

save_all_articles_text(all_articles_links, dir_name)

for filename in os.listdir(dir_name):
    if not filename.endswith(".txt"):
        # print("Skipping: ", filename)
        continue
    filepath = os.path.join(dir_name, filename)
    with open(filepath, "r") as myfile:
        print(myfile.name)
        article_text = myfile.read()
        docs = get_article_chunks(article_text)
        article_index = parse_article_index(myfile.name)
        print(article_index)
        print(f"Length of docs of article with index {article_index} = {len(docs)}")
        metadatas, ids = create_metadata(docs, article_index, all_articles_links, all_articles_titles)
        print(ids)
    vector_store.add_texts(texts=docs, ids=ids, metadatas=metadatas)
    time.sleep(0.5)


query = input("What would you like to know? ")
chain = RetrievalQAWithSourcesChain.from_llm(llm = llm, retriever = vector_store.as_retriever())

results = chain.invoke({"question": query}, return_only_outputs = True)

print(results[0].page_content)


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