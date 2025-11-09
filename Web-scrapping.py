import re
import requests
from bs4 import BeautifulSoup
from pprint import pprint

# Определяем список ключевых слов:
KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'пузырь']

url = 'https://habr.com/ru/articles/'

response = requests.get(url)
markup = response.text

soup = BeautifulSoup(markup, 'html.parser')

data = []

# Парсим страницу по ключевым аттрибутам для определения переменных date, title, link, article_text
cards = soup.find_all(attrs={'data-test-id': 'articles-list-item'})
for card in cards:
    link = 'https://habr.com' + card.find('a', class_='tm-article-datetime-published_link')['href']
    title = card.find('a', class_='tm-title__link').text
    date = card.find('time')['title']

    try:
        news_response = requests.get(link)
        news_markup = BeautifulSoup(news_response.text, 'html.parser')
        article_content = news_markup.find('article', class_='tm-article-presenter__content tm-article-presenter__content_narrow')

        if article_content:
            # Извлекаем весь текст статьи
            text_elements = article_content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'])
            article_text = ' '.join([elem.get_text(strip=True) for elem in text_elements]).replace('\xa0', ' ').replace('  ', ' ')
        else:
            article_text = "Текст статьи не найден"

    except Exception as e:
        print(e)

    # Формируем словарь
    item = {
        'title': title,
        'link': link,
        'text': article_text,
        'date': date
        }

    data.append(item)

# Опредеяем паттерн для поиска ключевых слов, в т.ч. составных.
pattern = r'(' + '|'.join(KEYWORDS) + r')'

# Цикл для поиска ключевых слов и вывода информации в необходимом формате + запись в файл result.md
with open('result.md', 'w', encoding='utf-8') as f:
    for item in data:
        title_match = re.search(pattern, item['title'], re.IGNORECASE)
        text_match = re.search(pattern, item['text'], re.IGNORECASE)
        if title_match:
            f.write(f'{item['date']} – {item['title']} – {item['link']}' + '\n')
            f.write(f'Это результат поиска по ключевому слову: "{title_match.group(0)}" в названии статьи' + '\n')
            print(f'{item['date']} – {item['title']} – {item['link']}')
            print(f'Это результат поиска по ключевому слову: "{title_match.group(0)}" в названии статьи')
        elif text_match:
            f.write(f'{item['date']} – {item['title']   } – {item['link']}' + '\n')
            f.write(f'Это результат поиска по ключевому слову: "{text_match.group(0)}" в тексте статьи' + '\n')
            print(f'{item['date']} – {item['title']} – {item['link']}')
            print(f'Это результат поиска по ключевому слову: "{text_match.group(0)}" в тексте статьи')