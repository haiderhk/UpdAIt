from data_ingestion.vector_db import get_vector_store
from data_ingestion.utils.utils import get_website_html
from data_ingestion.scraper import get_articles_publication_dates, extract_images_urls

THE_BATCH_URL = "https://www.deeplearning.ai/the-batch/"

def process_vector_store_metadatas():
    base_url_html = get_website_html(THE_BATCH_URL)
    vector_store = get_vector_store()
    vector_db = vector_store.get()
    metadatas = vector_db['metadatas']
    articles_metadatas = []
    for metadata in metadatas:
        if metadata['source'] == 0:
            articles_metadatas.append(metadata)

    articles_metadatas = sorted(articles_metadatas, key = lambda x: x['article_link'])
    articles_metadatas.reverse()
    articles_metadatas = [{k: v for k, v in met.items() if k != "source" and k != "chunk_heading"} for met in articles_metadatas]

    articles_dates = get_articles_publication_dates(base_url_html)
    
    dates_metadatas = []
    for metadata in zip(articles_metadatas, articles_dates):
        new_metadata = metadata[0]
        new_metadata["article_publication_date"] = metadata[1]
        dates_metadatas.append(new_metadata)

    image_urls = extract_images_urls(base_url_html)

    final_metadata = []
    for met in zip(dates_metadatas, image_urls):
        met[0]["article_image_url"] = met[1]
        final_metadata.append(met[0])

    return final_metadata






