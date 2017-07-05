"""mor extract test"""

import glob
from input_functions import *
from SOFL import SOFL
import nltk
import re

sofl = SOFL()
for file_name in glob.glob(r'*/*.cha'):
    line_clusters = line_cluster(split_meta_data(file_to_list(file_name))[1])
    for i in line_clusters:
        if i["ID"] == "*CHI":
            try:
                for j in re.split(r"[ ~]+",
                        re.sub(r"pro\|you", "pro:sub|you", i["%mor"])):
                    if "|" in j:
                        # sofl.ins(re.sub(r"\|\w*", "", j))
                        print(re.sub(r"^.*?#", "", re.sub(r"\|\w*", "", j)))
                        print(j)
                    else:
                        # print(j)
                        pass
                # for j in re.sub(r"\|.*?(?=[& ])", "", i[r"%mor"]).split():
                    # sofl.ins(j)
            except:
                # print(i)
                pass
# for i in sofl.rank:
    # print(i)
