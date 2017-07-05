"""a module to clean the data"""

import glob
import re
from input_functions import *
import os

regex1 = re.compile(r"[^a-z _'A-Z]")
regex2 = re.compile(r"\[.*?\]")

if not os.path.exists("Cleaned"):
    os.mkdir("Cleaned/SLI-narr")
    os.mkdir("Cleaned/SLI-spon")
    os.mkdir("Cleaned/typ-narr")
    os.mkdir("Cleaned/typ-spon")

for file_name in glob.glob(r'*/*.cha'):
    # import trancript as list of dictionaries
    line_clusters = line_cluster(split_meta_data(file_to_list(file_name))[1])
    # initialise new file
    new_file = open("Cleaned/" + file_name, "w")

    # clean each relevant line and write it to the new file
    for i in line_clusters:
        if i['ID'] == '*CHI':
            string = re.sub("_", " ", regex1.sub("", regex2.sub("", i["sentence"])))
            string = re.sub(r"[ ][ ]+", " ", string)
            string = re.sub(r"^[ ]", "", string)
            string = re.sub(r"[ ]$", "", string)
            new_file.write(string + "\n")
