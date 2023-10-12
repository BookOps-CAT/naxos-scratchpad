#xml_cid 
import os
import sys
import csv


from lxml import etree

def list_files(dir: str):
    file_list = []

    cwd = os.getcwd()
    for fh in os.listdir(dir):
        #yield os.path.join(cwd, fh)
        file_list.append(os.path.join(cwd,dir,fh))
    
    return file_list

def xml_001(fil):
    tree = etree.parse(fil)
    root = tree.getroot()
    print(root.tag)
    for record in root:
        print(record.tag)
        for child in record:
        
            #if child.tag == "{http://www.loc.gov/MARC21/slim}controlfield":
            
            #Oh boy!
            #So the "tag", as far as the parser is concerned, 
            #is "{http://www.loc.gov/MARC21/slim}controlfield", etc.

                #if child.attrib["tag"] == "001":

                #but the attribute "tag" is the MARC field.
                #Two options:
                #1) There is a marcxml parser available at https://github.com/edeposit/marcxml_parser
                ####it appears to have very little activity, I have no idea if it's good
                #2) I'll start building some functions here to handle this
            
            if child.tag == tagger(child,"controlfield"):
                print(child.tag,child.attrib)
                print("control num:",fielder(child,"001"))
            
#a function that will define the modifier .tag appropriately
def tagger(child,fieldtype):
    tagged = "".join(["{http://www.loc.gov/MARC21/slim}",fieldtype])
    return tagged

#a function that will define a field appropriately
def fielder(child,field):
    fields = []
    if child.attrib["tag"] == field:
        fields.append(child)
    return fields
    #this will now return a list of the elements that have this field.
    #need to work on returning the DATA next 

if __name__ == "__main__":
    file_list = list_files(sys.argv[1])
    for fil in file_list:
        print(fil)
        xml_001(fil)
        break