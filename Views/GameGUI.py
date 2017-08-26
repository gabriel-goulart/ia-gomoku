from tkinter import *
from Models.Tabuleiro import Tabuleiro


class GameGUI():
    
    def __init__(self, tabuleiro, controlador):
        self.tk = Tk()
        self.tk.geometry('700x700')
        self.tk.title('GoMoku')
        self.controlador = controlador
        self.tabuleiro = tabuleiro
        self.mainFrame = Frame(self.tk)
        # Frame.__init__(self, title= 'Jogo')
        self.start()
        mainloop()

    def start(self):
        self.casasList = []
        
        title = Label(self.mainFrame, text="GOMOKU")
        title.pack()
        self.frame_tabuleiro = Frame(self.mainFrame, width=300, height=300)

        # carregando o tabuleiro do jogo na interface
        self.carregaTabuleiro()
        self.frame_tabuleiro.pack()

        self.jogadorDaVezText = StringVar()
        self.jogadorDaVezLabel = Label(self.mainFrame, textvariable=self.jogadorDaVezText)
        self.jogadorDaVezText.set("Jogador")
        self.jogadorDaVezLabel.pack()

        self.mainFrame.pack()

    def setJogadorDaVez(self, jogadorText):
        self.jogadorDaVezText.set(jogadorText)
    
    def casaEscolhida(self, event, linha, coluna):
        self.setJogada(linha, coluna)

    def setJogada(self, linha, coluna):
        self.casasList[linha][coluna].configure(background='green')

    def carregaTabuleiro(self):
        linha = 0
        
        for row in self.tabuleiro.getEstadoAtual():
            coluna = 0
            rowList = []
            for casa in row:
                lb1 = Frame(self.frame_tabuleiro, width=30, height=30, relief='sunken')
                
                lb1.grid(row=linha, column=coluna)
                lb2 = Frame(lb1, width=30, height=30, relief='sunken')
                lb2.configure(background='grey')
                lb2.bind("<Button-1>", lambda event, arg1=linha, arg2=coluna : self.casaEscolhida(self, arg1, arg2))
                lb2.grid(padx=5, pady=5)
                rowList.append(lb2)
                coluna = coluna + 1

            self.casasList.append(rowList)
            linha = linha + 1

    