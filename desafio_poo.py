import getpass
from abc import ABC, abstractmethod
from datetime import datetime

# Limites padrões
LIMITE_SAQUES = 3
LIMITE_VALOR_SAQUE = 500

class Transacao(ABC):
    def __init__(self, valor: float):
        self.valor = valor

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def registrar(self, conta):
        conta.depositar(self.valor)
        conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)
        return sucesso

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao: Transacao):
        self.transacoes.append((datetime.now(), transacao))

    def imprimir(self):
        if not self.transacoes:
            print("Sem movimentações.")
            return
        print("========== EXTRATO ==========")
        for data, transacao in self.transacoes:
            tipo = "Depósito" if isinstance(transacao, Deposito) else "Saque"
            print(f"{data.strftime('%d/%m/%Y %H:%M:%S')} - {tipo}: R$ {transacao.valor:.2f}")
        print("=============================")

class Conta:
    def __init__(self, cliente, numero, agencia="0001"):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def saldo_atual(self):
        return self.saldo

    def sacar(self, valor: float):
        if valor > self.saldo:
            print("❌ Saldo insuficiente.")
            return False
        self.saldo -= valor
        return True

    def depositar(self, valor: float):
        if valor <= 0:
            print("❌ Valor inválido.")
            return False
        self.saldo += valor
        return True

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, agencia="0001", limite=500, limite_saques=LIMITE_SAQUES):
        super().__init__(cliente, numero, agencia)
        self.limite = limite
        self.limite_saques = limite_saques
        self.saques_realizados = 0

    def sacar(self, valor: float):
        if self.saques_realizados >= self.limite_saques:
            print("❌ Limite diário de saques atingido.")
            return False
        if valor > LIMITE_VALOR_SAQUE:
            print("❌ Valor excede o limite de saque.")
            return False
        if valor > self.saldo:
            print("❌ Saldo insuficiente.")
            return False
        self.saldo -= valor
        self.saques_realizados += 1
        return True

class Cliente:
    def __init__(self, nome, cpf, senha, endereco=""):
        self.nome = nome
        self.cpf = cpf
        self.senha = senha
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta: Conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta: Conta, transacao: Transacao):
        transacao.registrar(conta)

# Armazenar os clientes e contas
clientes = []
contas = []

def filtrar_cliente(cpf):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None

def criar_usuario():
    cpf = input("Informe o CPF (apenas números): ")
    if filtrar_cliente(cpf):
        print("Já existe um usuário com esse CPF.")
        return
    nome = input("Informe o nome completo: ")
    senha = getpass.getpass("Crie uma senha: ")
    endereco = input("Informe o endereço: ")
    cliente = Cliente(nome, cpf, senha, endereco)
    clientes.append(cliente)
    print("✅ Usuário criado com sucesso.")

def criar_conta():
    cpf = input("Informe o CPF do titular da conta: ")
    cliente = filtrar_cliente(cpf)
    if not cliente:
        print("❌ Usuário não encontrado. Cadastre o usuário primeiro.")
        return
    numero_conta = len(contas) + 1
    conta = ContaCorrente(cliente, numero_conta)
    cliente.adicionar_conta(conta)
    contas.append(conta)
    print(f"✅ Conta criada com sucesso. Número da conta: {numero_conta}")

def acessar_conta():
    cpf = input("CPF: ")
    senha = getpass.getpass("Senha: ")
    cliente = filtrar_cliente(cpf)
    if not cliente or cliente.senha != senha:
        print("❌ CPF ou senha incorretos.")
        return
    
    if not cliente.contas:
        print("❌ Este cliente não possui contas.")
        return

    print(f"\n✅ Bem-vindo(a), {cliente.nome}!")
    # Se houver mais de uma conta, deixar escolher qual acessar
    if len(cliente.contas) > 1:
        print("Selecione a conta:")
        for i, conta in enumerate(cliente.contas, 1):
            print(f"[{i}] Conta {conta.numero}")
        escolha = int(input("Número da conta: "))
        if escolha < 1 or escolha > len(cliente.contas):
            print("❌ Opção inválida.")
            return
        conta = cliente.contas[escolha-1]
    else:
        conta = cliente.contas[0]

    operacoes(conta)

def operacoes(conta):
    menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair da conta

=> """
    while True:
        opcao = input(menu).lower()

        if opcao == "d":
            valor = float(input("Valor do depósito: "))
            deposito = Deposito(valor)
            conta.cliente.realizar_transacao(conta, deposito)
            print("✅ Depósito realizado com sucesso.")

        elif opcao == "s":
            valor = float(input("Valor do saque: "))
            saque = Saque(valor)
            sucesso = conta.cliente.realizar_transacao(conta, saque)
            if sucesso is False:
                print("❌ Saque não realizado.")
            else:
                print("✅ Saque realizado com sucesso.")

        elif opcao == "e":
            conta.historico.imprimir()
            print(f"Saldo atual: R$ {conta.saldo:.2f}")

        elif opcao == "q":
            print("Saindo da conta...")
            break

        else:
            print("❌ Opção inválida.")

def menu_principal():
    while True:
        print("\n=== Banco Python ===")
        print("[1] Criar usuário")
        print("[2] Criar conta")
        print("[3] Acessar conta")
        print("[0] Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            criar_usuario()
        elif escolha == "2":
            criar_conta()
        elif escolha == "3":
            acessar_conta()
        elif escolha == "0":
            print("Saindo... Obrigado por usar o Banco Python!")
            break
        else:
            print("❌ Opção inválida.")

if __name__ == "__main__":
    menu_principal()
