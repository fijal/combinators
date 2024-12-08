
from soup import Soup
from signed_float import add_signed_float, Add, signed_val

EPSILON = 0.1

def equals_enough(one, two):
    if one == 0.0:
        return (one - two) < EPSILON
    return abs(one - two) / abs(one) < EPSILON

def test_signed_float():
    def check(a, b):
        s = Soup()
        add_signed_float(s, "a", a, extra=1000)
        add_signed_float(s, "b", b, extra=1000)
        assert equals_enough(signed_val(s, "a"), a)
        assert equals_enough(signed_val(s, "b"), b)
        s.add_operator(Add("a", "b", "c"))
        s.iterate(s.BASE_COUNT - 1000)
        assert equals_enough(signed_val(s, "c"), a + b)
        #for k in ['a_a', 'a_b', 'a_c', 'b_a', 'b_b', 'b_c']:
        #    assert s.soup[k] < 1000

    numbers = [-13, -1.5, -0.3, 0, 0.3, 1.5, 13]
    check(-13, 0.3)
    for n1 in numbers:
        for n2 in numbers:
            check(n1, n2)
