from csv import writer
import clipboard
from os import path
from os import stat
from pdfminer import pdfparser
import Tkinter
from os import walk, system
import os
import psutil
import shutil
from subprocess import check_call

# Note to self: When revising code, be careful with vars that contain path and those that do not. new_name_with_path, name_with_path


# List containing name and order of columns
columns = ['alt_email', 'year', 'gender', 'school', 'degree', 'gpa',
           'satv', 'satm', 'satw', 'tsat', 'tact',
           'major1', 'major2', 'minor1', 'minor2',
           'grad_school', 'grad_degree', 'grad_major', 'grad_year', 'grad_gpa',
           'notes']

# Class that stores candidate data and serves other simple functions.
class Candidate(object):

    # Assigns =NA() to all keys at first.
    def __init__(self, keys):

        na = '=NA()'
        self.keys = keys
        self.data = {key:na for key in keys}
        self.values = []


    # The following methods hardcode the name of the fields. This should be fixed in the future. If not, there is no
    # sense in initializing with the keys above.
    def set_basic_data(self, alt_email, year, school, degree,major1, major2, minor1, minor2, gpa):
        if alt_email.lower() != 'n':
            self.data['alt_email']=alt_email
        if year.lower() != 'n':
            self.data['year']=year
        if school.lower() != 'n':
            self.data['school']=school
        if degree.lower() != 'n':
            self.data['degree']=degree
        if major1.lower() != 'n':
            self.data['major1']=major1
        if major2.lower() != 'n':
            self.data['major2']=major2
        if minor1.lower() != 'n':
            self.data['minor1']=minor1
        if minor2.lower() != 'n':
            self.data['minor2']=minor2
        if gpa.lower() != 'n':
            self.data['gpa']=gpa

    def set_gender(self, gender):
        if gender.lower() != 'n':
            self.data['gender']=gender

    def set_scores(self, satv, satm, satw, tsat, tact):
        if satv.lower() != 'n':
            self.data['satv']=satv
        if satm.lower() != 'n':
            self.data['satm']=satm
        if satw.lower() != 'n':
            self.data['satw']=satw
        if str(tsat).lower() != 'n':
            self.data['tsat']=str(tsat)
        if tact.lower() != 'n':
            self.data['tact']=tact

    def set_grad(self, grad_school, grad_degree, grad_major, grad_year, grad_gpa):
        if grad_school.lower() != 'n':
            self.data['grad_school'] = grad_school
        if grad_degree.lower() != 'n':
            self.data['grad_degree'] = grad_degree
        if grad_major.lower() != 'n':
            self.data['grad_major'] = grad_major
        if grad_year.lower() != 'n':
            self.data['grad_year'] = grad_year
        if grad_gpa.lower() != 'n':
            self.data['grad_gpa'] = grad_gpa

    def set_notes(self, notes):
        if notes.lower() != 'n':
            self.data['notes'] = notes
        else:
            self.data['notes'] = ''

    def join_data(self):
        self.values = [self.data[key] for key in self.keys] # Why is it wrong to set an instance attr outside of init?
        # self.output = ', '.join(self.values)

    # Writes data to a backup CSV file, in case data is not pasted in spreadsheet by mistake
    def write_to_csv(self):
        f = 'temp.csv'
        if path.isfile(f) and stat(f).st_size > 0:
            with open(f, 'ab') as out_file:
                writer_obj = writer(out_file)
                writer_obj.writerow(self.values)
                out_file.close()
        else:
            with open(f, 'ab') as out_file:
                writer_obj = writer(out_file)
                writer_obj.writerow(self.keys)
                writer_obj.writerow(self.values)
                out_file.close()

    # Exports data to clipboard
    def data_to_clipboard(self):
        clipboard.copy('\t'.join(self.values))  # Copies data to clipboard

# Obtains a list of names of files and directories contained in the desired folder.
# Input: directory path. Output: directory path, list of file names, list of directory names
def get_dir_contents(dir_path):

    file_list = []
    dir_list = []
    for (root_path, dir_name, file_names) in walk(dir_path):
        # files = [path.join(root_path, name) for name in file_name]
        file_list = file_names
        dir_list = [path.join(root_path, name) for name in dir_name]
        break
    return dir_path, file_list, dir_list

# Path to directory. Eventually should be kept in a separate file and retrieved by the program.
# /Users/Twilit_Zero/Downloads/Snap/Metrics_Acquisition/Resumes/

# dir_path, files, directories = get_dir_contents(raw_input("Input Path: "))
dir_path, files, directories = get_dir_contents('/Users/Twilit_Zero/Downloads/Snap/Metrics_Acquisition/Resumes/')
dir_path = dir_path.replace(' ', '\ ')

