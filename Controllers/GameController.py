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

    # cria todos os objetos necessarios no sistema e inicia a interface gráfica
    def start(self, restart=False):
        self.fim = False
        self.isRunning = True
        self.profundidade = 0
        self.tabuleiro = Tabuleiro(15, 15)
        self.jogadorIA = Jogador("maquina", "red")
        self.jogador = Jogador("humano", "green")
        self.miniMax = MiniMax(self.jogadorIA, self.jogador)
        self.jogadorDaVez = self.jogador        
        if restart:
            self.gameGui.setTabuleiro(self.tabuleiro)
            self.gameGui.restart()
        else:
            self.gameGui = GameGUI(self.tabuleiro, self)
            self.gameGui.start()

    # reinicializa o sistema    
    def restart(self):
        
        del self.jogadorIA
        del self.jogador
        del self.tabuleiro
        del self.miniMax
        self.start(True)

    # seta o jogador inicial
    def setJogadorInicial(self, escolha):

        if escolha == 1:
            self.jogadorDaVez = self.jogadorIA
        else:
            self.jogadorDaVez = self.jogador    
        
        self.gameGui.carregaJogo()

    # atualiza o jogado da vez
    def setJogadorDaVez(self, jogador):
        self.jogadorDaVez = jogador 
        self.gameGui.setJogadorDaVez(jogador.getNome())  

    # retorna o jogador da vez
    def getJogadorDaVez(self):
        return self.jogadorDaVez     
  
    # chama a interface gráfica para mostrar a interface de fim de jogo
    def fimJogo(self, vencedor):
        self.gameGui.setVencedor(" !!!! VENCEDOR : " + str(vencedor.getNome()) + " !!!!")

    # seta na interface o jogador da vez    
    def setJogadorDaVezGUI(self):
        if self.fim:
            self.gameGui.setVencedor(" !!!! VENCEDOR : " + str(self.jogadorDaVez.getNome()) + " !!!!")
        else:
            self.gameGui.setJogadorDaVez(self.jogadorDaVez.getNome())     

    # executa o algoritmo para realizar a jogada do computador
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

    # cria uma thread para executar o minimax
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
            