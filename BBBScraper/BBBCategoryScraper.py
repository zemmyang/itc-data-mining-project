from argparse import Namespace
from BBBScraper import internal_config as ICFG
from BBBScraper import messages as M
from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs4
import requests
import random as r
import re
import logging


class BBBCategoryScraper:
    """
    scrapes all the company urls for one particular category
    """
    def __init__(self, bbb_args: Namespace, log: logging.Logger):
        self.cat = "-".join(bbb_args.cats).lower()
        self.args = bbb_args
        self.log = log
        self.company_urls = []

        self._start_cat_url = urljoin(ICFG.STARTING_URL, self.args.loc.lower() + "/category/" + self.cat + "/")
        self._start_req = requests.get(self._start_cat_url, headers=r.choice(ICFG.HEADERS))

        try:
            self._run_program_proper()
        except Exception as err:
            print(f"Error: {err}")

    def _run_program_proper(self) -> None:
        """ moves the program logic away from __init__ for organizational purposes"""
        self.log.debug(M.LOG_START_CAT_SCRAPER)
        _page_num = self._get_number_of_pages()
        _result_num = self._get_number_of_results()

        _current_page = self._start_cat_url
        _page = 1
        while not self._check_if_last_page(_current_page):
            self.log.debug(f"Scraping {_page} out of {_page_num}")
            self.log.debug(f"Scraping {_current_page}")
            _companies_in_page = self._get_company_urls_in_page(_current_page)
            self.log.debug(f"Adding {len(_companies_in_page)} in the database")

            self.company_urls.extend(_companies_in_page)
            _page += 1
            _current_page = self._get_next_page_url(_current_page)

        self.log.info(f"Category scraper completed with {len(self.company_urls)} in database")

    def _get_number_of_pages(self) -> int:
        """ looks for the "Page X in Y" format in the category page """
        _starting_cat_soup = bs4(self._start_req.content, ICFG.BS4_HTML_PARSER)
        _page_nums = self._find_in_text_and_extract_numbers(_starting_cat_soup, ICFG.REGEX_PAGE_X_OF_Y,
                                                            "section", "Indicator-wqrbkn-0")
        return _page_nums[1]

    def _get_number_of_results(self) -> int:
        """ looks for "Showing X results" in category page """
        _starting_cat_soup = bs4(self._start_req.content, ICFG.BS4_HTML_PARSER)
        _results = self._find_in_text_and_extract_numbers(_starting_cat_soup, ICFG.REGEX_SHOWING_X_RESULTS,
                                                          "h2", "search-heading__subtitle")
        return _results[0]

    def _check_if_last_page(self, url: str) -> bool:
        """ checks if the page being looked at is the last page """
        _req = requests.get(url, headers=r.choice(ICFG.HEADERS))
        _soup = bs4(_req.content, ICFG.BS4_HTML_PARSER)
        _page_nums = self._find_in_text_and_extract_numbers(_soup, ICFG.REGEX_PAGE_X_OF_Y,
                                                            "section", "Indicator-wqrbkn-0")
        return True if _page_nums[0] == _page_nums[1] else False

    @staticmethod
    def _find_in_text_and_extract_numbers(soup: bs4, regex_to_search: str,
                                          html_tag: str, html_class: str) -> list:
        """
        takes a soup, finds text according to regex in the html_tag/class specified
        and then returns all the integers in the text as a list
        """
        _text = soup.find(html_tag, class_=html_class)
        _string_with_numbers = re.match(regex_to_search, _text.text)
        return [int(s) for s in _string_with_numbers.group(0).split() if s.isdigit()]

    @staticmethod
    def _get_next_page_url(url: str) -> str:
        """ takes a url, finds the link that leads to the next page """
        _req = requests.get(url, headers=r.choice(ICFG.HEADERS))
        _soup = bs4(_req.content, ICFG.BS4_HTML_PARSER)
        _next_page_tag = _soup.find("a", class_="search-pagination__next-page", href=True)
        return _next_page_tag['href']

    @staticmethod
    def _get_company_urls_in_page(url: str) -> list:
        """  goes through a page with a bunch of companies listed and grabs the urls off them """
        _req = requests.get(url, headers=r.choice(ICFG.HEADERS))
        _soup = bs4(_req.content, ICFG.BS4_HTML_PARSER)

        _companies_in_page = []
        for link in _soup.find_all('h3', class_="result-item-ab__name"):
            _url_in_h3 = link.find("a", href=True)
            _di = {"Name": link.get_text(), "URL": _url_in_h3['href']}
            _companies_in_page.append(_di)

        return _companies_in_page
