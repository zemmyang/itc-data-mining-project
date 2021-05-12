YELPREQUESTER_CONFIG_FILE = 'yelprequester.json'
YELPREQUESTER_LOG_FILE = "yelprequester.log"
YELPREQUESTER_SQL_FILE = 'yrbbborg.sql'

API_KEY = None
STARTING_URL = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'
DETAILS_PATH = '/v3/businesses/{id}'

LOG_FORMAT = '%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s'

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

# regex
REGEX_STATE_AND_ZIP = r'(.. \d+-\d+)|(.. \d+)$'
REGEX_CITY_AND_STATE = r'(, \w+, ..)|(, \w+ , ..)'

# sql
SQL_INSERT_YELP_ID = """
INSERT INTO `yelp_business_id` (yelp_id, business_name, address, coord_lat, coord_long, display_phone, city, country, zipcode, yelp_url, yelp_rating)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
