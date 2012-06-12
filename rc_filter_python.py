import math

class RCFilter(object):
    def __init__(self, decaytime):
        self.output = 0.0
        self.coeff = 1.0 - math.exp(-1.0 / decaytime)

    def apply(self, input):
        self.output += self.coeff * (input - self.output)
        return self.output

def run_me():
    rc = RCFilter(10.0)

    for i in xrange(10):
        print rc.apply(1.0)
