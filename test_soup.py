
import math

from soup import Soup, Rename, Add

EPSILON = 0.1

def equals_enough(one, two):
    return abs(one - two) / one < EPSILON

def test_soup():
    s = Soup()
    s.add_num("x", 1.2)
    assert equals_enough(s.num("x"), 1.2)
    s.add_num("y", 0.75)
    assert equals_enough(s.num("y"), 0.75)

def test_rename():
    s = Soup()
    s.add_num("x", 0.125)
    s.add_num("y", 1.75)
    s.add_operator(Rename("x", "z"))
    s.add_operator(Rename("y", "foo"))
    s.iterate(Soup.BASE_COUNT)
    assert equals_enough(s.num("z"), 0.125)
    assert equals_enough(s.num("foo"), 1.75)
    s.add_num("xyz", 10)
    s.add_operator(Rename("xyz", "zzz"))
    s.iterate(Soup.BASE_COUNT)
    assert equals_enough(s.num("zzz"), 10)

def test_add():
    s = Soup()
    s.add_num("x", 0.125)
    s.add_num("y", 1.75)
    s.add_operator(Add("x", "y", "z"))
    s.iterate(Soup.BASE_COUNT)
    assert equals_enough(s.num("z"), 1.875)

    s = Soup()
    s.add_num("x", 1.125)
    s.add_num("y", 1.75)
    s.add_operator(Add("x", "y", "z"))
    s.iterate(Soup.BASE_COUNT)
    assert equals_enough(s.num("z"), 2.875)
