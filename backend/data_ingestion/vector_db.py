import os, time
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from config import EMBEDDING_MODEL, ARTICLES_COLLECTION_NAME, VECTOR_STORE_DIR
from utils import get_article_chunks, parse_article_index, extract_chunk_heading

class VectorDB:
    def __init__(self):
        embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

        self.vector_store = Chroma(
            collection_name=ARTICLES_COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=VECTOR_STORE_DIR
        )

    def add_articles(self, dir_name, all_articles_links, all_articles_titles):
        for filename in os.listdir(dir_name):
            if not filename.endswith(".txt"):
                # print("Skipping: ", filename)
                continue
            filepath = os.path.join(dir_name, filename)
            with open(filepath, "r") as myfile:
                article_text = myfile.read()
                docs = get_article_chunks(article_text)
                article_index = parse_article_index(myfile.name)
                print(article_index)
                print(f"Length of docs of article with index {article_index} = {len(docs)}")
                metadatas, ids = self.create_metadata(docs, article_index, all_articles_links, all_articles_titles)
                print(ids)
            self.vector_store.add_texts(texts=docs, ids=ids, metadatas=metadatas)
            time.sleep(0.5)

    def create_metadata(self, docs, article_index, all_articles_links, all_articles_titles):
        ids = []
        metadatas = []

        article_link = all_articles_links[article_index]
        article_title = all_articles_titles[article_index]
        
        for index, doc in enumerate(docs):
            heading = extract_chunk_heading(doc)
            metadatas.append(
                {
                    "chunk_heading": heading,
                    "source": index,
                    "article_title": article_title, 
                    "article_link": article_link
                })
            ids.append(f"id{article_index}_{index}")
        return metadatas, ids