import config as CFG
import time
import os
import requests
import logging as logg
from bs4 import BeautifulSoup


class BBBScraper:
    """
    the only thing that this scraper does outside of the class is to
    output a file or a database with the scraped data after the set-up is
    completed
    """
    def __init__(self):
        # all of these flags need to be True before the scrape command is called in the end
        self._url_is_set = False
        self.url = ""

    def set_starting_url(self, url):
        self._url_is_set = True
        self.url = url

    def _parse_url(self):
        _page = requests.get(self.url)
        return self._read_urls(_page.content)

    def _read_urls(self, page_content):
        _soup = BeautifulSoup(page_content, 'html.parser')
        return _soup

    def _read_links_in_page(self, soup):
        results_main = soup.find_all('div', class_="result-item__main")
        # TODO: check if the links correctly read to individual company pages
        links = results_main.find('a')
        return links

    def _get_categories(self):
        # TODO: SOMEHOW???
        pass

    def scrape(self):
        # TODO: the actual scraping
        self._read_links_in_page(self._read_urls(self._parse_url))  # TODO: there's probably a better way to do this...
        pass

    def output(self):
        # TODO: returns the output in whatever way the user wants it
        pass


def main():
    a = BBBScraper()
    a.set_starting_url(CFG.STARTING_URL)
    # TODO: possible other things that can be configured at runtime?
    a.scrape()


if __name__ == "__main__":
    main()
