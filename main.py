import config as CFG
import time
import os
import re
import requests
import logging as logg
from bs4 import BeautifulSoup
import json
from BBBScraper import BBBScraper


def test():
    bad_url_for_testing = 'http://po.ta.to/'
    a = BBBScraper()
    a.set_initial_values(url=CFG.STARTING_URL, country=CFG.COUNTRY, category=CFG.STARTING_CATEGORY)

    # # example of page that's normal
    # print(a._read_individual_pages('https://www.bbb.org/us/tx/odessa/profile/general-contractor/jamie-merrell-construction-0825-1000148213'))
    #
    # # example of page with an alert
    # print(a._read_individual_pages("https://www.bbb.org/us/ca/san-bernardino/profile/building-contractors/uribe's-general-contractor-1066-13185633"))
    #
    # # example of page with lots of info
    # print(a._read_individual_pages('https://www.bbb.org/us/wa/burien/profile/construction-services/vision-remodeling-construction-corporation-1296-1000064178'))

    print(a._scrape_main())


def main():
    a = BBBScraper()
    a.set_initial_values(url=CFG.STARTING_URL, country=CFG.COUNTRY, category=CFG.STARTING_CATEGORY)
    a.scrape()
    a.output('json', filename=os.path.join(CFG.SAVE_TO, CFG.SAVE_AS))


if __name__ == "__main__":
    main()
