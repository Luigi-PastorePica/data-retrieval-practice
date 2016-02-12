# Note: Get info does not return anything for the time being. This will change.


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
    
    student_list = []
    others_list = []

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

        for person in soup.find_all('tr', class_=re.compile('^record-person')):

            # Exception applied to handle an attribute error always present in the last iteration
            try:
                affiliation = person.find_next("div", {"class": "results-affiliation"}).get_text()
            except AttributeError as e:
                print (e)
            finally:

                if affiliation == "Student":

                    full_name = person.find_next("span", {"class": "link results-name"}).get_text()
                    # do smthg to separate name and lastname
                    last_name = "None right now"
                    email = person.find_next("td", {"class": "record-data-email"}).get_text()
                    major = person.find_next("td", {"class": "record-data-major"}).get_text()
                    student_list.append(CollegePersonInfo(full_name, last_name, major, email, affiliation))  # Thinking of having a parent class and adding one child for students and another for other people. Having other people could be useful down the road

                else:
                    full_name = person.find("span", {"class": "link results-name"})
                    # do smthg to separate name and lastname
                    last_name = "None right now"
                    email = person.find("td", {"class": "record-data-email"})
                    major = person.find("td", {"class": "record-data-major"})
                    others_list.append(CollegePersonInfo(full_name, last_name, "N/A", email, affiliation))

        time.sleep(15)      # Sleep time to prevent being treated as a bot.

    return student_list


# Test characters
start_char = 'q'        # Unique character chosen at random for debugging purposes
finish_char = 'q'

students = []
students = get_info("https://www.osu.edu/findpeople/", start_char, finish_char)

print  len(students)         # Debugging
for person in students:     # Debugging
    print person.name
    print person.last_name
    print person.email
    print person.major
    print person.affiliation

if students == None:
    print ("Page could not be opened")