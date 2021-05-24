ENTER_SQL_PASSWORD = "Please enter SQL database password here: "

# Argparser help
VERBOSE_HELP = "Makes output verbose (outputs debug log in terminal)"
CONFIG_HELP = "Uses a config.json file instead of passing arguments"
LOG_HELP = 'Print out warnings to utils log file (logs to log.txt by default'
TYPE_HELP = 'Save to utils different file type (Default: SQL)'
DEFAULT_HELP = 'Use some defaults (Scrapes Restaurants)'
YELP_HELP = "Uses YelpRequester to scrape additional information and reviews about a company"
CONTINUOUS_HELP = "Does not create new tables, tries to update whenever possible"

CATS_HELP = 'Categories to scrape (spaces are fine, but the CLI works for only one category per run. ' \
            'Use the config file for more)'
LIM_HELP = 'Limit number of companies to scrape'
LOC_HELP = 'Location (US or CA only. Default is US)'
ACC_HELP = "Get only BBB-accredited businesses"
ALL_HELP = "Scrape Everything? Everything (ignores cats if defined)."

# Notifications and logs
NO_CONFIG_USED = 'No config file specified, running using command-line arguments'

LOG_ASKING_FOR_SQL_PASSWORD = "Asking for password..."
LOG_START_SCRAPER = "Starting the scraper..."
LOG_START_CAT_SCRAPER = "Starting BBB Category Scraper..."
LOG_READING_SQL_FILE = "Reading SQL file..."
LOG_SAVING_COMPANIES_TO_FILE = "Saving companies to file..."
LOG_SAVING_CATEGORIES_TO_FILE = "Saving categories to file..."
LOG_COMMIT_EXECUTE = "Committing executions..."
LOG_YELP = "Also scraping information from YELP."

LOG_CATEGORY_FOUND_DEBUG = '{cats} found! Scraping URLs...'
LOG_CATS_NOT_FOUND = '{cats} not found. Exiting...'
LOG_LOGGING_SET_UP_DEBUG = "Logger set-up"
LOG_SITEMAP_READ_INFO = 'Found {catnum} categories'
LOG_EXECUTING_SQL_DEBUG = "Executing {query}"

# Error Messages
NO_ALL_FLAG_BUT_NO_CAT_ERROR = "Please provide a category to scrape."
CONFIG_NOT_IMPLEMENTED_ERROR = "Using config files is not implemented in this version"
SQL_BUT_NO_PASSWORD_ERROR = "Please enter a password for SQL"
SCRAPE_ALL_NOT_IMPLEMENTED_ERROR = "Scraping everything is not implemented yet"
SQL_FILE_NOT_FOUND_ERROR = "SQL file not found!"
TO_CSV_NOT_IMPLEMENTED_ERROR = "Exporting to CSV not yet implemented"

# this code is brought to you by our feline overlords!
EPILOGUE = "meow meow ani hatula"
