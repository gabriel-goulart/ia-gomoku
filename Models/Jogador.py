from Models.Peca import Peca


class Jogador:
    nome = ""
    peca = None

    def __init__(self, nome, pecaCor):
        self.nome = nome
        self.peca = Peca(pecaCor, self)

    def getNome(self):
        return self.nome

    def getPeca(self):
        return self.peca    