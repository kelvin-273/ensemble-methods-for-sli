"""File to vector function"""
from input_functions import *
from nlp_functions import *
# from random import random

def file_to_vector(file_name):
    """takes file_name and creates vector out of it"""
    output_vector = {}
    line_clusters = line_cluster(split_meta_data(file_to_list(file_name))[1])

    # vect_append(output_vector, random(), "JK")
    vect_append(output_vector, tnw(line_clusters), "TNW")
    vect_append(output_vector, num_errors(line_clusters), "ERR")
    vect_append(output_vector, assissted(line_clusters), "ASSI")
    vect_append(output_vector, err_rep_ret_fil(line_clusters), "ERRF")
    vect_append(output_vector, sentence_complexity(line_clusters), "SCPX")
    vect_append(output_vector, error_patterns(line_clusters), "EP")


    vect_append(output_vector, ngram_all(line_clusters),
        ("1", "2", "3", "4", "1", "2", "3", "4"))
    # # NDW doesn't work without ngrams
    vect_append(output_vector, ndp_ndw(output_vector), ("NDP", "NDW"))

    if file_name[4:8] == "narr":
        vect_append(output_vector, 1, "narr")
    elif file_name[4:8] == 'spon':
        vect_append(output_vector, 0, "narr")

    if file_name[:3] == 'SLI':
        vect_append(output_vector, 1, "SLI+")
    elif file_name[:3] == 'typ':
        vect_append(output_vector, 0, "SLI+")
    return output_vector

if __name__ == "__main__":
    vector = file_to_vector("SLI-narr/fssli009.cha")
    for i in vector:
        print(i + ":\t" + str(vector[i]))
