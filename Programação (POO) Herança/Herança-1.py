#Exemplo de Herança.

#Classe Base (classe pai)
class Funcionario:
    def __init__(self, nome, salario):
        self.nome = nome
        self.salario = salario

        def calcular_salario(self)

#Subclasse (classe filha)
class Gerente(Funcionario):
    def __init__(self, nome, slario, nivel_acesso):
        super().__init__(nome, salario)
        self.nivel_acesso = nivel_acesso

        def realizar_tarefa_genencial(self):

#Segundo exemplo!

class Animal:
    def __init__(self, nome):
        self.nome = nome

        def fazer_som(self):
            print("Algum som genérico de aniaml")

class Gato(Animal):
    def __init__(self):
        Super().fazer_som()
        print(f"{self.nome} faz 'miau!'")

#Criando uma istância da classe Gato
gato1 = Gato("tom", "cinza")

# Chmando o método fazer_som da classe Gato
gato1.fazer_som()