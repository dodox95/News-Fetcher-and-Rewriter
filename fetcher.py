import openai
import requests
from bs4 import BeautifulSoup
import os
import time
import urllib.request

openai.api_key = os.getenv('OPENAI_API_KEY')
print("Connected to OpenAI API...")

UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
UNSPLASH_URL = 'https://api.unsplash.com/search/photos'



url = 'https://cryptopotato.com/'
news_counter = 1
latest_title = None
current_link = None  # Define current_link as a global variable

def generate_keyword(text):
    max_attempts = 10
    for attempt in range(max_attempts):
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"{text}\n\nKeyword:",
            temperature=0.5,
            max_tokens=1
        )

        keyword = response.choices[0].text.strip()
        if keyword:
            return keyword

    raise Exception('Unable to generate keyword after 10 attempts.')

def get_image(keyword, counter):
    headers = {'Authorization': 'Client-ID ' + UNSPLASH_ACCESS_KEY}
    params = {'query': keyword, 'per_page': 1, 'license': 'public-domain|creative-commons'}
    response = requests.get(UNSPLASH_URL, headers=headers, params=params)
    response_json = response.json()

    if response_json['results']:
        result = response_json['results'][0]
        image_url = result['urls']['small']

        os.makedirs('thumbs', exist_ok=True)

        urllib.request.urlretrieve(image_url, os.path.join('thumbs', f"thumbnail_{counter}.jpg"))
        print(f'Thumbnail for keyword "{keyword}" has been created.')
    else:
        print('Nie znaleziono obrazów dla podanego słowa kluczowego.')

def fetch_article_content(article_link, counter):
    response = requests.get(article_link)
    soup = BeautifulSoup(response.content, 'html.parser')

    content_div = soup.find('div', {'class': 'coincodex-content'})

    for div in content_div.find_all('div', {'class': ['rp4wp-related-posts', 'entry-tags', 'code-block code-block-8', 'cz-sponsor', 'code-block code-block-12']}):
        div.decompose()

    article_content = content_div.get_text(separator="\n").strip()

    os.makedirs('article_fetched', exist_ok=True)
    with open(os.path.join('article_fetched', f'fetched_article_{counter}.txt'), 'w', encoding='utf-8') as f:
        f.write(article_content)
        f.write(f'\n\nŹródło: {article_link}')
    print(f'Saved article content to file: fetched_article_{counter}.txt')

def rewrite_article(text, counter, source):
    modified_article = ''
    time.sleep(3)

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"{text}\n\nPrzetłumacz i skróć ten artykuł do jednego akapitu w języku polskim.",
        temperature=0.3,
        max_tokens=1000  # określamy liczbę tokenów na jeden akapit
    )

    modified_article += response.choices[0].text.strip()
    modified_article += f'\n\nŹródło: {source}'

    os.makedirs('modified_article', exist_ok=True)
    with open(os.path.join('modified_article', f'modified_article_{counter}.txt'), 'w', encoding='utf-8') as f:
        f.write(modified_article.replace('\n', ' '))
    print(f'Saved modified article to file: modified_article_{counter}.txt')

    # Print the entire modified article
    print(f'\nModified Article:\n{modified_article}')


def generate_title_and_clickbait(text, counter):
    # Generate a concise title
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"{text}\n\nStwórz Krótki tytuł w języku polskim bazując na owym artykule.",
        temperature=0.3,
        max_tokens=100
    )
    title = response.choices[0].text.strip()

    os.makedirs('polish_title', exist_ok=True)

    # Save only the title, without any additional text
    with open(os.path.join('polish_title', f'polski_tytul_{counter}.txt'), 'w', encoding='utf-8') as f:
        f.write(title)

    print(f'Saved polish title to file: polski_tytul_{counter}.txt')


def fetch_news():
    global news_counter, latest_title, current_link
    print("Fetching news...")
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"Failed to fetch the news: {e}")
        return

    print("Processing news headlines...")
    news_headlines = soup.find_all('div', {'class': 'media-body'})

    if news_headlines:
        current_title = news_headlines[0].get_text().strip()
        current_link = news_headlines[0].find('a')['href']

        if latest_title != current_title:
            latest_title = current_title
            print(f"Found new article titled '{current_title}'")
            os.makedirs('fetched_head', exist_ok=True)

            try:
                with open(os.path.join('fetched_head', f'news_{news_counter}.txt'), 'w', encoding='utf-8') as f:
                    f.write(f'Title={current_title}\n')
                    f.write(f'Link={current_link}\n')
                print(f'Created news file: news_{news_counter}.txt')
            except Exception as e:
                print(f"Failed to create news file: {e}")
                return

            fetch_article_content(current_link, news_counter)

            time.sleep(3)

            try:
                with open(os.path.join('fetched_head', f'news_{news_counter}.txt'), 'r', encoding='utf-8') as f:
                    content = f.read()
                print(f'Fetched content from: news_{news_counter}.txt')
                keyword = generate_keyword(content)
                print(f'Generated keyword: {keyword}')
            except Exception as e:
                print(f"Failed to fetch content or generate keyword: {e}")
                return

            os.makedirs('shorts_title', exist_ok=True)
            try:
                with open(os.path.join('shorts_title', f'keyword_{news_counter}.txt'), 'w', encoding='utf-8') as f:
                    f.write(keyword)
                print(f'Saved keyword to file: keyword_{news_counter}.txt')
            except Exception as e:
                print(f"Failed to save keyword to file: {e}")
                return

            get_image(keyword, news_counter)

            try:
                with open(os.path.join('article_fetched', f'fetched_article_{news_counter}.txt'), 'r', encoding='utf-8') as f:
                    content = f.read()
                rewrite_article(content, news_counter, current_link)
                generate_title_and_clickbait(content, news_counter)  # Add this line after rewrite_article
            except Exception as e:
                print(f"Failed to rewrite article or generate titles: {e}")
            return

            news_counter += 1
        else:
            print(f'The article "{current_title}" already exists. No action taken.')
    else:
        print("No news headlines found.")

# Call rewrite_article function with text, counter and source
try:
    print("Reading fetched article...")
    with open(os.path.join('article_fetched', f'fetched_article_{news_counter}.txt'), 'r', encoding='utf-8') as f:
        content = f.read()
    rewrite_article(content, news_counter, current_link)
except Exception as e:
    print(f"Failed to read the fetched article or rewrite it: {e}")

while True:
    fetch_news()
    time.sleep(600)