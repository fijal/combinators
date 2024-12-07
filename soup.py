

import random, os

class Rename:
    def __init__(self, n1, n2):
        self.n1 = n1
        self.n2 = n2
        self.args = [n1 + "_1", n1 + "_2"]
        self.res = [n2 + "_1", n2 + "_2"]

    def operate(self, soup):
        rename_op(soup, self.args[0], self.args[1], self.res[0], self.res[1])

def rename_op(soup, x1, x2, xp1, xp2):
    count1 = soup.soup[x1]
    count2 = soup.soup[x2]
    if count1 > count2:
        soup.remove(x1)
        soup.add(xp1)
        if random.random() < count2 / count1:
            soup.remove(x2)
        if random.random() < count2 / count1:
            soup.add(xp2)
    else:
        soup.remove(x2)
        soup.add(xp2)
        if random.random() < count1 / count2:
            soup.remove(x1)
        if random.random() < count1 / count2:
            soup.add(xp1)

class Fork:
    def __init__(self, n, res1, res2):
        self.args = [n + "_1", n + "_2"]
        self.res = [res1 + "_1", res1 + "_2", res2 + "_1", res2 + "_2"]

    def operate(self, soup):
        x1 = self.args[0]
        x2 = self.args[1]
        count1 = soup.soup[x1]
        count2 = soup.soup[x2]
        if count1 > count2:
            soup.remove(x1)
            soup.add(self.res[0])
            soup.add(self.res[2])
            if random.random() < count2 / count1:
                soup.remove(x2)
            if random.random() < count2 / count1:
                soup.add(self.res[1])
            if random.random() < count2 / count1:
                soup.add(self.res[3])
        else:
            soup.remove(x2)
            soup.add(self.res[1])
            soup.add(self.res[3])
            if random.random() < count1 / count2:
                soup.remove(x1)
            if random.random() < count1 / count2:
                soup.add(self.res[0])
            if random.random() < count1 / count2:
                soup.add(self.res[1])


def add_relative_prob(soup, x1, x2, prob):
    if prob <= 1:
        soup.add(x1)
        soup.add_prob(x2, prob)
    else:
        soup.add(x2)
        soup.add_prob(x1, 1 / prob)

def remove_relative_prob(soup, x1, x2, prob):
    if soup.soup[x1] > soup.soup[x2]:
        assert prob <= 1
        soup.remove(x1)
        soup.remove_prob(x2, prob)
    else:
        assert 1 / prob <= 1
        soup.remove(x2)
        soup.remove_prob(x1, 1 / prob)

def create_op(name, operand, rev_operand):
    def wrapper(swap):
        def newop(soup, x1, x2, y1, y2, z1, z2):
            if soup.soup[y1] > soup.soup[x1]:
                if swap:
                    return op(soup, y1, y2, x1, x2, z1, z2)
                return reverseop(soup, y1, y2, x1, x2, z1, z2)
            # x1 > y1
            x1_count = soup.soup[x1]
            x2_count = soup.soup[x2]
            y1_count = soup.soup[y1]
            y2_count = soup.soup[y2]
            if x1_count > x2_count:
                #assert x1_count >= y1_count
                soup.remove(x1)
                soup.remove_prob(x2, x2_count / x1_count)
                if random.random() < y1_count / x1_count:
                    remove_relative_prob(soup, y1, y2, y2_count / y1_count)
            else:
                #assert x2_count >= y2_count
                soup.remove(x2)
                soup.remove_prob(x1, x1_count / x2_count)
                if random.random() < y2_count / x2_count:
                    remove_relative_prob(soup, y2, y1, y1_count / y2_count)
            if swap:
                v = rev_operand(x1_count / x2_count, y1_count / y2_count)
            else:
                v = operand(x1_count / x2_count, y1_count / y2_count)
            if v == 0:
                soup.add(z2)
            else:
                add_relative_prob(soup, z1, z2, 1 / v)
        newop.__name__ = name
        return newop

    reverseop = wrapper(True)
    op = wrapper(False)
    return op

