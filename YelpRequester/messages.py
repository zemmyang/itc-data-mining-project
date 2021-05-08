# YRBusinessID

YRBUSINESSID_NO_NAME_ARGS_WARNING = "No 'name' in kwargs dict passed to YRBusinessID"
YRBUSINESSID_NOT_FOUND_WARNING = "Business {name} not found using Yelp API. Setting business_id to Null"
YRBUSINESSID_BAD_ISO_WARNING = "Check input data. Invalid {what} code. Using Business Search Endpoint instead."

YRBUSINESSID_RUNNING_BSEARCH_INFO = "Running Business Search on {name}"
YRBUSINESSID_RUNNING_BMATCH_INFO = "Running Business Match on {name}"
YRBUSINESSID_RUNNING_AUTOCOM_INFO = "Running Autocomplete Search on {name}"

YRBUSINESSID_INITIALIZING_DEBUG = "YelpRequester BusinessID initialized"
YRBUSINESSID_MAKING_REQUEST_DEBUG = "Sending GET request for business ID"

# YRReviewScraper

YRREVIEWSCRAPER_REQUESTING_ID_INFO = "Running Reviews Search for {id}"

YRREVIEWSCRAPER_MAKING_REQUEST_DEBUG = "Sending GET request for review"

# YelpRequester

YELPREQUESTER_CONFIG_FILE_CRITICAL = 'yelprequester.json not found! API Key missing'
YELPREQUESTER_GENERIC_ERROR_CRITICAL = "Error found: {message}"

YELPREQUESTER_ERROR_IN_RESPONSE_WARNING = "Found error in OK response. Setting business_id to Null"

YELPREQUESTER_APIKEY_FOUND_DEBUG = "Obtained API key from {logfile}"
