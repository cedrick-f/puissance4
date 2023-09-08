from case import Case

####################################################################
class Colonne:
    def __init__(self):
        self.cases = [Case() for _ in range(6)]

    def est_remplie(self):
        return not self.cases[-1].est_occupee()
    
    def vider(self):
        for case in self.cases:
            case.liberer()

    def placer_pion(self, pion):
        l = 0
        while l < 6:
            if self.cases[l].est_libre():
                self.cases[l].placer_pion(pion)
                return True
            l += 1
        return False


####################################################################
####################################################################
if __name__ == "__main__":
    pass