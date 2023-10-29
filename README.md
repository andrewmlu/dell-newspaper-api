# Dell Newspaper API

Searches across news sites (currently WaPo) for top 10 headlines from yesterday.

How to run: `pip install newsapi-python && pip3 install newspaper3k`, then `python dell_newsapi.py`

For a given `article` in the `top_articles` list, to retrieve:
- Clean text: `article['clean_text']`
- Clean text with authors, headlines: `article['clean_text_with_headlines']`
