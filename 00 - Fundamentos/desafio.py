# Sistema Bancário v0.2 - Refatorado com Funções

def exibir_menu():
    """Exibe o menu de opções para o usuário."""
    menu = """
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [q]\tSair
    => """
    return input(menu)

def depositar(saldo, extrato, /):
    """
    Realiza a operação de depósito.
    Recebe o saldo e o extrato atuais e retorna os novos valores após a operação.
    Usa a sintaxe de 'positional-only' (/) para os argumentos.
    """
    valor = float(input("Informe o valor do depósito: "))

    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato

def sacar(*, saldo, extrato, limite, numero_saques, limite_saques):
    """
    Realiza a operação de saque.
    Recebe o estado atual da conta e retorna os novos valores após a operação.
    Usa a sintaxe de 'keyword-only' (*) para os argumentos.
    """
    valor = float(input("Informe o valor do saque: "))

    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    """
    Exibe o extrato da conta.
    Recebe o saldo (positional-only) e o extrato (keyword-only).
    """
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")

def main():
    """Função principal que executa o sistema bancário."""
    # Constantes
    LIMITE_SAQUES = 3
    
    # Variáveis de estado da conta
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0

    while True:
        opcao = exibir_menu()

        if opcao == "d":
            saldo, extrato = depositar(saldo, extrato)

        elif opcao == "s":
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "q":
            print("\nObrigado por usar nosso sistema. Até logo!")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

# Ponto de entrada do programa
if __name__ == "__main__":
    main()
