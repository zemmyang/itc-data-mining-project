import config as CFG
import time
import os
import re
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
        """
        initializes some of the class variables as well as the scraper flags
        """
        # all of these flags need to be True before the scrape command is called in the end
        self._url_is_set = False
        self._category_is_set = False
        self._country_is_set = False

        # initialize some class variables
        self.url = ""
        self.search_category = ""
        self.country = ""

    def set_starting_url(self, url):
        """ one of the setting functions that needs to be called in order to call the scrape command """
        self._url_is_set = True
        self.url = url

    def set_starting_category(self, category: str):
        self._category_is_set = True
        self.search_category = category.replace(" ", "%20")

    def set_country(self, country: str):
        self._country_is_set = True
        self.country = country.upper()

    def set_initial_values(self, url, country, category):
        " an alternative to the individual set functions "
        self._url_is_set = True
        self._category_is_set = True
        self._country_is_set = True

        self.url = url
        self.search_category = category.replace(" ", "%20")
        self.country = country.upper()

    def _build_search_url(self, page):
        _full_url = self.url + 'search?find_country=' + self.country + '&find_text=' + \
                    self.search_category + '&find_type=Category&sort=Relevance&page=' + str(page)
        return _full_url

    @staticmethod
    def _get_number_of_pages_in_results(link):
        """
        reads a link, looks for the "Page X of Y" pattern where
        X is current page
        Y is total number of pages
        and returns that as a tuple

        :param link: the link where to get the "Page X of Y" pattern
        :return: a tuple (X, Y)
        """
        _page = requests.get(link, headers=CFG.USER_AGENT)
        _soup = BeautifulSoup(_page.content, 'html.parser')
        _footer = _soup.footer

        if not _footer:
            raise RuntimeError("<footer> not found in page")

        _pattern = re.match(r'Page\s\d+\sof\s\d+', _footer.text)

        if not _pattern:
            raise RuntimeError("Internal error in search results page. Cannot find 'Page X in Y' pattern")

        _pages = re.findall(r'\d+', _pattern.group())
        return tuple([int(i) for i in _pages])

    @staticmethod
    def _parse_url(link):
        """
        takes a link and grabs the URLs out of it.
        removes duplicates (does not check for multiple locations)

        :param link: should be page results (i.e., _get_number_of_pages_in_results should return something)
        :return: a list of all the links in the page
        """
        _page = requests.get(link, headers=CFG.USER_AGENT)
        _soup = BeautifulSoup(_page.content, 'html.parser')
        _results_main = _soup.find_all('h3', class_="MuiTypography-root")

        if not _results_main:
            raise RuntimeError(f"Bad link passed to _parse_url: {link}")

        _links = [i.find('a', href=True) for i in _results_main]

        return list(set([i['href'] for i in _links]))

    @staticmethod
    def _read_individual_pages(link):
        """
        returns a dictionary with the business details
        """
        _page = requests.get(link + '/details', headers=CFG.USER_AGENT)
        _soup = BeautifulSoup(_page.content, 'html.parser')
        _alerts = _soup.find("section", id="all-alerts")

        if _alerts:
            return _alerts.h6.text

        _business_details = _soup.find("div", class_='business-details-card__content')

        if not _business_details:
            raise RuntimeError(f"Bad link passed to _read_individual_pages: {link}")

        return _business_details

    def _check_flags(self):
        """
        if all flags are True, return True
        if at least one flag is False, return a list of False flags
        """
        _flag_list = [self._url_is_set, self._category_is_set, self._country_is_set]
        if all(_flag_list):
            return True
        else:
            return False

    def _scrape_main(self):
        """
        the actual scraper, but without checking the flags.
        mostly meant to keep the scrape function cleaner
        """
        _number_of_pages = self._get_number_of_pages_in_results(self._build_search_url(1))

        _company_page_links = []
        for page in range(_number_of_pages[0], _number_of_pages[1]):
            _single_page_link = self._build_search_url(page)
            _company_page_links.extend(self._parse_url(_single_page_link))

        return _company_page_links

    def scrape(self):
        """
        performs the actual scraping, but checks the flags first
        returns nothing, just call the function.
        to get usable data out, call the output function
        """
        _flags = self._check_flags()
        if _flags:
            self._scrape_main()
        else:
            raise RuntimeError(f"Something is not set properly!")

    def output(self, output_format):
        """ user needs to call scrape before calling output """
        # TODO: returns the output in whatever way the user wants it
        pass


def test():
    bad_url_for_testing = 'http://po.ta.to/'

    a = BBBScraper()
    a.set_initial_values(url=CFG.STARTING_URL, country=CFG.COUNTRY, category=CFG.STARTING_CATEGORY)

    # example of page that's normal
    # print(a._read_individual_pages('https://www.bbb.org/us/tx/odessa/profile/general-contractor/jamie-merrell-construction-0825-1000148213'))

    # example of page with an alert
    print(a._read_individual_pages("https://www.bbb.org/us/ca/san-bernardino/profile/building-contractors/uribe's-general-contractor-1066-13185633"))


def main():
    a = BBBScraper()
    a.set_initial_values(url=CFG.STARTING_URL, country=CFG.COUNTRY, category=CFG.STARTING_CATEGORY)
    # TODO: possible other things that can be configured at runtime?
    a.scrape()


if __name__ == "__main__":
    test()
