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


# Function get_person_info() is not intended to be reusable
# Takes (link, name) tuple. Returns StudentPersonInfo object
def get_person_info(link_and_name):

    if type(link_and_name) is tuple:
        mini_soup = BeautifulSoup(urlopen('http://whitepages.tufts.edu/' + str(link_and_name[1])).read(), "html.parser")
        full_name = name_splitter(link_and_name[0])
    elif type(link_and_name) is BeautifulSoup:
        mini_soup = link_and_name
        full_name = None
    else:
        raise AttributeError('link_and_name must be either a tuple or a BeautifulSoup instance')
        mini_soup = None
        student = None

    if mini_soup is not None:

        td_tags = mini_soup.find_all('td')

        if full_name is None:
            name = td_tags[1].get_text().strip()
            full_name = name_splitter(name, False)

        email = td_tags[9].get_text().strip()

        # If there is no e-mail or no name, there is no use for the
        if email is None or email == '' or full_name is None or full_name == '':
            student = None

        else:

            major = td_tags[5].get_text().strip()
            affiliation = td_tags[11].get_text().strip()
            if affiliation is None or affiliation == '':
                affiliation = '=NA()'

            student = StudentPersonInfo(full_name[1], full_name[2], full_name[0], email, affiliation, "=NA()", major)

    return student

url = 'http://directory.tufts.edu/asearch.cgi'
person_page_url = 'http://directory.tufts.edu/'
first_char = 'a'
last_char = 'a'


query_strings = char_list_generator(first_char, last_char)

for query_string in query_strings:

    # Instantiation of a browser object
    browser_obj = instantiate_browser(url, False)

    soup = BeautifulSoup(get_form_response(browser_obj, query_string).read(), "html.parser")

    soup.html.extract()  # Removes the whole html tag. Only what is after the html tag is required. Returned object lost.

    a_tags = soup.find_all('a')  # Gets all the link tags

    print query_string  #Debugging
    print len(a_tags)   #Debugging

    if len(a_tags) == 0:
        continue
    del a_tags[-1]               # Last link removed, not relevant.

    if a_tags[-1].get('href').startswith('mailto'):
        for i,b in enumerate(soup.find_all('td')):
            print str(i) + b.get_text()
        student_list = [get_person_info(soup)]

    else:
        # List of StudentPersonInfo objects. None objects not appended.
        try:
            student_list = filter(None, (get_person_info(get_name_link(a_tag)) for a_tag in a_tags))
        except AttributeError:
            continue
        else:
            export_to_csv('tuft_student_dir.csv', student_list)

print "Application quit normally"
exit()



