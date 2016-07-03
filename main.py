import sys
from core.raw_environment import RawEnvironment
from simple import types
from oeis import IntegerSequenceEncyclopedia

print "Let's understand something!"

if len(sys.argv) > 1:
    something = sys.argv[1:]
else:
    something = raw_input("Input: ")

env = RawEnvironment()

env.todo(lambda: types.IsLocalFilePath.verbose_check(env, something))
env.todo(lambda: types.IsNumericalSequence.verbose_check(env, something))
env.todo(lambda: types.IsNumerical.verbose_check(env, something))

env.register('intseq', lambda env, xs: env.todo(lambda: IntegerSequenceEncyclopedia.verbose_check(env, xs)))

while True:
    env.step()

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


