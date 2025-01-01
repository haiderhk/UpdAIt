import os, time
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from utils.utils import get_article_chunks, parse_article_index, create_metadata


def get_vector_store():
    embeddings = OpenAIEmbeddings(model = "text-embedding-3-small")
    return Chroma(collection_name="articles_collection", embedding_function=embeddings, persist_directory="./vector_db")

def add_articles_to_vector_db(dir_name, vector_store, all_articles_links, all_articles_titles):
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