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


class Node():
    def __init__(self, sequence=None):
        self.left = None
        self.right = None
        self.parent = None
        self.seq = sequence


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


def min_pairs(sequences, d):
    indices = {x: 0 for x in range(len(sequences))}
    minimumD = math.inf
    minIndex = (0, 0)
    count = 1

    for row in range(len(d)):

        if indices.get(row) == 0:
            for col in range(count, len(d)):
                print(row, col)
                if indices.get(col) == 0:
                    if d[row][col] < minimumD:
                        minimumD = d[row][col]
                        minIndex = (row, col)
                else:
                    col += 1
            count += 1
            print(minIndex)
            indices[row] = minIndex
            indices[minIndex[1]] = minIndex
            print(indices)
            minimumD = math.inf
            minIndex = (0, 0)
        else:
            row += 1
            count = row + 1
    # dictionary of inital leaf pairs
    return indices


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


def leaf_subs(min):
    nodes = []
    for i in min:
        strings = min.get(i)
        if strings == None:
            continue
        print(min.get(i))
        temp1 = Node(strings[0])
        temp2 = Node(strings[1])
        temp3 = Node(temp1.seq)
        temp3.left = temp1
        temp3.right = temp2
        min[strings[0]] = None
        min[strings[1]] = None
        nodes.append(temp3)
    return (nodes)


def build_tree(to_merge, d):
    min_dist = math.inf
    min_indices = None
    while len(to_merge) > 1:
        print("Subtrees left:{0}".format(len(to_merge)))
        for k in range(len(to_merge)):
            i = k + 1
            for i in range(len(to_merge)):
                dist = d[to_merge[k].seq][to_merge[i].seq]
                if dist < min_dist:
                    min_dist = dist
                    min_indices = (k, i)
        new_parent = Node(to_merge[min_indices[0]].seq)
        new_parent.left = to_merge[min_indices[0]]
        new_parent.right = to_merge[min_indices[1]]
        to_merge.append(new_parent)
        if min_indices[0] > min_indices[1]:
            del to_merge[min_indices[0]]
            del to_merge[min_indices[1]]
        else:
            del to_merge[min_indices[1]]
            del to_merge[min_indices[0]]
        min_dist = math.inf
        min_indices = None
    return (to_merge[0])


def traverse(root):
    current_level = [root]
    while current_level:
        print(' '.join(str(node.seq) for node in current_level))
        next_level = list()
        for n in current_level:
            if n.left:
                next_level.append(n.left)
            if n.right:
                next_level.append(n.right)
            current_level = next_level

def main():
    sequences = read_sequences()
    d = build_d(sequences)
    print(d)
    min = min_pairs(sequences, d)
    # Parent nodes of the leaf sequences
    first_internals = leaf_subs(min)
    root = build_tree(first_internals, d)
    traverse(root)


if __name__ == '__main__':
    main()
