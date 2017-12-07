'''
Carsen Ball, Bradley White
Homework #5: Phylogeny Prediction
CSCI 451/551
December 6, 2017
'''

# Interpreter: Python 3.6.3

import numpy as np
import sys


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
    for i in range(len(d)):
        j = i
        d[i][j] = 0
        j += 1
        for j in range(len(d)):
            d[i][j] = edit_distance(sequences[i], sequences[j])

    return d


def read_sequences():
    file = 'sequences.txt'
    sequences = []
    with open(file, 'r') as seq:
        length = 0
        checkLen = 0
        for line in seq:
            line = line.strip()
            length = len(line)
            print(length)
            if checkLen == 0:
                checkLen = length
            elif length != checkLen:
                print('Sequences are not of same length, end program')
                sys.exit()
            line = list(line)
            sequences.append(line)
    for i in sequences:
        print(i)

    return sequences


def main():
    sequences = read_sequences()
    d = build_d(sequences)
    print(d)

main()
