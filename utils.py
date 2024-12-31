import requests, re
from langchain.text_splitter import MarkdownTextSplitter

def get_website_html(url):
    response = requests.get(url)
    return response.text


def get_article_chunks(article_text):
    markdown_splitter = MarkdownTextSplitter(chunk_size = 2000, chunk_overlap = 200)
    docs = markdown_splitter.split_text(article_text)
    return docs


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
        
