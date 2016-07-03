import numpy as np
import pandas as pd
import statsmodels.api as sm

def OLSTechnique(RawTechnique):
    def inputs(self):
        return {'y': type(np.array([])), \
                'X': type(pd.DataFrame())}

    def conditions(self):
        def check_conforms(self, y, X):
            assert len(x) == len(X)

        return [check_conforms]

    def output(self):
        return type(np.array([]))

    #def costs(self, x):
    #    return []

    def apply(self, y, X):
        X = sm.add_constant(X)
        model = sm.OLS(y, X)
        results = model.fit()
        return results.params
