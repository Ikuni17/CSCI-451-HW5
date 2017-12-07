'''
Carsen Ball, Bradley White
Homework #5: Phylogeny Prediction
CSCI 451/551
December 6, 2017
'''

# Interpreter: Python 3.6.3

import numpy as np


def edit_distance(s, t):
    count = 0
    for i in range(len(s)):
        if s[i] == t[i]:
            continue
        else:
            count += 1

    return count


def build_d(sequences):
    d = np.ndarray(shape=(len(sequences), len(sequences[0])))
