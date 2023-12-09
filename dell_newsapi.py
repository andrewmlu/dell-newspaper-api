from newsapi import NewsApiClient
import newspaper
import re

#!pip install newsapi-python
#!pip3 install newspaper3k

def extract_data_from_url(url):
  article = newspaper.Article(url)
  # article.html
  article.download()
  article.parse()
  return {'text': article.text, 'title': article.title, 'authors': article.authors, 'date': article.publish_date, 'html': article.html}


def extract_from_first_caps(text):
    # Regular expression to match a word that's all caps after a newline
    pattern = r'(?<=\n\n)\b([A-Z]{2,})\b'

    # Find all all-caps words
    matches = re.findall(pattern, text)

    # If no matches, return None
    if not matches:
        return None

    # Find the position of the first all-caps word after a newline and extract from that position till the end
    start_pos = text.find(matches[0])

    return text[start_pos:]


def extract_after_double_newline(text):
    # Split the text at the first occurrence of \n\n
    parts = text.split('\n\n', 1)

    # If there's a second part after splitting, return it
    if len(parts) > 1:
        return parts[1]
    else:
        return None


def remove_ads(text):
  return text.replace("Advertisement\n\n", "")


def remove_double_spaces(text):
  return re.sub(r' +', ' ', text)


def main():
    # free account -- don't worry about API key haha
    newsapi = NewsApiClient(api_key='6c34b8a2b3e94334bb0ce0ce92d24939')

    top_headlines = newsapi.get_top_headlines(sources="associated-press", page_size=10)
    top_headlines_list = list(top_headlines.items())[2][1]

    top_articles = top_headlines_list[:]
    for article in top_articles:
        headline_url = (article['url'])
        article['text'] = extract_data_from_url(headline_url)['text']

    other = []
    for article in top_articles:
        print(article)
        article_text = article['text']
        headline = article['title']
        author = article['author']

        # AP text cleaning
        article['clean_text'] = article_text
        article['clean_text_with_headline'] = headline + "\n\n" + author + "\n\n" + article_text if author else headline + "\n\n" + article_text

        # WaPo text cleaning
        # cleaned_article1 = extract_from_first_caps(article_text)
        # cleaned_article2 = extract_after_double_newline(article_text)
        # if cleaned_article1:
        #     article['clean_text'] = remove_double_spaces(remove_ads(cleaned_article1))
        #     article['clean_text_with_headline'] = headline + "\n\n" + article['author'] + "\n\n" + remove_double_spaces(
        #         remove_ads(cleaned_article1))
        # elif cleaned_article2:
        #     article['clean_text'] = remove_double_spaces(remove_ads(cleaned_article2))
        #     article['clean_text_with_headline'] = headline + "\n\n" + article['author'] + "\n\n" + remove_double_spaces(
        #         remove_ads(cleaned_article2))
        # else:
        #     other.append(article)
        #     top_headlines_list.remove(article)

    return top_articles

if __name__ == '__main__':
    print(main())