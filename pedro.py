INFINITY = float('inf')
NERVOSO = 0
NORMAL = 1

class Pikas:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade
        self.bitches = 0
        self.fome = 100
        self.sede = 100
        self.peso = 60 #KG
        self.estado = NORMAL

    def cagar(self, quantidade):
        self.sede += 10
        self.peso -= quantidade

    def raptar(self, pessoa):
        pessoa.estado = NERVOSO


class Pedro:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade
        self.bitches = INFINITY
        self.fome = 100
        self.sede = 100
        self.peso = 90 #KG

    def comer(self):
        self.fome = 0

    def cagar(self, quantidade):
        self.sede += 10
        self.peso -= quantidade

    def sairCom(self, pessoa):
        self.bitches += 1
        pessoa.bitches += 1
        pessoa.fome += INFINITY


def main():
    nome = "Pedro"
    idade = 38 #anos

    #create Pedro
    Pedro = Pedro(nome, idade)


    nome = "Pikas"
    idade = 20

    #create Pikas
    Pikas = Pikas(nome, idade)

    Pedro.sairCom(Pikas)
    Pikas.estado = NERVOSO

    quantidade = 2 #KG
    Pikas.cagar(quantidade)

    Pikas.estado = NORMAL
    Pikas.raptar(Pedro)

