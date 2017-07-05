import pickle
import numpy as np
import pandas as pd
# from file_to_vector import file_to_vector
from sklearn import cross_validation
from sklearn import linear_model
from sklearn import svm
from sklearn import tree
from sklearn import naive_bayes
from sklearn import neighbors
from sklearn import ensemble
from sklearn import preprocessing
from sklearn.feature_selection import SelectKBest, f_classif, VarianceThreshold

d = pickle.load(open("pure_data.data","rb"))
d = d.loc[d["narr"] == 1]
X, Y = d.drop(pd.Index(["narr", "SLI+"]), axis=1), d["SLI+"]
print(X)
print(Y)
# X = X[['1Words beehive', '1Words birthday', '2POS WP NNP', '2Words Dog to', '2Words I woke', '2Words because like', '2Words climbed outof', '2Words er when', '2Words he be', '2Words in there', '2Words rock and', '2Words still looked', '2Words they could', '2Words thought that', '2Words went looking', '3POS JJ CC JJ', '3POS JJ RB .', '3POS RB , WRB', '3Words . squirrel got', '3Words and chucked him', '3Words and smashed the', '3Words and was not', '3Words basically so ...', '3Words couldnt find the', '3Words do what they', '3Words forgot and he', '3Words frogs and a', '3Words he brought home', '3Words he could find', '3Words he stood on', '3Words high up .', '3Words his frog ,', '3Words playing around with', '3Words shouted at .', '3Words so he thinks', '3Words the dogs still', '3Words yesterday a boy', '4POS CC NNS IN RB', '4POS CC RB IN PDT', '4POS CC VBD NNS TO', '4POS CC VBD PRP RP', '4POS CC WRB NN VBZ', '4POS NN CC RB VBG', '4POS NN PRP CC DT', '4POS NNP VBD VBN IN', '4POS PRP IN DT JJ', '4POS PRP VBP RP DT', '4POS RP CC JJ RB', '4POS VBP VB WP JJ', '4POS WP VBZ VBN ,', '4Words and a dog was', '4Words and see if the', '4Words and they fell into', '4Words angry beaver or something', '4Words back of my garden', '4Words because as I woke', '4Words bought a frog .', '4Words he found the frog', '4Words he punches me ,', '4Words his lights out .', '4Words like oh she is', '4Words my brother really annoys', '4Words saying that I copy', '4Words says um all ...', '4Words side of the rock', '4Words the frog had escaped', '4Words the frog has disappeared', '4Words the little boy is', '4Words the little boy was', '4Words up on his head', '4Words was a beehive there', '4Words was a swarm a', '4Words went into the forest']]
FS1 = VarianceThreshold(threshold=0.000001).fit(X)
# print(sum(FS1.get_support()))
X = FS1.transform(X)
# print(len(X), len(X[0]))
FS2 = SelectKBest(f_classif, 10).fit(X, Y)
X = FS2.transform(X)
# print(len(X), len(X[0]))
X = preprocessing.scale(X)
# print(FS2.get_support())
# print(d.columns)
# print(d.drop(["SLI+", "narr"], axis=1).columns[FS1.get_support()][FS2.get_support()])
# print(d[d.drop(["SLI+", "narr"], axis=1).columns[FS1.get_support()][FS2.get_support()]])
# print(d[d.drop(["SLI+", "narr"], axis=1).columns[FS1.get_support()][FS2.get_support()]].mean(),
#     d[d.drop(["SLI+", "narr"], axis=1).columns[FS1.get_support()][FS2.get_support()]].std()
# )

raw_classifiers = (
    linear_model.Perceptron(),
    linear_model.SGDClassifier(),
    linear_model.LogisticRegression(),
    tree.DecisionTreeClassifier(),
    naive_bayes.GaussianNB(),
    neighbors.KNeighborsClassifier(n_neighbors=5),
    svm.SVC(kernel="rbf"),
    svm.SVC(kernel="linear"),
    svm.SVC(kernel="poly")
    # ensemble.RandomForestClassifier()
)

rc_labels = (
    "Perceptron",
    "SGDClassifier",
    "LogisticRegression",
    "DecisionTreeClassifier",
    "GaussianNB",
    "KNeighborsClassifier",
    "SVC_rbf",
    "SVC_linear",
    "SVC_poly"
    # "RandomForestClassifier"
)

assert len(raw_classifiers) == len(rc_labels)

self_made_ensembles = (
    ensemble.GradientBoostingClassifier(),
    ensemble.RandomForestClassifier(),
    ensemble.ExtraTreesClassifier()
)

single_base_ensembles = (
    lambda x: x,
    ensemble.AdaBoostClassifier,
    ensemble.BaggingClassifier
)


