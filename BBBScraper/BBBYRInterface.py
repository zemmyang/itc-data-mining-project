# prevents BBBScraper from looking for the YelpRequester modules if the
# yelp flag is not used


def connect():
    """
    I understand that this is against PEP-8 conventions, but I wanted a
    way to make sure that BBBScraper still works even without the
    YelpRequester module
    """
    try:
        from YelpRequester.YRBBBCompanyFileHandler import YRBBBCompanyFileHandler
    except ModuleNotFoundError:
        raise ModuleNotFoundError("YelpRequester module not found")
    else:
        # do Yelp stuff
        yrbbb = YRBBBCompanyFileHandler()
        yrbbb.run()
