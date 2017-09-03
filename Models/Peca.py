class Peca:

    cor = "green"
    dono = None

    def __init__(self, cor, dono):
        self.cor = cor
        self.dono = dono

    # retorna a cor da peca
    def getCor(self):
        return self.cor    

    # retorna o jogador dono da peca    
    def getDono(self):
        return self.dono