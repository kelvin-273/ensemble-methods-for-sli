"""class for ngram tree"""

class Node(object):
    """docstring for Node"""
    def __init__(self, ngram):
        super(Node, self).__init__()
        assert ngram.__class__.__name__ == "list"
        self.gram = ngram[0]
        self.children = []
        self.counts = 0
        self.parent = None
        self.ins(ngram[1:])

    def get_conditional_probability(self):
        """returns condtional probablities"""
        return self.counts / self.parent.counts

    def ins(self, nminus1_gram):
        """inserts n-1gram into partial tree and increrases it's counts value"""
        assert nminus1_gram.__class__.__name__ == "list"
        self.counts += 1
        if len(nminus1_gram) > 0:
            for i in range(len(self.children)):
                if nminus1_gram[0] == self.children[i].gram:
                    self.children[i].ins(nminus1_gram[1:])
                    self._sort(i)
                    return
            self.children.append(Node(nminus1_gram))
            self.children[-1].parent = self

    def _sort(self, i):
        """sorts tree to keep computational complexity down"""
        while i > 0:
            if self.children[i-1].counts < self.children[i].counts:
                self.children[i-1], self.children[i] = self.children[i], self.children[i-1]
                i -= 1
            else:
                return

class NgramTree(object):
    """docstring for NgramTree"""
    def __init__(self, gram):
        super(NgramTree, self).__init__()
        self.gram = gram
        self.children = []
        self.counts = 0

    def ins(self, ngram):
        """inserts n-1gram into partial tree and increrases it's counts value"""
        assert ngram.__class__.__name__ == "list"
        if len(ngram) > 0:
            self.counts += 1
            for i in range(len(self.children)):
                if ngram[0] == self.children[i].gram:
                    self.children[i].ins(ngram[1:])
                    self._sort(i)
                    return
            self.children.append(Node(ngram))
            self.children[-1].parent = self

    def _sort(self, i):
        """sorts tree to keep computational complexity down"""
        while i > 0:
            if self.children[i-1].counts < self.children[i].counts:
                self.children[i-1], self.children[i] = self.children[i], self.children[i-1]
                i -= 1
            else:
                return

def treePrint(w, n):
    """print out the tree structure"""
    print("\t"*n + str(w.gram))
    for i in w.children:
        treePrint(i, n+1)

def get_titles(tree):
    """gather lists of titles using pre-order traversal"""
    titles = []
    for child in tree.children:
        get_titles_aux(child, 0, tree.gram, titles)
    return titles

def get_titles_aux(node, depth, previous_string, titles):
    """auxiliary function to get_titles"""
    while len(titles) < depth + 1:
        titles.append([])
    name = previous_string + " " + node.gram
    titles[depth].append(name)
    for child in node.children:
        get_titles_aux(child, depth + 1, name, titles)

def get_dictionaries(tree):
    dictionaries = [{j:0 for j in i} for i in get_titles(tree)]
    for child in tree.children:
        get_dictionaries_aux(child, 0, tree.gram, dictionaries)
    return dictionaries

def get_dictionaries_aux(node, depth, previous_string, dictionaries):
    """auxiliary function to get_dictionaries"""
    name = previous_string + " " + node.gram
    dictionaries[depth][name] = node.get_conditional_probability()
    for child in node.children:
        get_dictionaries_aux(child, depth + 1, name, dictionaries)
