from tkinter import *

###################################################################################
class IHM_tk(Tk):
    def __init__(self, jeu):
        super().__init__()
        self.jeu = jeu
        self.title("Puissance 4")
        
        self.w = 400
        self.h = 450
        self.minsize(self.w, self.h)      # taille de fenêtre
        self.geometry(f"{self.w}x{self.h}")
        self.update()
        
        # dimensions grille
        self.r = 20
        self.ex = 50 # écart entre trous
        self.px = 30 # écart trou/bordure
        self.ey = 50
        self.py = 30
        self.w = (7-1)*self.ex + 2*self.px
        self.h = (6-1)*self.ey + 2*self.py

        # Une méthode séparée pour construire le contenu de la fenêtre
        self.createWidgets()

    def lancer(self):
        self.mainloop()

    # Méthode de création des widgets
    def createWidgets(self):
              
        # Création des widgets
        self.message = StringVar()
        self.lbl_message = Label(self, textvariable = self.message,
                                 font=("Arial", 15))
        self.lbl_message.pack(ipadx = 10, ipady = 6)
        

        # Boutons
        self.frame_boutons = Frame(self, width = self.w, height=self.r*2)
        self.boutons = []
        self.place = IntVar()
        for c in range(len(self.jeu.grille.colonnes)):
            r = Radiobutton(self.frame_boutons, variable=self.place, value=c, 
                            command = self.placer)
            r.place(x = self.px+self.ex*c-self.r/2, y = self.py/2)
            r['state'] = 'disabled'
            self.boutons.append(r)
        self.place.set(None)
        self.frame_boutons.pack()

        # Grille
        self.grille = Canvas(self, width = self.w, height = self.h, bg="blue")
        self.grille.pack()
        self.draw_grille()
        
        # Un bouton pour demarrer la partie
        b = Frame()
        self.startButton = Button(b, text = "", 
                                 command = self.demarrer_partie,
                                 font=("Arial", 15))
        self.startButton.pack(side = LEFT)

        # Un bouton pour quitter l'application
        self.quitButton = Button(b, text = "Quitter", 
                                 command = self.destroy,
                                 font=("Arial", 15))
        self.quitButton.pack(side = RIGHT)
        b.pack()

        self.terminer_partie()
        self.initialiser_partie()
        

    def demarrer_partie(self):
        if self.jeu.etat == 2:
            self.initialiser_partie()
            return
        self.jeu.demarrer_partie()
        for r in self.boutons:
            r['state'] = 'active'
        self.changer_joueur_courant()
        self.startButton['state'] = 'disabled'
        self.startButton['text'] = 'Démarrer'
        

    def initialiser_partie(self):
        self.jeu.initialiser_partie()
        self.message.set('Cliquer sur Démarrer')
        self.lbl_message.config(bg = 'SystemButtonFace')
        self.draw_grille()
        self.startButton['text'] = 'Démarrer'
        
    def terminer_partie(self):
        self.jeu.terminer_partie()
        self.startButton['state'] = 'active'
        for r in self.boutons:
            r['state'] = 'disabled'
        self.startButton['text'] = 'Recommencer'
        

    def get_coul(self, code_coul):
        if code_coul == "R":
            return "red"
        elif code_coul == "J":
            return "yellow"
        else:
            return "white"
    
    def changer_joueur_courant(self):
        self.jeu.changer_joueur_courant()
        self.message.set('Joueur ')
        self.lbl_message.config(bg = self.get_coul(self.jeu.get_joueur_courant().get_coul()))

    def placer(self):
        if self.jeu.get_joueur_courant().placer_pion(self.jeu.get_colonne(self.place.get())):
            self.draw_grille()
            j = self.jeu.get_joueur_gagnant()
            if j is not None:
                self.message.set('Joueur gagne !')
                self.lbl_message.config(bg = self.get_coul(j.get_coul()))
                self.terminer_partie()
            else:
                self.changer_joueur_courant()
        self.place.set(None)


    def draw_grille(self):
        """ Dessine la grille sur le canvas
        """
        for c, col in enumerate(self.jeu.grille.colonnes):
            for l, case in enumerate(col.cases):
                x = self.px + self.ex*c
                y = self.h-self.ey*l-self.py
                self.grille.create_oval(x-self.r, y-self.r, 
                                        x+self.r, y+self.r, 
                                        fill=self.get_coul(case.get_coul()))
        



