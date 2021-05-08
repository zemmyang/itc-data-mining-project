from YelpRequester import YelpRequester
from YelpRequester import internal_config as ICFG
from YelpRequester import messages as M


class YRBusinessID:
    """
    one class instance is used for every company

    uses the Business Match endpoint to find the Yelp ID of the company
    if not found, tries the phone search endpoint
    if still not found, then it tries the autocomplete endpoint
    """
    def __init__(self, **kwargs):
        self.yelp_requester = YelpRequester()
        self.yelp_requester.logger.debug(M.YRBUSINESSID_INITIALIZING_DEBUG)
        self.kwargs_dict = kwargs
        self._run_search()

    def _run_search(self):
        """ uses the endpoints depending on what arguments are available """

        _kwd = self.kwargs_dict
        _keys_to_use_with_business_match = ['name', 'address', 'city', 'state', 'country']
        _keys_to_use_with_business_search = ['name', 'location']

        if 'name' not in _kwd.keys():
            self.yelp_requester.logger.warning(M.YRBUSINESSID_NO_NAME_ARGS_WARNING)
            self.business_id = "Null"
        else:
            if all(k in _kwd.keys() for k in _keys_to_use_with_business_match):
                _response = self._business_match_endpoint(name=_kwd['name'], address=_kwd['address'],
                                                          city=_kwd['city'], state=_kwd['state'],
                                                          country=_kwd['country'])
            elif all(k in _kwd.keys() for k in _keys_to_use_with_business_search):
                _response = self._business_search_endpoint(name=_kwd['name'], location=_kwd['location'])
            else:
                _response = self.yelp_requester.return_fake_request()

            if self.yelp_requester.check_response(_response):
                # if the response is ok
                self.business_id = _response.json()["businesses"][0]['id']
            else:
                self.yelp_requester.logger.warning(M.YRBUSINESSID_NOT_FOUND_WARNING.format(name=_kwd['name']))
                self.business_id = "Null"

    def _make_request(self, path, url_params):
        """ send the actual request """
        self.yelp_requester.logger.debug(M.YRBUSINESSID_MAKING_REQUEST_DEBUG)
        return self.yelp_requester.request(path, url_params)

    def _business_match_endpoint(self, name, address, city, state, country):
        """ when very precise information is available. state and country should be ISO 3166-2 """
        if len(state) > 2:
            self.yelp_requester.logger.warning(M.YRBUSINESSID_BAD_ISO_WARNING.format(what=state))
            return self._business_search_endpoint(name, city)
        elif len(country) > 2:
            self.yelp_requester.logger.warning(M.YRBUSINESSID_BAD_ISO_WARNING.format(what=country))
            return self._business_search_endpoint(name, city)
        else:
            self.yelp_requester.logger.info(M.YRBUSINESSID_RUNNING_BMATCH_INFO.format(name=name))
            url_params = {
                'name': name.replace(' ', '+'),
                'address1': address.replace(' ', '+'),
                'city': city.replace(' ', '+'),
                'state': state,
                'country': country,
                'limit': self.yelp_requester.get_limit()
            }

            return self._make_request(ICFG.SEARCH_PATH, url_params)

    def _business_search_endpoint(self, name, location):
        """ when only a general location and the name is available """
        self.yelp_requester.logger.info(M.YRBUSINESSID_RUNNING_BSEARCH_INFO.format(name=name))

        url_params = {
            'term': name.replace(' ', '+'),
            'location': location.replace(' ', '+'),
            'limit': self.yelp_requester.get_limit(),
            'locale': self.yelp_requester.get_locale()
        }

        return self._make_request(ICFG.SEARCH_PATH, url_params)

    def __getitem__(self, item):
        """ returns the data used to make the search """
        if item == "business_id" or item == 'id':
            return self.business_id
        elif item in self.kwargs_dict.keys():
            return self.kwargs_dict[item]
        else:
            return None


def test():
    yr = YRBusinessID(name='filipino food', location='Los Angeles, CA')
    print(yr['name'], yr['id'])

    another_yr = YRBusinessID(name='aaa')
    print(another_yr['name'], another_yr['business_id'])


if __name__ == "__main__":
    test()
