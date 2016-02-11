# Note: Get info does not return anything for the time being. This will change.
# Large portion of commented code. Do not pay attention, all of it will likely be absent from the next commit


from bs4 import BeautifulSoup
from mechanize import urlopen       # mechanize implements urllib2 and expands it
from mechanize import Browser
from mechanize import HTTPError
from mechanize import URLError
import time
import re       # Please provide feedback on this library.
                # Used to find classes in the html code that start with a specific string
import csv      # Not implemented yet


# Generates an ordered alphabetic list that spans from "start" to "finish" (inclusive)
# Asterisk added after each character (website's form's specific requirement)
# If "start"'s and "finish"'s order is inverted, the function puts them in order
def char_list_generator(start, finish):

    start, finish = char_fix(start, finish)
    ascii_code_list = range(ord(start), ord(finish) + 1)
    char_list = []
    for code in ascii_code_list:
        char_list.append(chr(code) + '*')

    return char_list

# Determines whether the characters "first" and "last" are in valid Alphabetic range
# Returns uppercase version "first" and "last" in alphabetic order
def char_fix(first, last):

    # Determines range of valid ASCII characters
    initial_limit_lower = ord('a')
    final_limit_lower = ord('z')
    initial_limit_upper = ord('A')
    final_limit_upper = ord('Z')

    # Converts characters to ASCII code equivalent
    first_ascii = ord(first)
    last_ascii = ord(last)

    # Exceptions in case a non alphabetic character is used by mistake
    # Not sure whether I am implementing this properly
    try:
        if first_ascii < initial_limit_upper or first_ascii > final_limit_upper:        # If alpha and uppercase, nothing is done
            if first_ascii < initial_limit_lower or first_ascii > final_limit_lower:    # If not within limits, then it is not alpha
                raise CharacterDomainError(first)
            else:
                first = first.upper()               # Converts alpha lowercase to uppercase
                first_ascii = ord(first)            # And reassigns to proper ASCII code

    except CharacterDomainError as e:
        print(e.value, "character does not belong to the English alphabet")
        return None

    try:
        if last_ascii < initial_limit_upper or last_ascii > final_limit_upper:          # If alpha and upper, nothing is done
            if last_ascii < initial_limit_lower or last_ascii > final_limit_lower:      # If not within limits, then it is not alpha
                raise CharacterDomainError(last)
            else:
                last = last.upper()                 # Converts alpha lowercase to uppercase
                last_ascii = ord(last)              # And reassigns to proper ASCII code

    except CharacterDomainError as e:
        print(e.value, "character does not belong to the English alphabet")
        return None

    # Places initial and final characters in order if required
    if first_ascii > last_ascii:
        first, last = last, first

    return (first, last)


class CharacterDomainError (Exception):             # Not sure I am implementing this properly
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class CollegePersonInfo:

    def __init__(self, name, last_name, major, email, affiliation):

        self.name = name
        self.last_name = last_name
        self.major = major
        self.email = email
        self.affiliation = affiliation


# Gets the information of every person in the directory
def get_info(urlin, first_char, last_char):

    br = Browser()

    # Exception handling for page open request
    try:
        br.open(urlin)
    except HTTPError as e:
        print(e)
        return None
    except URLError as e:
        print(e)
        return None

    query_chars = char_list_generator(first_char, last_char)
    print query_chars                                           #Debugging
    info_list = []

    for string in query_chars:
        br.form = list(br.forms())[0]       # Used to select form w/o name attribute
        br['lastname'] = string             # Places query string into last name field
        br.submit()

        # Exception handling for response
        try:
            soup = BeautifulSoup(br.response().read(), "html.parser")   # HTML file containing response page code
        except AttributeError as e:
            print(e)
            return None

        # Records html code inside the tr tags that contain classes that start with record-person (each represented by var person).
        # Inside each of these tr tags there are different td tags with the desired info.
        # I am planning to make a list of these code sections and extracting the pertinent info on each iteration.
        for person in soup.findAll('tr', class_=re.compile('^record-person')):
            print person        # print for Debugging purposes
            return person       # return for debugging purposes. Must remove


        # Please disregard the commented section bellow. It is part of the old code and will most probably be removed completely
        '''
        i = 0
        for aName in soup.find_all("span", {"class": "link results-name"}):

            n = aName.get_text()            # remember to parse name and last name if necessary.
            info_list.nameList.append(n)     # Remember to get rid of "(Click to show details)"

            print(info_list.nameList[i])
            i += 1

        i = 0
        for anEmail in soup.find_all("td",{"class": "record-data-email"}):

            e = anEmail.get_text()
            info_list.emailList.append(e)

            print(info_list.email[i])
            i += 1

        i = 0
        for anAffiliation in soup.find_all("div", {"class": "results-affiliation"}):

            aff = anAffiliation.get_text()
            info_list.affiliationList.append(aff)

            print(info_list.affiliationList[i])
            i += 1

        time.sleep(15)  # Forces 15 second wait time until next request (to prevent being detected as a bot)

    return info_list'''

# Test characters
start_char = 'Z'
finish_char = 'a'

names = get_info("https://www.osu.edu/findpeople/", start_char, finish_char)
print names

if names == None:
    print ("Page could not be opened")