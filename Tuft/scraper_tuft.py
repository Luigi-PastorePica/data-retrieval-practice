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


# Function get_person_info() is not intended to be reusable
# Takes (link, name) tuple. Returns StudentPersonInfo object
def get_person_info(link_and_name):

    info_page_url = 'http://directory.tufts.edu/'
    # If name and individual's info page's link were obtained from list of students, open the info page and assign name
    if type(link_and_name) is tuple:
        mini_soup = BeautifulSoup(urlopen(info_page_url + str(link_and_name[1])).read(), "html.parser")
        full_name = name_splitter(link_and_name[0])
    # Else, if search yielded only one result, the individual's info page itself is passed as a BS object.
    elif isinstance(link_and_name, BeautifulSoup):
        mini_soup = link_and_name
        full_name = None
    # If there were no results, use variables as flags to skip to next search.
    else:
        mini_soup = None    # Consider raising an AttributeError. Code to catch it is already in place.
        student = None

    # If there is at least one result, execute this part
    # Consider raising an AttributeError as stated above to prevent this if statement
    if mini_soup is not None:

        # If the full_name has not been acquired yet, try to get it from individual's info page.
        # If keep value becomes false at any point, a NoneType object is returned and the individual is skipped
        if full_name is None:
            try:
                name_b_tag = mini_soup(text=compile('^Name:'))[0].parent
            except IndexError:
                keep = False        # Flag. Name was not obtained. Skip individual.
            else:
                if name_b_tag is None:
                    keep = False        # Flag.Name was not obtained. Skip individual.
                else:
                    full_name = name_splitter(name_b_tag.find_next('td').get_text(), False)  # Parse and store name
                    keep = True         # Flag. Name was obtained
        else:
            keep = True # Flag. Name was obtained at a previous point

        # Try to acquire e-mail
        if keep is True:
            try:
                email_b_tag = mini_soup(text=compile('^Email Address:'))[0].parent
            except IndexError:
                keep = False        # Flag. e-mail could not be acquired. Skip individual.
            else:
                if email_b_tag is None:
                    keep = False    # Flag. e-mail could not be acquired. Skip individual.
                else:
                    email = email_b_tag.find_next('td').get_text().strip()  # Store e-mail

        # Try to acquire affiliation
        if keep is True:
            try:
                affiliation_b_tag = mini_soup(text=compile('^Primary Affiliation:'))[0].parent
            except IndexError:
                affiliation = '=NA()'   # Affiliation not available
            else:
                if affiliation_b_tag is None:
                    affiliation = '=NA()'   # Affiliation not available
                else:
                    affiliation = affiliation_b_tag.find_next('td').get_text().lstrip()     # Store affiliation
                    # If the primary affiliation is not Student, skip individual.
                    if not affiliation.startswith(('Student','student')):
                        keep = False

        # Try to acquire major
        if keep is True:
            try:
                major_b_tag = mini_soup(text=compile('^Major:'))[0].parent
            except IndexError:
                major = '=NA()'         # Major not available
            else:
                if major_b_tag is None:
                    major = '=NA()'     # Major not available
                else:
                    major = major_b_tag.find_next('td').get_text().lstrip()     # Store major

            # Create StudentPersonInfo instance with acquired info
            # No organization available for most students. Value was hard coded for improved efficiency
            student = StudentPersonInfo(full_name[1], full_name[2], full_name[0],\
                                        email, affiliation, "=NA()", major)

            print student.join_info()   # Debugging

        # If keep flag became false at any point, skip individual by returning None.
        else:
            student = None

    return student

url = 'http://directory.tufts.edu/asearch.cgi'
first_char = 'v'
last_char = 'z'

query_strings = char_list_generator(first_char, last_char)      # Generate two character strings

for query_string in query_strings:

    browser_obj = instantiate_browser(url, False)   # Instantiation of a browser object. Ignore robots.txt

    soup = BeautifulSoup(get_form_response(browser_obj, query_string).read(), "html.parser")   # Fill form, get response

    a_tags = soup.find_all(href=compile('^ldapentry'))  # Gets a list with all the relevant link tags

    print query_string  #Debugging
    print len(a_tags)   #Debugging

    # If there are no relevant tags, pass the BeautifulSoup object instead to check if the result is a single
    #  individual's info page instead
    for tries in range(3):
        if len(a_tags) == 0:
            try:
                student_list = [get_person_info(soup)]
            except HTTPError as e:
                print e
                print "Tried to reach page " + str(tries + 1) + " times"
                if tries > 2:
                    exit()          # If the page could not be reached after 3 tries, exit. Consider alternative
            except URLError as e:
                print e
                print "Tried to reach page " + str(tries + 1) + " times"
                if tries > 2:
                    exit()          # If the page could not be reached after 3 tries, exit. Consider alternative
            except AttributeError:  # Not used for now. Left in place in case get_person_info is changed in the future
                break
            else:
                if student_list[0] is None:     # Exceptions done separately to prevent checking this condition w/o need
                    if len(student_list) == 1:
                        break
                    else:
                        pass    # Consider adding an error message. There should be only one element in list
                else:
                    export_to_csv('tuft_student_dir.csv', student_list)     # Write a single student's info to CSV file
                break               # Continue to next query string
        else:
            # Try to obtain a list of StudentPersonInfo objects. None objects not appended.
            try:
                student_list = filter(None, (get_person_info(get_name_link(a_tag)) for a_tag in a_tags))
            except HTTPError as e:
                print e
                print "Tried to reach page " + str(tries + 1) + " times"
                if tries > 2:
                    exit()          # If the page could not be reached after 3 tries, exit. Consider alternative
            except URLError as e:
                print e
                print "Tried to reach page " + str(tries + 1) + " times"
                if tries > 2:
                    exit()          # If the page could not be reached after 3 tries, exit. Consider alternative
            except AttributeError:  # Not used for now. Left in place in case get_person_info is changed in the future
                break               # Continue to next query string

            else:
                export_to_csv('tuft_student_dir.csv', student_list)

print "Application quit normally"
exit()



