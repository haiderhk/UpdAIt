import re
from urllib.parse import unquote
from langchain.text_splitter import MarkdownTextSplitter


def extract_original_url(url_str):
    match = re.search(r'url=(.*?)(?:&amp;|&)', url_str)
    if match:
        return unquote(match.group(1))
    return None


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