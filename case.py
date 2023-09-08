####################################################################
class Case:
    def __init__(self):
        self.pion = None

    def placer_pion(self, pion):
        self.pion = pion

    def est_occupee(self):
        return self.pion is not None
    
    def est_libre(self):
        return self.pion is None
    
    def liberer(self):
        self.pion = None

    def get_coul(self):
        if self.pion is not None:
            return self.pion.couleur
        
####################################################################
class Pion:
    def __init__(self, couleur):
        self.couleur = couleur


####################################################################
####################################################################
if __name__ == "__main__":
    pass