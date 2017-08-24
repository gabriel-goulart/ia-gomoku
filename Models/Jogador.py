class Jogador:
    nome = ""
    pecaCor = "green" 

    def __init__(self, nome, pecaCor):
        self.nome = nome
        self.pecaCor = pecaCor

    def getNome(self):
        return self.nome

    def getpecaCor(self):
        return self.pecaCor    