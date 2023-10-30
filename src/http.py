###Finding records in Sierra that do not have working links###

#10/11: formatted imports to match discussion
import csv
#10/11: had to pip install requests in this venv. Resolved
import requests
from pymarc import Field,Subfield,MARCReader

class Rowish:
    def __init__(self,control,url,bib_code,suppressed,live):
        self.control = control,
        #10/11: added a comma below. Oops
        self.url = url,
        self.bib_code = bib_code,
        self.suppressed = suppressed,
        self.live = live

###10/11: may be more helpful to use namedtuples
#ex: 
#Rowish_named = namedtuple("Rowish_named","control,url,bib_code,suppressed,live")
#for row in map(Rowish_named._make,csv.reader(open("foo.csv","rb"))):
#   print(row.control,row.url)

def csv_classer(file):
    classed = []
    for row in file:
        new_row = Rowish(row[0],row[1],row[2],False,True)
        classed.append(new_row)
    #Rowish_named = namedtuple("Rowish_named","control,url,bib_code,suppressed,live")
    #for row in map(Rowish_named._make,csv.reader(open("file","rb"))):
    #   classed.append(row)
    return classed

def mrc_classer(file):
    classed = []
    for record in file:
        control = record.get_fields["001"]
        #10/11: need to test^
        #probably should be:
        #record.get_fields("001")
        #which will return a list
        url = record.get_fields["856"]["u"]
        #10/11: currently not getting bib_code. Whoops.
        #plugging in -9 as fill for now
        bib_code = -9
        new_row = Rowish(control,url,bib_code,False,True)
        classed.append(new_row)
    return classed

#10/11: On 10/3, we discussed combining the two above into one larger function that handles all file types.
#could then handle any file with one function
#e.g. if foo is a .csv, .mrc, whatever:
#classer(foo)


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
    
    #10/11:can use sys.argv
    #can define sys.argv[foo] as bar
    #cmd line ex:
    #c:\Users\BookOps\Documents\GitHub\naxos-scratchpad>python src\http.py foo.mrc
    #
    #file_extension = sys.argv[1].split(".")[1]
    #^Q: would this be correct?
    ###: would I need some sort of try/except to ensure that the file extension was correct, file exists, etc?
    
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
    
