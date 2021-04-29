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

