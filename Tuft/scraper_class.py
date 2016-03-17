

# This class is in early development. Not used in any form in the project yet

from bs4 import BeautifulSoup
from mechanize import urlopen
from mechanize import Browser
from mechanize import URLError
from mechanize import HTTPError
from time import sleep
from random import seed
from random import randint
from re import compile
from scrape_util import *           # Everything in module is used
from person_class import *          # Everything in module is used

class Scraper(object):

    # Constructor
    def __init__(self, url, ignore_robots):
        self.instantiate_browser(self, url, ignore_robots)


def instantiate_browser(self, url, ignore_robots = True):
    self.br_obj = Browser()
    self.br_obj.set_handle_equiv(True)
    # browser_obj.set_handle_gzip(True)     # Throws a warning, I have to check more in depth what this does
    self.br_obj.set_handle_redirect(True)
    self.br_obj.set_handle_referer(True)
    if ignore_robots is False:              # Ignores robots only if requested in instantiate_browser() call
        self.br_obj.set_handle_robots(False)
    self.br_obj.open(url)


def select_form(self, form_name = None):       # Could using the same method name as mechanize cause any conflicts?
    if form_name is None:
        self.br_obj.form = list(self.br_obj.forms())[0]     # Selects form w/o name. Careful, there could be more than one form!!!
    elif form_name is int:
        self.br_obj.form = list(self.br_obj.forms())[form_name]
    else:
        self.br_obj.select_form(form_name)      # Beware. Which select_name is called? My guess is Browser class'


def fill_form_control(self, control_type, control_name, control_value):
    if control_type.lower() == "radio" or control_type.lower() == "dropdown":
        self.br_obj[control_name]=[control_value]
    elif control_type.lower() == "text_box":
        self.br_obj[control_name]=control_value
    else:
        pass        # error here


# intended for use only within class. Is this bad practice?
def get_response(self):
    self.br_obj.submit()
    return self.br_obj.response()


# I have to give more though as to what is needed here. When and where will scraper class be instantiated
# Consider hard-coding parser. The class is designed with html.parser in mind anyway
def get_soup (self, parser, url = None):
    if url is None:
        return BeautifulSoup(get_response(self).read(), parser)
    elif type(url) == str:
        return BeautifulSoup(urlopen(url), parser)
    else:
        pass    # error here
    



