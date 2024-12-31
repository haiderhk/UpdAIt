import requests
from bs4 import BeautifulSoup

def get_article_titles(base_url_html):
    soup = BeautifulSoup(base_url_html, "html.parser")
    articles_titles = []
    article_cards = soup.select("div.p-6")
    for card in article_cards:
        h2_tag = card.find("h2")
        if not h2_tag:
            continue
        title = h2_tag.get_text(strip=True)
        articles_titles.append(title)
    return articles_titles

def get_featured_article_link(base_url_html):
    base_url = "https://www.deeplearning.ai"
    soup = BeautifulSoup(base_url_html, "html.parser")
    featured_article_div = soup.find("div", class_ = "col-span-1 lg:col-span-2")
    link = featured_article_div.find_all("a", href=True)
    if len(link) < 2:
        print("There was a problem fetching featured article's link")
        return ""
    return base_url + link[1]['href']

def get_articles_links(base_url_html):
    base_url = "https://www.deeplearning.ai"
    soup = BeautifulSoup(base_url_html, "html.parser")
    article_links = []
    article_cards = soup.select("div.p-6")
    for card in article_cards:
        a_tag = card.find_all("a", href=True)
        if len(a_tag) < 2:
            print("Invalid article link (It is probably a featured article)...continuing")
            continue
        article_links.append(base_url + a_tag[1]["href"])
    return article_links

def get_formatted_article_text(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Could not fetch article with the URL {url}")
        return ""
    
    soup = BeautifulSoup(response.text, "html.parser")
    print("Successfully fetched the article with link: ", url)

    article_content = soup.find("div", class_ = "prose--styled justify-self-center post_postContent__wGZtc")

    if article_content:
        print(f"\tExtracting text...")
        def preserve_links(tag):
            """
            Replace each <a> with its text (surrounded by spaces to avoid concatenation).
            Then gather all text from the tag.
            """
            for a_tag in tag.find_all("a"):
                link_text = a_tag.get_text(strip=True)
                a_tag.replace_with(f" {link_text} ")
            return " ".join(tag.stripped_strings)
        
        content = {}
        content["Introduction"] = []
        current_heading = None

        for elem in article_content.find_all(['h1', 'p', 'ul'], recursive=True):
            if elem.name == 'h1':
                heading_text = preserve_links(elem)
                current_heading = heading_text
                content[current_heading] = []

            elif elem.name == 'p': 
                paragraph_text = preserve_links(elem) 
                if current_heading:
                    content[current_heading].append(paragraph_text)
                else:
                    content["Introduction"].append(paragraph_text)
            elif elem.name == "ul":
                # For lists, each <li> is appended as a bullet item
                list_items = elem.find_all("li", recursive=False)
                for li in list_items:
                    bullet_text = preserve_links(li)
                    bullet_line = f"- {bullet_text}"
                    if current_heading:
                        content[current_heading].append(bullet_line)
                    else:
                        content["Introduction"].append(bullet_line)
        
        formatted_content_list = []
        for heading, paragraphs in content.items():
            # Skip empty headings
            if not paragraphs:
                continue

            # Build a string for each heading
            section_text = f"## {heading}\n" + "\n".join(paragraphs)
            formatted_content_list.append(section_text)

        formatted_content = "\n\n".join(formatted_content_list)

        print("Formatted Content for LLM:")
        return formatted_content
        # print(formatted_content)
    else:
        print("Could not find the main article content container for link: ", url)
        return ""





















# # Base URL
# base_url = "https://www.deeplearning.ai"
# page = requests.get(base_url)

# # Parse the main page
# soup = BeautifulSoup(page.content, "html.parser")

# def get_featured_article():
#     # Locate the link for the featured article
#     featured_article_tag = soup.find("a", href="/the-batch/issue-281/")
#     featured_article_link = featured_article_tag['href'] if featured_article_tag else None

#     if featured_article_link:
#         full_url = base_url + featured_article_link
#         print(f"Featured Article URL: {full_url}")

#         # Navigate into the article
#         response = requests.get(full_url)

#         # Ensure we actually got a response to the article
#         if response.status_code == 200:
#             article_soup = BeautifulSoup(response.text, "html.parser")
#             print("Successfully fetched the featured article page!")

#             # Locate the main content container
#             article_content = article_soup.find("div", class_="prose--styled justify-self-center post_postContent__wGZtc")

#             if article_content:

#                 def preserve_links(tag):
#                     """
#                     Replace each <a> with its text (surrounded by spaces to avoid concatenation).
#                     Then gather all text from the tag.
#                     """
#                     for a_tag in tag.find_all("a"):
#                         link_text = a_tag.get_text(strip=True)
#                         a_tag.replace_with(f" {link_text} ")
#                     return " ".join(tag.stripped_strings)

#                 # We'll store content in a dict: { heading: [list_of_paragraphs_or_bullets] }
#                 content = {}
#                 content["Introduction"] = []  # paragraphs before the first H1
#                 current_heading = None

#                 # We include <h1>, <p>, and <ul> in the search so we can capture bullet points as well.
#                 for elem in article_content.find_all(["h1", "p", "ul"], recursive=True):
#                     if elem.name == "h1":
#                         # Start a new section
#                         heading_text = preserve_links(elem)
#                         # If we haven't stored anything yet, that means it's the first heading.
#                         # We'll create a new list in the dict for this heading.
#                         current_heading = heading_text
#                         content[current_heading] = []

#                     elif elem.name == "p":
#                         # Paragraph text
#                         paragraph_text = preserve_links(elem)
#                         if current_heading:
#                             # Add paragraph to the current heading
#                             content[current_heading].append(paragraph_text)
#                         else:
#                             # If no heading yet, this belongs to Introduction
#                             content["Introduction"].append(paragraph_text)

#                     elif elem.name == "ul":
#                         # For lists, each <li> is appended as a bullet item
#                         list_items = elem.find_all("li", recursive=False)
#                         for li in list_items:
#                             bullet_text = preserve_links(li)
#                             bullet_line = f"- {bullet_text}"
#                             if current_heading:
#                                 content[current_heading].append(bullet_line)
#                             else:
#                                 content["Introduction"].append(bullet_line)

#                 # Create a formatted version for the LLM
#                 # If a heading has no content, skip it. If Introduction is empty, skip it.
#                 formatted_content_list = []
#                 for heading, paragraphs in content.items():
#                     # Skip empty headings
#                     if not paragraphs:
#                         continue

#                     # Build a string for each heading
#                     section_text = f"## {heading}\n" + "\n".join(paragraphs)
#                     formatted_content_list.append(section_text)

#                 formatted_content = "\n\n".join(formatted_content_list)

#                 print("Formatted Content for LLM:")
#                 return formatted_content
#                 # print(formatted_content)

#             else:
#                 print("Could not find the main article content container.")
#                 return None
#     else:
#         print(f"Failed to fetch the article. Status code: {response.status_code}")
#         return None