from parsing import *
from sources.constraint_programming import constraint_programming
import string

dico = parseWords("sources/words1.txt")
letter = set(string.ascii_lowercase)
cells = parseVar("sources/crossword1.txt")

var = {x: set(dico) for x in cells if x[1] != x[0]} #If it's a sequence in the grid, the possible values are words from the dictionnaries
var2 = {x: set(letter) for x in cells if x[1] == x[0]} #If it's a cell in the grid, the possible values are a letter 
for elt in var2:
    var[elt] = var2[elt]

#Need to add constraint !


