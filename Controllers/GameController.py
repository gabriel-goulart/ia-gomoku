from Models.Tabuleiro import Tabuleiro
from Models.Jogador import Jogador
from Views.GameGUI import GameGUI
from Models.MiniMax import MiniMax


class GameController:

    isRunning = False
    tabuleiro = None
    jogadorDaVez = None
    gameGui = None

    def start(self):
        self.fim = False
        self.isRunning = True
        self.profundidade = 0
        self.tabuleiro = Tabuleiro(15, 15)
        self.jogadorIA = Jogador("maquina", "red")
        self.jogador = Jogador("humano", "green")
        self.miniMax = MiniMax(self.jogadorIA, self.jogador)
        self.jogadorDaVez = self.jogador
        
        # for row in self.tabuleiro.gerarPossiveisJogadas():
        #    print(row)
        
        # print(self.tabuleiro.getEstadoAtual())
        self.gameGui = GameGUI(self.tabuleiro, self)
        
        self.gameGui.start()
    
    def setJogadorDaVez(self, jogador):
        self.jogadorDaVez = jogador   

    def getJogadorDaVez(self):
        return self.jogadorDaVez     

    def getJogadorDaVezToGUI(self):
        return self.jogadorDaVez.getNome()

    def setJogadorDaVezGUI(self):
        if self.fim:
            self.gameGui.setVencedor(" !!!! VENCEDOR : " + str(self.jogadorDaVez.getNome()) + " !!!!")
        else:
            self.gameGui.setJogadorDaVez(self.jogadorDaVez.getNome())     

    def executaMiniMax(self):
        self.profundidade = 2
        jogada = self.miniMax.start(self.profundidade, self.tabuleiro)
        pontuacao = jogada[0]
        linha = jogada[1]
        coluna = jogada[2]

        if pontuacao > 900000000 or pontuacao < -900000000:
            self.fim = True
        self.movimentacao(linha, coluna)

    def setJogadaGUI(self, linha, coluna):
        self.gameGui.setJogada(linha, coluna, self.jogadorDaVez.getPeca().getCor())
     
    # Repassa a movimentacao para o tabuleiro e para a interface grafica 
    def movimentacao(self, linha, coluna):

        self.tabuleiro.getEstadoAtual()[linha][coluna] = self.jogadorDaVez.getPeca()
        self.setJogadaGUI(linha, coluna)
        # print( self.tabuleiro.getEstadoAtual())
        if self.jogadorDaVez is self.jogador:

            if self.fim is False:
                self.setJogadorDaVez(self.jogadorIA)

            self.setJogadorDaVezGUI()
            # manda executar o minimax
            self.executaMiniMax()
        else:
            if self.fim is False:
                self.setJogadorDaVez(self.jogador)

            self.setJogadorDaVezGUI()    

         