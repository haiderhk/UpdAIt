import requests, re
from bs4 import BeautifulSoup
from urllib.parse import unquote
from backend.data_ingestion.config import BASE_URL
from backend.data_ingestion.utils import extract_original_url

class Scraper:
    def __init__(self, base_url):
        response = requests.get(base_url)
        self.homepage_html = response.text
        self.soup = BeautifulSoup(self.homepage_html, "html.parser")

    
    def get_featured_article_link(self):
        featured_article_div = self.soup.find("div", class_ = "col-span-1 lg:col-span-2")
        link = featured_article_div.find_all("a", href = True)
        if len(link) < 2:
            print("There was a problem fetching featured article's link")
            return ""
        return BASE_URL + link[1]['href']
    
    
    def get_all_links(self): #Excluding featured article
        article_links = []
        article_cards = self.soup.select("div.p-6")
        for card in article_cards:
            a_tag = card.find_all("a", href=True)
            if len(a_tag) < 2:
                print("Invalid article link (It is probably a featured article)...continuing")
                continue
            article_links.append(BASE_URL + a_tag[1]["href"])
        return article_links       
    
    
    def get_all_titles(self):
        articles_titles = []
        article_cards = self.soup.select("div.p-6")
        for card in article_cards:
            h2_tag = card.find("h2")
            if not h2_tag:
                continue
            title = h2_tag.get_text(strip=True)
            articles_titles.append(title)
        return articles_titles
    
    
    def _preserve_links_(self, tag):
        """
        Replace each <a> with its text (surrounded by spaces to avoid concatenation).
        Then gather all text from the tag.
        """
        for a_tag in tag.find_all("a"):
            link_text = a_tag.get_text(strip=True)
            a_tag.replace_with(f" {link_text} ")
        return " ".join(tag.stripped_strings)
    
    
    def format_article_text(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Could not fetch article with the URL {url}")
            return ""
        
        soup = BeautifulSoup(response.text, "html.parser")
        print("Fetching article text with link: ", url)

        article_content = soup.find("div", class_ = "prose--styled justify-self-center post_postContent__wGZtc")

        if article_content:
            content = {}
            content["Introduction"] = []
            current_heading = None

            for elem in article_content.find_all(['h1', 'p', 'ul'], recursive=True):
                if elem.name == 'h1':
                    heading_text = self._preserve_links_(elem)
                    current_heading = heading_text
                    content[current_heading] = []

                elif elem.name == 'p': 
                    paragraph_text = self._preserve_links_(elem) 
                    if current_heading:
                        content[current_heading].append(paragraph_text)
                    else:
                        content["Introduction"].append(paragraph_text)
                elif elem.name == "ul":
                    # For lists, each <li> is appended as a bullet item
                    list_items = elem.find_all("li", recursive=False)
                    for li in list_items:
                        bullet_text = self._preserve_links_(li)
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
        
    
    def get_all_publication_dates(self):
        article_dates = []
        featured_article_date = self.soup.find("div", class_ = "inline-flex rounded-md py-1 px-3 text-[13px] font-medium mb-3 relative z-10 bg-white text-slate-500")
        article_dates.append(featured_article_date.text)
        dates_div = self.soup.find_all("div", class_ = "inline-flex rounded-md py-1 px-3 text-[13px] font-medium mb-3 relative z-10 bg-slate-100 text-slate-500")
        for div in dates_div:
            article_dates.append(div.text)
        return article_dates
    
    
    def _get_featured_article_image_url_(self):
        noscript_img = self.soup.select_one("div.aspect-w-16 noscript img")

        if noscript_img and noscript_img.get('src'):
            src = noscript_img.get('src')
            # Extract everything between 'url=' and '&' or '&amp;'
            url_part = re.search(r'url=(.*?)(?:&amp;|&)', src).group(1)
            original_url = unquote(url_part)
            print("Featured image URL:", original_url)
            return original_url
        else:
            print("Could not find the featured image URL")
            return ""
    
    
    def get_all_images_urls(self):
        image_urls = []
        image_urls.append(self._get_featured_article_image_url_())
        article_divs = self.soup.find_all("div", class_="aspect-w-16 aspect-h-9 rounded-t-lg overflow-hidden bg-slate-200")
        for div in article_divs:
            span = div.find("span")
            if span:
                noscript = span.find("noscript")
                if noscript:
                    img = noscript.find("img")
                    if img and img.get('src'):
                        url = extract_original_url(img.get('src'))
                        if url:
                            image_urls.append(url)
                            # Get the alternative text (if needed)
                            # alt_text = img.get('alt', '')
                            # image_urls.append({'url': url, 'alt': alt_text})
        return image_urls