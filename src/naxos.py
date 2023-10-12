import csv
from pymarc import marcxml

def marcified(naxos):
    rec = (marcxml.parse_xml_to_array(naxos))
    #rec = rec[0]
    #return rec
    #as discussed
    return rec[0]

if __name__ == "__main__":
    directory = "C:/Users/BookOps/Documents/GitHub/naxos/NAXOS_xml"
    folder = csv.reader(open("C:/Users/BookOps/Documents/GitHub/naxos/dirlist.csv"), delimiter=",")
    for row in folder:
        folder_list = row
    file_list = []
    for fil in folder_list:
        naxos = '/'.join([directory,fil])
        file_list.append(naxos)
    rec_list = []
    for naxos in file_list:
        rec = marcified(naxos)
        rec_list.append(rec)
        print(naxos)
    with open('20230914.mrc','ab') as out:
        for rec in rec_list:
            print(rec)
            out.write(rec.as_marc21())