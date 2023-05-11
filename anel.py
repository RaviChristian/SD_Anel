import socket

# Define o endereço IP e a porta usada para a comunicação
IP = '127.0.0.1'
PORT = 5000

# Define a estrutura de dados para representar um processo
class Process:
    def __init__(self, id, ip, port):
        self.id = id
        self.ip = ip
        self.port = port
        self.leader = None  # armazena o id do processo líder

        # Inicializa o socket TCP/IP para o processo
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(1)


# Define uma lista encadeada circular de processos
processes = [
    Process(0, IP, PORT),
    Process(1, IP, PORT + 1),
    Process(2, IP, PORT + 2),
    Process(3, IP, PORT + 3)
]

# Define a função para enviar uma mensagem para o próximo processo no anel
def send_message(msg, next_process):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((next_process.ip, next_process.port))
    sock.send(msg.encode())
    sock.close()

# Define a função para receber e processar uma mensagem recebida
def process_message(msg, process):
    if msg.startswith("original"):
        next_process = processes[(process.id + 1) % len(processes)]
        send_message(msg, next_process)

    elif msg.startswith("election"):
        initiator_id = int(msg.split(":")[1])
        if initiator_id > process.id:
            # passa a mensagem de eleição para o próximo processo no anel
            next_process = processes[(process.id + 1) % len(processes)]
            send_message(msg, next_process)
        elif initiator_id < process.id:
            # se o número do processo iniciador for menor, se declara como líder
            process.leader = process.id
            # envia mensagem de confirmação para o próximo processo no anel
            leader_msg = f"leader:{process.id}"
            next_process = processes[(process.id + 1) % len(processes)]
            send_message(leader_msg, next_process)
        else:
            # o processo iniciador completou a volta no anel, se declara como líder
            process.leader = process.id
            # envia mensagem de confirmação para todos os outros processos no anel
            for p in processes:
                if p.id != process.id:
                    leader_msg = f"leader:{process.id}"
                    send_message(leader_msg, p)

    elif msg.startswith("leader"):
        leader_id = int(msg.split(":")[1])
        if leader_id == process.id:
            # processo reconhece que é o líder
            process.leader = process.id
        else:
            # passa a mensagem de confirmação para o próximo processo no anel
            next_process = processes[(process.id + 1) % len(processes)]
            send_message(msg, next_process)

    def send_election_message(next_process):
        msg = f"ELECTION {process.id}"
        send_message(msg, next_process)
# Define o loop principal do processo
while True:
    # Aguarda a chegada de uma conexão de entrada
    conn, addr = s.accept()

    # Recebe a mensagem enviada pelo processo vizinho
    msg = conn.recv(1024).decode()

    # Processa a mensagem recebida
    process_message(msg, processes[0])
    # Envia mensagem de eleição para o primeiro processo no anel
    send_election_message(processes[1])

    # Aguarda até que o líder seja definido
    while True:
        if processes[0].leader is not None:
            print(f"Processo {processes[0].id} é o líder.")
            break

    # Fecha a conexão de entrada
    conn.close()
