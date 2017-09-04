class Tabuleiro:

    def __init__(self, dimX, dimY):
        self.estadoAtual = [[0 for i in range(dimX)] for j in range(dimY)]

    # retorna o estado atual do tabuleiro
    def getEstadoAtual(self):
        return self.estadoAtual

    # atualiza o estado atual do tabuleiro    
    def setEstadoAtual(self, estadoAtual):
        self.estadoAtual = estadoAtual    

    # gera as possiveis jogadas a partir do estado atual do tabuleiro    
    def gerarPossiveisJogadas(self, linhaLimit=None):

        possiveisJogadas = []
        linhaLimitInferior = 0
        linhaLimitSuperior = 0
        if linhaLimit is not None:

            if linhaLimit - 5 > 0:
                linhaLimitInferior = linhaLimit - 5

            if linhaLimit + 5 >= len(self.estadoAtual[0]):
                linhaLimitSuperior = len(self.estadoAtual[0])
            else:
                linhaLimitSuperior = linhaLimit + 5

            for row in range(linhaLimitInferior, linhaLimitSuperior, 1):
                
                for column in range(len(self.estadoAtual[0])):
                    if self.estadoAtual[row][column] == 0:
                        possiveisJogadas.append([row, column])
         
        else:
            for row in self.estadoAtual:

                coluna = 0

                for column in row:

                    if self.estadoAtual[linha][coluna] == 0:
                        possiveisJogadas.append([linha, coluna])

                    coluna = coluna + 1

                linha = linha + 1            
        
        return possiveisJogadas

