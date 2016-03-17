import csv


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
    def __str__(self):
        return ', '.join(self.join_info())

    # Returns an iterator with all the attributes of PersonInfo
    def join_info(self):

        info = [self.person_last_name, self.person_name, self.person_middle_name,
                self.person_email, self.person_affiliation, self.person_organization]
        return info

    def write_to_csv(self, writer_obj, file_name):
        writer_obj.writerow(file_name)


# Expands PersonInfo class in case person is a student
class StudentPersonInfo(PersonInfo):

    # Constructor
    def __init__(self, name, middle_name, last_name, email, affiliation, organization, major):
        super(StudentPersonInfo, self).__init__(name, middle_name, last_name, email, affiliation, organization)
        self.person_major = major

    # Overrides parent class' (PersonInfo) __str__() method
    def __str__(self):
        return ', '.join(self.join_info())

    # Overrides parent class' (PersonInfo) join_info() method
    def join_info(self):
        info = (super(StudentPersonInfo, self).join_info())
        info.append(self.person_major)
        return info

    def write_to_csv(self, writer_obj, file_name):
        writer_obj.writerow(file_name)
