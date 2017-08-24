from Models.Tabuleiro import Tabuleiro
from Models.Jogador import Jogador
from Views.GameGUI import GameGUI


class GameController:

    isRunning = False
    tabuleiro = None

    def start(self):
        self.isRunning = True
        self.tabuleiro = Tabuleiro(15, 15)

        for row in self.tabuleiro.getEstadoAtual():
            print(row)

        # print(self.tabuleiro.getEstadoAtual())
        game = GameGUI(self.tabuleiro, self)