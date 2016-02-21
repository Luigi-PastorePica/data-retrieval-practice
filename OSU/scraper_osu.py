
from bs4 import BeautifulSoup
from mechanize import urlopen       # mechanize implements urllib2 and expands it
from mechanize import Browser
from mechanize import HTTPError
from mechanize import URLError
import time
import random
import re
from osu_mod import *
import csv      # Not implemented yet



# Instances of this class store information of individuals registered in the institution
# Organization might be dropped eventually. Keeping it depends on it being useful for our purposes.
class PersonInfo(object):

    # Constructor
    def __init__(self, name, middle_name, last_name, email, affiliation, organization):

        self.person_name = name
        self.person_middle_name = middle_name
        self.person_last_name = last_name
        self.person_email = email
        self.person_affiliation = affiliation
        self.person_organization = organization

    # Overrides default __str__() method
    # Consider printing result of join_info() instead
    def __str__(self):
        print str(self.person_name)
        print str(self.person_middle_name)
        print str(self.person_last_name)
        print str(self.person_email)
        print str(self.person_affiliation)
        print str(self.person_organization)

    # Joins information in a string separated by delimiter
    def join_info(self, delimiter):                        # is it fine to use a variable called delimiter? See csv doc.

        info = [self.person_last_name, self.person_name, self.person_middle_name,
                self.person_email, self.person_affiliation, self.person_organization]
        return delimiter.join(info)


# Expands PersonInfo class in case person is a student
class StudentPersonInfo(PersonInfo):

    # Constructor
    def __init__(self, name, middle_name, last_name, email, affiliation, organization, major):
        super(StudentPersonInfo, self).__init__(name, middle_name, last_name, email, affiliation, organization)
        self.person_major = major

    # Overrides parent class' (PersonInfo) __str__() method
    # Consider printing result of join_info() instead
    def __str__(self):
        super(StudentPersonInfo, self).__str__()
        print str(self.person_major)

    # Overrides parent class' (PersonInfo) join_info() method
    def join_info(self, delimiter):
        info = [super(StudentPersonInfo, self).join_info(delimiter), self.person_major]
        return delimiter.join(info)


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

    for element in query_chars:                 # The following three lines of code work only because start of html does not change
        br.form = list(br.forms())[0]           # Used to select form w/o name attribute
        br['lastname'] = element                # Places query string into last name field
        br.submit()

        # Exception handling for response
        try:
            soup = BeautifulSoup(br.response().read(), "html.parser")   # HTML file containing response page code
        except AttributeError as e:
            print(e)
            return None

        # Records html code inside the tr tags that contain classes that start with record-person (each represented by var person).
        # Inside each of these tr tags there are different td tags with the desired info.
        i = -1       # Using counter to skip duplicates (each individual has two tr tags assigned that begin with 'record-person')
        for person in soup.find_all('tr', class_=re.compile('^record-person')):

            i += 1
            if i % 2 == 1:
                continue

            # These exceptions are a temporary fix applied to handle an AttributeError always present in the last iteration
            try:
                raw_name = person.find_next("span", {"class": "link results-name"}).get_text()

                # Does the same as function name_splitter.
                # Left it here because it is more readable, and I think more efficient also.
                '''
                full_name = re.split(',+', person.find_next("span", {"class": "link results-name"}).get_text(), 1 ) # gets all name info and separates last name
                last_name = full_name[0].lstrip()                              # Cleans and assigns last name
                full_name[1] = full_name[1].lstrip()
                name_and_middle = re.split(' +', full_name[1],1)               # Splits first and middle names
                name, middle_name = name_and_middle[0], name_and_middle[1]
                middle_name = (middle_name.replace('(Click to show details)', '')).rstrip()  # Cleans middle name from undesired string
                '''
            except AttributeError as e:
                print e         # debug
                continue        # Name is required. If not found, skip to next person.
            else:
                person_name = name_splitter(raw_name)
                last_name = person_name[0]
                name = person_name[1]
                middle_name = person_name[2]

            try:
                email = person.find_next("td", {"class": "record-data-email"}).get_text()
            except AttributeError as e:
                print (e)       # debug
                continue        # e-mail is required. If not found, skip to next person.

            try:
                affiliation = person.find_next("div", {"class": "results-affiliation"}).get_text()
            except AttributeError as e:
                print (e)                       # debug
                affiliation = "Aff. N/A"        # If there is no affiliation, the person is placed in others_list

            try:
                organization = person.find_next("td", {"class": "record-data-org"}).get_text()
            except AttributeError as e:
                print (e)                   # debug
                organization = "Org. N/A"
            else:
                if not organization:            # Might have to change this condition.
                    organization = "Org. N/A"

            if affiliation == "Student" or affiliation == "Student, Student Employee":
            # if  re.compile('^Student') == affiliation:
                try:
                    major = person.find_next("td", {"class": "record-data-major"}).get_text()
                except AttributeError as e:
                    print (e)               # debug
                    pass
                else:
                    student_list.append(StudentPersonInfo(name, middle_name, last_name, email, affiliation, organization, major))

            else:
                others_list.append(PersonInfo(name, middle_name, last_name, email, affiliation, organization))

        # Pseudo-random sleep time generator (to prevent being treated as a bot)
        # Obtaining information from website takes some time. This might not be needed,
        random.seed()
        time.sleep(random.randint(3,10))

    return student_list     # Needs to return student_list and others_list. Consider using another list or a dict.


# Test characters
start_char = 'q'        # Unique character chosen at random for debugging purposes
finish_char = 'q'

students = []
students = get_info("https://www.osu.edu/findpeople/", start_char, finish_char)

print len(students)         # Debug
for person in students:     # Debug
    # person.__str__()
    print person.join_info(',')
    print '\n'

if students == None:
    print ("Page could not be opened")