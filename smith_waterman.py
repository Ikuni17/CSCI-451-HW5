'''
Carsen Ball, Bradley White
Homework #5: Phylogeny Prediction
CSCI 451/551
December 6, 2017
'''

# Interpreter: Python 3.6.3

# Global variables
# Directions: 1 is diagonal, 2 is left, 3 is up
# @param global_max: the score and index for the current highest scoring sub string
# @param score_array: 3D array which has a score and the direction from which thatscore was calculated in the final list
# @param x_list: the input strings converted to lists so the letters can indexed easier
from random import choice

global_max = [0, (0, 0)]
score_array = [[[]]]
s_list = []
t_list = []


# Calculate the max score for a given index based on its coordinate (i, j)
def calc_v(i, j):
    global global_max
    global score_array
    global s_list
    global t_list

    # @param local_max: the maximum score for the current index
    # @param local_max_dir: the direction which local_max was computed from
    # @param have_match: Boolean determining if the letters at the i and j indices are the same letter
    # @param coord_list: the coordinates for each index which can compute the current index
    local_max = 0
    local_max_dir = None
    have_match = False
    coord_list = [(i - 1, j - 1), (i, j - 1), (i - 1, j)]

    # Determine if we have matching letters
    if s_list[i] == t_list[j]:
        have_match = True

    # Iterate through all coordinates
    for k in range(len(coord_list)):
        # If we have a match score it based on the diagonal coordinate
        if have_match is True and k == 0:
            score = score_array[coord_list[k][0]][coord_list[k][1]][0] + 2
        # Otherwise compute the score based on which coordinate we're using
        else:
            score = score_array[coord_list[k][0]][coord_list[k][1]][0] - 1

        # Check if we have a new local max from this coordinate
        if score > local_max:
            local_max = score
            local_max_dir = k + 1

    # Update the score and direction for this index
    score_array[i][j][0] = local_max
    score_array[i][j][1] = local_max_dir

    # Check if we have a new global max, if so record the score and index
    if local_max >= global_max[0]:
        global_max[0] = local_max
        global_max[1] = (i, j)


# Returns the correct alignment
def create_alignment(s, t):
    # The finalized local alingment
    alignment_s = ''
    alignment_t = ''
    # Stacks to hold the characters for the alignment
    s_prime = []
    t_prime = []
    # Initialized the local score to the max score
    score = global_max[0]
    # The starting position that coresponds to the maximum alingment score
    i = global_max[1][0]
    j = global_max[1][1]
    # Will continue until it reaches a score of 0, indicating that the local allingment has been done
    while (score != 0):
        direction = score_array[i][j][1]
        # Diagnoal direction, copying the char at the current index into the alignment
        if direction == 1:
            s_prime.append(s[i])
            t_prime.append(t[j])
            # Moves the local position "diagonaly"
            i = i - 1
            j = j - 1
        # Direction to the left, add a space into the S string alingment
        # Copy the current char in T, to the t aligments
        elif direction == 2:
            s_prime.append("_")
            t_prime.append(t[j])
            # i'th index does not change, move "left" for the jth index
            j = j - 1
        # Direction is up, add a space into the T alingment
        # Copy the char at the curent index in S into the s aligment
        else:
            t_prime.append("_")
            s_prime.append(s[i])
            # j'th index does not change, move "up" for the ith index
            i = i - 1
        score = score_array[i][j][0]
    # Creates the alignment from the stack
    for x in range(len(s_prime)):
        alignment_s += s_prime.pop()
    for y in range(len(t_prime)):
        alignment_t += t_prime.pop()
    # Prints the alignment
    print("\t" + alignment_s)
    print("\t" + alignment_t)


def main():
    global global_max
    global score_array
    global s_list
    global t_list

    # Input strings, examples used in the book
    #s = "acaatcg"
    #t = "ctcatgc"
    # Randomly generated strings
    length = 12
    s = ''.join(choice('actg') for i in range(length))
    t = ''.join(choice('actg') for i in range(length))

    # Convert the strings to list for easier indexing
    s_list = list(s)
    t_list = list(t)

    # Insert a "blank" before the string
    s_list.insert(0, '_')
    t_list.insert(0, '_')

    # Initial all indices with a score of zero and no direction
    score_array = [[[0, None] for i in range(len(t_list))] for j in range(len(s_list))]

    for i in range(1, len(score_array)):
        for j in range(1, len(score_array[i])):
            calc_v(i, j)

    print("Input Strings:\ns = {0}\nt = {1}\n".format(s,t))
    print_scores()
    print("\n\nAlignment score: {0}".format(global_max[0]))
    print("Alignment of strings:")
    create_alignment(s_list, t_list)


# Prints the scores in a matrix for easier viewing
def print_scores():
    global score_array

    print("Matrix produced:")
    for i in range(len(score_array)):
        if i != 0:
            print()
        for j in range(len(score_array[i])):
            print(score_array[i][j][0], end=" ")


# Start
main()
