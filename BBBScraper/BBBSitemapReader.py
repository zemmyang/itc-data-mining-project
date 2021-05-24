from BBBScraper import internal_config as ICFG
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser
from bs4 import BeautifulSoup as bs
import random as r
import requests


class BBBSitemapReader:
    """ gets the category names from the sitemaps """
    def __init__(self, location: str, get_accredited: bool):
        self._robot_parser = RobotFileParser()
        self._robot_parser.set_url(urljoin(ICFG.STARTING_URL, 'robots.txt'))
        self._robot_parser.read()
        self._site_maps = self._robot_parser.site_maps()

        self.location = location.lower()
        self._acc = get_accredited

    def _get_category_sitemap(self) -> str:
        """
        cleans up the results from parsing the sitemaps and removes the
        sitemaps that specify the city/state/province (because they're the same)
        """
        _list = [i for i in self._site_maps if i.find("categories") + 1 and i.find(self.location) + 1
                 and (not i.find("city") + 1 and not i.find("state") + 1 and not i.find("province") + 1)]

        if not self._acc:
            for i in _list:
                _list.pop(i.find("accredited"))
            return _list[0]
        else:
            for i in _list:
                return _list.pop(i.find("accredited"))

    def _read_urls_from_sitemap_link(self) -> list:
        """ uses the result from _get_category_sitemap to get the urls of the categories """
        return self._scrape_sitemap_pages(self._get_category_sitemap())

    def _read_categories_from_sitemaps(self) -> list:
        """
        uses the results from _read_urls_from_sitemap_link, and cleans up the names of
        the categories from the URLs. makes it easier to compare it with the
        input argument
        """
        self._cats = [self._scrape_sitemap_pages(cats) for cats in self._read_urls_from_sitemap_link()][0]

        _left_strip = ICFG.STARTING_URL + self.location + "/category/"
        _right_strip = "/accredited" if self._acc else ""
        return [cats.removeprefix(_left_strip).removesuffix(_right_strip).replace("-", " ").title()
                for cats in self._cats]

    @staticmethod
    def _scrape_sitemap_pages(url: str) -> list:
        """ used to clean up the data from the XML sitemaps and put them in a list """
        _reqs = requests.get(url, headers=r.choice(ICFG.HEADERS))
        soup = bs(_reqs.content, "lxml-xml")
        return [i.get_text() for i in soup.find_all('loc')]

    def get_length_of_categories(self) -> int:
        """ is actually __len__ but is also more descriptive """
        self._read_categories_from_sitemaps()
        return len(self._cats)

    def get_categories(self) -> list:
        """ returns _read_categories_from_sitemaps but with a cleaner function name """
        return self._read_categories_from_sitemaps()


def read_all_sitemaps(get_accredited: bool, get_page=0):
    """
    get all the companies using the sitemaps. get_page is used for batch processes.
    set it to -1 to get everything. returns a list of the companies in BBB
    """
    robot_parser = RobotFileParser()
    robot_parser.set_url(urljoin(ICFG.STARTING_URL, 'robots.txt'))
    robot_parser.read()
    site_maps = robot_parser.site_maps()

    sitemap_list = [i for i in site_maps if i.find("sitemap") + 1 and i.find('business-profiles-index') + 1]
    if not get_accredited:
        [sitemap_list.pop(i.find("accredited")) for i in sitemap_list]
        sitemap = sitemap_list[0]
    else:
        sitemap = [sitemap_list.pop(i.find("accredited")) for i in sitemap_list][0]

    sitemap_pages = requests.get(sitemap, headers=r.choice(ICFG.HEADERS))
    soup = bs(sitemap_pages.content, "lxml-xml")

    pages_with_business_profiles = [i.get_text() for i in soup.find_all('loc')]

    business_profile_list = []
    if get_page == -1:
        for page in pages_with_business_profiles:
            business_pages = requests.get(page, headers=r.choice(ICFG.HEADERS))
            soup = bs(business_pages.content, "lxml-xml")
            business_profile_list.extend([i.get_text() for i in soup.find_all('loc')])
    else:
        page = pages_with_business_profiles[get_page]
        business_pages = requests.get(page, headers=r.choice(ICFG.HEADERS))
        soup = bs(business_pages.content, "lxml-xml")
        business_profile_list.extend([i.get_text() for i in soup.find_all('loc')])

    return business_profile_list


def get_number_of_pages_of_all_sitemaps(get_accredited: bool):
    robot_parser = RobotFileParser()
    robot_parser.set_url(urljoin(ICFG.STARTING_URL, 'robots.txt'))
    robot_parser.read()
    site_maps = robot_parser.site_maps()

    sitemap_list = [i for i in site_maps if i.find("sitemap") + 1 and i.find('business-profiles-index') + 1]
    if not get_accredited:
        [sitemap_list.pop(i.find("accredited")) for i in sitemap_list]
        sitemap = sitemap_list[0]
    else:
        sitemap = [sitemap_list.pop(i.find("accredited")) for i in sitemap_list][0]

    sitemap_pages = requests.get(sitemap, headers=r.choice(ICFG.HEADERS))
    soup = bs(sitemap_pages.content, "lxml-xml")

    pages_with_business_profiles = [i.get_text() for i in soup.find_all('loc')]
    return len(pages_with_business_profiles)


if __name__ == "__main__":
    print(get_number_of_pages_of_all_sitemaps(False))
