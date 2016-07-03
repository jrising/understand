from core.raw_environment import RawEnvironment
from simple import types
from oeis import IntegerSequenceEncyclopedia

def understand(something):
    env = RawEnvironment()

    env.todo(lambda: types.IsLocalFilePath.verbose_check(env, something))
    env.todo(lambda: types.IsNumericalSequence.verbose_check(env, something))
    env.todo(lambda: types.IsNumerical.verbose_check(env, something))

    env.register('intseq', lambda env, xs: env.todo(lambda: IntegerSequenceEncyclopedia.verbose_check(env, xs)))

    while env.todos:
        env.step()

    return env
