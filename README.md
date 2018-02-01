This project is related to the course of Optimisation at EcoleCentraleSupélec.
It enables to fill a crossword under a specific format and with a related
vocabulary.

## Steps to run the program
1/ Run the model python file
2/ Enter the path of the crossword file
3/ Enter the path of the dico file
4/ Choose to use arc consistency of not

## Our work
All the functions are documented in the source code.


### Variables
- the cells of the crossword that we need to fill, with their coordinates. The domain is the letters in the dictionnary
- the horizontal and vertical sequences of cells that we need to fill, coded
with the coordinates of the first and the last cell of a sequence. The domain is
the list of words that match the length of the sequence for each sequence.

### Constraints
For each sequence, we add a constraint to each cell of a sequence.
The constraint is between the sequence and each cell of that sequence, and we
enforce that a word can be included in the beginning of that sequence (ie for
each subsequence, we can put a word in). This ensures that a cell can contains
only one letter, that the words fit in the crossword and that the words will be
valid ones.

## Main Steps
1/ We parse the crossword file to get the grid, and the convert the grid into the list of variables. This is detailed in parsing.py
2/ We parse the dictionnary file to get the letters domain ant words domain
3/ We declare the varialbes and add the constraints to the constraint
programming problem

## Results
We tried with arc consistency method and without. Here are our results :
- without arc consistency : exec time for crossword2 is around 21 sec on one
computer
- with arc consistency : exec time for crossword2 is around 27 sec on one
computer
=> Ici l'arc consistance n'améliore pas le temps d'éxecution.
