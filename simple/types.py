import collections, re, os
import numpy as np
import pandas as pd
from core.raw_conditional import RawConditional

class IsSequence(RawConditional):
    def check(self, xs, **kwargs):
        return isinstance(xs, collections.Sequence)

    def describe(self, value):
        if value:
            print "It's a sequence, with a length."

class IsNumerical(RawConditional):
    def check(self, xs, **kwargs):
        try:
            self.env.set('numeric', float(xs))
            return True
        except:
            return False

    def describe(self, value):
        if value:
            print "It's a number."

class IsNumericalSequence(IsSequence):
    def check(self, xs, confidence=1):
        if isinstance(xs, str):
            match = re.match(r'\s*([-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?|[0-9]+\.)([^-+.0-9]+)([-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?|[0-9]+\.)', xs)
            if match:
                # Does this entirely consist of such numbers?
                delimiter = match.group(3)
                try:
                    self.env.set('numseq', map(float, xs.split(delimiter)))
                except:
                    return IsNumerical(self.env).check(xs, confidence=confidence)
                try:
                    self.env.set('intseq', map(int, xs.split(delimiter)))
                except:
                    return float

                self.env.trigger('intseq', self.env.get('intseq'))

                return int

        if not super(IsNumericalSequence, self).check(xs, confidence=confidence):
            return False

        try:
            if np.all([isinstance(x, int) for x in np.random.choice(xs, int(np.ceil(len(xs) * confidence)), replace=False)]):
                self.env.set('numseq', xs)
                self.env.set('intseq', xs)

                self.env.trigger('intseq', xs)
                return int
        except:
            pass

        try:
            if np.all([isinstance(x, int) or isinstance(x, float) for x in np.random.choice(xs, np.ceil(len(xs) * confidence), replace=False)]):
                self.env.set('numseq', xs)
                return float
        except:
            pass

        return False

    def describe(self, value):
        if value == int:
            print "It's a sequence of integers."

        if value == float:
            print "It's a sequence of numbers."

class IsLocalFilePath(RawConditional):
    def check(self, xs, **kwargs):
        if isinstance(xs, str):
            if os.path.exists(xs):
                if xs[-4] == '.csv':
                    self.env.set('panda.read', pd.read_csv)
                    return 'csv'
                return True

        return False

    def describe(self, value):
        if isinstance(value, str):
            print "This is a local " + value.upper() + " file."
        elif value:
            print "This is a local file."

