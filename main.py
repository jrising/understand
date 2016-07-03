import sys
import logic

print "Let's understand something!"

if len(sys.argv) > 1:
    something = sys.argv[1:]
else:
    something = raw_input("Input: ")

logic.understand(something)

# Old code:
file_type = types.IsLocalFilePath.verbose_check(env, something)

is_numseq = types.IsNumericalSequence(env)
numseq_property = is_numseq.check(something)
is_numseq.describe(numseq_property)

if numseq_property == int:
    oeis = IntegerSequenceEncyclopedia(env)
    sequences = oeis.check(env['intseq'])
    oeis.describe(sequences)

is_numerical = types.IsNumerical(env)
is_numerical.describe(is_numerical.check(something))


