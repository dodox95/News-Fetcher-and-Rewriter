News Fetcher and Rewriter

This script fetches the latest news articles from cryptopotato.com, extracts the content, and then uses OpenAI's API to rewrite the article in a concise manner. Additionally, it generates a keyword for the article and fetches a relevant image from Unsplash.
Features

    Fetch Latest News: Automatically fetches the latest news from cryptopotato.com.
    Content Extraction: Extracts the content of the news article.
    Article Rewriting: Uses OpenAI's API to rewrite the article in a concise manner.
    Keyword Generation: Generates a keyword for the article using OpenAI's API.
    Image Fetching: Fetches a relevant image from Unsplash based on the generated keyword.
    Title Generation: Generates a concise title for the article using OpenAI's API.
    Continuous Monitoring: Continuously monitors the news source and processes new articles.

Prerequisites

    Python 3.x
    openai, requests, beautifulsoup4 Python libraries.
    OpenAI API key.
    Unsplash API key.

Setup

    Ensure you have the required Python libraries installed:

pip install openai requests beautifulsoup4

Replace the placeholder values for openai.api_key and UNSPLASH_ACCESS_KEY with your actual OpenAI and Unsplash API keys respectively.

Run the script:

php

    python <script_name>.py

How It Works

    The script first connects to the OpenAI API.
    It then fetches the latest news from cryptopotato.com.
    If a new article is found, it extracts its content.
    The content is then passed to OpenAI's API to generate a keyword.
    Using the keyword, a relevant image is fetched from Unsplash.
    The article content is rewritten in a concise manner using OpenAI's API.
    A concise title for the article is also generated.
    The script then waits for 10 minutes before checking for new articles again.

Output

The script saves the fetched articles, rewritten articles, generated keywords, and fetched images in separate directories (fetched_head, article_fetched, shorts_title, modified_article, polish_title, and thumbs).
