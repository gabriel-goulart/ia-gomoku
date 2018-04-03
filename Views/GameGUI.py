from tkinter import *
from tkinter import messagebox

from Models.Tabuleiro import Tabuleiro


class GameGUI():
    
    # construtor
    def __init__(self, tabuleiro, controlador):
        self.tk = Tk()
        self.tk.geometry('700x700')
        self.tk.title('GoMoku')
        self.controlador = controlador
        self.tabuleiro = tabuleiro
        self.mainFrame = Frame(self.tk)
        
    # inicia a interface gráfica
    def start(self):
        
        self.escolherPrimeiroJogador()
        self.tk.mainloop()

    # reinicializa a interface gráfica
    def restart(self):
        for row in self.casasList:
            for column in row:
                column.configure(background='grey')

        self.setJogadorDaVez(self.controlador.getJogadorDaVez().getNome())        

    # passa para o controlador o jogador escolhido na interface gráfica
    def jogadorEscolhidoGUI(self):
        # print(self.jogadorEscolhido.get())
        self.controlador.setJogadorInicial(self.jogadorEscolhido.get())

    # mostra para o usuário a tela para escolher o jogador inicial
    def escolherPrimeiroJogador(self):       
        self.jogadorEscolhido = IntVar()
        self.jogadorEscolhido.set(0)
        self.jogadorEscolha = Frame(self.tk)
        title = Label(self.jogadorEscolha, text="Escolher quem iniciará o jogo")
        title.pack()

        escolha1 = Radiobutton(self.jogadorEscolha, text="Computador", value=1, variable=self.jogadorEscolhido, command=self.jogadorEscolhidoGUI).pack(anchor=W)
        escolha2 = Radiobutton(self.jogadorEscolha, text="Humano", value=2, variable=self.jogadorEscolhido, command=self.jogadorEscolhidoGUI).pack(anchor=W)
         
        self.jogadorEscolha.pack()
       
    # carrega a tela que mostrará o tabuleiro do jogo
    def carregaJogo(self):
        self.jogadorEscolha.destroy()
        # lista que armazenará os frames que representarão as casas do tabuleiro    
        self.casasList = []
        
        title = Label(self.mainFrame, text="GOMOKU")
        title.pack()

        # frame que manterá o tabuleiro
        self.frame_tabuleiro = Frame(self.mainFrame, width=300, height=300)

        # carregando o tabuleiro do jogo na interface
        self.carregaTabuleiro()
        self.frame_tabuleiro.pack()

        # variavel e label que mostrarão quem é o jogador da vez
        self.jogadorDaVezText = StringVar()
        self.jogadorDaVezText.set(self.controlador.getJogadorDaVez().getNome()) # pegando no controlador qual o usuario da vez
        self.jogadorDaVezLabel = Label(self.mainFrame, textvariable=self.jogadorDaVezText)
        self.jogadorDaVezLabel.pack()

        self.mainFrame.pack()

        if self.jogadorEscolhido.get() == 1:
            self.controlador.executaMiniMax(0)

    # atualiza o tabuleiro, esse método é usado quando o jogo é reiniciado
    def setTabuleiro(self, tabuleiro):
        self.tabuleiro = tabuleiro    

    # mostrando na interface quem é o jogador da vez
    def setJogadorDaVez(self, jogadorText):
        self.jogadorDaVezText.set(jogadorText)
    
    # mostra mensagem quem venceu o jogo e verifica se quer jogar novamente
    def setVencedor(self, vencedor):
        jogarNovamente = messagebox.askquestion("FIM DE JOGO", "!! VENCEDOR : " + str(vencedor) + "!!!! \n\n Jogar Novamente ?")
        
        if jogarNovamente == "yes":
            self.controlador.restart()
        else:
            self.tk.destroy()
        
    # funcao de callback quando uma casa é escolhida
    def casaEscolhida(self, event, linha, coluna):
        if self.tabuleiro.getEstadoAtual()[linha][coluna] == 0:                 
            self.controlador.movimentacao(linha, coluna)

    # carregando a joga feita na interface (pintando o quadrado)
    def setJogada(self, linha, coluna, cor):
        self.casasList[linha][coluna].configure(background=cor)

    # carregando o tabuleiro na interface
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

    