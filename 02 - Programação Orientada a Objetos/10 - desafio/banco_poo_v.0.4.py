# Importação de bibliotecas necessárias
import textwrap
from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime

# --- Classes do Domínio ---

class Cliente:
    """
    Classe que representa um cliente do banco.

    Atributos:
        endereco (str): O endereço do cliente.
        contas (list): Lista de contas bancárias associadas ao cliente.
    """
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        """
        Realiza uma transação em uma conta específica do cliente.

        Args:
            conta (Conta): A conta na qual a transação será realizada.
            transacao (Transacao): O objeto de transação (Saque ou Deposito).
        """
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        """Adiciona uma nova conta à lista de contas do cliente."""
        self.contas.append(conta)


class PessoaFisica(Cliente):
    """
    Classe que representa um cliente do tipo Pessoa Física, herdando de Cliente.

    Atributos:
        nome (str): Nome completo do cliente.
        data_nascimento (str): Data de nascimento do cliente.
        cpf (str): CPF do cliente.
        endereco (str): Endereço do cliente.
    """
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    """
    Classe que representa uma conta bancária.

    Atributos:
        _saldo (float): Saldo da conta.
        _numero (int): Número da conta.
        _agencia (str): Número da agência (padrão "0001").
        _cliente (Cliente): Objeto cliente associado à conta.
        _historico (Historico): Objeto que armazena o histórico de transações.
    """
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        """Método de classe para criar uma nova instância de Conta."""
        return cls(numero, cliente)

    # Propriedades para acessar os atributos encapsulados
    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        """
        Realiza um saque na conta.

        Args:
            valor (float): O valor a ser sacado.

        Returns:
            bool: True se o saque for bem-sucedido, False caso contrário.
        """
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        """
        Realiza um depósito na conta.

        Args:
            valor (float): O valor a ser depositado.

        Returns:
            bool: True se o depósito for bem-sucedido, False caso contrário.
        """
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False


class ContaCorrente(Conta):
    """
    Classe que representa uma Conta Corrente, herdando de Conta.

    Atributos:
        _limite (float): Limite de valor por saque.
        _limite_saques (int): Número máximo de saques permitidos.
    """
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        """
        Sobrescreve o método sacar para incluir validações de limite e número de saques.
        """
        # Conta o número de transações do tipo 'Saque' no histórico
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print(f"\n@@@ Operação falhou! O valor do saque (R$ {valor:.2f}) excede o limite de R$ {self._limite:.2f}. @@@")
        elif excedeu_saques:
            print(f"\n@@@ Operação falhou! Número máximo de {self._limite_saques} saques excedido. @@@")
        else:
            # Se passar nas validações, chama o método sacar da classe pai (Conta)
            return super().sacar(valor)

        return False

    def __str__(self):
        """Retorna uma representação em string formatada da conta corrente."""
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    """
    Classe para gerenciar o histórico de transações de uma conta.
    """
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        """
        Adiciona uma nova transação ao histórico.

        Args:
            transacao (Transacao): O objeto de transação a ser adicionado.
        """
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"), # Formato de data corrigido
            }
        )


# --- Classes de Transação (Abstratas e Concretas) ---

class Transacao(ABC):
    """Classe abstrata para definir a estrutura de uma transação."""
    @property
    @abstractmethod
    def valor(self):
        """Propriedade abstrata para o valor da transação."""
        pass

    @abstractmethod
    def registrar(self, conta):
        """Método abstrato para registrar a transação em uma conta."""
        pass


class Saque(Transacao):
    """Classe concreta para transações de saque."""
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        """Registra um saque, se a operação na conta for bem-sucedida."""
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    """Classe concreta para transações de depósito."""
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        """Registra um depósito, se a operação na conta for bem-sucedida."""
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


# --- Funções Auxiliares da Interface ---

def menu():
    """Exibe o menu principal e retorna a opção escolhida pelo usuário."""
    menu_texto = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_texto))


def filtrar_cliente(cpf, clientes):
    """
    Busca um cliente na lista de clientes a partir do CPF.

    Args:
        cpf (str): O CPF a ser buscado.
        clientes (list): A lista de clientes.

    Returns:
        PessoaFisica or None: O objeto cliente se encontrado, senão None.
    """
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    """
    Recupera a conta de um cliente. Se houver mais de uma, permite a seleção.

    Args:
        cliente (PessoaFisica): O cliente dono da conta.

    Returns:
        Conta or None: A conta do cliente ou None se não houver contas.
    """
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None

    # Se o cliente tiver apenas uma conta, retorna ela diretamente.
    if len(cliente.contas) == 1:
        return cliente.contas[0]

    # Se tiver múltiplas contas, permite que o usuário escolha.
    print("\nCliente possui mais de uma conta. Por favor, selecione uma:")
    for i, conta in enumerate(cliente.contas):
        print(f"[{i+1}] Conta Corrente: {conta.numero}")

    while True:
        try:
            escolha = int(input("Digite o número da conta desejada: "))
            if 1 <= escolha <= len(cliente.contas):
                return cliente.contas[escolha - 1]
            else:
                print("\n@@@ Opção inválida! Tente novamente. @@@")
        except ValueError:
            print("\n@@@ Entrada inválida! Por favor, digite um número. @@@")


def depositar(clientes):
    """Função para orquestrar a operação de depósito."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    try:
        valor = float(input("Informe o valor do depósito: "))
        transacao = Deposito(valor)
    except ValueError:
        print("\n@@@ Valor inválido! A operação foi cancelada. @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    """Função para orquestrar a operação de saque."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    try:
        valor = float(input("Informe o valor do saque: "))
        transacao = Saque(valor)
    except ValueError:
        print("\n@@@ Valor inválido! A operação foi cancelada. @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    """Função para exibir o extrato de uma conta."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['data']} - {transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes):
    """Função para criar um novo cliente (Pessoa Física)."""
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas):
    """Função para criar uma nova conta corrente."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print("\n=== Conta criada com sucesso! ===")
    print(f"Agência: {conta.agencia}, C/C: {conta.numero}")


def listar_contas(contas):
    """Função para listar todas as contas criadas no sistema."""
    if not contas:
        print("\n@@@ Nenhuma conta foi criada ainda. @@@")
        return
        
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


# --- Função Principal ---

def main():
    """Função principal que executa o programa do sistema bancário."""
    clientes = []
    contas = []

    # Loop infinito para manter o menu em execução até o usuário decidir sair
    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)
        elif opcao == "s":
            sacar(clientes)
        elif opcao == "e":
            exibir_extrato(clientes)
        elif opcao == "nu":
            criar_cliente(clientes)
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "q":
            print("\nSaindo do sistema... Obrigado por usar nossos serviços!")
            break
        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

# Ponto de entrada do programa
if __name__ == "__main__":
    main()
