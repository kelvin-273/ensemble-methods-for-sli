"""
Self Ordering Frequency List module

This class is a list that stores pairs of items and their frequency
    and sorts itself with each insert
when used in applications like natural language where
    the distribution of frequencies with respect to
    their rank follows a 1/N distribution, the armortised
    runtime can reach O(1)
"""
# still used in nsyl_test

class SOFL(object):
    """Self Ordering Frequency List class"""
    def __init__(self):
        super(SOFL, self).__init__()
        self.rank = []
        self.total = 0

    def ins(self, seq):
        """find seq in obj and increment it or append it"""
        self.total += 1
        for i in range(len(self.rank)):
            if self.rank[i][0] == seq:
                self.rank[i][1] += 1
                self._rise(i)
                return
        self.rank.append([seq, 1])

    def _rise(self, i):
        """bubbles item up to its respective rank"""
        while i > 0:
            if self.rank[i-1][1] < self.rank[i][1]:
                self.rank[i-1], self.rank[i] = self.rank[i], self.rank[i-1]
                i -= 1
            else:
                return

    def percent(self, i):
        """gives indexed item's percentage frequency"""
        return self.rank[i][0], self.rank[i][1] / self.total

    def titles(self):
        return [i[0] for i in self.rank]

    def __str__(self):
        return str(self.rank)

    def __len__(self):
        return len(self.rank)