add_op = create_op("add", lambda a, b: a + b, lambda a, b: a + b)
#sub_op = create_op("sub", lambda a, b: a - b, lambda a, b: crash)
#greater_op = create_op("greater", lambda a, b: a > b, lambda a, b: a <= b)

class Add:
    def __init__(self, n1, n2, res):
        self.n1 = n1
        self.n2 = n2
        self.res = res
        self.args = [n1 + "_1", n1 + "_2", n2 + "_1", n2 + "_2"]
        self.res = [res + "_1", res + "_2"]

    def operate(self, soup):
        add_op(soup, self.args[0], self.args[1], self.args[2], self.args[3], self.res[0], self.res[1])

    def probability(self, soup):
        if soup[self.args[1]] == 0 or soup[self.args[3]] == 0:
            return 0
        return ((soup[self.args[0]] + soup[self.args[1]]) *
                (soup[self.args[2]] + soup[self.args[3]]) /
                (soup.total * soup.total))

class Sub:
    def __init__(self, n1, n2, res):
        self.n1 = n1
        self.n2 = n2
        self.res = res
        self.args = [n1 + "_1", n1 + "_2", n2 + "_1", n2 + "_2"]
        self.res = [res + "_1", res + "_2"]

    def operate(self, soup):
        sub_op(soup, self.args[0], self.args[1], self.args[2], self.args[3], self.res[0], self.res[1])

class Greater:
    def __init__(self, n1, n2, res):
        self.n1 = n1
        self.n2 = n2
        self.res = res
        self.args = [n1 + "_1", n1 + "_2", n2 + "_1", n2 + "_2"]
        self.res = [res + "_1", res + "_2"]

    def operate(self, soup):
        greater_op(soup, self.args[0], self.args[1], self.args[2], self.args[3], self.res[0], self.res[1])

class Soup:
    BASE_COUNT = 100000
    MIN = 100
    
    def __init__(self):
        self.soup = {}
        self.total = 0
        self.operators = []

    def __getitem__(self, item):
        return self.soup.get(item, 0)

    def num(self, n):
        if self.soup.get(n + "_1", 0) + self.soup.get(n + "_2", 0) < self.MIN:
            return "NaN"
        return self.soup.get(n + "_1", 0) / self.soup[n + "_2"]

    def add(self, token, count=1):
        if token not in self.soup:
            self.soup[token] = count
        else:
            self.soup[token] += count
        self.total += count

    def add_operator(self, op):
        self.operators.append(op)

    def add_prob(self, token, prob):
        if random.random() < prob:
            self.add(token)

    def remove_prob(self, token, prob):
        if random.random() < prob:
            self.remove(token)

    def remove(self, token, count=1):
        self.soup[token] -= count
        assert self.soup[token] >= 0
        self.total -= count

    def pick_random_op(self):
        # XXX we might want to *not* recalculate the probabilities
        #     with every random op, but it's hard to calculate exactly
        #     how many iterations we need to do that
        lst = []
        ans = []
        for op in self.operators:
            lst.append(op.probability(self))
            ans.append(op)
        idx = random.random() * sum(lst)
        i = 0
        cur = 0.0
        if sum(lst) == 0:
            return None
        while True:
            cur += lst[i]
            if idx < cur:
                return ans[i]
            i += 1


    def iterate(self, count):
        for i in range(count):
            op = self.pick_random_op()
            if op is None:
                return
            op.operate(self)

    def add_num(self, name, val):
        if val > 1:
            self.add(name + "_1", self.BASE_COUNT)
            self.add(name + "_2", int(self.BASE_COUNT / val))
        else:
            self.add(name + "_1", int(self.BASE_COUNT * val))
            self.add(name + "_2", self.BASE_COUNT)
