'''
========================================================================================================================
Name: Mahathir Maxim

Documentation:
It was created as a pycharm project using python 3
========================================================================================================================
'''

import sys
import pathlib
import re
import pickle

class Person:
    '''
    This class holds the information for each individual employee
    contains first, last and middle name; id number and phone number in good format
    '''

    def __init__(self, first, mi, last, id, phone):
        '''
        constructor function for Person
        :param first:
        :param mi:
        :param last:
        :param id:
        :param phone:
        '''

        self.last=last
        self.first=first
        self.mi=mi
        self.id=id
        self.phone=phone

    def display(self):
        '''
        displays the fields for a Person object
        '''

        print('Employee id: ', self.id)
        print('        ', self.first, self.mi, self.last)
        print('        ', self.phone)
        print('\n')




def readfile(filepath):
    '''
    opens the input file and reads from it
    Args:
        filepath: the relative path of the file
    Returns:
        the read text splitted into line separated list
    '''

    with open(pathlib.Path.cwd().joinpath(filepath), 'r') as f:
        text_in = f.read().splitlines()
    return text_in




def getdict(txtlines):
    '''
    creates the dictionary by processing each line of the input text

    Args:
        txtlines: list of line separated texts each representing one employees information

    Returns:
        A dict where key is the id of the employee and value is a person object for the employee
    '''

    people = {}
    for line in txtlines:

        infolist = line.split(",")

        first = infolist[0].strip().capitalize() #gets the first name
        last = infolist[1].strip().capitalize() #gets the last name

        #this block gets the middle initial and make sures its in correct form
        if (infolist[2].strip() == ''):
            mi = 'X'
        elif (len(infolist[2]) > 1):
            mi = infolist[2].strip()
            mi = mi[0].capitalize()
        else:
            mi = infolist[2].capitalize()

        #this block gets the id and makes sure its in the correct form by checking against regex
        id = infolist[3].strip()
        idtruth = re.match('[a-zA-Z]{2}\d{4}', id)
        if idtruth:
            id = id.upper()
        else:
            while not re.match('[a-zA-Z]{2}\d{4}', id):
                emsg=id+' is invalid! ID is two letters followed by 4 digits\n'
                id = input(emsg)
            id = id.upper()

        # this block gets the phone number and makes sure its in the correct form by checking against regex
        phone = infolist[4].strip()
        phonetruth = re.match('\d{3}-\d{3}-\d{4}', phone)
        if not phonetruth:
            while not re.match('\d{3}-\d{3}-\d{4}', phone):
                errormsg = 'Phone ' + phone + ' is invalid. Enter in XXX-XXX-XXXX format\n'
                phone = input(errormsg)

        # this block creates the person objects from the formatted infos and inserts into the dict
        person = Person(first, mi, last, id, phone)
        while id in people:
            errormessage='Id'+id+ ' already exists. Enter a valid id with two letters followed by 4 digits\n'
            id = input(errormessage)
            id = id.upper()

        people[id] = person

    return people #returns the created dict




def main():
    '''
    Functions as the driver function for producing intended output of standardized well formetted text

    Args:
        no parameter

    Returns:
        does not return any object but prints the formatted text

    Example:
        >> Last,First,Middle Initial,ID,Office phone
            Smith,Smitty,S,WH1234,5557771212
        >> Employee id:  WH1234
                    Smith S Smitty
                    555-777-1212
    '''
    sys.argv.append('data/data.csv') #relative path

    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
    else:
        fp = sys.argv[1]
        txtlines = readfile(fp) #call readfile with relative path to get the text

        txtlines.remove(txtlines[0]) #remove first line since that is just heading line
        people=getdict(txtlines) #call getdict to get the dict of Persons
        pickle.dump(people, open('people.p', 'wb')) #create pickle file
        people_in=pickle.load(open('people.p', 'rb')) # read from pickle file

        print('Employee list: \n\n')
        for x in people_in:         #make sure pickle file works and print out the formatted employee info
            people_in[x].display()




if __name__ == '__main__':
    main()

