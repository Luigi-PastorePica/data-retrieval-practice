# Note: Get info does not return anything for the time being. This will change.


from bs4 import BeautifulSoup
from mechanize import urlopen       # mechanize implements urllib2 and expands it
from mechanize import Browser
from mechanize import HTTPError
from mechanize import URLError
import time
import random
import re       # Please provide feedback on this library.
                # Used to find classes in the html code that start with a specific string
import csv      # Not implemented yet


# Generates an ordered alphabetic list that spans from "start" to "finish" (inclusive)
# Asterisk added after each character (website's form's specific requirement)
# If "start"'s and "finish"'s order is inverted, the function puts them in order
def char_list_generator(start, finish):

    try:
        start, finish = char_fix(start, finish)
    except TypeError as e:
        print e
    ascii_code_list = range(ord(start), ord(finish) + 1)
    char_list = []
    for code in ascii_code_list:
        char_list.append(chr(code) + '*')

    return char_list

# Determines whether the characters "first" and "last" are in valid alphabetic range
# Returns uppercase version "first" and "last" in alphabetic order
def char_fix(first, last):

    if len(first) == 1 and first.isalpha():
        first = first.upper()
        if len(last) == 1 and last.isalpha():
            last = last.upper()

            # Places initial and final characters in order if required
            if ord(first) > ord(last):
                first, last = last, first

        else:
            print "Error: '" + last + "' is not an alpha character"   ##### Will update later, when I have a better understanding of error handling
            return None                                             ##### Address this. Multiple return statements.
    else:
        print "Error: '" + first + "' is not an alpha character"  ##### Will update later, when I have a better understanding of error handling
        return None                                             ##### Address this

    return (first, last)

    '''Determines range of valid ASCII characters
    initial_limit_lower = ord('a')
    final_limit_lower = ord('z')
    initial_limit_upper = ord('A')
    final_limit_upper = ord('Z')
    Exceptions in case a non alphabetic character is used by mistake
    Not sure whether I am implementing this properly
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
        return None'''


class CharacterDomainError (Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

# Objects of this class store information of individuals registered in the institution
# Organization might be dropped eventually. Keeping it depends on it being useful for our purposes.
class PersonInfo(object):

    def __init__(self, name, last_name, email, affiliation, organization):

        self.person_name = name
        self.person_last_name = last_name
        self.person_email = email
        self.person_affiliation = affiliation
        self.person_organization = organization

class StudentPersonInfo(PersonInfo):

    def __init__(self, name, last_name, email, affiliation, organization, major):
        super(StudentPersonInfo, self).__init__(name, last_name, email, affiliation, organization)
        self.person_major = major


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

    for element in query_chars:
        br.form = list(br.forms())[0]       # Used to select form w/o name attribute
        br['lastname'] = element             # Places query string into last name field
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

            # These exceptions are a temporary fix applied to handle an AttributeError always present in the last iteration
            try:
                name = person.find_next("span", {"class": "link results-name"}).get_text()
            except AttributeError as e:
                print (e)
            # do smthg to separate name and lastname
            try:
                last_name = "None right now"
            except AttributeError as e:
                print (e)
            try:
                email = person.find_next("td", {"class": "record-data-email"}).get_text()
            except AttributeError as e:
                print (e)
            try:
                affiliation = person.find_next("div", {"class": "results-affiliation"}).get_text()
            except AttributeError as e:
                print (e)
            try:
                organization = person.find_next("td", {"class": "record-data-org"}).get_text()
            except AttributeError as e:
                print (e)

            finally:

                if affiliation == "Student":
                    try:
                        major = person.find_next("td", {"class": "record-data-major"}).get_text()
                    except AttributeError as e:
                        print (e)
                    student_list.append(StudentPersonInfo(name, last_name, email, affiliation, organization, major))

                else:
                    others_list.append(PersonInfo(name, last_name, email, affiliation, organization))

        # Pseudo-random sleep time generator (to prevent being treated as a bot)
        # Obtaining information from website takes some time. This might not be needed,
        random.seed()
        time.sleep(random.randint(3,10))

    return student_list


# Test characters
start_char = 'q'        # Unique character chosen at random for debugging purposes
finish_char = 'q'

students = []
students = get_info("https://www.osu.edu/findpeople/", start_char, finish_char)

print  len(students)         # Debugging
for person in students:     # Debugging
    print person.person_name
    print person.person_last_name
    print person.person_email
    print person.person_major
    print person.person_affiliation

if students == None:
    print ("Page could not be opened")