__author__ = 'Dmytro Chasovskyi'

from SuperclassSearch import *

class AmainhobbiesSearch(Search):

    def __init__(self, data_for_search, domain="http://amainhobbies.com"):
        Search.__init__(self, data_for_search, domain)

    def get_price(self, web_element):
        return web_element.get_attribute("data-price")

    def pull_price_from_search_data(self):
        return Search.pull_price_from_set_data(self, self.get_price, "quick_find", "//div[@data-position='1']")
