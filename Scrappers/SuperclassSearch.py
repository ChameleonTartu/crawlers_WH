__author__ = 'Dmytro Chasovskyi'

from selenium import webdriver
from collections import defaultdict
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, UnexpectedAlertPresentException
import time
import random

class Search(object):

    def __init__(self, data_for_search, domain):
        self.data__for_search = data_for_search
        self.domain = domain
        self.driver = webdriver.Firefox()
        self.driver.get(domain)
        self.data = defaultdict(lambda: "n/a")

    def filter_price_query(self, price):
        return price.replace("$", "").replace(" ", "")

    def sleep_immediately(self, seconds):
        time.sleep(random.choice(xrange(seconds, 2*seconds)))
        return None

    def submit_search_query(self, search_button_id, item_for_search):
        element = self.driver.find_element_by_id(search_button_id)
        element.clear()
        try:
            alert_ = self.driver.switch_to.alert
            alert_.dismiss()
        except NoAlertPresentException:
            pass
        element.send_keys(item_for_search)
        element.submit()

    def pull_price_from_set_data(self, get_price, search_button_id, xpath_for_search_item,
                                 usual_stop=5, accidental_stop=20):
        for item_for_search in self.data__for_search:
            try:
                try:
                    self.submit_search_query(search_button_id, item_for_search)
                    self.sleep_immediately(usual_stop)
                except NoSuchElementException:
                    self.sleep_immediately(accidental_stop)
                    try:
                        self.driver.get(self.domain)
                    except NoSuchElementException:
                        print "Impossible to scarp this website"
                        self.driver.close()
                        return None
            except UnexpectedAlertPresentException:
                alert_ = self.driver.switch_to.alert
                alert_.dismiss()
                self.sleep_immediately(accidental_stop)

            self.pull_search_item(get_price, xpath_for_search_item, item_for_search)
            print self.driver.current_url
        self.driver.close()
        return self.data

    def pull_search_item(self, get_price, xpath_for_search_item, item_for_search):
        try:
            html_block = self.driver.find_element_by_xpath(xpath_for_search_item)
            price = get_price(html_block)
            self.data[item_for_search] = self.filter_price_query(price)
        except NoSuchElementException:
            create_item = self.data[item_for_search]
        return None

