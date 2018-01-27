def parseCrossword(filename):
    """Parse the crossword into a matrix (list of the rows)"""
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
    """Parse the words into a list"""
    L = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            L.append(line.replace("\n",""))
    return L

def parseVar(filename):
    """It returns variables adapted for the model"""
    grid = parseCrossword(filename)
    var = [] #variables : tuples ((x,y),(x',y')) ;(x,y)=(x',y') if it's a cell
    n = len(grid)
    m = len(grid[0])
    buffer_line = []
    buffer_column = []
    for i in range(n):
        for j in range(m):
            if grid[i][j][1] == 1:
                var.append(((i,j),(i,j)))
                if not buffer_column:
                    buffer_column = ((i,j), 0)
                elif (i,j) == (buffer_column[0][0], buffer_column[0][1] + 1):
                    buffer_column = ((i,j), buffer_column[1] + 1)

            elif buffer_column and buffer_column[1] > 0:
                var.append(((buffer_column[0][0], buffer_column[0][1] - buffer_column[1]),(buffer_column[0][0],buffer_column[0][1])))
                buffer_column = ()

            else:
                buffer_column = ()
            
    
    for j in range(m):
        for i in range(n):
            if grid[i][j][1] == 1:            
                if not buffer_line:
                    buffer_line = ((i,j), 0)
                elif (i,j) == (buffer_line[0][0] + 1, buffer_line[0][1]):
                    buffer_line = ((i,j), buffer_line[1] + 1)

            elif buffer_line and buffer_line[1] > 0:
                var.append(((buffer_line[0][0] - buffer_line[1],buffer_line[0][1]),(buffer_line[0][0],buffer_line[0][1])))
                buffer_line = ()
            
            else:
                buffer_line = ()
            
    return var




