from parsing import *
from sources.constraint_programming import constraint_programming
import string



def getListOfCellsInASequence(coord):
    L = []
    if coord[0][0] == coord[1][0]: #For a row
        a = coord[1][1] - coord[0][1] #get the size of the sequence
        for i in range(a + 1):
            L.append((coord[0][0],coord[0][1] + i))
    if coord[0][1] == coord[1][1]: #For a column
        a = coord[1][0] - coord[0][0]
        for i in range(a + 1):
            L.append((coord[0][0] + i, coord[0][1]))
    
    return L

def getCoordInterSequence(var1, var2):
    """Get the coordonates of the intersection between 2 sequences.
        Return format x1, x2 : x1 is the distance between the first letter of var1 (same for x2 )
        """
    L1 = getListOfCellsInASequence(var1)
    L2 = getListOfCellsInASequence(var2)
    a = ()
    for elt in L1:
        if elt in L2:
            a = elt
            break
    
    if a!= ():
        x1 = 0
        x2 = 0
        if L1[0][0] == a[0]:
            x1 = a[1] - L1[0][1]
        elif L1[0][0] != a[0]:
            x1 = a[0] - L1[0][0]
        if L2[0][0] == a[0]:
            x2 = a[1] - L2[0][1]
        elif L2[0][0] != a[0]:
            x2 = a[0] - L2[0][0]
            
        return x1,x2
    
    else:
        return False

def getTypeVariables(var):
    #Check if the variable is a term or a sequence
    if var[0] == var[1]:
        return "term"
    else:
        return "sequence"

def getCorrectWordLenght(x,words):
    L = []
    l = lenSequence(x)
    for w in words:
        if len(w) == l:
            L.append(w)
    return L

def lenSequence(x):
    if x[0][0] == x[1][0]:
        l = x[1][1] - x[0][1] + 1
    else:
        l = x[1][0] - x[0][0] + 1
    return l


if __name__ == "__main__":
    dico, letters = parseWords("sources/words2.txt")
    cells = parseVar("sources/crossword2.txt")

    #Add a filter with the size of the sequence
    var = {x: set(getCorrectWordLenght(x,dico)) for x in cells if x[1] != x[0]} #If it's a sequence in the grid, the possible values are words from the dictionnaries
    var2 = {x: set(letters) for x in cells if x[1] == x[0]} #If it's a cell in the grid, the possible values are a letter 
    for elt in var2:
        var[elt] = var2[elt]

    #Need to add constraint !

    #1- Intersection de 2 séquences : même lettre
    #2- Une case = une lettre
    #3- Une séquence = un mot
    #4- Une séquence -> Une succession de lettres 

    P = constraint_programming(var)


    R1 = { (i,j) for i in dico for j in dico }
    R2 = { (i,j) for i in letters for j in letters if i!=j }
    #R3 = { (i,j) for i in dico for j in letter if i[getIndexTermFromSequence(i,j)] == j}
    
    #Intersection between a row and a column is the same term
    def functR4(xi,xj):
        R4= { (i,j) for i in dico for j in dico if i[xi]==j[xj] }
        print(R4)
        return R4

    for a in var:
        if getTypeVariables(a) == "sequence":
            for b in var:
                if getTypeVariables(b) == "sequence" and a!=b:
                    if getCoordInterSequence(a,b) == False:
                        P.addConstraint(a,b,R1)
                    elif getCoordInterSequence(a,b) != False:
                        xa,xb = getCoordInterSequence(a,b)
                        P.addConstraint(a,b,functR4(xa,xb))
                    
                        




    """for a in var:
        for b in var:
            if getTypeVariables(a) != getTypeVariables(b):
                if getTypeVariables == "sequence":
                    P.addConstraint(a,b,R3)
                else:
                    P.addConstraint(b,a,R3)
            else:
                if getTypeVariables(a) == "sequence" and a!=b:
                    if getCoordOfIntersectionSequence(a,b) == False:
                        P.addConstraint(a,b,R1)
                    if getCoordOfIntersectionSequence(a,b) != False:
                        P.addConstraint(a,b,R4)
                if getTypeVariables(a) == "term" and a!=b:
                    P.addConstraint(a,b,R2)
"""
    sol = P.solve()

    if sol:
        print(sol)
    else:
        print("No solution")  
                    