ens_results = []
for ens in single_base_ensembles:
    predictions = []
    results = []
    for clf in raw_classifiers:
        try:
            dump = pickle.dumps(ens(clf))

            clf_temp = pickle.loads(dump)
            # X = RFE(clf_temp, 6).fit_transform(X, Y)

            L = [] # list to store pthe redictions
            for train, test in cross_validation.LeaveOneOut(len(d)):
                clf_temp = pickle.loads(dump)
                clf_temp.fit(X[train], Y.iloc[train])
                L.append(clf_temp.predict(X[test])[0])

            L = pd.Series(L, index=Y.axes)
            name = clf.__class__.__name__
            accuracy = (Y == L).mean()
            recall = (Y == L)[Y == 1].mean()
            precision = (Y == L)[L == 1].mean()
            f1 = 2 * recall * precision / (recall + precision)
            predictions.append(L.tolist())
            results.append([name, accuracy, recall, precision, f1])
            # print("tick:\t" + clf.__class__.__name__)
        except Exception as e:
            pass
            # print(clf.__class__.__name__, e)
    ens_results.append(results)
    results = pd.DataFrame(results, columns=["name","accuracy","recall","precision","f1"])
    print("\n" + str(ens) + "\n")
    print(results)

predictions = []
results = []
for clf in self_made_ensembles:
    try:
        dump = pickle.dumps(clf)

        clf_temp = pickle.loads(dump)
        # X = RFE(clf_temp, 6).fit_transform(X, Y)

        L = []
        for train, test in cross_validation.LeaveOneOut(len(d)):
            clf_temp = pickle.loads(dump)
            clf_temp.fit(X[train], Y.iloc[train])
            L.append(clf_temp.predict(X[test])[0])

        L = pd.Series(L, index=Y.axes)
        name = clf.__class__.__name__
        accuracy = (Y == L).mean()
        recall = (Y == L)[Y == 1].mean()
        precision = (Y == L)[L == 1].mean()
        f1 = 2 * recall * precision / (recall + precision)
        predictions.append(L.tolist())
        results.append([name, accuracy, recall, precision, f1])
        # print("tick:\t" + clf.__class__.__name__)
    except Exception as e:
        pass
        # print(clf.__class__.__name__, e)

results = pd.DataFrame(results, columns=["name","accuracy","recall","precision","f1"])
print("\nself-made ensembles\n")
print(results)


voting_ensembles = (
    ensemble.VotingClassifier(
        estimators=[(rc_labels[i], raw_classifiers[i]) for i in range(len(rc_labels))],
        voting="hard"),
    ensemble.VotingClassifier(
        estimators=[(rc_labels[i], raw_classifiers[i]) for i in range(len(rc_labels))],
        voting="hard",
        weights=[i[4] for i in ens_results[0]]),
    ensemble.VotingClassifier(
        estimators=[(rc_labels[i], raw_classifiers[i]) for i in range(2, 6)],
        voting="hard"),
    ensemble.VotingClassifier(
        estimators=[(rc_labels[i], raw_classifiers[i]) for i in range(2, 6)],
        voting="hard",
        weights=[ens_results[0][i][4] for i in range(2, 6)]),
    ensemble.VotingClassifier(
        estimators=[(rc_labels[i], raw_classifiers[i]) for i in range(2, 6)],
        voting="soft"),
    ensemble.VotingClassifier(
        estimators=[(rc_labels[i], raw_classifiers[i]) for i in range(2, 6)],
        voting="soft",
        weights=[ens_results[0][i][4] for i in range(2, 6)]),
)

# voting ensemble method
predictions = []
results = []
for clf in voting_ensembles:
    try:
        dump = pickle.dumps(clf)

        clf_temp = pickle.loads(dump)
        # X = RFE(clf_temp, 6).fit_transform(X, Y)

        L = []
        for train, test in cross_validation.LeaveOneOut(len(d)):
            clf_temp = pickle.loads(dump)
            clf_temp.fit(X[train], Y.iloc[train])
            L.append(clf_temp.predict(X[test])[0])

        L = pd.Series(L, index=Y.axes)
        name = clf.__class__.__name__
        accuracy = (Y == L).mean()
        recall = (Y == L)[Y == 1].mean()
        precision = (Y == L)[L == 1].mean()
        f1 = 2 * recall * precision / (recall + precision)
        predictions.append(L.tolist())
        results.append([name, accuracy, recall, precision, f1])
        # print("tick:\t" + clf.__class__.__name__)
    except Exception as e:
        print(clf.__class__.__name__, e)
        pass

results = pd.DataFrame(results, columns=["name","accuracy","recall","precision","f1"])
print("\nVoting classifiers\n")
print(results)

# Soft voting doesn't work with linear_model or svm
