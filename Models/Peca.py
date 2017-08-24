class Peca:

    cor = "green"
    dono = None

    def __init__(self, cor, dono):
        self.cor = cor
        self.dono = dono

    def getCor(self):
        return self.cor    

    def getDono(self):
        return self.dono