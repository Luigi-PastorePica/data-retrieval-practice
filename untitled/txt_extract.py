# Notes to self
# Maybe finding gpa is not the best idea. It takes more time to answer to a list than typing answer
# The match string is doing funny things. It is matching some other colleges that are not even in the resume


from re import findall
import re
from pdfextract import get_pages
from docx2txt import process
from docx2txt import process_args


# Returns a list of e-mail addresses (in contrast to the one above)
def find_email(text):
    # emails = findall('\S+@[a-zA-Z0-9.]+', text)  # For some reason [:alnum:.] does not work and \S+ matches characters no displayed in the text file
    emails = findall('[a-zA-Z0-9._-]+@[a-zA-Z0-9.]+', text)
    return emails


# Finds all floating point numbers in text an returns a list of them
def get_float(text):
    float_ = findall('[0-9]+[.][0-9]+', text)
    return float_


# This one finds the pattern, but only once (due to greediness). Making non greedy yields undesired results
def get_gpa(text):
    # gpas = findall(r"G.*P.*A.*(0|1|2|3|4|5|6|7|8|9+[.]0|1|2|3|4|5|6|7|8|9+)", text)
    gpas = findall(r"(G.*P.*A.*([0-9]+[.][0-9]+))", text)
    return gpas


# Does not work properly yet
def get_phone(text):
    phones = findall('([0-9]{3}).{0,5}([0-9]{3}).{0,5}([0-9]{4})', text)
    return phones


# Checks whether first "word_limit" words from 'match" are present in "text".
# Regular expression "meta_string" is used between words belonging to "match"
# Returns "match" if there is a match. Returns None otherwise
def match_alnum(text, match, word_limit = None, regx_string=r'.*', ignore_words=None):

    match_re = re.sub('[^a-zA-Z0-9]', ' ', '{0}'.format(match))
    word_list_raw = match_re.split()
    word_list = [word.strip() for word in word_list_raw[:word_limit]]

    if ignore_words:
        ignore_str = ' '.join(ignore_words)
        word_list = [word for word in word_list if word not in ignore_str]

    match_re = regx_string.join(word_list)
    # match_re = match_re + '\\s'
    if re.search('{0}'.format(match_re), text):
        return match
    else:
        return False

# def get_year(text):

# This function has to be changed so it can identify and decode other formats
# def text_prep(file_text, f_extension):
#     text = " ".join(file_text)
#     text = text.replace('\n', '\t')
#     print text
#     text = str(text.decode('ascii', errors='ignore'))
#     # if f_extension.endswith('pdf'):
#     #     text = str(text.decode('ascii', errors='ignore'))
#     # elif f_extension.endswith('doc') or f_extension.endswith('docx'):
#     #     pass
#     # else:
#     #     raise IOError ("File type not supported\n"
#     #                    "File must have extension .pdf, .doc, or .docx")
#     return text

def get_text (file_path, f_extension):
    if f_extension.endswith('pdf'):
        text = get_pages(file_path)
        text = str(text.decode('ascii', errors='ignore'))
    elif f_extension.endswith('docx'):
        text = process(file_path)
    elif f_extension.endswith('doc'):
        raise IOError("File type (doc) not supported yet."
                      "Please come back later")
    else:
        raise IOError ("File type not supported\n"
                       "File must have extension .pdf, .doc, or .docx")
    return text


def text_prep(file_text):
    text = ''.join(file_text)
    return text.replace('\n', '\t')

def list_menu(lst):
    for n, element in enumerate(lst, start=1):
        print str(n) + '\t' + element
    print str(len(lst) + 1) + '\t' + 'None of the above'
    option = int(raw_input())
    if option <= len(lst):
        answer = lst[option-1]
    else:
        answer = None

    return answer

# Converts strings in lst (an iterable) into lowercase
def to_lowercase(lst):
    for pos in range(len(lst)):
        lst[pos] = lst[pos].lower()
    return lst




def _test_module(file_path):
    with open (file_path) as f:

        text = text_prep(f)
        print find_email(text)
        print get_float(text)
        print get_phone(text)
        coll_list = ['University of Chicago']
        print match_alnum(text, coll_list, 5)


# test_module('/Users/Twilit_Zero/Desktop/trash/temp.txt')