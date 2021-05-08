from YelpRequester import YelpRequester
from YelpRequester import internal_config as ICFG
from YelpRequester import messages as M


class YRReviewScraper:
    def __init__(self, business_id):
        self.yelp_requester = YelpRequester()
        self.business_id = business_id

    def _make_request(self, path, url_params):
        """ send the actual request """
        self.yelp_requester.logger.debug(M.YRREVIEWSCRAPER_MAKING_REQUEST_DEBUG)
        return self.yelp_requester.request(path, url_params)

    def _review_endpoint(self):
        self.yelp_requester.logger.info(M.YRREVIEWSCRAPER_REQUESTING_ID_INFO.format(id=self.business_id))
        url_params = {"locale": self.yelp_requester.get_locale()}
        return self._make_request(ICFG.REVIEW_PATH.format(business_id=self.business_id), url_params)

