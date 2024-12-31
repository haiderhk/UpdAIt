import requests

def get_website_html(url):
    response = requests.get(url)
    return response.text