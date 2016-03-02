from bs4 import BeautifulSoup
from mechanize import urlopen
from mechanize import Browser
from mechanize import URLError
from mechanize import HTTPError
from time import sleep
from random import seed
from random import randint
import re
from scrape_util import *       # Is it preferable to just import the module and call funct. in this way: scrape_util.instantiate_browser()
from person_class import *

url = 'http://directory.tufts.edu/asearch.cgi'
first_char = 'a'
last_char = 'a'

# Instantiation of a browser
browser_obj = instantiate_browser(url, False)
browser_obj.select_form("search")

query_chars = char_list_generator(first_char, last_char)

# start a for loop here to iterate over query_chars

# This function will eventually be moved to scrape_util module
# Fills directory form and submits it. Returns the response from the mechanize browser object
# Fields to be filled and values are mostly predetermined. Only query_char (second argument) changes when called.
def fill_form(browser_object, query_string):
    browser_object['type'] = ['Students']
    browser_object['LastOption'] = ['starts']
    browser_object['getLast'] = query_string     # Temporarily using only one set of chars for development and debugging


    # This piece of code below does exactly the same

    # control1 = browser_obj.form.find_control('type')
    # control1.value = ['Students']
    # control2 = browser_obj.form.find_control('LastOption')
    # control2.value = ['starts']
    # control3 = browser_obj.form.find_control('getLast')
    # control3.value = query_char

    # And yet again, the code below does exactly the same
    
    # control1 = browser_obj.form.find_control('type')
    # browser_obj[control1.name] = ['Students']
    # control2 = browser_obj.form.find_control('LastOption')
    # browser_obj[control2.name] = ['starts']
    # control3 = browser_obj.form.find_control('getLast')
    # browser_obj[control3.name] = query_char

    browser_object.submit()
    return browser_object.response()

soup = BeautifulSoup(fill_form(browser_obj, query_chars[0]).read(), "html.parser")  # Testing with only one query_string

soup.html.extract()  # Removes the whole html tag. Only what is after the html tag is required. Returned object lost.

link_tags = soup.find_all('a')  # Gets all the link tags
del link_tags[-1]               # Last link removed, not relevant.

for link_tag in link_tags:
    full_name = link_tag.string.extract()
    print full_name
    # link_tag.a.unwrap()
    print


for link_tag in link_tags:
    print link_tag
    print



# Each link will be opened and BeautifulSoup will be used to get all relevant info from response.
# BeautifulSoup object will be overwritten on each loop.
# Once all links checked, go back to first browser object and enter new chars into form.




print "Application quit normally"
exit()

# def get_info(url_in):


