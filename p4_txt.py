import time
import keyboard
import re
from colorama import Fore, Back, Style

###################################################################################
class IHM_txt:
    """ Box-drawing characters : https://en.wikipedia.org/wiki/Box-drawing_character
    """
    def __init__(self, jeu):
        self.jeu = jeu
        self.pos_pion = 0 # position du pion en attente d'être placé
        self.g = GestionnaireEvenements(self)

        self.modif = True # True si un rafraichissement de l'affichage est nécessaire
        self.message = ''

    def afficher(self):
        if self.modif:
            print('\n'.join(self.draw_jeu()))
            self.modif = False

    def lancer(self):
        """ Lance la boucle principale 
            qui change es états du jeu
        """
        while not self.jeu.etat == 3:   # jeu_termine
            if self.jeu.etat == 0:      # attente
                self.set_message('⏎ pour démarrer')
            self.afficher()
            time.sleep(.1)

    def action_clavier(self, event):
        if event == 'enter':
            if self.jeu.etat == 0:
                self.jeu.demarrer_partie()
                self.set_message('Joueur '+self.draw_joueur(self.jeu.get_joueur_courant()))
            elif self.jeu.etat == 2:
                self.jeu.initialiser_partie()
                self.set_message('⏎ pour démarrer')

        elif event == 'gauche':
            if self.jeu.etat == 1 and self.pos_pion > 0:
                self.pos_pion -= 1
                self.modif = True

        elif event == 'droite':
            if self.jeu.etat == 1 and self.pos_pion < 6:
                self.pos_pion += 1
                self.modif = True

        elif event == 'bas':
            if self.jeu.etat == 1 and self.jeu.get_joueur_courant().placer_pion(self.jeu.get_colonne(self.pos_pion)):
                self.pos_pion = 0
                self.modif = True
                j = self.jeu.get_joueur_gagnant()
                if j is not None:
                    self.set_message('Joueur '+self.draw_joueur(j)+' gagne !')
                    return
                self.jeu.changer_joueur_courant()
                self.set_message('Joueur '+self.draw_joueur(self.jeu.get_joueur_courant()))
    
        elif event == 'esc':
            self.jeu.quitter_jeu()

    def set_message(self, message):
        if message != self.message:
            self.message = message
            self.modif = True
        
    def draw_pion(self, case):
        """ Renvoie le motif correspondant à un pion '●' ou '○'
            ou une case vide ' '
        """
        coul = case.get_coul()
        if coul is None:
            return ' '
        elif coul == 'R':
            return Fore.RED+'●'+Fore.RESET
        else:
            return Fore.YELLOW+'○'+Fore.RESET
    
    def draw_colonne(self, colonne):
        """ Renvoie le motif correspondant à une colonne :
            [' ',
             '●',
             '●',
             '◉'
             '◎'
             '○', '◙'
             '◘'
             '■',
             '□',
             '○',
             '○']
        """
        return [self.draw_pion(case) for case in colonne.cases]
    
    def draw_grille(self, grille):
        """ Renvoie le motif correspondant à une grille
            (avec séparateurs '─', '│', '┼', '┐', '┌', '└', '┘', '├', '┤', '┬', '┴') :
            ['│ │ │●│ │○│○│ │',
             '│ │ │●│ │○│●│ │',
             '│●│ │●│○│○│○│ │',
             '│●│○│○│●│○│○│○│',
             '│○│○│●│○│○│○│●│',
             '│○│○│●│●│●│○│○│',
             '└─┴─┴─┴─┴─┴─┴─┘']
        """
        col = [self.draw_colonne(colonne) for colonne in grille.colonnes]
        g = []
        for l in range(6+1):
            ligne = ''
            for c in range(7*2+1):
                if l == 6:
                    if c == 0:
                        ligne += '└'
                    elif c == 14:
                        ligne += '┘'
                    elif c%2 == 0:
                        ligne += '┴'
                    else:
                        ligne += '─'
                else:
                    if c%2 == 0:
                        ligne += '│'
                    else:
                        ligne += col[c//2][5-l]
            g.append(ligne)
        return g
    
    def draw_joueur(self, joueur):
        """
        """
        if joueur.couleur == 'R':
            return Fore.RED+'●'+Fore.RESET
        else:
            return Fore.YELLOW+'○'+Fore.RESET
     
    def draw_jeu(self):
        """ Dessine le plateau de jeu complet :
             - titre
             - invite à jouer
             - grille
             - pions restants
             - message 
            le tout encadré.
        """
        largeur = 21 #caractères
        bordure = 1  #caractère

        # Titre
        j = ["     Puissance 4"]
        j.append(' ')

        # Invite
        if self.jeu.etat == 1: # partie_demarree
            j.append('    ' + ' '*self.pos_pion*2 + self.draw_joueur(self.jeu.get_joueur_courant()))
        else:
            j.append(' ')

        # Grille
        for l in self.draw_grille(self.jeu.grille):
            j.append('   ' + l)

        # Pions restants
        for joueur in self.jeu.joueurs:
            j.append(self.draw_joueur(joueur)*joueur.nbr_pions_restants())
        j.append(' ')

        # Message
        j.append(self.message)

        # Ajustement largeur
        for l in range(len(j)):
            #j[l] = j[l].ljust(largeur)
            j[l] += ' '*(largeur-len2(j[l]))

        # Ajout du cadre
        for l in range(len(j)):
            j[l] = '│'+j[l]+'│'
        j.insert(0, '┌'+'─'*largeur+'┐')    
        j.append('└'+'─'*largeur+'┘')
        return j


def len2(s):
    """ Renvoie la longueur de la chaîne s
        sans compter les caractères ANSI (couleur, ...)

        source : https://stackoverflow.com/questions/68627535/how-to-get-the-length-of-a-string-without-calculating-the-formatting-of-the-text
    """
    return len(re.sub(
        r'[\u001B\u009B][\[\]()#;?]*((([a-zA-Z\d]*(;[-a-zA-Z\d\/#&.:=?%@~_]*)*)?\u0007)|((\d{1,4}(?:;\d{0,4})*)?[\dA-PR-TZcf-ntqry=><~]))', '', s))



###################################################################################
# Classe qui exploite de gestionnaire d'événement
####################################################################################
class GestionnaireEvenements:
    def __init__(self, parent = None):
        self.parent = parent
        # On initialise l'écouteur d'événements clavier (ici : appui sur une touche)
        keyboard.on_press(self.action_clavier)

    def __del__(self):
        """ Méthode appelée automatiquement à la destruction de l'objet
            nécessaire pour arrêter l'écouteur d'événements clavier
        """
        keyboard.unhook_all()
    
    def action_clavier(self, event):
        """ Callback lancé à chaque appui sur une touche
        """
        if self.parent is not None:
            self.parent.action_clavier(event.name) 

####################################################################
####################################################################
if __name__ == "__main__":
    pass
    
    