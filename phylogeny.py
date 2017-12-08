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
                # print(row, col)
                if indices.get(col) == 0:
                    if d[row][col] < minimumD:
                        minimumD = d[row][col]
                        minIndex = (row, col)
                else:
                    col += 1
            count += 1
            # print(minIndex)
            indices[row] = minIndex
            indices[minIndex[1]] = minIndex
            # print(indices)
            minimumD = math.inf
            minIndex = (0, 0)
        else:
            row += 1
            count = row + 1
    # dictionary of inital leaf pairs
    return indices

#Reads a file names seqeunces.txt, each line becomes an array representing the sequences
#If the sequences in the text file are not the same length, the program ends
#returns a double array holding the sequences
def read_sequences():
    file = 'sequences.txt'
    sequences = []
    with open(file, 'r') as seq:
        checkLen = 0
        for line in seq:
            line = line.strip()
            length = len(line)
            if checkLen == 0:
                checkLen = length
            elif length != checkLen:
                print('Sequences are not of same length, end program')
                sys.exit()
            line = list(line)
            sequences.append(line)
    return sequences

#Accepts a dictionary of pairs of seqeunces that represents the closest sequences to be merges to make a parent node
#That is the first internal node from the leaf nodes
#Returns a list of each parent node to the leaf nodes
def leaf_subs(min):
    #holds the parent nodes
    nodes = []
    for i in min:
        #A tuple of the indices that are seqeunces in the sequences array
        strings = min.get(i)
        #If the two sequences have already been merged, skip them
        if strings == None:
            continue
        #Makes two children with the two sequences that have been selected to merge
        temp1 = Node(strings[0])
        temp2 = Node(strings[1])
        #Makes a parent node
        temp3 = Node(temp1.seq)
        temp3.left = temp1
        temp3.right = temp2
        min[strings[0]] = None
        min[strings[1]] = None
        #Adds parent node to the list to be returned
        nodes.append(temp3)
    #Returns the list of the parent nodes
    return (nodes)

#Accepts a list of parent nodes that are the result of merging each leaf node
#Builds a tree bottom up, and then selects the value to be held by each internal node that is the sequence with the
#minimum average edit distance to its children
#Returns the root node
def build_tree(to_merge, d):
    #initial min distance is infinity
    min_dist = math.inf
    min_indices = None
    #To merge is appended too, with parents of two internal nodes that have merged
    #When the length is one, all the internal nodes have merged together to make the root node
    while len(to_merge) > 1:
        #Calculates the pair of nodes in to_merge with the smallest edit distance between their sequence values
        #The pair to be merged is represented by a tuple, holding the indeces of the selected nodes in to_merge
        for k in range(len(to_merge)):
            for i in range(k + 1, len(to_merge)):
                dist = d[to_merge[k].seq][to_merge[i].seq]
                if dist < min_dist:
                    min_dist = dist
                    min_indices = (k, i)
        #Parent of the merged internal nodes
        new_parent = Node(to_merge[min_indices[0]].seq)
        #Sets the children of the new parent node
        new_parent.left = to_merge[min_indices[0]]
        new_parent.right = to_merge[min_indices[1]]
        #adds parent node to the list
        to_merge.append(new_parent)
        #Removes the two children nodes from to_merge
        if min_indices[0] > min_indices[1]:
            del to_merge[min_indices[0]]
            del to_merge[min_indices[1]]
        else:
            del to_merge[min_indices[1]]
            del to_merge[min_indices[0]]
        #Resests the minimum distance and the indices of ther nodes to merge to initial values
        min_dist = math.inf
        min_indices = None
    #Returns the only node left in to_merge, the root
    return (to_merge[0])

#Traverses the tree after it has been build, prints the seqeunce at each node, starting with the root
def traverse(root, seq):
    current_level = [root]
    print('Resulting Phylogeny Tree By Layer')
    while current_level:
        print(' '.join(str(seq[node.seq]) for node in current_level))
        next_level = list()
        for n in current_level:
            if n.left:
                next_level.append(n.left)
            if n.right:
                next_level.append(n.right)
            current_level = next_level

#A program that builds a phylogeny tree from a file of sequences, names 'sequences.txt'
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
