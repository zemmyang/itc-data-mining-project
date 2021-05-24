from BBBScraper.BBBCompanyScraper import BBBCompanyScraper, read_company_page
from BBBScraper.BBBCategoryScraper import BBBCategoryScraper
from BBBScraper.BBBCompanyFileHandler import BBBCompanyFileHandler
import pandas as pd
from BBBScraper import BBBSQLSetup
from BBBScraper.BBBSitemapReader import BBBSitemapReader, read_all_sitemaps, get_number_of_pages_of_all_sitemaps
import logging
from argparse import Namespace
from unittest.mock import Mock
from BBBScraper import internal_config as ICFG


class BBBScraperInterface:
    def __init__(self, args, logger, cats, engine):
        self.args = args
        self.log = logger
        self.all_categories = cats
        self.engine = engine

    def run(self):
        self._main_scraper_logic()

    def _main_scraper_logic(self):
        # first you get a list of all the categories.
        # in this case, that's already handled outside by the cats argument

        _category_series = pd.Series(self.all_categories)
        _category_dict = {'category_id': _category_series.index.astype(str).str.zfill(4),
                          'category_name': self.all_categories}
        pd.DataFrame(_category_dict).to_sql('categories', con=self.engine, if_exists='append', chunksize=1000,
                                            index=False)

        #     # and then save to SQL table
        # _bbb_category_filehandler = BBBCategoryFileHandler(self.all_categories, self.args, self.log,
        #                                                    password=self.pw, connection=self.connection)

        if self.args.all:
            for i in range(1): #range(get_number_of_pages_of_all_sitemaps(get_accredited=self.args.acc)):
                _company_list = read_all_sitemaps(get_accredited=self.args.acc, get_page=i)
                _df = pd.DataFrame(_company_list, columns=["BBB URL"])

                # generate "ID numbers" for each company
                _df["id_num"] = _df["BBB URL"].str.extract(r'(\/..\/..\/)') + _df["BBB URL"].str.extract(r'(\d+-\d+$)')
                _df["business_id"] = _df['id_num'].str.replace("/", "").str.replace("-", "")
                _df = _df.dropna(axis=0)

                _df["TEST"] = _df['BBB URL'].apply(read_company_page)
                _df = pd.DataFrame(_df["TEST"].values.tolist())

        else:
            _cat_scraper = BBBCategoryScraper(self.args, self.log)
            # this generates an attribute called company_urls, which is a list of the company URLs in that category

            _df = pd.DataFrame(_cat_scraper.company_urls)

            # generate "ID numbers" for each company
            _df["id_num"] = _df["URL"].str.extract(r'(\/..\/..\/)') + _df["URL"].str.extract(r'(\d+-\d+$)')
            _df["business_id"] = _df['id_num'].str.replace("/", "").str.replace("-", "")
            _df = _df.dropna(axis=0)

            _df["TEST"] = _df['URL'].apply(read_company_page)
            _df = pd.concat([_df['business_id'], _df["Name"], pd.DataFrame(_df["TEST"].values.tolist())],
                            axis=1, join="inner")

            _df.to_sql('business_profile', con=self.engine, if_exists='append', chunksize=1000, index=False)

        #
        #     # and then save to SQL table
        # _bbb_company_filehandler = BBBCompanyFileHandler(_cat_scraper.company_urls, self.args, self.log,
        #                                                  password=self.pw, connection=self.connection)

        # and then you get the details of each company
            # which is handled by CompanyScraper inside CompanyFileHandler

        # and then you get the reviews
        # and the complaints
        # and if you want to get more than one category, return to second comment
