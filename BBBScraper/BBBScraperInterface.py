from BBBScraper.BBBCompanyScraper import BBBCompanyScraper
from BBBScraper.BBBCategoryScraper import BBBCategoryScraper
from BBBScraper.BBBCategoryFileHandler import BBBCategoryFileHandler
from BBBScraper.BBBCompanyFileHandler import BBBCompanyFileHandler
from BBBScraper.BBBSitemapReader import BBBSitemapReader
import logging
from argparse import Namespace
from unittest.mock import Mock


class BBBScraperInterface:
    def __init__(self, args, logger, cats, conn, password):
        self.args = args
        self.log = logger
        self.all_categories = cats
        self.connection = conn
        self.pw = password

    def run(self):
        self._main_scraper_logic()

    def _main_scraper_logic(self):
        # first you get a list of all the categories.
        # in this case, that's already handled outside by the cats argument

            # and then save to SQL table
        _bbb_category_filehandler = BBBCategoryFileHandler(self.all_categories, self.args, self.log,
                                                           password=self.pw, connection=self.connection)

        # and then you get all the companies in a category
        _cat_scraper = BBBCategoryScraper(self.args, self.log)
            # this generates an attribute called company_urls, which is a list of the company URLs in that category

            # and then save to SQL table
        _bbb_company_filehandler = BBBCompanyFileHandler(_cat_scraper.company_urls, self.args, self.log,
                                                         password=self.pw, connection=self.connection)

        # and then you get the details of each company
            # which is handled by CompanyScraper inside CompanyFileHandler

        # and then you get the reviews
        # and the complaints
        # and if you want to get more than one category, return to second comment
