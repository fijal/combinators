
from pprint import pprint
import random

from soup import Soup

soup = Soup()
#soup.add("x1", 3)
#soup.add("x2", 5)

def op1(soup):
    if random.random() < 1 / soup.soup["x1"]:
        soup.remove("x1")
    soup.remove("x2")
    soup.add("x3")

soup.add("x1", 200000)
soup.add("x2", 120000)
soup.add("y1", 50000)
soup.add("y2", 400000)

OPERATORS = {
#    ("x1", "x2"): lambda soup, x1, x2: rename_op(soup, x1, x2, x1, x2)
    ("y1", "y2", "x1", "x2"): add_op,
}

if __name__ == '__main__':
    for i in range(100000):
        if i % 10000 == 0 and i > 0:
            print("%.3f %.3f %.3f %d" % (soup["x1"] / soup["x2"], soup["y1"] / soup["y2"], soup["z1"] / soup["z2"], soup.total))

        soup.iterate()
    pprint(soup.soup)

