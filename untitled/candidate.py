class Candidate(object):

    # Assigns =NA() to all keys at first.
    def __init__(self, keys, na = '=NA()'):

        self.keys = keys
        self.data = {key:na for key in keys}
        self.values = []


    def set_key(self, key, value = 'n'):
        if value                        # Find newline on command line . What does it look like for the interpreter.
        self.data[key] = value

    # The following methods hardcode the name of the fields. This should be fixed in the future. If not, there is no
    # sense in initializing with the __init__  "keys" argument above.
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
        copy('\t'.join(self.values))  # Copies data to clipboard