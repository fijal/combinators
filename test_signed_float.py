
from soup import Soup
from signed_float import add_signed_float, Add, signed_val

EPSILON = 0.1

def equals_enough(one, two):
    if one == 0.0:
        return (one - two) < EPSILON
    return abs(one - two) / one < EPSILON

def test_signed_float():
    s = Soup()
    add_signed_float(s, "a", 0.35)
    add_signed_float(s, "b", -0.1)
    s.add_operator(Add("a", "b", "c"))
    s.iterate(s.BASE_COUNT)
    assert equals_enough(signed_val(s, "c"), 0.25)