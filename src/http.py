###Finding records in Sierra that do not have working links###

import csv
import requests
from pymarc import Field,Subfield,MARCReader

class Rowish:
    def __init__(self,control,url,bib_code,suppressed,live):
        self.control = control,
        self.url = url
        self.bib_code = bib_code,
        self.suppressed = suppressed,
        self.live = live

def csv_classer(file):
    classed = []
    for row in file:
        new_row = Rowish(row[0],row[1],row[2],False,True)
        classed.append(new_row)
    return classed

def mrc_classer(file):
    classed = []
    for record in file:
        control = record.get_fields["001"]
        url = record.get_fields["856"]["u"]
        #bib_code = 
        new_row = Rowish(control,url,bib_code,False,True)
        classed.append(new_row)
    return classed

def quick_and_the_dead(classed):
    for row in classed:
        if row.bib_code == "n":
            row.suppressed = True

        #gets response code from http call (404 if not working)
        response = requests.get(row.url)

        #if the link is not responsive, add the control number to a list.
        if response == '404':
            row.live = False
        if response == "202":
            row.live = True

    return classed

def executor(treated):
    to_suppress = []
    to_unsuppress = []
    for row in treated:
        if not row.suppressed and not row.live:
            to_suppress.append(row.control)
        if row.suppressed and row.live:
            to_unsuppress.append(row.control)
    return to_suppress,to_unsuppress

def printer(list,file):
    to_print = open(file,"a")
    to_print.writelines(list)
    to_print.close


if __name__ == "__main__":
    file_name = input("File name: ")
    file_extension = file_name.split(".")[1]

    if file_extension == "csv":
        file = csv.reader(open(file_name, newline=''))
        classed = csv_classer(file)
    if file_extension == "mrc":
        #file = MARCReader###!!!###
        classed = mrc_classer(file)

    treated = quick_and_the_dead(classed)
    to_suppress,to_unsuppress = executor(treated)
    print(to_unsuppress,to_suppress)
    
