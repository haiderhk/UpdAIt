import os, re, time
from urllib.parse import unquote
from langchain.text_splitter import MarkdownTextSplitter

from backend.data_ingestion.config import ARTICLES_DIRECTORY


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
    

def save_articles(scraper, links):
    os.makedirs(ARTICLES_DIRECTORY, exist_ok=True)
    saved_issues = set()
    
    for index, link in enumerate(links):
        article_text = scraper.format_article_text(link)
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
        file_path = os.path.join(ARTICLES_DIRECTORY, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(article_text)
            print(f"Saved: {file_path}\n")
        time.sleep(1) # Delay to not overwhelm the server :)



def retrieve_article_text(article_link, directory = "saved_articles"):
    slug = re.sub(r'https?://[^/]+/', '', article_link)  # remove scheme and domain
    slug = slug.strip("/").replace("/", "_")     # turn '/the-batch/issue-281/' -> 'the-batch_issue-281'
    for file in os.listdir(directory):
            if file.endswith(f"{slug}.txt"):
                print("File found, retrieving its text!")
                file_path = os.path.join(directory, file)
                with open(file_path, 'r') as article_file:
                    article_text = article_file.read()
                    return article_text
                
    print("File cannot be found!")
    return ""