from tkinter import *
from Models.Tabuleiro import Tabuleiro


class GameGUI(Frame):
    
    def __init__(self, tabuleiro, controlador):
        self.controlador = controlador
        self.tabuleiro = tabuleiro
        Frame.__init__(self, width=600, height=600)
        self.start()
        mainloop()

    def start(self):
        self.msg = Label(self, text="GOMOKU")
        self.msg.pack()
        self.frame_tabuleiro = Frame(self, width=300, height=300)
        self.carregaTabuleiro()
        self.frame_tabuleiro.pack()
        self.pack()

    def carregaTabuleiro(self):
        linha = 0
        
        for row in self.tabuleiro.getEstadoAtual():
            coluna = 0
            for casa in row:
                lb = Frame(self.frame_tabuleiro, width=20, height=20, borderwidth=2)
                lb.configure(background='green')
                lb.grid(row=linha, column=coluna)
                coluna = coluna + 1

            linha = linha + 1
        