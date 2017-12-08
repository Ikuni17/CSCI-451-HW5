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


# Clas to handle a node within the phylogeny tree. Seq is the index within the sequence array
class Node():
    def __init__(self, sequence=None):
        self.left = None
        self.right = None
        self.seq = sequence


# Finds the edit distance between two sequences
def edit_distance(s, t):
    count = 0
    for i in range(len(s)):
        if s[i] == t[i]:
            continue
        else:
            count += 1
    return count


# Create the distance matrix for all pairwise sequences
def build_d(sequences):
    d = np.ndarray(shape=(len(sequences), len(sequences)))
    for i in range(len(d)):
        j = i
        d[i][j] = 0
        j += 1
        # Find the edit distance between the ith sequence and all other sequence and populate the distance matrix
        for j in range(len(d)):
            d[i][j] = edit_distance(sequences[i], sequences[j])
    return d


# Creates the leaf pairs which make up the bottom of the tree based on the minimum distance between two sequences
# which haven't been put within a pair yet
def min_pairs(sequences, d):
    # Keep track of which sequence is paired with another. If no pair yet, the value is 0
    indices = {x: 0 for x in range(len(sequences))}
    # Keep track of the minimum distance and the corresponding indices
    minimumD = math.inf
    minIndex = (0, 0)
    count = 1

    # Iterate through all sequences
    for row in range(len(d)):
        # Check if this index has a pair already
        if indices.get(row) == 0:
            # Iterate through all available sequences
            for col in range(count, len(d)):
                if indices.get(col) == 0:
                    # Keep track of the minimum distance for this sequence
                    if d[row][col] < minimumD:
                        minimumD = d[row][col]
                        minIndex = (row, col)
            count += 1
            # Put the pair in the dictionary so they cannot be selected for others
            indices[row] = minIndex
            indices[minIndex[1]] = minIndex
            # Reset the minimum for the next pair to be found
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
            # print(length)
            if checkLen == 0:
                checkLen = length
            elif length != checkLen:
                print('Sequences are not of same length, end program')
                sys.exit()
            line = list(line)
            sequences.append(line)
    # for i in sequences:
    #    print(i)

    return sequences


def leaf_subs(min):
    nodes = []
    for i in min:
        strings = min.get(i)
        if strings == None:
            continue
        # print(min.get(i))
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
        for k in range(len(to_merge)):
            for i in range(k + 1, len(to_merge)):
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


def traverse(root, seq):
    current_level = [root]
    while current_level:
        print(' '.join(str(seq[node.seq]) for node in current_level))
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
    min = min_pairs(sequences, d)
    # Parent nodes of the leaf sequences
    first_internals = leaf_subs(min)
    root = build_tree(first_internals, d)
    for i in range(len(sequences)):
        sequences[i] = ''.join(x for x in sequences[i])
    traverse(root, sequences)



if __name__ == '__main__':
    main()
