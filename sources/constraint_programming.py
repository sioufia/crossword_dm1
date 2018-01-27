#!/usr/bin/env python3

# 2018 - Ecole Centrale Supélec - c. dürr

import sys

class constraint_programming:
    """Implémente un solveur de programmation par contraintes
    """

    def __init__(self, var):
        """Crée un problème de satisfaction par contraintes.
        :param var: dictionnaire associant à des noms de variables leur domaine (ensemble de valeurs)
        """
        self.var = var
        self.conflict = {x:[] for x in self.var}    # associe à x, une liste de couples (y, rel), pour chaque contrainte binaire
        self.assigned = {x:None for x in self.var}  # code une solution partielle
        self.context = []                           # mémorise les restrictions de domaines de la forme (x, vals_à_enlever_du_domaine)
        self.nodes = 0                              # nombre de noeuds parcouru lors de la résolution
        self.print_tree = False
        self.maintain_AC = False
        # sanity check
        for x in self.var:
            for y in self.var:
                if x != y and self.var[x] is self.var[y]:
                    print("ERROR: variables %s and %s have the same domain object." % (x, y))
                    return
        sys.setrecursionlimit(max(sys.getrecursionlimit(), len(self.var) + 10))


    def addConstraint(self, x, y, relation):
        """Ajoute une contrainte binaire sur le couple de variables x et y.
        :param x, y: noms de variables
        :param relation: ensemble de couples de valeurs u,v tel que
        l'affectation x := u, y := u satisfait la contrainte.
        (par abus de notation x est la variable *et* son nom).
        """
        self.conflict[x].append((y, relation))
        self.conflict[y].append((x, {(v, u) for (u, v) in relation}))

    def maintain_arc_consistency(self):
        self.maintain_AC = True

    def solve(self, father=None):
        """Tente de compléter la solution partielle courante.
        En cas de succès retourne un dictionnaire nom variable -> valeur,
        et en cas d'échec retourne None.

        nodes contiendra à tout moment le nombre de nœuds de l'arbre d'exploration.
        print_tree indique si solve() doit afficher une ligne par nœud de l'arbre.
        maintain_AC indique si solve() doit maintenir l'arc consistance.
        """
        self.nodes += 1
        x = self.selectVar()
        if x is None:                  # toutes les variables sont affectées
            return self.assigned       # on a trouvé une solution
        else:
            for u in self.var[x]:      # essayer toutes les affectations x := u pour u du domaine de x.
                self.assigned[x] = u
                if self.print_tree:
                    depth = len([z for z in self.var if self.assigned[z] is not None])
                    print("%s %s := %s" % ("  " * depth, x, u))
                history = self.save_context()
                Q = self.forward_check(x)    # maintenir consistance locale
                if self.maintain_AC:         # établir la maintenance de l'arc constance si nécessaire
                    self.arc_consistency(Q)
                sol = self.solve()           # appel récursif
                if sol:                      # succès ?
                    return sol
                self.restore_context(history)
                self.assigned[x] = None      # remettre en état
            return None                      # annoncer échec

    # --- gestion de contexte

    def save_context(self):
        return len(self.context)

    def restore_context(self, history):
        while len(self.context) > history:
            x, vals = self.context.pop()
            self.var[x] |= vals

    def remove_vals(self, x, vals):
        self.context.append((x, vals))
        self.var[x] -= vals

    # --- exploration

    def selectVar(self):
        """choisit une variable de branchement.
        Heuristique: choisir la variable au domaine minimal

        :returns: un indice de variable ou Npne, si toutes les variables sont affectées
        """
        choice = None
        for x in self.var:
            if self.assigned[x] is None and  \
               (choice is None or len(self.var[x]) < len(self.var[choice])):
               choice = x
        return choice

    def forward_check(self, x):
        """Effectue la vérification en avant après une affectation à x
        :returns: l'ensemble des variables qui ont vu leur domaine diminuer
        """
        u = self.assigned[x]
        Q = set()
        for y, rel in self.conflict[x]:
            to_remove = set()
            for v in self.var[y]:
                if (u, v) not in rel:
                    to_remove.add(v)
            if to_remove:
                self.remove_vals(y, to_remove)
                Q.add(y)
        return Q

    # --- arc consistance

    def arc_consistency(self, Q):
        """Le domaine des variables dans Q a été réduit.
        Maintenir l'arc consistance.
        Implémente l'algorithme AC3.
        """
        while Q:
            x = Q.pop()
            for y, relation in self.conflict[x]:
                if self.assigned[y] is None:
                    if self.revise(x, y, relation):
                        Q.add(y)


    def revise(self, x, y, relation):
        """le domaine de x vient d'être réduit.
        Vérifier si celui de y doit être réduit à son tour.
        :returns: True si le domaine de y a été réduit
        """
        to_remove = set()
        for v in self.var[y]:
            if not self.hasSupport(y, v, x, relation):
                to_remove.add(v)
        self.remove_vals(y, to_remove)
        return to_remove

    def hasSupport(self, y, v, x, relation):
        """est-ce que l'affectation y := v a un support dans le domaine de x ?
        """
        for u in self.var[x]:
            if (u, v) in relation:
                    return True
        return False

