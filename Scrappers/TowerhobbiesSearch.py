__author__ = 'Dmytro Chasovskyi'

from SuperclassSearch import *

class TowerhobbiesSearch(Search):

    def __init__(self, data_for_search, domain="http://www3.towerhobbies.com/"):
        Search.__init__(self, data_for_search, domain)

    def get_price(self, web_element):
        return web_element.text

    def pull_price_from_search_data(self):
        return Search.pull_price_from_set_data(self, self.get_price, "isearch", "//font[color='RED'']")
