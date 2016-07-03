import urllib
from core.raw_conditional import RawConditional
from simple.types import IsNumericalSequence

class IntegerSequenceEncyclopedia(RawConditional):
    def check(self, xs, **kwargs):
        if self.env.get('intseq') is None:
            if IsNumericalSequence(self.env).check(xs) != int:
                return False
            
        url = "http://oeis.org/search?fmt=text&q=" + ','.join(map(str, self.env.get('intseq')))
        fp = urllib.urlopen(url)

        sequences = []
        midseq = False
        for line in fp:
            if len(line) <= 2:
                midseq = False
                
            if midseq:
                sequences[-1] += line
            elif len(line) > 2 and line[0] == '%':
                sequences.append(line)
                midseq = True

        return sequences

    def describe(self, sequences):
        if sequences:
            if len(sequences) == 10:
                print "There are at least 10 known sequences containing these numbers."
            else:
                print "There are %d known sequences containing these numbers." % (len(sequences))
                
