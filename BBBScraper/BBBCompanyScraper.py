from BBBScraper import internal_config as ICFG
from bs4 import BeautifulSoup
import requests
import random as r
import logging
from argparse import Namespace
import re


class BBBCompanyScraper:
    """ scrapes the data for each individual company """
    def __init__(self, company_url: str, bbb_args: Namespace, log: logging.Logger):
        # self.args = bbb_args
        # self.log = log
        self.company_data = dict()

        # self.company_name = company_name_and_url["Name"]
        self.company_url = company_url

        self._run_program_proper()

    def get_company_details(self):
        return self.company_data

    def _run_program_proper(self) -> None:
        """ moves the program logic away from __init__ for organizational purposes"""
        self.company_data = read_company_page(self.company_url)


def read_company_page(url):
    """ returns the company metadata as a dictionary for filehandler to use """
    _data = dict()
    _page = requests.get(url + '/details', headers=r.choice(ICFG.HEADERS))
    _soup = BeautifulSoup(_page.content, ICFG.BS4_HTML_PARSER)

    # business_id INT NOT NULL,
    # _char_id = "A" #re.search(ICFG.REGEX_GET_IDNUM_FROM_URL, url).group(0).replace("//", "")
    # _id = re.search(ICFG.REGEX_GET_IDNUM_FROM_URL, url).group(1).replace("-", "")
    # _data["id_num"] = _char_id + "".join(list(str(_id))).zfill(24)

    # business_name VARCHAR(100) NOT NULL,
    # _data["Name"] = self.company_name
    # _name = _soup.find("header", class_="styles__Title")
    # _data["Name"] = _name.h3.text

    # check if it's a charity. the scraper is not designed to handle these
    _title = _soup.find("title")
    if "Charity" in _title.text:
        _data["Alerts"] = None
        _data["Address"] = None
        _data["url"] = None
        _data["Phone"] = None
        _data["url"] = None
        _data["Rating"] = None
        _data["BBB File Opened"] = None
        _data["Type of Entity"] = None
        return _data

    # alerts VARCHAR(200) NULL,
    _alerts = _soup.find("section", id="all-alerts")
    if _alerts:
        _data["Alerts"] = _alerts.h6.text
    else:
        _data["Alerts"] = None

    # location VARCHAR(400) NULL,
    _location = _soup.find('span', class_='dtm-address')
    if _location:
        _data["Address"] = _location.text.strip("Location of This Business")
    else:
        _data["Address"] = None

    # website VARCHAR(50) NULL,
    _url = _soup.find("span", class_="dtm-url")
    if _url:
        _data["url"] = _url.text
    else:
        _data["url"] = None

    # phone_number INT NULL,
    _phone = _soup.find("a", class_="dtm-phone")
    if _phone:
        _data["Phone"] = _phone.text
    else:
        _data["Phone"] = None

    # bbb_rating VARCHAR(5) NULL,
    _bbb_rating = _soup.find("span", class_="LetterGrade-sc")
    if _bbb_rating:
        _data["Rating"] = _bbb_rating.text
    else:
        _data["Rating"] = None

    _business_details = _soup.find("div", class_='business-details-card')

    if not _business_details:
        # self.log.error(f"Missing business details for {_data['Name']}!")
        _data["BBB File Opened"] = None
        _data["Type of Entity"] = None
        return _data

    _table = _business_details.find("table")
    for row in _table.findAll('tr'):
        _table_header = row.find('th')
        _table_detail = row.find('td')

        if _table_header and _table_detail:
            _data[_table_header.text.strip(":")] = _table_detail.text

    # bbb_file_opened DATE NULL,
    if "BBB File Opened" not in _data:
        _data["BBB File Opened"] = None

    # type_of_entity VARCHAR(45) NULL,
    if "Type of Entity" not in _data:
        _data["Type of Entity"] = None

    return _data
