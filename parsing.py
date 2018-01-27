def parseCrossword(filename):
    grid = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            row = []
            i = 0
            for box in line:
                if box == ".":
                    row.append((i,1))
                elif box == "#":
                    row.append((i,0))
                i += 1
            grid.append(row)
    
    return grid

def parseWords(filename):
    L = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            L.append(line.replace("\n",""))
    return L


