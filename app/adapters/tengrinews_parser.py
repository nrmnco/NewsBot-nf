import requests
from bs4 import BeautifulSoup as bsoup

# requests and bs4 to requirmnts

url = 'https://tengrinews.kz'
links = set()
counter = 0

def get_all_todays_urls(url: str, links: set = set(), counter: int = 0):
    if counter < 5:
        res = requests.get(url)
        doc = bsoup(res.text, 'html.parser')
        news = doc.find_all('div', {'class': 'tn-tape-item'})

        for i in news:
            part = str(i)
            if "Сегодня" in part:
                doc_s = bsoup(part, 'html.parser')
                a_tags = doc_s.find('a', {'class': 'tn-tape-title'})
                doc_s = bsoup(str(a_tags), 'html.parser')
                asd = doc_s.find('a', href=True)
                if 'kazakhstan_news' in asd['href']:
                    link = 'https://tengrinews.kz' + asd['href']
                    links.add(link)
                    counter += 1
                    get_all_todays_urls(link, links, counter)

        return links
    else:
        return 0

def get_article_text(link):
    res = requests.get(link)
    doc = bsoup(res.text, 'html.parser')
    article = doc.find('article', {'class': 'tn-news-text'})
    plain_text = ''

    doc = bsoup(str(article), 'html.parser')
    paragraphs = doc.find_all('p')
    for paragraph in paragraphs:
        for link in paragraph.find_all('a'):
            link.extract()

        for img in paragraph.find_all('img'):
            img.extract()

        plain_text += paragraph.get_text()

    text = plain_text.replace('\n', '')
    

    return text


def get_title(link):
    res = requests.get(link)
    doc = bsoup(res.text, 'html.parser')
    title = doc.find('h1', {'class': 'tn-content-title'})
    span = title.find('span', {'class': 'tn-hidden'})
    span.extract()
    text = title.get_text().replace('\n', '')
    return text

def parse_news_website():
    url = 'YOUR_NEWS_WEBSITE_URL'
    links = set()
    counter = 0
    get_all_todays_urls(url, links, counter)
    
    articles = []
    for link in links:
        title = get_title(link)
        content = get_article_text(link)
        theme_tags = ['TAG1', 'TAG2']  # Replace with the actual theme tags for the article
        article = {
            'title': title,
            'content': content,
            'theme_tags': theme_tags
        }
        articles.append(article)
    
    return articles

print(get_all_todays_urls(url, links, counter))

print(links)

text = get_article_text(next(iter(links)))

print(text)