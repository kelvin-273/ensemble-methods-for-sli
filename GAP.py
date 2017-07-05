"""Genetic Algorithm Predictor"""
import numpy as np
import pandas as pd
import pickle
from sklearn import cross_validation

from sklearn import naive_bayes
# from sklearn import tree

d = pickle.load(open("pure_data.data","rb"))
# d = d.loc[d["narr"] == 0]
X, Y = d.drop(pd.Index(["SLI+"]), axis=1), d["SLI+"]
# X, Y = d.drop(pd.Index(["narr", "SLI+"]), axis=1), d["SLI+"]
f = open("ga_restults.txt", "w")

def ga():
    dna = [np.random.rand(len(X.columns)) < 0.00008 for i in range(80)]
    fitness = [LOO_test(naive_bayes.GaussianNB(), X[X.columns[i]].as_matrix(), Y) for i in dna]

    for i in range(len(dna)):
        print(fitness[i])
    maxi = find_maxi(fitness)
    print(maxi,"\n")
    f.write(str(fitness[maxi]) + ", " + str(X.columns[dna[maxi]]) + "\n")

    while True:
        dna = kill(dna, fitness, 0.5)
        dna = breed(dna)

        fitness = [LOO_test(naive_bayes.GaussianNB(), X[X.columns[i]].as_matrix(), Y) for i in dna]

        for i in range(len(dna)):
            print(fitness[i])
        maxi = find_maxi(fitness)
        print(maxi,"\n")
        f.write(str(fitness[maxi]) + ", " + str(X.columns[dna[maxi]]) + "\n")

def find_maxi(fitness):
    maxf = fitness[0]
    maxi = 0
    for i in range(1, len(fitness)):
        if fitness[i] > maxf:
            maxi = i
            maxf = fitness[i]
    return maxi

def kill(dna, fitness, p):
    """sort and kill some portion of the population"""
    assert 0 < p < 1
    dna, fitness = kill_sort(dna, fitness)
    return dna[:(len(dna)//2)]

def kill_sort(dna, fitness):
    index = [(fitness[i], i) for i in range(len(fitness))]
    # sorting method goes here
    # for i in index:
    #     print(i)
    index = qsort(index)
    # print("tick")
    # for i in index:
    #     print(i)
    dna = [dna[i[1]] for i in index]
    fitness = [fitness[i[1]] for i in index]
    return dna, fitness

def qsort(L):
    return (qsort([y for y in L[1:] if y[0] >  L[0][0]]) +
            L[:1] +
            qsort([y for y in L[1:] if y[0] <= L[0][0]])) if len(L) > 1 else L

def breed(dna):
    """
    takes current population breeds more
    parent pairs are created, bread, and clidren are appended
    """
    for i in range(len(dna) // 2):
        dna += sexy_time(dna[2*i], dna[2*i + 1], 2)
    return dna

def sexy_time(x, y, n):
    """2 parent boolean arrays x,y breed n children arrays"""
    assert len(x) == len(y)
    z = np.zeros(len(x), dtype="bool")
    children = []
    for n in range(n):
        for i in range(len(z)):
            z[i] = np.random.choice((x[i], y[i]))
        z = mutate(z, 0.00001)
        children.append(z)
    return children

def mutate(z, p):
    """mutates boolean vector with probability p"""
    assert 0 < p < 1
    m = np.random.rand(len(z)) < p
    # return ((z - m * z) + m * (1 -z)).astype("bool")
    # the above statement can be proved to be
    # return (z - m)**2
    # which is equivalent to
    return np.logical_xor(z, m)
# print(X.columns[dna])

# print(len(d))
# for i in X.index:
#     print(i, len(X.loc[i]))
# print(X.loc[117])
# print(X.loc[118])
# print(X.columns)
def LOO_test(clf, X, Y):
    try:
        dump = pickle.dumps(clf)

        clf_temp = pickle.loads(dump)
        # X = RFE(clf_temp, 6).fit_transform(X, Y)

        L = []
        for train, test in cross_validation.LeaveOneOut(len(d)):
            # print(test)
            clf_temp = pickle.loads(dump)
            # print("tick")
            # print(X.as_matrix()[train])
            # print(Y.irow(train))
            # print(len(X.as_matrix()))
            # print(len(X.as_matrix().T))
            # print(len(X.as_matrix()[train]))
            clf_temp.fit(X[train], Y.irow(train))
            L.append(clf_temp.predict(X[test])[0])

        L = pd.Series(L, index=Y.axes)
        # name = clf.__class__.__name__
        # accuracy = (Y == L).mean()
        recall = (Y == L)[Y == 1].mean()
        precision = (Y == L)[L == 1].mean()
        f1 = 2 * recall * precision / (recall + precision)
        # return [name, accuracy, recall, precision, f1]
        return f1
        # print("tick:\t" + clf.__class__.__name__)
    except Exception as e:
        pass
        # print(clf.__class__.__name__, e)

if __name__ == '__main__':
    ga()
