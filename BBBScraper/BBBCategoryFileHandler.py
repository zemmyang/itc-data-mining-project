from argparse import Namespace
from BBBScraper import internal_config as ICFG
from BBBScraper import messages as M
import logging
from os import path


class BBBCategoryFileHandler:
    """
    saves categories in the SQL databse
    """
    def __init__(self, category_list: list, bbb_args: Namespace, log: logging.Logger, **kwargs):

        self.args = bbb_args
        self.log = log
        self.categories = category_list
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

        self.log.debug(M.LOG_SAVING_CATEGORIES_TO_FILE)

        for cat in self.categories:
            self.log.debug(f'Inserting category {cat} into the database.')
            self._cursor.execute(ICFG.SQL_INSERT_CATEGORIES, cat)

        self._connection.commit()
        self.log.debug(M.LOG_COMMIT_EXECUTE)

        self._cursor.close()

    # def _get_sql_from_file(self):
    #     _file = ICFG.BBBORG_SQL_FILEintegers
    #
    #     if path.isfile(_file) is False:
    #         raise FileNotFoundError(M.SQL_FILE_NOT_FOUND_ERROR)
    #     else:
    #         with open(_file, "r") as f:
    #             _sql_file = f.read().split(';')
    #             self.log.info(M.LOG_READING_SQL_FILE + _file)
    #
    #         for i in range(len(_sql_file)-1):
    #             self.log.debug(f"Executing {(''.join(list(_sql_file[i])[:40])).strip()}")  # shorten the debug output
    #             self._cursor.execute(_sql_file[i])
