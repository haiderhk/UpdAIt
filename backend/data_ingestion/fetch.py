from data_ingestion.vector_db import VectorDB
from data_ingestion.scraper import Scraper
from data_ingestion.metadata_schema import ArticleMetadata
from data_ingestion.config import THE_BATCH_URL

def process_vector_store_metadatas():
    scraper = Scraper(THE_BATCH_URL)
    vectordb = VectorDB()

    metadatas = vectordb.get_metadatas()
    articles_metadatas = []
    for metadata in metadatas:
        if metadata['source'] == 0:
            articles_metadatas.append(metadata)

    articles_metadatas = sorted(articles_metadatas, key = lambda x: x['article_link'])
    articles_metadatas.reverse()
    articles_metadatas = [{k: v for k, v in met.items() if k != "source" and k != "chunk_heading"} for met in articles_metadatas]

    publication_dates = scraper.get_all_publication_dates()
    image_urls = scraper.get_all_images_urls()
    
    final_metadata = []
    
    for metadata, pub_date, image_url in zip(articles_metadatas, publication_dates, image_urls):
        final_metadata.append(ArticleMetadata(
            article_link=metadata.get("article_link"),
            article_title=metadata.get("article_title"),
            article_image_url=image_url,
            article_publication_date=pub_date
        ))

    return final_metadata