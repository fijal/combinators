

""" Signed float is represented by (a - b) / c
"""

import random
from soup import add_relative_prob, remove_relative_prob

class SignedFloatBinaryOp:
    pass

def add_signed_float(soup, name, f_v, extra=0):
    """ Add a signed float to the soup
    """
    if f_v > 0.0:
        soup.add(name + "_b", extra)
        if f_v >= 1.0:
            soup.add(name + "_a", soup.BASE_COUNT + extra)
            soup.add(name + "_c", int(soup.BASE_COUNT / f_v))
        else:
            soup.add(name + "_a", int(f_v * soup.BASE_COUNT) + extra)
            soup.add(name + "_c", soup.BASE_COUNT)
    else:
        if f_v < -1.0:
            soup.add(name + '_a', extra)
            soup.add(name + '_b', soup.BASE_COUNT + extra)
            soup.add(name + '_c', int(soup.BASE_COUNT / (-f_v)))
        else:
            soup.add(name + "_a", extra)
            soup.add(name + "_b", int(-f_v * soup.BASE_COUNT) + extra)
            soup.add(name + "_c", soup.BASE_COUNT)

def signed_val(soup, n):
    return (soup[n + "_a"] - soup[n + "_b"]) / soup[n + "_c"]

#def remove_relative_prob(soup, xa, xb, xc, prob):
#    if soup.soup[xa] + soup.soup[xb] > soup.soup[xc]:
#        assert prob <= 1
#        soup.remove(x1)
#        soup.remove_prob(x2, prob)
#    else:
#        assert 1 / prob <= 1
#        soup.remove(x2)
#        soup.remove_prob(x1, 1 / prob)

class Add(SignedFloatBinaryOp):
    def __init__(self, n1, n2, res):
        self.n1 = n1
        self.n2 = n2
        self.res = res
        self.args = [n1 + "_a", n1 + "_b", n1 + "_c", n2 + "_a", n2 + "_b", n2 + "_c"]
        self.res = [res + "_a", res + "_b", res + "_c"]

    def probability(self, soup):
        if soup[self.args[2]] == 0 or soup[self.args[5]] == 0:
            return 0
        return ((soup[self.args[0]] + soup[self.args[1]] + soup[self.args[2]]) *
                (soup[self.args[3]] + soup[self.args[4]] + soup[self.args[5]]) /
                (soup.total * soup.total))

#    def operate(self, soup):
#        assert soup[self.args[0]] + soup[self.args[1]] > soup[self.args[3]] + soup[self.args[4]]
#        xxx

    def operate(self, soup):
        xa, xb, xc = self.args[0], self.args[1], self.args[2]
        ya, yb, yc = self.args[3], self.args[4], self.args[5]
        za, zb, zc = self.res[0], self.res[1], self.res[2]
#        if soup.soup[y1] > soup.soup[x1]:
#            crash
        # x1 > y1
        xa_count, xb_count, xc_count = soup.soup[xa], soup.soup[xb], soup.soup[xc]
        ya_count, yb_count, yc_count = soup.soup[ya], soup.soup[yb], soup.soup[yc]
        if xa_count + xb_count > xc_count:
            soup.remove_prob(xa, xa_count / (xa_count + xb_count))
            soup.remove_prob(xb, xb_count / (xa_count + xb_count))
            soup.remove_prob(xc, xc_count / (xa_count + xb_count))
            remove_relative_prob(soup, ya, yb, yc, (ya_count + yb_count) / (xa_count + xb_count))
        else:
            soup.remove(xc)
            soup.remove_prob(xa, xa_count / xc_count)
            soup.remove_prob(xb, xb_count / xc_count)
            remove_relative_prob(soup, ya, yb, yc, yc_count / xc_count)
#        if swap:
#            v = rev_operand(x1_count / x2_count, y1_count / y2_count)
#        else:
        v = ((xa_count - xb_count) / xc_count) + ((ya_count - yb_count)/ yc_count)
#            v = operand(x1_count / x2_count, y1_count / y2_count)
        if v == 0:
            soup.add(zc)
        elif v > 0:
            add_relative_prob(soup, za, zb, zc, 1 / v)
        else:
            add_relative_prob(soup, zb, za, zc, 1 / -v)

def remove_relative_prob(soup, ya, yb, yc, prob):
    if random.random() < prob:
        ya_count, yb_count, yc_count = soup.soup[ya], soup.soup[yb], soup.soup[yc]
        if ya_count + yb_count > yc_count:
            soup.remove_prob(ya, ya_count / (ya_count + yb_count))
            soup.remove_prob(yb, yb_count / (ya_count + yb_count))
            soup.remove_prob(yc, yc_count / (ya_count + yb_count))
        else:
            soup.remove(yc)
            soup.remove_prob(ya, ya_count / yc_count)
            soup.remove_prob(yb, yb_count / yc_count)


def add_relative_prob(soup, za, zb, zc, prob):
    assert prob >= 0
    if prob <= 1:
        soup.add(za)
        soup.add(zb, 0)
        soup.add_prob(zc, prob)
    else:
        soup.add(zc)
        soup.add(zb, 0)
        soup.add_prob(za, 1 / prob)
