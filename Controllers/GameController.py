import _thread
from Models.Tabuleiro import Tabuleiro
from Models.Jogador import Jogador
from Views.GameGUI import GameGUI
from Models.MiniMax import MiniMax


class GameController:

    isRunning = False
    tabuleiro = None
    jogadorDaVez = None
    gameGui = None

    def start(self, restart=False):
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
        if restart:
            self.gameGui.setTabuleiro(self.tabuleiro)
            self.gameGui.restart()
        else:
            self.gameGui = GameGUI(self.tabuleiro, self)
            self.gameGui.start()
        
    def restart(self):
        
        del self.jogadorIA
        del self.jogador
        del self.tabuleiro
        del self.miniMax
        self.start(True)

    def setJogadorInicial(self, escolha):
        print(escolha)

        if escolha == 1:
            self.jogadorDaVez = self.jogadorIA
        else:
            self.jogadorDaVez = self.jogador    
        
        self.gameGui.carregaJogo()

    def setJogadorDaVez(self, jogador):
        self.jogadorDaVez = jogador 
        self.gameGui.setJogadorDaVez(jogador.getNome())  

    def getJogadorDaVez(self):
        return self.jogadorDaVez     
  
    def fimJogo(self, vencedor):
        self.gameGui.setVencedor(" !!!! VENCEDOR : " + str(vencedor.getNome()) + " !!!!")
        
    def setJogadorDaVezGUI(self):
        if self.fim:
            self.gameGui.setVencedor(" !!!! VENCEDOR : " + str(self.jogadorDaVez.getNome()) + " !!!!")
        else:
            self.gameGui.setJogadorDaVez(self.jogadorDaVez.getNome())     

    def executaMiniMax(self, linha):
        self.profundidade = 2
        jogada = self.miniMax.start(self.profundidade, self.tabuleiro, linha)
        pontuacao = jogada[0]
        linha = jogada[1]
        coluna = jogada[2]

        if pontuacao > 900000000:
            self.fimJogo(self.jogadorIA) 
        elif pontuacao < -900000000:
            self.fimJogo(self.jogador)
        else:
            self.movimentacao(linha, coluna)

    def startJogadaIa(self, linha):
        _thread.start_new_thread(self.executaMiniMax, (linha, ))
     
    # Repassa a movimentacao para o tabuleiro e para a interface grafica 
    def movimentacao(self, linha, coluna):
        self.tabuleiro.getEstadoAtual()[linha][coluna] = self.jogadorDaVez.getPeca()
        self.gameGui.setJogada(linha, coluna, self.jogadorDaVez.getPeca().getCor())
        # print( self.tabuleiro.getEstadoAtual())
        if self.jogadorDaVez is self.jogador:
            self.setJogadorDaVez(self.jogadorIA)
            # manda executar o minimax
            self.startJogadaIa(linha)
        else:
            self.setJogadorDaVez(self.jogador)
            