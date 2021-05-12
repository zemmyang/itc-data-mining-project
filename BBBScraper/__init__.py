from argparse import ArgumentParser, Namespace
from getpass import getpass
import logging
import sys

from BBBScraper.BBBArgParser import define_required_args, check_passed_args
from BBBScraper.BBBSitemapReader import BBBSitemapReader
from BBBScraper.BBBScraperInterface import BBBScraperInterface
from BBBScraper import BBBYRInterface
from BBBScraper import internal_config as ICFG
from BBBScraper import messages as M
import pymysql
from os import path


TESTING = True


class BBBScraper:
    """
    reads the arguments, sets up the logger
    """
    def __init__(self, **kwargs):
        """ sets up the parser and logger functions """
        self.kwargs = kwargs
        self.parser = None
        self.args = None
        self.log = None

        if TESTING:
            # the error output is better without the try-except clause but it's not user-friendly
            self._run_program_proper()
        else:
            try:
                self._run_program_proper()
            except Exception as err:
                print(f"Error: {err}")

    def _run_program_proper(self) -> None:
        """ moves the program logic away from __init__ for organizational purposes"""

        if self.kwargs.keys():
            #  uses args from BBBScraper instead of the args
            self._set_kwargs_defaults()
            self.args = Namespace(**self.kwargs)
        else:
            self._set_up_parser()

        self._set_up_logger()
        self._ask_for_pw_if_type_is_sql()
        self.log.debug(M.LOG_START_SCRAPER)

        self._read_sitemaps()

        if self._check_if_arg_is_a_cat():
            self.log.info(M.LOG_CATEGORY_FOUND_DEBUG.format(cats=self.args.cats))
            self._set_up_sql_tables()

            self.scraper_interface = BBBScraperInterface(args=self.args, logger=self.log,
                                                         cats=self._cats, conn=self.connection,
                                                         password=self.pw)

            self.scraper_interface.run()

            if self.args.yelp:
                self.log.info(M.LOG_YELP)
                BBBYRInterface.connect()

            self.connection.close()
        else:
            self.log.critical(M.LOG_CATS_NOT_FOUND.format(self.args.cats))
            raise LookupError(M.LOG_CATS_NOT_FOUND.format(self.args.cats))

    def _set_up_parser(self) -> None:
        """
        creates an argumentparser object, populates it with the arguments,
        the parses the args to see if anything is invalid
        """
        self.parser = ArgumentParser()
        define_required_args(self.parser)

        self.args = self.parser.parse_args()
        check_passed_args(self.args)

        if self.args.default:
            self._set_default_args()
            self.args = Namespace(**self.kwargs)

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

        self.log.debug(M.LOG_LOGGING_SET_UP_DEBUG)

    def _read_sitemaps(self) -> None:
        """ reads the sitemap off BBB.org """
        _sitemap_reader = BBBSitemapReader(location=self.args.loc, get_accredited=self.args.acc)
        self.log.info(M.LOG_SITEMAP_READ_INFO.format(catnum=_sitemap_reader.get_length_of_categories()))
        self._cats = _sitemap_reader.get_categories()

    def _check_if_arg_is_a_cat(self) -> bool:
        """ checks if the input argument is one of the categories """
        return True if " ".join(self.args.cats) in self._cats else False

    def _ask_for_pw_if_type_is_sql(self) -> None:
        if self.args.type == "SQL":
            self.log.debug(M.LOG_ASKING_FOR_SQL_PASSWORD)

            if TESTING:
                self.pw = ICFG.ZEMMY_PW
            else:
                self.pw = getpass(M.ENTER_SQL_PASSWORD)

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
                    self.log.debug(M.LOG_EXECUTING_SQL_DEBUG.format(query=''.join(list(_sql_file[i])[:40])).strip())
                    self._cursor.execute(_sql_file[i])
                self.connection.commit()

    def _set_kwargs_defaults(self) -> None:
        if 'log' not in self.kwargs.keys():
            self.kwargs['log'] = 'log.txt'
        if 'type' not in self.kwargs.keys():
            self.kwargs['type'] = 'SQL'
        if 'loc' not in self.kwargs.keys():
            self.kwargs['loc'] = 'US'
        if 'acc' not in self.kwargs.keys():
            self.kwargs['acc'] = False
        if 'all' not in self.kwargs.keys():
            self.kwargs['all'] = False
        if 'verbose' not in self.kwargs.keys():
            self.kwargs['verbose'] = True
        if  'yelp' not in self.kwargs.keys():
            self.kwargs['yelp'] = False

    def _set_default_args(self) -> None:
        """ for use with the default flag """
        self.kwargs['cats'] = ['Restaurants']

        self._set_kwargs_defaults()
