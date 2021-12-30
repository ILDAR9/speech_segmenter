# -*- coding: utf-8 -*-

import numpy as np


def pred2logemission(pred, eps=1e-10):
    pred = np.array(pred)
    ret = np.ones((len(pred), 2)) * eps
    ret[pred == 0, 0] = 1 - eps
    ret[pred == 1, 1] = 1 - eps
    return np.log(ret)

def log_trans_exp(exp,cost0=0, cost1=0):
    # transition cost is assumed to be 10**-exp
    cost = -exp * np.log(10)
    ret = np.ones((2,2)) * cost
    ret[0,0]= cost0
    ret[1,1]= cost1
    return ret

def diag_trans_exp(exp, dim):
    cost = -exp * np.log(10)
    ret = np.ones((dim, dim)) * cost
    for i in range(dim):
        ret[i, i] = 0
    return ret
