from argparse import ArgumentParser
from getpass import getpass
import logging
import sys

from BBBScraper.BBBArgParser import define_required_args, check_passed_args
from BBBScraper.BBBSitemapReader import BBBSitemapReader
from BBBScraper.BBBCategoryScraper import BBBCategoryScraper
from BBBScraper.BBBCompanyFileHandler import BBBCompanyFileHandler
from BBBScraper.BBBCategoryFileHandler import BBBCategoryFileHandler
from BBBScraper import internal_config as ICFG
from BBBScraper import messages as M
from BBBScraper import logger
import pymysql
from os import path


__author__ = "Angeleene Ang"
__version__ = "0.5.0"
__email__ = "angeleene.ang@gmail.com"
__status__ = "Prototype"


class BBBScraper:
    """
    sets up the arguments, grabs them, and passes them to the relevant classes.
    also sets up the logger
    """
    def __init__(self):
        """ sets up the parser and logger functions """
        self.parser = None
        self.args = None
        self.log = None

        try:
            self._run_program_proper()
        except Exception as err:
            print(f"Error: {err}")

    def _run_program_proper(self) -> None:
        """ moves the program logic away from __init__ for organizational purposes"""
        self._set_up_parser()
        self._set_up_logger()
        self._ask_for_pw_if_type_is_sql()
        self.log.debug(M.LOG_START_SCRAPER)

        self._read_sitemaps()

        if self._check_if_arg_is_a_cat():
            self.log.info(f'{self.args.cats} found! Scraping URLs...')
            self._set_up_sql_tables()

            _cat_scraper = BBBCategoryScraper(self.args, self.log)
            _bbb_company_filehandler = BBBCompanyFileHandler(_cat_scraper.company_urls, self.args, self.log,
                                                             password=self.pw, connection=self.connection)
            _bbb_category_filehandler = BBBCategoryFileHandler(self._cats, self.args, self.log,
                                                               password=self.pw, connection=self.connection)
            self.connection.close()
        else:
            self.log.critical(f'{self.args.cats} not found. Exiting...')
            raise LookupError(f"{self.args.cats} is not in the category list")

    def _set_up_parser(self) -> None:
        """
        creates an argumentparser object, populates it with the arguments,
        the parses the args to see if anything is invalid
        """
        self.parser = ArgumentParser()
        define_required_args(self.parser)

        self.args = self.parser.parse_args()
        check_passed_args(self.args)

    def _set_up_logger(self) -> None:
        """
        sets up the logger. if the verbose flag is on in the CLI arguments,
        the logger also prints output in the terminal
        """
        self.log = logging.getLogger('bbbscraper')
        self.log.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(self.args.log)
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(ICFG.LOG_FORMAT)
        self.log.addHandler(file_handler)

        if self.args.verbose:
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setLevel(logging.DEBUG)
            stream_handler.setFormatter(ICFG.LOG_FORMAT)
            self.log.addHandler(stream_handler)

        self.log.debug("Logger set-up")

    def _read_sitemaps(self) -> None:
        """ reads the sitemap off BBB.org """
        _sitemap_reader = BBBSitemapReader(location=self.args.loc, get_accredited=self.args.acc)
        self.log.info(f'Found {_sitemap_reader.get_length_of_categories()} categories')
        self._cats = _sitemap_reader.get_categories()

    def _check_if_arg_is_a_cat(self) -> bool:
        """ checks if the input argument is one of the categories """
        return True if " ".join(self.args.cats) in self._cats else False

    def _ask_for_pw_if_type_is_sql(self) -> None:
        if self.args.type == "SQL":
            self.log.debug(M.LOG_ASKING_FOR_SQL_PASSWORD)
            self.pw = getpass("Please enter SQL database password here: ")
            # self.pw = ICFG.ZEMMY_PW

            self.connection = pymysql.connect(host=ICFG.SQL_HOST, user=ICFG.SQL_USER,
                                              passwd=self.pw, db=ICFG.SQL_DB)

    def _set_up_sql_tables(self) -> None:
        if self.args.type == "SQL":
            self._cursor = self.connection.cursor()
            _file = ICFG.BBBORG_SQL_FILE

            if path.isfile(_file) is False:
                raise FileNotFoundError(M.SQL_FILE_NOT_FOUND_ERROR)
            else:
                with open(_file, "r") as f:
                    _sql_file = f.read().split(';')
                    self.log.info(M.LOG_READING_SQL_FILE + _file)

                for i in range(len(_sql_file) - 1):
                    self.log.debug(
                        f"Executing {(''.join(list(_sql_file[i])[:40])).strip()}")  # shorten the debug output
                    self._cursor.execute(_sql_file[i])
                self.connection.commit()
