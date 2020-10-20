"""
this module generates the numerical tabular data from the transcripts and
serialises it with pickle
"""

import glob
import pandas as pd
import pickle
from random import shuffle
from file_to_vector import file_to_vector

if __name__ == '__main__':
    files = glob.glob(r"*/*.cha")
    shuffle(files)
    d = pd.DataFrame([file_to_vector(i) for i in files])
    pickle.dump(d, open("pure_data.data","wb"))
