class Tabuleiro:

    def __init__(self, dimX, dimY):
        self.estadoAtual = [[0 for i in range(dimX)] for j in range(dimY)]

    def getEstadoAtual(self):
        return self.estadoAtual

    def setEstadoAtual(self, estadoAtual):
        self.estadoAtual = estadoAtual    

    # otimizacao (pegar a linha em que o usuario jogou e gerar os estados filhos a partir dessa linha)
    # gera as possiveis jogadas a partir do estado atual do tabuleiro    
    def gerarPossiveisJogadas(self):

        possiveisJogadas = []

        linha = 0

        for row in self.estadoAtual:

            coluna = 0

            for column in row:

                if self.estadoAtual[linha][coluna] == 0:
                    possiveisJogadas.append([linha, coluna])

                coluna = coluna + 1

            linha = linha + 1            

        return possiveisJogadas

