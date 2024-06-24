from abc import ABC, abstractclassmethod, abstractproperty

class Transacao(ABC):
   
    @property
    @abstractproperty
    def valor (self):
        pass
    @abstractclassmethod
    def registrar(self,conta):
        pass
    
class Historico:
    def __init__(self):
        self._transacoes = []
    def transacoes(self):
        return self._transacoes 
    def adicionar_transacoes(self,transacao):
        self._transacoes.append({
                "tipo" : transacao.__class__.__name__,
                "valor" :transacao.valor
            })

    
class Cliente:
    def __init__(self,endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self,conta, transacao):
        transacao.registrar(conta)
    def adicionar_conta(self, conta):
        self.contas.append(conta)
    
class Pessoa_fisica(Cliente):
    def __init__(self,cpf,nome, data_nascimento,endereco):
        super().__init__(endereco)
        self.cpf=cpf
        self.nome=nome
        self.data_nascimento=data_nascimento
class Conta:
    def __init__(self,numero_conta,cliente):
        self._saldo=0
        self._numero_conta= numero_conta
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    def Sacar(self, valor):
        saldo=self._saldo
        excedeu_saldo = valor > saldo
        if excedeu_saldo:
            print("Saldo insuficiente!")
        elif valor > 0:
            self._saldo -= valor
            return True
        else:
            print ("Operação Inválida!")
        return False
    def Depositar(self, valor):
        saldo=self._saldo
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso!")
        else:
            print("Operação inválida!")
            return False
        return True
    @property
    def saldo (self):
        return self._saldo
    @property
    def numero_conta(self):
        return self._numero_conta
    @property
    def agencia(self):
        return self._agencia
    @property
    def cliente(self):
        return self._cliente
    @classmethod
    def nova_conta(cls, cliente, numero_conta):
        return cls(numero_conta,cliente)
class Conta_Corrente(Conta):
    def __init__(self, numero_conta,cliente, limite=500,limite_saques=3):
        super().__init__(numero_conta,cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def Sacar(self, valor):
        numero_saques = len(
            
            [transacao for transacao in self._historico.transacoes if transacao["tipo"] == "Saque"]

            )
        excedeu_limite =  valor > self.limite
        excedeu_saques = numero_saques>=self.limite_saques
        if excedeu_limite:
            print("Limite excedido.")
        elif excedeu_saques:
            print("Número de saques diários excedidos!")
        else:
            return super().Sacar(valor)
        return False
    def __str__(self):
            return f"Agência: {self.agencia}; Conta: {self.numero_conta}; Titular: {self.cliente.nome}"
class Saque(Transacao):
    def __init__(self,valor):
        self._valor = valor
    @property
    def valor (self):
        return self._valor
    def registrar(self,conta):
        sucesso = conta.Sacar(self.valor)
        if sucesso:
            conta._historico.adicionar_transacoes(self)
class Deposito(Transacao):
    def __init__(self,valor):
        self._valor = valor
    @property
    def valor (self):
        return self._valor
    def registrar(self,conta):
        sucesso = conta.Depositar(self.valor)
        if sucesso:
            conta._historico.adicionar_transacoes(self)
        

