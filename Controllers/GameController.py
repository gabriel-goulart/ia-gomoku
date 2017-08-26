from Models.Tabuleiro import Tabuleiro
from Models.Jogador import Jogador
from Views.GameGUI import GameGUI


class GameController:

    isRunning = False
    tabuleiro = None
    jogadorDaVez = None
    gameGui = None

    def start(self):
        self.isRunning = True
        self.tabuleiro = Tabuleiro(15, 15)
        self.jogadorIA = Jogador("maquina", "red")
        self.jogador = Jogador("humano", "green")
        self.jogadorDaVez = self.jogador
        
        # for row in self.tabuleiro.gerarPossiveisJogadas():
        #    print(row)
        print(self)
        # print(self.tabuleiro.getEstadoAtual())
        self.gameGui = GameGUI(self.tabuleiro, self)
        print(self.gameGui)
        self.gameGui.start()
    
    def setJogadorDaVez(self, jogador):
        self.jogadorDaVez = jogador    

    def getJogadorDaVezToGUI(self):
        return self.jogadorDaVez.getNome()

    def setJogadorDaVezGUI(self):
        self.gameGui.setJogadorDaVez(self.jogadorDaVez.getNome())  
     
    def show(self):
        print(self) 

    def movimentacao(self, linha, coluna):

        self.tabuleiro.getEstadoAtual()[linha][coluna] = self.jogadorDaVez.getPeca()
        self.gameGui.setJogada(linha, coluna, self.jogadorDaVez.getPeca().getCor())

        if self.jogadorDaVez is self.jogador:
            self.setJogadorDaVez(self.jogadorIA)
            self.setJogadorDaVezGUI()
            # manda executar o minimax
        else:
            self.setJogadorDaVez(self.jogador)
            self.setJogadorDaVezGUI()    

         