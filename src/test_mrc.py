from pymarc import MARCReader
from datetime import datetime
import csv

folder = csv.reader(open("C:/Users/BookOps/Documents/GitHub/naxos/dirlist.csv"), delimiter=",")
for row in folder:
    folder_list = row
    
opened_file = open('20230914.mrc', 'rb')
reader = MARCReader(opened_file)
none_counter = 0
good_counter = 0
rec_count = 0
slash_count = 0
slash_list = []

print(reader)

for record in reader:
    rec_count += 1
    if record is None:
        none_counter += 1
        print("NONE",record)
    if record is not None:
        good_counter += 1
        control = ".".join([(str(record["001"]).split("  ")[1]),"xml"])
        if "\\" in control:
            slash_count += 1
            control = control.replace("\\"," ")
            slash_list.append(control)
        if control not in folder_list:
            print(f"KEEP {control}")
        if control in folder_list:
            print(f"REMOVE {control}")
            folder_list.remove(control)

#Currently 478 records unaccounted for. 
#this pulls the control nummbers (file names)
#so I can then maybe create a new list
#from the original dirlist.csv? where for each control here
#I remove it from the csv...which should leave
#478 file names to check. Maybe.
#or 478 files to create another mrc file that I can copy and paste.

#after further nonsense, found a record (one) with a space at the end of its control number.
#fixed that one but going to have to see if there are other such typos that are causing this issue.
#I'm going to have to see if there's something like that in other files.
#!!!DATA CLEANING!!!
#remove spaces from the beginning and end of control numbers?

today = datetime.now()
y = today.year
m = today.month
d = today.day
h = today.hour

schrift = f"{y}{m}{d}{h}"

with open(f'{schrift}.txt','a') as out:
    #for rec in folder_list:
    #    print(rec+",")
    #    out.write(rec+",")
    out.write(f"""total: {rec_count}
none: {none_counter}
good: {good_counter}

folder: {len(folder_list)}

""")
    for i in folder_list:
        out.write(f"""
{i}

""")
    out.write(f"""slash: {slash_count}

""")
    for i in slash_list:
        out.write(f"""
{i}                  

""")