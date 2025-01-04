import requests, re, time, os
from langchain.text_splitter import MarkdownTextSplitter
from data_ingestion.scraper import get_formatted_article_text

def get_website_html(url):
    response = requests.get(url)
    return response.text


def get_article_chunks(article_text):
    markdown_splitter = MarkdownTextSplitter(chunk_size = 2000, chunk_overlap = 200)
    docs = markdown_splitter.split_text(article_text)
    return docs


def save_all_articles_text(all_articles_links, dir_name):
    os.makedirs(dir_name, exist_ok=True)
    saved_issues = set()
    
    for index, link in enumerate(all_articles_links):
        article_text = get_formatted_article_text(link)
        slug = re.sub(r'https?://[^/]+/', '', link)  # remove scheme and domain
        slug = slug.strip("/").replace("/", "_")     # turn '/the-batch/issue-281/' -> 'the-batch_issue-281'
        
        # Extract issue number from slug
        issue_match = re.search(r'issue-(\d+)', slug)
        if issue_match:
            issue_number = issue_match.group(1)
            if issue_number in saved_issues:
                print(f"Skipping duplicate issue: {issue_number}")
                continue
            saved_issues.add(issue_number)
        
        file_name = f"article_{index}_{slug}.txt"
        file_path = os.path.join(dir_name, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(article_text)
            print(f"Saved: {file_path}\n")
        time.sleep(1) # Delay to not overwhelm the server :)


def parse_article_index(filename: str) -> int:
    """
    Extracts the integer that follows 'article_' from a filename like:
      'article_12_the-batch_issue-269.txt'
    Returns 12 as int.
    """
    pattern = r"article_(\d+)_"
    match = re.search(pattern, filename)
    if match:
        return int(match.group(1))
    return None


def extract_chunk_heading(doc):
    if doc.startswith('##'):
        pattern = re.compile(r'^##\s+(.*)$', re.MULTILINE)
        match = pattern.search(doc)
        heading = match.group(1)
        return heading
    else:
        words = doc.split()
        first_four = words[:4]
        heading = ' '.join(first_four)
        return heading


def create_metadata(docs, article_index, all_articles_links, all_articles_titles):
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
        



def create_vector_store_response(docs):
    sources = []
    links = []

    for doc in docs:
        article_link = doc[0].metadata['article_link']
        article_title = doc[0].metadata['article_title']
        chunk_heading = doc[0].metadata['chunk_heading']
        score = doc[1]

        if article_link not in links:
            article_dict = {
                "article_link": article_link,
                "article_title": article_title,
                "chunk_heading": chunk_heading,
                "score": score
            }

            sources.append(article_dict)

            links.append(article_link)
    return sources
