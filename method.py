from scipy import stats
import pandas as pd
import random
from math import sqrt, floor


def random_sample(frame : pd,samples_total = 300, sample_size = 30,var = False):
    sample_stats = []
    for a_sample in range(samples_total):
        # pick random elts of sample_size and add to samples list
        samples = []
        for elt in range(sample_size):
            samples.append(frame.iloc[floor(frame.shape[0]*(random.random()))])

        if var:
            sample_stats.append(stats.tvar(samples))
        else:
            sample_stats.append(stats.tmean(samples))
    return sample_stats

def t_interval(list, alf = .95):
    return stats.t.interval(alf,len(list)-1, loc = stats.tmean(list) )

def chi_2(list, alf = .95):
    upper = ((len(list)-1)*stats.tvar(list)) / (stats.chi2.ppf(alf/2, len(list)-1))
    lower = ((len(list)-1)*stats.tvar(list)) / (stats.chi2.ppf(1 - (alf/2), len(list)-1))

    return (lower,upper)