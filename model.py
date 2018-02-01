from parsing import *
from sources.constraint_programming import constraint_programming
import time


def getListOfCellsInASequence(sequence):
    """Take a sequence and returns its cells under the format of variable"""
    L = []
    if sequence[0][0] == sequence[1][0]: #For a row
        a = sequence[1][1] - sequence[0][1] #get the size of the sequence
        for i in range(a + 1):
            L.append(((sequence[0][0],sequence[0][1] + i),(sequence[0][0],sequence[0][1] + i)))
    if sequence[0][1] == sequence[1][1]: #For a column
        a = sequence[1][0] - sequence[0][0] #get the size of the sequence
        for i in range(a + 1):
            L.append(((sequence[0][0] + i, sequence[0][1]),(sequence[0][0] + i, sequence[0][1])))
    return L


def getTypeVariables(var):
    """Check if the variable is a letter or a sequence."""
    if var[0] == var[1]:
        return "letter"
    else:
        return "sequence"


def getCorrectWordLenght(x,words):
    """It takes the lenght of a sequence and a list of words.
       It returns the list of the words with the same length of the sequence."""
    L = []
    l = lenSequence(x)
    for w in words:
        if len(w) == l:
            L.append(w)
    return L


def lenSequence(x):
    """Get a variable and calculate its length"""
    if x[0][0] == x[1][0]: #If it's a row
        l = x[1][1] - x[0][1] + 1
    else:
        l = x[1][0] - x[0][0] + 1 #It it's a column
    return l


def functR3(dico, letters, xj):
    """A sequence is the concatenation of its letters.
       i is a sequence ; j is a letter in the sequence j at the index xj
       dico is the dictionnary of words
       letters are the letters in the dico"""
    #i is a sequence
    #j is a letter in the sequence j at the index xj
    new_dico = []
    for elt in dico:
        if len(elt) > xj: #We enable the sequence from the dico with a sufficient length
            new_dico.append(elt)

    R3 = { (i,j) for i in new_dico for j in letters if i[xj]==j}
    return R3


def main(crossword_file, crossword_dico, maintain_arc_consistency):
    start_time = time.time()
    dico, letters = parseWords(crossword_dico)
    cells = parseVar(crossword_file)

    var = {}
    var1 = {x: set(getCorrectWordLenght(x,dico)) for x in cells if x[1] != x[0]}#It's a sequence in the grid, the possible values are words from the dictionnaries with the same length of the sequence.
    var2 = {x: set(letters) for x in cells if x[1] == x[0]} #It's a cell in the grid, the possible values are a letter
    for elt in var1:
        var[elt] = var1[elt]
    for elt in var2:
        var[elt] = var2[elt]

    P = constraint_programming(var)

    for a in var:
        if getTypeVariables(a) == "sequence":
            i=0
            for var_letter in getListOfCellsInASequence(a):
                P.addConstraint(a, var_letter, functR3(dico, letters, i))
                i += 1 #the position of the letter within the sequence

    if maintain_arc_consistency == "y":
        print("Using arc consistency")
        P.maintain_arc_consistency()
    sol = P.solve()

    if sol:
        print(sol)
        print("Time of resolution : {} seconds".format(time.time() - start_time))
    else:
        print("No solution")

if __name__ == "__main__":
    crossword_file = input("Path of the crossword file: ")
    crossword_dico = input("Path of the crossword dico: ")
    maintain_arc_consistency = input("Arc Consistency (y/N) : ")
    main(crossword_file, crossword_dico, maintain_arc_consistency)