# Makes the program repeat itself until user wants to quit
while True:

    file_name = files[1].replace(' ', '\ ')     # Gets the first filename in the list

    # Opens file with Preview app. This should change depending on OS
    # Funtion to open with default exists. I think it would make the code more portable, but not convenient for me now.
    # check_call(["open", "-a", '/Volumes/Macintosh\ HD/Applications/Preview.app', dir_path + '/' + file])
    os.system("open -a /Volumes/Macintosh\ HD/Applications/Preview.app " + dir_path + file_name)


    # Candidate class Instantiation
    candidate = Candidate(columns)

    # If opened document is not a resume, move it to Not_Reviewed directory
    if raw_input("Is this a resume?\t\t\t\t\t\t\t\t").lower() == 'n':
        os.system('mv ' + (dir_path + file_name).replace(' ', '\ ') +
                  ' ' + dir_path + "__0A_Not_Reviewed")
        del files[1]
        continue
    print

    resume_email = raw_input("Resume e-mail\t\t\t\t\t")   # Eventually this will be replaced by a function that
                                                        # automatically retrieves the e-mail from the file when possible.
    print

    same_email = raw_input("Is the e-mail the same as in the spreadsheet?\t")
    print

    name_with_path, ext = os.path.splitext(dir_path + file_name)    # Splits name of file and extension

    # Renames file by adding to it the e-mail in the spreadsheet.
    # Adds alternate e-mail to exported information if required.
    if same_email.lower() == 'y':
        alt_email = 'n'
        new_name_with_path = name_with_path + ' ' + resume_email + ext
        os.rename(dir_path + file_name, new_name_with_path)  #  Remember, if I decide to return full path instead of name only, change this accordingly
    elif same_email.lower() == 'n':
        alt_email = resume_email
        original_email = raw_input("Original e-mail\t\t\t\t\t")
        new_name_with_path = name_with_path + ' ' + original_email + ext
        os.rename(dir_path + file_name, new_name_with_path)      #  Remember, if I decide to return full path instead of name only, change this accordingly
    else:
        pass # I will eventually add something to handle this issue. Maybe a simple loop

    # Asks for data input
    # alt_email = raw_input("Alternate e-mail\t\t\t\t")
    school = raw_input("Undergrad college\t\t\t\t")
    year = raw_input("Undergrad graduation year\t\t")
    gpa = raw_input("Undergraduate GPA\t\t\t\t")
    degree = raw_input("Undergraduate degree\t\t\t")
    print
    major1 = raw_input("Major 1\t\t\t\t\t\t\t")
    major2 = raw_input("Major 2\t\t\t\t\t\t\t")
    minor1 = raw_input("Minor 1\t\t\t\t\t\t\t")
    minor2 = raw_input("Minor 2\t\t\t\t\t\t\t")
    print

    # Stores acquired data in candidate object
    candidate.set_basic_data(alt_email, year, school, degree,major1, major2, minor1, minor2, gpa)

    # If the candidate provided standardized test scores, ask for input.
    scores = raw_input("Does the candidate have test scores?\t\t\t")
    print
    if scores.lower() == 'y':
        satv = raw_input("Reading SAT (SAT V) score\t\t")
        satm = raw_input("Math SAT (SAT M) score\t\t\t")
        satw = raw_input("Writing SAT (SAT W) score\t\t")

        if satv.lower() != 'n' and satm.lower() != 'n' and satw.lower() != 'n':
            tsat = int(satv) + int(satm) + int(satw)
        else:
            tsat = raw_input("Total SAT score\t\t\t\t\t")

        tact = raw_input("Composite ACT\t\t\t\t\t")
        print
        candidate.set_scores(satv,satm, satw, tsat, tact)

    # If the candidate has (or will obtain) a graduate degree, ask for data.
    grad = raw_input("Does the candidate have a graduate degree?\t\t")
    print
    if grad.lower() == 'y':
        grad_school = raw_input("Graduate college\t\t\t\t")
        grad_year = raw_input("Graduate year\t\t\t\t\t")
        grad_gpa = raw_input("Graduate GPA\t\t\t\t\t")
        grad_degree = raw_input("Graduate degree\t\t\t\t\t")
        grad_major = raw_input("Graduate major\t\t\t\t\t")
        print
        candidate.set_grad(grad_school, grad_degree, grad_major, grad_year, grad_gpa)

    # Ask for user gender. Accepts shortcut
    while True:
        gender = raw_input("Please input gender\t\t\t\t")
        if gender.lower() == 'm' or gender.lower() == 'male':
            candidate.set_gender('Male')
            break
        elif gender.lower() == 'f' or gender.lower() == 'female':
            candidate.set_gender('Female')
            break
        elif gender.lower() == 'n':
            candidate.set_gender('n')
            break
        else:
            print (" There was a mistake.")
    print

    # Ask for notes on resume (if any).
    # If there are notes, use that as cue to move file to appropriate folder.
    notes = raw_input("Insert your notes regarding the resume here\t\t")
    print

    if notes == 'n':
        os.system('mv ' + new_name_with_path.replace(' ', '\ ') +
                  ' ' + dir_path + "__0A_Reviewed")    # This should not be hard coded. Planning to use same dictionary converting function I will create for column values
        print "File moved to Reviewed folder"
    elif notes != 'n':
        incomplete = raw_input("Send to Incomplete folder?\t")
        if incomplete == 'y':
            # shutil.move(new_name_with_path, dir_path + "__0A_Incomplete")
            os.system('mv ' + new_name_with_path.replace(' ', '\ ') +
                      ' ' + dir_path + "__0A_Incomplete")
        elif incomplete == 'n':
            # shutil.move(new_name_with_path, dir_path + "__0A_Not_Reviewed")
            os.system('mv ' + new_name_with_path.replace(' ', '\ ') +
                      ' ' + dir_path + "__0A_Not_Reviewed")
        else:
            pass    # Solve this with a loop
    else:
        pass    # Solve this with simple loop

    candidate.set_notes(notes)

    # Here I was trying to kill the process for Preview. Did not work though
    # process_name = 'Preview.app'
    # for process in psutil.process_iter():
    #     if process == process_name:
    #         process.kill()

    print
    print "PLEASE REMEMBER TO PASTE THE INFORMATION INTO THE SPREADSHEET"
    print "______________________________________________________________________________"
    print

    candidate.join_data()
    candidate.write_to_csv()
    candidate.data_to_clipboard()

    keep_going = raw_input("Do you want to review another resume?\t\t\t")
    print

    if keep_going.lower() == 'n':
        # os.kill()
        break
#      os.kill()

    del files[1]    # Removes name of file just reviewed from list.

print ('Have a good night')     # Silly program-quit message
