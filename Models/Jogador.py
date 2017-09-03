from Models.Peca import Peca


class Jogador:
    nome = ""
    peca = None

    def __init__(self, nome, pecaCor):
        self.nome = nome
        self.peca = Peca(pecaCor, self)

    # retorna o nome do jogador
    def getNome(self):
        return self.nome

    # retorna a peca do jogador    
    def getPeca(self):
        return self.peca    