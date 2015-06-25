from technique import InteractiveTechnique

from __future__ import division
import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.spatial as spatial

def make_m(T, series,e,tau):
    """creates the shadow manifold M for a series of length T, with embedding dimension e and lag length tau. Series is an array of time series"""
    t = np.random.randint(T,series.shape[0]) # picks a T-length slice at random
    y = series[t-T:t,:]
    numvar = series.shape[1]
    #Create lagged-coordinate vectors
    vecs = np.arange((e-1)*tau,T)
    lagged_vec = np.zeros([e,len(vecs),numvar])
    for var in range(0,numvar):
        for t in range(0,len(vecs)):
            lags = np.where(np.array([i%tau for i in range(0,e*tau)])==0)
            indices = vecs[t]- lags 
            lagged_vec[:,t,var] = y[indices,var]
    return lagged_vec

def predict(series, sh_manifold, var_predict, var_predicted, t, e):
    """Creates a prediction for var_predict at time t, using the shadow manifold derived the time series  var_predicted"""
    kdtree =spatial.KDTree(np.transpose(sh_manifold[:,:,var_predict]))
    dis, ind = kdtree.query(sh_manifold[:,t,var_predict],e+2)
    ind.sort() 
    ind = ind 
    predictive_values = series[ind[1:],var_predicted]
    ui = np.exp(-dis[1:]/dis[1])
    wi = ui/np.sum(ui)
    y_predicted = sum(predictive_values*wi)
    return y_predicted

def get_rho(T,series,var_predict,var_predicted, e, tau):
    """Computes the correlation between the cross-map prediction of var_predicted and its actual value, using a time series of length T."""
    manifold = make_m(T,series,e,tau)
    predicted = []
    true_val = []   
    for t in range(0,manifold.shape[1]):

        predicted.append(predict(series,manifold,var_predict,var_predicted,t, e))
        true_val.append(series[t,var_predicted])

    values =np.ma.compress_cols(np.ma.masked_invalid(np.array([predicted,true_val]))) # deals with any nan values
    cor = np.corrcoef(values)[0,1]
    return cor

def CrossConvergentMappingTechnique(Technique):
    def inputs(self):
        return {'T': I11Unsigned("Length of time series to analyze"),
                'series': TimeSeriesArray(),
                'var_predict': I11Unsigned("Series used to predict"),
                'var_predicted': I11Unsigned("Series to be predicted"),
                'e': I11Unsigned("Embedding dimension"),
                'tau': I11Unsigned("Lag length")}

    def conditions(self):
        def checks(x):
            assert x['T'] < x['XY'].shape[0]
            assert x['var_predict'] < x['XY'].shape[1]
            assert x['var_predicted'] < x['XY'].shape[1]
            assert x['var_predict'] != x['var_predicted']
            assert x['e'] > 1

        return [checks]

    def output(self):
        return I11Probability()
    
    def possible_interprets(self):
        return ['A predicts B', 'A does not predict B']

    def costs(self, x):
        return x['T']

    def apply(self, x):
        return get_rho(x['T'], x['series'], x['var_predict'], x['var_predicted'], x['e'], x['tau'])

    def interpret(self, y):
        TODO
    
    @staticmethod
    def example():
        X = []
        Y = []
        X.append(0.8)
        Y.append(0.8)
        r_x = 3.8
        r_y = 3.5
        beta_xy = 0.05
        beta_yx = 0.1
        Z = np.sin(np.pi * np.linspace(0,300,3001))
        for t in range(0,3000):
            X.append(X[t]*(r_x-r_x*X[t]-beta_xy *Y[t] - .1*Z[t]))
            Y.append(Y[t]*(r_y-r_y*Y[t]-beta_yx *X[t]))
   
        series = np.transpose(np.array([X,Y,Z]))

        rhos02 = []
        tau = 1
        time_lengths = np.arange(200,1000,100)
        for t in time_lengths:
            rhos02.append(get_rho(t,series,0,2,3,tau))

        rhos20 = []
        for t in time_lengths:
            rhos20.append(get_rho(t,series,2,0,3,tau))

        rhos10 = []
        for t in time_lengths:
            rhos10.append(get_rho(t,series,1,0,3,tau))

        rhos01 = []
        for t in time_lengths:
            rhos01.append(get_rho(t,series,0,1,3,tau))

        plt.plot(time_lengths, rhos01, time_lengths, rhos10, time_lengths, rhos20, time_lengths, rhos02)
        plt.legend(['X predicts Y', 'Y predicts X', 'Z predicts X', 'X predicts Z'])
        plt.xlabel('length of series')
        plt.ylabel('rho')
