__author__ = 'Dmytro Chasovskyi'

import urllib2
from bs4 import BeautifulSoup
import httplib
import socket


class AmainhobbiesCrawler:

    def __init__(self, start_url):
        self.start_url = start_url
        self.safe_start_url = start_url.replace("http://", "https://")
        self.content = dict()
        self.link_queue = [start_url]

    def add_and_filtering_url(self, link):
        new_url = link.attrs['href'].strip()
        if new_url not in self.link_queue:
            image_extensions = [".jpg", ".png", ".jpeg", ".gif", ".bmp", ".dib", ".jpe", ".jfif", ".tif", ".tiff"]
            for extension in image_extensions:
                if extension in new_url:
                    return None
            if "#tab-feedback" in new_url or "@" in new_url or " " in new_url:
                return None

            if "http://" in new_url and self.start_url[:-1] not in new_url:
                return None
            if "https://" in new_url and self.safe_start_url[:-1] not in new_url:
                return None

            if new_url[0] == "/":
                if new_url[1:] in self.link_queue:
                    return False
                self.link_queue.append(new_url[1:])
            else:
                self.link_queue.append(new_url)
        return None

    def get_data_from_object_if_possible(self, bs_object):
        try:
            item_id = bs_object.find(itemprop="identifier").get_text().strip()
            price = bs_object.find(itemprop="price").get_text().strip()
            if item_id in self.content:
                return None
            self.content[item_id] = price

            print "Identifier: " + item_id + "\t" + "Price: " + price
        except:
            pass
        return None

    def get_links_from_object(self, bs_object):
        for link in bs_object.findAll("a"):
            if 'href' in link.attrs and link.attrs['href'] != '':
                self.add_and_filtering_url(link)
        return None

    def get_content_and_all_links_from_link(self, page_url):
        page_url = u"{}".format(page_url).encode('ascii', 'ignore')

        try:
            if self.start_url[:-1] in page_url or self.safe_start_url[:-1] in page_url:
                html = urllib2.urlopen(page_url)
            elif "http://" not in page_url and "https://" not in page_url:
                html = urllib2.urlopen(self.start_url + page_url)
            else:
                html = ""

            if html != "":
                try:
                    bs_object = BeautifulSoup(html, "html.parser")
                    self.get_data_from_object_if_possible(bs_object)
                    self.get_links_from_object(bs_object)
                except httplib.IncompleteRead as e:
                    print "Partial: " + e.partial

        except urllib2.URLError as e:
            print "urllib2.URLError"
        except ValueError as e:
            print "Value Error"
        except socket.error as e:
            print "Socket error"
        #except urllib2.HTTPError as e:
        #    print "urllib2.HTTPError"
        return None

    def pull_data(self):
        for item in self.link_queue:
            self.get_content_and_all_links_from_link(item)
        return None

    def get_content(self):
        return self.content
