class Tabuleiro:

    def __init__(self, dimX, dimY):
        self.estadoAtual = [[0 for i in range(dimX)] for j in range(dimY)]

    def getEstadoAtual(self):
        return self.estadoAtual    
