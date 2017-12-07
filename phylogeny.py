'''
Carsen Ball, Bradley White
Homework #5: Phylogeny Prediction
CSCI 451/551
December 6, 2017
'''

# Interpreter: Python 3.6.3
import sys
def main():
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

main()