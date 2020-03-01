import requests
from bs4 import BeautifulSoup
from python_autocite.lib.citation import Citation
from python_autocite.lib.formatter import APAFormatter
from python_autocite.lib.datafinder import Datafinder
from ArticleScraper import getArticle

import datetime

def getCitation(url):
    article = getArticle(url)
    citation = Citation()
    citation.authors = article.authors
    citation.title = article.title
    citation.access_date = datetime.datetime.now()
    citation.publication_date = article.publish_date
    citation.url = url

    formatter = APAFormatter()

    return formatter.format(citation)