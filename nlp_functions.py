"""functions for NLP"""

import re
import nltk
import words_and_pos2
from input_functions import nword, npos, syllables
from NgramTree import NgramTree, get_dictionaries

def tnw(line_clusters):
    """returns the total number of words1"""
    total = 0
    for i in line_clusters:
        if i["ID"] == "*CHI":
            total += len(re.sub(r"[^\w ]", '', i["sentence"]).split())
    return total

def num_errors(line_clusters):
    """searches the list of line_clusters counts total number of lines,
    number of errors and percentage errors to total lines"""
    num_ID = 0
    num_err = 0
    for i in line_clusters:
        if i["ID"] == "*CHI":
            num_ID += 1
            try:
                if i[r"%err"]:
                    num_err += 1
            except KeyError:
                pass
    return (num_err, num_ID, num_err/num_ID)

def assissted(line_clusters):
    """percentage INV assisstances / all sentences"""
    num_assissts = 0
    for i in line_clusters:
        if i["ID"] == "*INV" and not "&www" in i["sentence"]:
            num_assissts += 1
    return num_assissts / len(line_clusters)

def rv_v(output_vector):
    """returns the ratio of raw verbs to verbs using the output_vector"""
    raw_verbs = output_vector["1POS VB"]
    all_verbs = output_vector["1POS VB"] + \
                output_vector["1POS VBD"] + \
                output_vector["1POS VBG"] + \
                output_vector["1POS VBN"] + \
                output_vector["1POS VBP"] + \
                output_vector["1POS VBZ"]
    return raw_verbs / all_verbs

def sentence_complexity(line_clusters):
    """returns the values determining sentence_complexity ie
        mean length of utterance in words,
        average number of syllables per word,
        average number of clauses per sentence,
        flesch-kincaid
    """
    # list to store number of clauses
    mlu_aspw_acps = ([],[],[])
    regex1 = re.compile(r"[^a-z _'A-Z]") # punctuation are not words
    regex2 = words_and_pos2.regex2
    for i in line_clusters:
        if i["ID"] == "*CHI":
            string = re.sub("_", " ", regex1.sub("", regex2.sub("", i["sentence"])))
            tokens = nltk.pos_tag(nltk.word_tokenize(string))

            mlu_aspw_acps[0].append(len(tokens))

            cpi = 1
            for j in tokens:
                mlu_aspw_acps[1].append(syllables(j[0]))
                if j[1] in ("IN", "CC", "UH"):
                    cpi += 1

            mlu_aspw_acps[2].append(cpi)

    mlu = sum(mlu_aspw_acps[0]) / len(mlu_aspw_acps[0])
    aspw = sum(mlu_aspw_acps[1]) / len(mlu_aspw_acps[1])
    acps = sum(mlu_aspw_acps[2]) / len(mlu_aspw_acps[2])
    fks = 11.8 * aspw + 0.39 * mlu - 15.59
    return mlu, aspw, acps, fks

def err_rep_ret_fil(line_clusters):
    """returns the number of errors, repititions, retraces, false_starts,
    fillers, replacements found in the text and a linear combination of them"""
    errors = 0
    repititions = 0
    retraces = 0
    false_starts = 0
    fillers = 0
    replacements = 0
    regex = re.compile(r"\[.*?\]|&")
    for i in line_clusters:
        if i["ID"] == "*CHI":
            # print(regex.findall(i['sentence']))
            for j in regex.findall(i["sentence"]):
                if str(j) == "[*]":
                    errors += 1
                elif str(j) == "[/]":
                    repititions += 1
                elif str(j) == "[//]":
                    retraces += 1
                elif str(j) == "[/-]":
                    false_starts += 1
                elif str(j) == "&":
                    fillers += 1
                elif str(j)[:3] == "[: ":
                    replacements += 1
                else:
                    pass
                    # print("we missed one: " + str(j))
    return (errors, repititions, retraces, false_starts, fillers, replacements,
            sum((errors,
                repititions,
                retraces,
                false_starts,
                fillers,
                replacements)))

def ndp_ndw(output_vector):
    """uses the output_vector to count the number of different unigrams
    for words and POS tags"""
    ndw = 0
    ndp = 0
    for i in output_vector:
        if "1Words" in i:
            ndw += 1
        elif "1POS" in i:
            ndp += 1
    return ndw, ndp

def error_patterns(line_clusters):
    """returns the number of bigram error_patterns found in the text"""
    from possible_error_tags import possible_error_tags
    out = 0
    patterns = (
        ("det", "noun_pl"),
        ("det_pl", "noun"),
        ("pro_per", "verb_s"),
        ("pro_per", "aux_s"),
        ("noun", "aux"),
        ("noun", "aux_s"),
        ("noun", "verb"),
        ("noun", "verb_s"),
    )
    for i in line_clusters:
        try:
            if i["ID"] == "*CHI":
                for j in nltk.ngrams(
                    re.split(r"[ ]+",
                    re.sub(r"^.*?#", "",
                    re.sub(r"\|\w*", "",
                    re.sub(r"pro\|you", "pro:sub|you",
                    re.sub(r"~", " ",
                    i["%mor"]))))), 2):
                    # print(j)
                    try:
                        # print(tuple(map(lambda x: possible_error_tags[x], j)))
                        if tuple(map(lambda x: possible_error_tags[x], j)) in patterns:
                            # print(j)
                            out += 1
                    except KeyError as e:
                        # print(e)
                        pass
        except KeyError as f:
            # print(f)
            pass
    return out

def ngram_all(line_clusters):
    w = NgramTree("Words")
    p = NgramTree("POS")
    pos_dict = [{j:0 for j in i} for i in words_and_pos2.pos_titles]
    words_dict = [{j:0 for j in i} for i in words_and_pos2.word_titles]
    regex1 = words_and_pos2.regex1
    regex2 = words_and_pos2.regex2

    for i in line_clusters:
        if i['ID'] == '*CHI':
            string = re.sub("_", " ", regex1.sub("", regex2.sub("", i["sentence"])))
            tokens = nltk.pos_tag(nltk.word_tokenize(string))
            # print(len(tokens))
            if len(tokens) > 4:
                n = 4
            else:
                n = len(tokens)

            for i in nltk.ngrams(tokens, n):
                tempW = nword(i)
                tempP = npos(i)
                w.ins(tempW)
                p.ins(tempP)
            for i in range(1, n):
                w.ins(tempW[i:])
                p.ins(tempP[i:])

    out1 = get_dictionaries(p)
    for i in range(len(words_and_pos2.pos_titles)):
        for j in words_and_pos2.pos_titles[i]:
            if j in out1[i]:
                pos_dict[i][j] = out1[i][j]
    out2 = get_dictionaries(w)
    for i in range(len(words_and_pos2.word_titles)):
        for j in words_and_pos2.word_titles[i]:
            if j in out2[i]:
                words_dict[i][j] = out2[i][j]

    return pos_dict + words_dict
    # we now have trees and two dictionaries
    # and then return LoL
