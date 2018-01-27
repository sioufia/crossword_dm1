#Let's make a matrice with the column as the number of the house and the lines as the attributes

from DM.constraint_programming import constraint_programming

n = 5 #5 houses

N = range(n)

noms = [
    ["norvégien", "anglais", "espagnol", "ukrainien", "japonais"],
    ["bleue", "rouge", "verte", "blanche", "jaune"],
    ["chien", "escargot", "renard", "cheval", "zebre"],
    ["lait", "café", "thé", "vin", "coca"],
    ["kools", "cravens", "old golds", "gitanes", "chesterfields"]
]

var = {x: set(N) for categories in noms for x in categories} # Construct the init matrice

var["norvégien"] = set([0])
var["bleue"] = set([1])
var["lait"] = set([2])

P = constraint_programming(var)
#Relations
EQ= { (i,i) for i in N }
NEQ= { (i,j) for i in N for j in N if i != j}
COTE= { (i,j) for i in N for j in N if abs(i-j) == 1 }
APRES= { (i,j) for i in N for j in N if j-i == 1 }

P.addConstraint("anglais", "rouge", EQ)
P.addConstraint("café", "verte", EQ)
P.addConstraint("jaune", "kools", EQ)
P.addConstraint("verte","blanche", APRES)
P.addConstraint("espagnol", "chien", EQ)
P.addConstraint("ukrainien", "thé", EQ)
P.addConstraint("japonais", "cravens", EQ)
P.addConstraint("old golds", "escargot", EQ)
P.addConstraint("gitanes", "vin", EQ)
P.addConstraint("chesterfields", "renard", COTE)
P.addConstraint("kools", "cheval", COTE)

for categories in noms:
    for x in categories:
        for y in categories:
            if x != y:
                P.addConstraint(x, y, NEQ)

sol = P.solve()

if sol:
    print(sol)
else:
    print("No solution")













