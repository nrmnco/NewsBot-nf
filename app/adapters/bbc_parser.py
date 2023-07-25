import requests
from bs4 import BeautifulSoup as bsoup


url = "https://www.bbc.com/news/world"


def get_all_todays_urls(url: str, links: set = set(), counter: int = 0):
    res = requests.get(url)
    doc = bsoup(res.text, 'html.parser')
    # news = doc.find_all('div', {'class': 'gel-wrap gs-u-box-size'})
    link_tags = doc.select('a[class^="gs-c-promo-heading gs-o-faux-block-link__overlay-link"]')

    # Extract the links
    links = [tag["href"] for tag in link_tags]


    for link in links:
        if 'article' in link or 'culture' in link:
            links.remove(link)

    for link in links:
        if "news" not in link or "live" in link:
            links.remove(link)

    for count, link in enumerate(links):
        if "https://www.bbc.com" not in link:
            links[count] = "https://www.bbc.com" + link


    return links


def get_article_text(link):
    res = requests.get(link)
    doc = bsoup(res.text, 'html.parser')
    article = doc.find_all("div", class_="ssrcss-11r1m41-RichTextComponentWrapper")

    text = [div.get_text(strip=True) for div in article]

    res = ''

    for i in text:
        i.replace('\n', '')
        res += i

    return res


def get_title(link):
    res = requests.get(link)
    doc = bsoup(res.text, 'html.parser')
    title = doc.find('h1', {'id': 'main-heading'})
    # text = title.get_text().replace('\n', '')
    text = title.get_text()
    return text
#
# print(get_all_todays_urls(url))
#
# print(get_article_text('https://www.bbc.com/news/entertainment-arts-66216417'))
