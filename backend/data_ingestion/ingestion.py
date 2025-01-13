from backend.data_ingestion.scraper import Scraper
from backend.data_ingestion.vector_db import VectorDB
from backend.data_ingestion.config import THE_BATCH_URL, ARTICLES_DIRECTORY
from backend.data_ingestion.utils import save_articles


def ingest_articles():
    scraper = Scraper(THE_BATCH_URL)
    vector_db = VectorDB()

    links = scraper.get_all_links()
    titles = scraper.get_all_titles()

    save_articles(scraper, links)
    vector_db.add_articles(ARTICLES_DIRECTORY, links, titles)

    print("\n\n***** ARTICLES SUCCESSFULLY INGESTED *****\n\n")



