import datetime
import sys
import json
from pathlib2 import Path


def usage():
    print "Usage: "
    print sys.argv[0]+" <inputfile.data> <outputfile.json>"



if len(sys.argv) < 2:
    usage()

filename = sys.argv[1]
output = sys.argv[2]
backlog = Path(output)
sch_req_list = []




def parse_txt2dict(line, dict_object):
    """ Converts a line of string into a dictionary key-value pair 
    and updates the dict_object[key] = value.
    """
    clean_line = line.translate(None, "{}',\n")
    split_line = clean_line.split(":")
    split_line[0] = split_line[0].strip(" ")
    dict_object[split_line[0]] = split_line[1]
    
    

def read_from_file(filename):

    put_in_dictionary = False
    new_dict = {}

    with open(filename, 'r') as input_file:
        #import pdb; pdb.set_trace()
        for line in input_file.readlines():
            if '}' in line:
                put_in_dictionary = False
                parse_txt2dict(line, new_dict)
                sch_req_list.append(new_dict)
                new_dict = {}
            elif '{' in line:
                put_in_dictionary = True
                parse_txt2dict(line, new_dict)
            elif put_in_dictionary:
                parse_txt2dict(line, new_dict)
        print new_dict

                



read_from_file(filename)
with open(output, mode='w') as f:
    json.dump(sch_req_list, f)


    
