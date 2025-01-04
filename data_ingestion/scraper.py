import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.deeplearning.ai"

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
    soup = BeautifulSoup(base_url_html, "html.parser")
    featured_article_div = soup.find("div", class_ = "col-span-1 lg:col-span-2")
    link = featured_article_div.find_all("a", href=True)
    if len(link) < 2:
        print("There was a problem fetching featured article's link")
        return ""
    return BASE_URL + link[1]['href']


def get_articles_images_descriptions(base_url_html):
    soup = BeautifulSoup(base_url_html, "html.parser")
    article_images_descriptions = []
    article_cards = soup.find_all("div", class_="aspect-w-16 aspect-h-9 rounded-t-lg overflow-hidden bg-slate-200")
    for card in article_cards:
        img_tag = card.find("img")
        if img_tag:
            image_description_tag = card.find_next("alt")
            image_description = image_description_tag.get_text(strip=True) if image_description_tag else "No Title found"

            article_images_descriptions.append(image_description)
        else:
            print("No image description found for this article")

    return article_images_descriptions

def get_articles_links(base_url_html):
    soup = BeautifulSoup(base_url_html, "html.parser")
    article_links = []
    article_cards = soup.select("div.p-6")
    for card in article_cards:
        a_tag = card.find_all("a", href=True)
        if len(a_tag) < 2:
            print("Invalid article link (It is probably a featured article)...continuing")
            continue
        article_links.append(BASE_URL + a_tag[1]["href"])
    return article_links

def get_formatted_article_text(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Could not fetch article with the URL {url}")
        return ""
    
    soup = BeautifulSoup(response.text, "html.parser")
    print("Fetching article text with link: ", url)

    article_content = soup.find("div", class_ = "prose--styled justify-self-center post_postContent__wGZtc")

    if article_content:
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
        return formatted_content
        # print(formatted_content)
    else:
        print("Could not find the main article content container for link: ", url)
        return ""