#!/usr/bin/env python
"""
Python-based scraper for BBB.org

usage:
    from BBBScraper import BBBScraper
    BBBScraper()
"""


from BBBScraper import BBBScraper


__author__ = "Angeleene Ang"
__version__ = "0.5.0"
__email__ = "angeleene.ang@gmail.com"
__status__ = "Prototype"

BBBScraper(cats=['Restaurants'], verbose=True, yelp=True)

# BBBScraper()
