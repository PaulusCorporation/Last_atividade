"""
Controle de reservas de salas — versão orientada a objetos.

Refatoração do código-base com listas/funções, adicionando:
- verificação de conflito de horários;
- cancelamento de reservas.
"""


class Usuario:
    def __init__(self, nome):
        nome = nome.strip()
        if not nome:
            raise ValueError("Nome do responsável não pode ser vazio.")
        self.nome = nome

    def __str__(self):
        return self.nome


class Sala:
    def __init__(self, nome, capacidade):
        self.nome = nome
        self.capacidade = capacidade
        self.reservas = []

    def comporta(self, pessoas):
        return 1 <= pessoas <= self.capacidade

    def tem_conflito(self, dia, inicio, fim):
        """Retorna a primeira reserva conflitante ou None."""
        for reserva in self.reservas:
            if reserva.conflita_com(dia, inicio, fim):
                return reserva
        return None

    def __str__(self):
        return f"{self.nome} (capacidade: {self.capacidade})"


class Reserva:
    _proximo_id = 1

    def __init__(self, usuario, sala, pessoas, dia, inicio, fim):
        self.id = Reserva._proximo_id
        Reserva._proximo_id += 1

        self.usuario = usuario
        self.sala = sala
        self.pessoas = pessoas
        self.dia = dia
        self.inicio = inicio
        self.fim = fim

    def conflita_com(self, dia, inicio, fim):
        """Dois intervalos [inicio, fim) se sobrepõem se um começa antes do outro terminar."""
        return (
            self.dia == dia
            and inicio < self.fim
            and fim > self.inicio
        )

    def __str__(self):
        return (
            f"#{self.id} | {self.sala.nome} | "
            f"{self.dia} {self.inicio}-{self.fim} | "
            f"{self.usuario}"
        )


class SistemaReservas:
    def __init__(self):
        self.salas = {}
        self.reservas = []

    def adicionar_sala(self, sala):
        self.salas[sala.nome] = sala

    def registrar(self, nome_usuario, nome_sala, pessoas, dia, inicio, fim):
        usuario = Usuario(nome_usuario)

        sala = self.salas.get(nome_sala)
        if sala is None:
            raise ValueError("Sala inexistente.")

        if not sala.comporta(pessoas):
            raise ValueError("A quantidade excede a capacidade ou é inválida.")

        if not dia or not inicio or not fim or inicio >= fim:
            raise ValueError("Dados incompletos ou horário inválido.")

        conflito = sala.tem_conflito(dia, inicio, fim)
        if conflito:
            raise ValueError(
                f"Conflito de horário com a reserva #{conflito.id} "
                f"({conflito.inicio}-{conflito.fim}, {conflito.usuario})."
            )

        reserva = Reserva(usuario, sala, pessoas, dia, inicio, fim)
        sala.reservas.append(reserva)
        self.reservas.append(reserva)
        return reserva

    def cancelar(self, id_reserva):
        for reserva in self.reservas:
            if reserva.id == id_reserva:
                self.reservas.remove(reserva)
                reserva.sala.reservas.remove(reserva)
                return reserva
        raise ValueError("Reserva não encontrada.")

    def listar(self):
        return list(self.reservas)


# ---------------- MENU ----------------

def menu_registrar(sistema):
    try:
        nome = input("Nome do responsável: ")
        print("\nSalas disponíveis:")
        for sala in sistema.salas.values():
            print(" -", sala)

        sala = input("\nSala: ").strip()
        pessoas = int(input("Quantidade de pessoas: "))
        dia = input("Data (AAAA-MM-DD): ").strip()
        inicio = input("Início (HH:MM): ").strip()
        fim = input("Fim (HH:MM): ").strip()

        reserva = sistema.registrar(nome, sala, pessoas, dia, inicio, fim)
        print(f"\nReserva #{reserva.id} cadastrada.")

    except ValueError as erro:
        print("\nErro:", erro)


def menu_listar(sistema):
    reservas = sistema.listar()
    if not reservas:
        print("\nNenhuma reserva cadastrada.")
        return

    print("\n--- RESERVAS CADASTRADAS ---")
    for reserva in reservas:
        print(reserva)


def menu_cancelar(sistema):
    try:
        id_reserva = int(input("ID da reserva a cancelar: "))
        reserva = sistema.cancelar(id_reserva)
        print(f"\nReserva #{reserva.id} cancelada.")
    except ValueError as erro:
        if str(erro) == "Reserva não encontrada.":
            print(erro)
        else:
            print("ID inválido.")


# ---------------- PROGRAMA PRINCIPAL ----------------

def main():
    sistema = SistemaReservas()
    sistema.adicionar_sala(Sala("Lab 1", 20))
    sistema.adicionar_sala(Sala("Lab 2", 35))
    sistema.adicionar_sala(Sala("Auditório", 80))

    while True:
        print("\n1 - Registrar reserva | 2 - Listar | 3 - Cancelar | 0 - Sair")
        opcao = input("Opção: ").strip()

        if opcao == "1":
            menu_registrar(sistema)
        elif opcao == "2":
            menu_listar(sistema)
        elif opcao == "3":
            menu_cancelar(sistema)
        elif opcao == "0":
            print("Encerrando...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()