import glob
import pandas as pd
import pickle
from random import shuffle
from file_to_vector import file_to_vector
files = glob.glob(r"*/*.cha")
shuffle(files)
d = pd.DataFrame([file_to_vector(i) for i in files])
# print(d["EP"].mean(), d["EP"].std())
# print(d["EP"].loc[d["narr"] == 1].mean(), d["EP"].loc[d["narr"] == 1].std())
# print(d["EP"].loc[d["narr"] == 0].mean(), d["EP"].loc[d["narr"] == 0].std())
# print(d.corr())
# print(d.loc[d["narr"] == 1].corr())
# print(d.loc[d["narr"] == 0].corr())
pickle.dump(d, open("pure_data.data","wb"))
