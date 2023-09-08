from colonne import Colonne

####################################################################
class Grille:
    def __init__(self):
        self.colonnes = [Colonne() for _ in range(7)]

    def vider(self):
        for colonne in self.colonnes:
            colonne.vider()

    def get_colonne(self, num):
        return self.colonnes[num]
    
    def get_coul_case(self, l, c):
        if l < 4 and c < 7:
            return self.colonnes[c].cases[l].get_coul()

    def get_alignement(self):
        """ Recherche des alignements dans la grille
            renvoie un tuple : ligne, colonne, couleur
             (ligne et colonne sont les coordonnées du pion 
              le plus en bas à gauche
              de l'alignement)
        """
        def get_align_h(l, c, coul, n = 3):
            if coul != self.get_coul_case(l,c):
                return None
            if n == 1:
                return l, c-3, coul
            return get_align_h(l, c+1,coul, n-1)
        
        def get_align_v(l, c, coul, n = 3):
            if coul != self.get_coul_case(l,c):
                return None
            if n == 1:
                return l-3, c, coul
            return get_align_v(l+1, c,coul, n-1)
        
        def get_align_dm(l, c, coul, n = 3):
            if coul != self.get_coul_case(l,c):
                return None
            if n == 1:
                return l-3, c-3, coul
            return get_align_dm(l+1, c+1,coul, n-1)
        
        def get_align_dd(l, c, coul, n = 3):
            if coul != self.get_coul_case(l,c):
                return None
            if n == 1:
                return l-3, c-3, coul
            return get_align_dd(l-1, c+1,coul, n-1)
        
        l0 = 0
        while l0 < 4:
            c0 = 0
            while c0 < 7:
                coul0 = self.get_coul_case(l0,c0)
                if coul0 is not None:
                    r = get_align_h(l0, c0+1, coul0)
                    if r is not None:
                        return r
                    r = get_align_v(l0+1, c0, coul0)
                    if r is not None:
                        return r
                    r = get_align_dm(l0+1, c0+1, coul0)
                    if r is not None:
                        return r
                    r = get_align_dd(l0-1, c0+1, coul0)
                    if r is not None:
                        return r
                c0 += 1
            l0 += 1
        return


####################################################################
####################################################################
if __name__ == "__main__":
    pass