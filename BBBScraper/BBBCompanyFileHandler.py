from argparse import Namespace
from BBBScraper import internal_config as ICFG
from BBBScraper import messages as M
from BBBScraper.BBBCompanyScraper import BBBCompanyScraper
import logging
from os import path


class BBBCompanyFileHandler:
    """
    a thing that goes in between categoryscraper and companyscraper.
    this takes the list of companies from catscraper, runs them in companyscraper
    one-by-one, and them puts them in an output file
    """
    def __init__(self, company_dict_list: list, bbb_args: Namespace, log: logging.Logger, **kwargs):

        self.args = bbb_args
        self.log = log
        self.company_list = company_dict_list
        self.db_password = None

        if self.args.type == "SQL":
            self.db_password = kwargs["password"]
            self._connection = kwargs["connection"]
            self._cursor = self._connection.cursor()

            self._run_program_proper_sql()

            if not kwargs["password"]:
                raise ConnectionError(M.SQL_BUT_NO_PASSWORD_ERROR)

    def _run_program_proper_sql(self) -> None:
        """
        moves the program logic away from __init__ for organizational purposes
        only works for SQL
        """
        # self._get_sql_from_file()

        self.log.debug(M.LOG_SAVING_COMPANIES_TO_FILE)
        for company in self.company_list:
            _company_scraper = BBBCompanyScraper(company, self.args, self.log)
            _item = _company_scraper.company_data
            self.log.debug(f'Inserting {_item["Name"]} into the databse.')
            self._cursor.execute(ICFG.SQL_INSERT_BUSINESS_PROFILE, (_item["Name"], _item["Alerts"],
                                                                    _item["Address"], _item["url"], _item["Phone"],
                                                                    _item["BBB File Opened"], _item["Type of Entity"],
                                                                    _item["Rating"]))
        self._connection.commit()
        self.log.debug(M.LOG_COMMIT_EXECUTE)

        self._cursor.close()

    def _get_sql_from_file(self):
        _file = ICFG.BBBORG_SQL_FILE

        if path.isfile(_file) is False:
            raise FileNotFoundError(M.SQL_FILE_NOT_FOUND_ERROR)
        else:
            with open(_file, "r") as f:
                _sql_file = f.read().split(';')
                self.log.info(M.LOG_READING_SQL_FILE + _file)

            for i in range(len(_sql_file)-1):
                self.log.debug(f"Executing {(''.join(list(_sql_file[i])[:40])).strip()}")  # shorten the debug output
                self._cursor.execute(_sql_file[i])
