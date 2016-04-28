import csv
import re


def get_col_contents(file_path, col_name):

    with open(file_path) as f:
        reader = csv.reader(f,dialect='excel')
        for row in reader:
            col_num = col_id(row, col_name)
            break
        if col_num >= 0:
            column = [row[1] for row in reader]
        elif col_num == -1:
            raise IndexError
        else:
            pass

    return sorted(set(column))

def col_id(row, match_id):
    for col_num in range(len(row)):
        if re.search('{0}'.format(match_id), row[col_num]):
            return col_num
    return -1

def write_coll_to_csv(coll_contents, dest_file):

    with open (dest_file, 'wb') as f:
        inst_list = csv.writer(f)
        for row in coll_contents:
            print row
            inst_list.writerow([row])



# coll_contents = get_col_contents('/Users/Twilit_Zero/Snaptest/untitled/'
#                                  'Accreditation_2015_12/Accreditation_2015_12.csv', 'Institution_Name')
#
# write_coll_to_csv(coll_contents, '/Users/Twilit_Zero/Snaptest/untitled/institutions.csv')