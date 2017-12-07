'''
Carsen Ball, Bradley White
Homework #5: Phylogeny Prediction
CSCI 451/551
December 6, 2017
'''

# Interpreter: Python 3.6.3

import numpy as np
import sys
import math


def edit_distance(s, t):
    count = 0
    for i in range(len(s)):
        if s[i] == t[i]:
            continue
        else:
            count += 1

    return count


def build_d(sequences):
    d = np.ndarray(shape=(len(sequences), len(sequences)))
    for i in range(len(d)):
        j = i
        d[i][j] = 0
        j += 1
        for j in range(len(d)):
            d[i][j] = edit_distance(sequences[i], sequences[j])
    return d

def build_tree(sequences, d):
    indices = {x: 0 for x in range(len(sequences))}
    minimumD = math.inf
    minIndex = (0,0)
    count = 1

    for row in range(len(d)):

        if indices.get(row) == 0:
            for col in range(count, len(d)):
                print(row, col)
                if indices.get(col) == 0:
                    if d[row][col] < minimumD:
                        minimumD = d[row][col]
                        minIndex = (row,col)
                else:
                    col += 1
            count+= 1
            print(minIndex)
            indices[row] = minIndex
            indices[minIndex[1]] = minIndex
            print(indices)
            minimumD = math.inf
            minIndex = (0,0)
        else:
            row += 1
            count = row + 1
    print(indices)


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
    build_tree(sequences, d)

main()
