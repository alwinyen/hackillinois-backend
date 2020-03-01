import requests
from bs4 import BeautifulSoup
from python_autocite.lib.citation import Citation
from python_autocite.lib.formatter import APAFormatter
from python_autocite.lib.datafinder import Datafinder
import datetime

def url_to_soup(url):
    # Some websites are unhappy with no user agent, so here's
    # one that looks nice.
    header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',}

    try:
        page = requests.get(url)
        return BeautifulSoup(page.text, 'html5lib')
    except Exception as e:
        print(e)
        return None

def soup_to_citation(url, soup):
    df = Datafinder(soup)

    citation = Citation()
    citation.authors = df.get_authors()
    citation.title = df.get_title()
    citation.access_date = datetime.datetime.now()
    citation.publication_date = df.get_publication_date()
    citation.url = url

    formatter = APAFormatter()

    return formatter.format(citation)

def getCitation(url):
    soup = url_to_soup(url)
    return soup_to_citation(url, soup)