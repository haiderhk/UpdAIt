from data_ingestion.utils.utils import get_website_html, save_all_articles_text
from data_ingestion.vector_db import get_vector_store, add_articles_to_vector_db
from data_ingestion.scraper import get_featured_article_link, get_articles_links, get_article_titles, get_articles_images_descriptions

THE_BATCH_URL = "https://www.deeplearning.ai/the-batch/"


vector_store = get_vector_store()
home_page_html = get_website_html(THE_BATCH_URL)
unfeatured_articles_links = get_articles_links(home_page_html)
featured_article_link = get_featured_article_link(home_page_html)
all_articles_links = [featured_article_link] + unfeatured_articles_links
all_articles_titles = get_article_titles(home_page_html)
print("Getting images and descriptions")
all_articles_images = get_articles_images_descriptions(home_page_html)

print(f"Successfully retrieved {len(all_articles_links)} article(s) and {len(all_articles_titles)} title(s) with images descriptions of length {len(all_articles_images)} (Sample description: {all_articles_images[7]})\n")

dir_name="saved_articles"
save_all_articles_text(all_articles_links, dir_name)
add_articles_to_vector_db(dir_name, vector_store, all_articles_links, all_articles_titles)
print("Articles Successfully ingested to vector db.")