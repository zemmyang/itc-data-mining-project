import pymysql
import pandas as pd
import re
from YelpRequester import YelpRequester
from YelpRequester.YRBusinessID import YRBusinessID
from YelpRequester import internal_config as ICFG
from YelpRequester import messages as M
import os


class YRBBBCompanyFileHandler:
    """
    Queries the BBBOrg database for companies in the list
    and adds information from yelp

    Only be used through BBBYRInterface
    """
    def __init__(self):
        self.yelp_requester = YelpRequester()

    def run(self):
        self.yelp_requester.logger.info("Starting YRBBBCompanyFileHandler")
        self._main_program_logic()

    def _main_program_logic(self):
        self._set_up_sql_conn()
        self._set_up_yrbbb_table()

        # should query the database for what companies are in there
        self._read_table()

        # and then fills out the information
        self._append_yelp_details()

    def _set_up_sql_conn(self):
        _sql_credentials = self.yelp_requester.get_sql_credentials()
        self.connection = pymysql.connect(host=_sql_credentials['sql_host'], user=_sql_credentials['sql_user'],
                                          passwd=_sql_credentials['sql_password'], db=_sql_credentials['sql_db'])

    def _set_up_yrbbb_table(self):
        _cursor = self.connection.cursor()
        _file = ICFG.YELPREQUESTER_SQL_FILE

        try:
            with open(os.path.join(os.getcwd(), _file), "r") as f:
                _sql_file = f.read().split(';')
                self.yelp_requester.logger.info("reading sql file" + _file)

            for i in range(len(_sql_file) - 1):
                # self.yelp_requester.logger.debug(M.LOG_EXECUTING_SQL_DEBUG.format(query=''.join(list(_sql_file[i])[:40])).strip())
                _cursor.execute(_sql_file[i])
            self.connection.commit()
            _cursor.close()
        except FileNotFoundError:
            raise FileNotFoundError("File not found")

    def _read_table(self):
        _query = """
        SELECT business_name, location FROM bbborg.business_profile;
        """

        self.bbb_company_table = pd.read_sql(_query, self.connection)
        _business_name = self.bbb_company_table.pop('business_name')

        self.bbb_company_table = self.bbb_company_table['location'].str.split(", ", expand=True)
        self.bbb_company_table = self.bbb_company_table.rename(columns={0: "address", 1: "city", 2: "state zip"})

        _state_zip = self.bbb_company_table['state zip'].str.split(" ", expand=True)
        _state_zip = _state_zip.rename(columns={0: "state", 1: "zip"})

        self.bbb_company_table = pd.concat([self.bbb_company_table, _state_zip], axis=1)
        self.bbb_company_table = self.bbb_company_table.drop(["state zip", 3], axis=1)

        self.bbb_company_table = pd.concat([_business_name, self.bbb_company_table], axis=1)

    def _append_yelp_details(self):
        _cursor = self.connection.cursor()

        for item in self.bbb_company_table:
            print(item)
            print(type(item))
            print(self.bbb_company_table[item])
            print(type(self.bbb_company_table[item]))
            _yr_business_id = YRBusinessID(name=item["business_name"], address=item["address"], city=item["city"],
                                           state=item['state'], country=item['country'])

            self.yelp_requester.logger.debug(f"Found details for {_yr_business_id['yelp_id']}, appending...")
            _cursor.execute(ICFG.SQL_INSERT_YELP_ID, (_yr_business_id["yelp_id"], _yr_business_id["business_name"],
                                                      _yr_business_id["address"], _yr_business_id["coord_lat"],
                                                      _yr_business_id["coord_long"], _yr_business_id["display_phone"],
                                                      _yr_business_id["city"], _yr_business_id["country"],
                                                      _yr_business_id['zipcode'], _yr_business_id['yelp_url'],
                                                      _yr_business_id['yelp_rating']))
        self.connection.commit()
        _cursor.close()


def test():
    a = YRBBBCompanyFileHandler()
    a.run()
    print(a.bbb_company_table.sample(1))


if __name__ == "__main__":
    test()
