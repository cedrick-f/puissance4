from case import Pion

####################################################################
class Joueur:
    def __init__(self, couleur):
        self.couleur = couleur
        self.pions = []
        self.distribuer()

    def placer_pion(self, colonne):
        if self.nbr_pions_restants() == 0:
            return False
        return colonne.placer_pion(self.pions.pop())

    def nbr_pions_restants(self):
        return len(self.pions)
    
    def distribuer(self):
        self.pions = [Pion(self.couleur) for _ in range(21)]

    def get_coul(self):
        return self.couleur


####################################################################
####################################################################
if __name__ == "__main__":
    pass