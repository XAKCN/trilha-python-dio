# Sistema Bancário v0.3.py - Refatorado com Usuários e Contas
import textwrap
import os  # Importado para a função de limpar a tela

def limpar_tela():
    """Função para limpar o terminal, melhorando a experiência do usuário."""
    # 'nt' é para Windows, 'posix' para Linux/Mac
    os.system('cls' if os.name == 'nt' else 'clear')

def menu():
    """
    Exibe o menu de opções e captura a escolha do usuário.
    
    Returns:
        str: A opção escolhida pelo usuário.
    """
    menu_texto = """
    ================ MENU ================
    [d]  Depositar
    [s]  Sacar
    [e]  Exibir Extrato
    
    [nu] Novo Usuário
    [nc] Nova Conta
    [lc] Listar Contas
    
    [q]  Sair
    ======================================
    => """
    return input(textwrap.dedent(menu_texto))


def depositar(saldo, valor, extrato, /):
    """
    Realiza um depósito na conta.

    Args:
        saldo (float): O saldo atual da conta.
        valor (float): O valor a ser depositado.
        extrato (str): O extrato atual da conta.

    Returns:
        tuple: Uma tupla contendo o novo saldo e o extrato atualizado.
    """
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("\n--- Depósito realizado com sucesso! ---")
    else:
        print("\n!!! Operação não realizada! O valor informado é inválido. !!!")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """
    Realiza um saque da conta, validando as regras de negócio.

    Args:
        saldo (float): O saldo atual da conta.
        valor (float): O valor a ser sacado.
        extrato (str): O extrato atual da conta.
        limite (float): O limite de valor por saque.
        numero_saques (int): A quantidade de saques já realizados.
        limite_saques (int): O limite de saques diários.

    Returns:
        tuple: Uma tupla contendo o novo saldo, o extrato e o número de saques atualizados.
    """
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n!!! Operação não realizada! Saldo insuficiente. !!!")
    elif excedeu_limite:
        print(f"\n!!! Operação não realizada! O valor do saque excede o limite de R$ {limite:.2f}. !!!")
    elif excedeu_saques:
        print("\n!!! Operação não realizada! Número máximo de saques excedido. !!!")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:    R$ {valor:.2f}\n"
        numero_saques += 1
        print("\n--- Saque realizado com sucesso! ---")
    else:
        print("\n!!! Operação não realizada! O valor informado é inválido. !!!")

    # Retorna o numero_saques atualizado, corrigindo o bug da versão original
    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    """
    Exibe o extrato de transações e o saldo final da conta.

    Args:
        saldo (float): O saldo atual da conta.
        extrato (str): O histórico de transações.
    """
    print("\n================ EXTRATO ================")
    print("Nenhuma movimentação foi realizada." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")


def criar_usuario(usuarios):
    """
    Cadastra um novo usuário no sistema.

    Args:
        usuarios (list): A lista de usuários existentes.
    """
    cpf = input("Informe o CPF (somente números): ")
    usuario_existente = filtrar_usuario(cpf, usuarios)

    if usuario_existente:
        print("\n!!! Atenção! Já existe um usuário com este CPF. !!!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    novo_usuario = {
        "nome": nome, 
        "data_nascimento": data_nascimento, 
        "cpf": cpf, 
        "endereco": endereco
    }
    usuarios.append(novo_usuario)

    print("\n--- Usuário criado com sucesso! ---")


def filtrar_usuario(cpf, usuarios):
    """
    Busca um usuário na lista pelo seu CPF.

    Args:
        cpf (str): O CPF a ser pesquisado.
        usuarios (list): A lista de usuários para busca.

    Returns:
        dict or None: Retorna o dicionário do usuário se encontrado, caso contrário, None.
    """
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    """
    Cria uma nova conta bancária vinculada a um usuário.

    Args:
        agencia (str): O número da agência.
        numero_conta (int): O número da nova conta.
        usuarios (list): A lista de usuários cadastrados.

    Returns:
        dict or None: Retorna o dicionário da nova conta se criada com sucesso, senão None.
    """
    cpf = input("Informe o CPF do titular da conta: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n--- Conta criada com sucesso! ---")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n!!! Usuário não encontrado! Processo de criação de conta encerrado. !!!")
    return None


def listar_contas(contas):
    """
    Exibe uma lista formatada de todas as contas cadastradas.

    Args:
        contas (list): A lista de contas a serem exibidas.
    """
    if not contas:
        print("\nNenhuma conta foi cadastrada ainda.")
        return
        
    print("\n================ LISTA DE CONTAS ================")
    for conta in contas:
        linha = f"""\
            Agência:  {conta['agencia']}
            Conta:    {conta['numero_conta']}
            Titular:  {conta['usuario']['nome']}
        """
        print(textwrap.dedent(linha))
    print("================================================")


def main():
    """
    Função principal que executa o sistema bancário.
    """
    # Constantes do sistema
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    # Variáveis de estado da conta (simulando uma única conta/sessão)
    saldo = 0.0
    limite = 500.0
    extrato = ""
    numero_saques = 0
    
    # Listas para armazenar dados do sistema
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            limpar_tela()
            print("--- Operação de Depósito ---")
            try:
                valor = float(input("Informe o valor a ser depositado: R$ "))
                saldo, extrato = depositar(saldo, valor, extrato)
            except ValueError:
                print("\n!!! Erro! Por favor, digite um valor numérico válido. !!!")

        elif opcao == "s":
            limpar_tela()
            print("--- Operação de Saque ---")
            try:
                valor = float(input("Informe o valor a ser sacado: R$ "))
                # Correção do bug: a função sacar agora retorna o numero_saques
                saldo, extrato, numero_saques = sacar(
                    saldo=saldo,
                    valor=valor,
                    extrato=extrato,
                    limite=limite,
                    numero_saques=numero_saques,
                    limite_saques=LIMITE_SAQUES,
                )
            except ValueError:
                print("\n!!! Erro! Por favor, digite um valor numérico válido. !!!")

        elif opcao == "e":
            limpar_tela()
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            limpar_tela()
            print("--- Cadastro de Novo Usuário ---")
            criar_usuario(usuarios)

        elif opcao == "nc":
            limpar_tela()
            print("--- Criação de Nova Conta ---")
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == "lc":
            limpar_tela()
            listar_contas(contas)

        elif opcao == "q":
            print("\nObrigado por utilizar nosso sistema. Até logo!\n")
            break

        else:
            print("\n!!! Operação inválida! Por favor, selecione uma das opções do menu. !!!")
        
        # Pausa para o usuário ler a mensagem antes de voltar ao menu
        input("\nPressione Enter para continuar...")
        limpar_tela()

# Ponto de entrada do programa
if __name__ == "__main__":
    main()