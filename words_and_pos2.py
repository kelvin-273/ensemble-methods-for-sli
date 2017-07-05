import glob
from input_functions import *
from NgramTree import NgramTree, treePrint, get_titles
import nltk
import re

regex1 = re.compile(r"[^a-z _'A-Z.,]")
regex2 = re.compile(r'\[.*?\]')
w = NgramTree("Words")
p = NgramTree("POS")
for file_name in glob.glob(r'*/*.cha'):
    line_clusters = line_cluster(split_meta_data(file_to_list(file_name))[1])
    for i in line_clusters:
        if i['ID'] == '*CHI':
            string = re.sub("_", " ", regex1.sub("", regex2.sub("", i["sentence"])))
            tokens = nltk.pos_tag(nltk.word_tokenize(string))
            for i in nltk.ngrams(tokens, 4):
                tempW = nword(i)
                tempP = npos(i)
                w.ins(tempW)
                p.ins(tempP)
            w.ins(tempW[1:])
            w.ins(tempW[2:])
            w.ins(tempW[3:])
            p.ins(tempP[1:])
            p.ins(tempP[2:])
            p.ins(tempP[3:])

word_titles = get_titles(w)
pos_titles = get_titles(p)
# treePrint(p, 0)
# treePrint(w, 0)
