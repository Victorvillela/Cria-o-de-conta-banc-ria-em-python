import getpass

usuarios = []
contas = []

# Limites padrões
LIMITE_SAQUES = 3
LIMITE_VALOR_SAQUE = 500

def criar_usuario():
    cpf = input("Informe o CPF (apenas números): ")
    usuario = filtrar_usuario(cpf)

    if usuario:
        print("Já existe um usuário com esse CPF.")
        return

    nome = input("Informe o nome completo: ")
    senha = getpass.getpass("Crie uma senha: ")
    
    usuarios.append({"nome": nome, "cpf": cpf, "senha": senha})
    print("✅ Usuário criado com sucesso. Agora você voltará ao menu, crie sua conta ou acesse demais opções.")

def filtrar_usuario(cpf):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None

def criar_conta():
    cpf = input("Informe o CPF do titular da conta: ")
    usuario = filtrar_usuario(cpf)

    if not usuario:
        print("❌ Usuário não encontrado. Cadastre o usuário primeiro.")
        return

    numero_conta = len(contas) + 1
    contas.append({
        "usuario": usuario,
        "numero": numero_conta,
        "saldo": 0,
        "extrato": "",
        "saques": 0
    })
    print(f"✅ Conta criada com sucesso. Número da conta: {numero_conta}")

def acessar_conta():
    cpf = input("CPF: ")
    senha = getpass.getpass("Senha: ")
    
    for conta in contas:
        if conta["usuario"]["cpf"] == cpf and conta["usuario"]["senha"] == senha:
            print(f"\n✅ Bem-vindo(a), {conta['usuario']['nome']}!")
            operacoes(conta)
            return
    
    print("❌ CPF ou senha incorretos.")

def operacoes(conta):
    menu = """
    
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair da conta

    => """

    while True:
        opcao = input(menu)

        if opcao == "d":
            valor = float(input("Valor do depósito: "))
            if valor > 0:
                conta["saldo"] += valor
                conta["extrato"] += f"Depósito: R$ {valor:.2f}\n"
                print("✅ Depósito realizado com sucesso.")
            else:
                print("❌ Valor inválido.")

        elif opcao == "s":
            valor = float(input("Valor do saque: "))

            if valor > conta["saldo"]:
                print("❌ Saldo insuficiente.")
            elif valor > LIMITE_VALOR_SAQUE:
                print("❌ Valor excede o limite de saque.")
            elif conta["saques"] >= LIMITE_SAQUES:
                print("❌ Limite diário de saques atingido.")
            elif valor > 0:
                conta["saldo"] -= valor
                conta["extrato"] += f"Saque: R$ {valor:.2f}\n"
                conta["saques"] += 1
                print("✅ Saque realizado com sucesso.")
            else:
                print("❌ Valor inválido.")

        elif opcao == "e":
            print("\n========== EXTRATO ==========")
            print(conta["extrato"] if conta["extrato"] else "Sem movimentações.")
            print(f"Saldo atual: R$ {conta['saldo']:.2f}")
            print("=============================")

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

menu_principal()
