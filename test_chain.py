
from soup import Soup, Rename, Add, Sub, Greater, Fork

EPSILON = 0.1

def equals_enough(one, two):
    if one == 0.0:
        return (one - two) < EPSILON
    return abs(one - two) / one < EPSILON

def test_chain():
    s = Soup()
    for n in range(10):
        s.add_num("x%d" % n, 0.75)
    s.add_num("i0", 0)
    for n in range(10):
        s.add_operator(Add("x%d" % n, "i%d" % n, "i%d" % (n + 1)))

    for k in range(30):
        print([s.num("i%d" % i) for i in range(11)])
        print([s["i%d_1" % i] for i in range(11)])
        s.iterate(Soup.BASE_COUNT)