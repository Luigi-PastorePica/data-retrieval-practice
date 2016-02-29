from bs4 import BeautifulSoup
from mechanize import urlopen
from mechanize import Browser
from mechanize import URLError
from mechanize import HTTPError
from time import sleep
from random import seed
from random import randint
import re
from scrape_util import *
from person_class import *

url = 'http://directory.tufts.edu/asearch.cgi'
first_char = 'a'
last_char = 'a'

browser_obj = instantiate_browser(url, False)
browser_obj.select_form("search")

query_chars = char_list_generator(first_char, last_char)

# start a for loop here to iterate over query_chars

# This portion, which fills the appropriate fields in the directory form, might become a function in the future.
# For that purpose browser object and query_char would be the arguments
browser_obj['type'] = ['Students']
browser_obj['LastOption'] = ['starts']
browser_obj['getLast'] = query_chars[0]     # Temporarily using only one set of chars for development and debugging


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

browser_obj.submit()

# Next, checking the response and using a loop to go through all the links provided.
# Each link will be opened and BeautifulSoup will be used to get all relevant info from response.
# BeautifulSoup object will be overwritten on each loop.
# Once all links checked, go back to first browser object and enter new chars into form.



# This part is used only for getting html in a file. Will be removed eventually.
# with open('tuft_page_response.txt', 'wb') as f:
#     f.write(browser_obj.response().read())



print "Application quit normally"
exit()

# def get_info(url_in):


