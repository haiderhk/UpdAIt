import re
from urllib.parse import unquote


def extract_original_url(url_str):
    match = re.search(r'url=(.*?)(?:&amp;|&)', url_str)
    if match:
        return unquote(match.group(1))
    return None