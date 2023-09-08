# Choisir ici le type d'interface :
from p4_txt import IHM_txt as IHM
#
# from p4_tk import IHM_tk as IHM
#from p4_html import IHM_html as IHM

from grille import Grille
from joueur import Joueur
from colonne import Colonne
from case import Case, Pion


class Puissance4:
    def __init__(self):
        self.grille = Grille()
        self.joueurs = [Joueur('R'), Joueur('J')]
        self.ihm = IHM(self)

        # États du jeu
        self.etat = 0
        self.num_joueur_courant = 0
        
    def lancer_jeu(self):
        """ Lance la boucle principale
        """
        self.ihm.lancer()
            
    def initialiser_partie(self):
        """ Initialise la partie
        """
        self.etat = 0
        self.grille.vider()
        for joueur in self.joueurs:
            joueur.distribuer()

    def demarrer_partie(self):
        self.etat = 1

    def terminer_partie(self):
        self.etat = 2

    def quitter_jeu(self):
        self.etat = 3

    def changer_joueur_courant(self):
        self.num_joueur_courant = 1-self.num_joueur_courant

    def get_joueur_courant(self):
        return self.joueurs[self.num_joueur_courant]

    def get_colonne(self, num):
        return self.grille.get_colonne(num)
    
    def get_joueur_gagnant(self):
        r = self.grille.get_alignement()
        if r is not None:
            self.terminer_partie()
            return self.get_joueur_coul(r[2])
    
    def get_joueur_coul(self, coul):
        if coul == 'R':
            return self.joueurs[0]
        elif coul == 'J':
            return self.joueurs[1]


####################################################################
####################################################################
if __name__ == "__main__":
    p4 = Puissance4()
    p4.lancer_jeu()