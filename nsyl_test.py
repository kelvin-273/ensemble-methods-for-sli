"""testing the syllables function"""

import glob
from input_functions import *
from SOFL import SOFL
import nltk
import re

sofl = SOFL()
regex1 = re.compile(r'[^a-z A-Z]')
regex2 = re.compile(r'\[.*?\]')
for file_name in glob.glob(r'*/*.cha'):
    line_clusters = line_cluster(split_meta_data(file_to_list(file_name))[1])
    for i in line_clusters:
        if i['ID'] == '*CHI':
            string = re.sub("_", " ", regex1.sub("", regex2.sub("", i["sentence"])))
            tokens = nltk.word_tokenize(string)
            for j in tokens:
                try:
                    sofl.ins((syllables(j),j))
                except Exception as e:
                    print(j,e)

for i in sofl.rank:
    print(i)
