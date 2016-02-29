from mechanize import Browser
import re
import csv
from string import capwords
import os


# Generates an ordered list containing combinations of two English alphabetic characters.
# The first character of each string is limited by "first" and "last" arguments, and it is uppercase.
# The second character will range from a to z (lowercase)
# Setting optional arguments "add_chars" to True and assigning a string to "extra_chars" will add that string
# at end of each element of the list
# If "start"'s and "finish"'s order is inverted, they are put in order
def char_list_generator(start, finish, add_chars = None, extra_chars = None):

    try:
        start, finish = char_fix(start, finish, True)
    # Consider removing exceptions. Error has to be carried to the top
    except TypeError as e:                 # Needs to raise a flag instead
        print e
        raise
    except ValueError as e:                # Needs to raise a flag instead
        print e
        raise
    except UnboundLocalError as e:
        print e                             # Needs to raise a flag instead
        raise
    else:
        ascii_code_list = range(ord(start), ord(finish) + 1)

        alpha_list_lower = alpha_generator()        # Iterable's purpose is to prevent multiple function calls.
        char_list = []

        # Generates query strings without extra strings at the end, e.g. [Aa, Ab, Ac, ...]
        if (add_chars == None or add_chars == False):
            if extra_chars == None:
                for code in range(ord(start), ord(finish) + 1):
                    sub_list = [chr(code) + character for character in alpha_list_lower]
                    char_list.extend(sub_list)
            else:
                # Cannot get this to work properly. Also, I read the stack is lost in this way.
                raise TypeError('no extra_chars argument expected unless add_chars argument set to True')   # Stack lost, consider revising

        # Generates query strings with extra strings at the end, e.g. when extra_string = '*': [Aa*, Ab*, Ac*, ...]
        elif add_chars == True:
            if extra_chars == None:
                raise TypeError ('extra_chars argument expected')       # Stack lost, consider revising
            else:
                for code in range(ord(start), ord(finish) + 1):
                    sub_list = [chr(code) + character + extra_chars for character in alpha_list_lower]
                    char_list.extend(sub_list)
        else:
            # Cannot get this to work properly. Also, I read the stack is lost in this way.
            raise TypeError('Boolean type argument expected for add_chars argument')    # Stack lost, consider revising

        return char_list

    return "Not a character"        # Any idea on what to return here?


# Generates a simple iterable containing the alphabet in either uppercase or lowercase
#
def alpha_generator(uppercase = None):

    # Generates iterable containing iterable in lowercase
    if uppercase == None or uppercase == False:
        alpha_char_list = [chr(ascii_code) for ascii_code in range(97, 123)]

    # Generates iterable containing iterable in lowercase
    elif uppercase == True:
        alpha_char_list = [chr(ascii_code) for ascii_code in range(65, 91)]
    else:
        raise TypeError('Boolean type argument expected for uppercase argument')    #Stack lost, consider revising

    return alpha_char_list

# Determines whether the characters "first" and "last" are in valid alphabetic range
# Returns uppercase version "first" and "last" in alphabetic order
def char_fix(first, last, uppercase = None):

    if uppercase == None or uppercase == False:
        if len(first) == 1 and first.isalpha():
            first = first.lower()
            if len(last) == 1 and last.isalpha():
                last = last.lower()
            else:
                raise # Check what to raise
        else:
            raise #Check what to raise

    elif uppercase == True:
        if len(first) == 1 and first.isalpha():
            first = first.upper()
            if len(last) == 1 and last.isalpha():
                last = last.upper()
            else:
                raise # Check what to raise
        else:
            raise #Check what to raise

    else:
        raise TypeError('Boolean type uppercase argument expected')

    # Places initial and final characters in order if required
    if ord(first) > ord(last):
        first, last = last, first


    return (first, last)

# Divides and individual's name and cleans it from whitespaces and undesired strings
def name_splitter(raw_name):
    full_name = re.split(',+', raw_name, 1)
    full_name[0] = capwords(full_name[0].lstrip())                # Last name
    full_name[1] = full_name[1].lstrip()                # First name and middle name
    name_and_middle = re.split(' +', full_name[1],1)    # Splits first name and middle name
    full_name[1] = capwords(name_and_middle[0])                   # First name
    middle_name = (name_and_middle[1].replace('(Click to show details)', '')).rstrip()  # Middle name. Removes undesired string.
    full_name.append(capwords(middle_name))                  # Extra step only for readability
    return full_name


def export_to_csv(file_name, people_list):

        # Places heading in file. I know I will have to change this to apply only when file is new.
        # I also have to consider selecting whether Major is printed on file or not.
        if people_list[0].person_affiliation.startswith(("Student", "student")):
            row_heading = ['Last Name', 'Name', 'Middle Name', 'e-mail', 'Affiliation', 'Organization', 'Major']
        else:
            row_heading = ['Last Name', 'Name', 'Middle Name', 'e-mail', 'Affiliation', 'Organization']

        info_for_csv = [person.join_info() for person in people_list]    # Prepares data for csv writer

        # If the file exists and is not empty, just add data
        if os.path.isfile(file_name) and os.stat(file_name).st_size > 0:

            with open(file_name, "ab") as csv_output_file:
                writer = csv.writer(csv_output_file)
                writer.writerows(info_for_csv)      # Writes data on file
                csv_output_file.close()

        # Else, first write a heading and then the data
        else:

            with open(file_name, "ab") as csv_output_file:
                writer = csv.writer(csv_output_file)
                writer.writerow(row_heading)        # Writes heading
                writer.writerows(info_for_csv)      # Writes data on file
                csv_output_file.close()


# Handles the creation of a browser object.
# url is the target URL. url must be a string
# If 'robots' set to false, robots.txt IS ignored. If left blank or set to any other value, robots.txt IS NOT ignored.
# Consider adding other useful instructions in the future
def instantiate_browser(url, robots = None):
    br_obj = Browser()
    br_obj.set_handle_equiv(True)
    # browser_obj.set_handle_gzip(True)     # Throws a warning, I have to check more in depth what this does
    br_obj.set_handle_redirect(True)
    br_obj.set_handle_referer(True)
    if robots == False:                     # Ignores robots only if requested in instantiate_browser() call
        br_obj.set_handle_robots(False)
    br_obj.open(url)

    return br_obj

# Not used anymore
class CharacterDomainError (Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
