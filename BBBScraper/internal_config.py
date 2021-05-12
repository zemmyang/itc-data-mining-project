import logging


LOG_FORMAT = \
    logging.Formatter('%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s')


# constants

STARTING_URL = 'https://www.bbb.org/'
BBBORG_SQL_FILE = 'bbborg.sql'  # make sure this is in root, not in bbbscraper directory
SQL_HOST = 'localhost'
SQL_USER = 'root'
SQL_DB = 'bbborg'

REGEX_PAGE_X_OF_Y = r'((Page)\s\d+\s(of)\s\d+)'
REGEX_SHOWING_X_RESULTS = r'((Showing:)\s\d+\s(results))'
REGEX_GET_IDNUM_FROM_URL = r'(\d+-\d+)'

# headers
HEADERS = [{
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'referer': 'https://www.google.com/',
    'accept-language': 'en-US,en;q=0.9'
},
{
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://duckduckgo.com/',
    'Connection': 'keep-alive',
},
{
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 OPR/75.0.3969.93',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'referer': 'https://www.facebook.com/',
    'accept-language': 'en-US,en;q=0.9'
}
]

BS4_HTML_PARSER = 'html.parser'

ZEMMY_PW = 'd4rth!x3mnas'

SQL_INSERT_BUSINESS_PROFILE = """
INSERT INTO `business_profile` (business_name, alerts, location, website, phone_number, bbb_file_opened, type_of_entity, bbb_rating)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

SQL_INSERT_CATEGORIES = """
INSERT INTO `categories` (category_name)
VALUES (%s)
"""