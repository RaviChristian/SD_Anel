import threading
import time
import socket

id_lider = 3

class Processo:
    def __init__(self, id, ip, port):
        self.id = id
        self.ativo = True
        self.lider = None
        self.nextProcesso = None
        self.ip = ip
        self.port = port

    def enviar_mensagem(self, destinatario, mensagem):
        time.sleep(0.5)
        if destinatario.lider == destinatario.id and not destinatario.ativo:
            print(f"Processo {self.id}: Enviando mensagem para o processo {destinatario.id}: {mensagem}")
            print(f"O processo {destinatario.id} é o líder e está inativo.")
            print("Iniciando uma nova eleição de líder \n")
            idEleicao = []
            idAlreadySent = []
            self.eleicao(idEleicao, idAlreadySent)
        print(f"Processo {self.id}: Enviando mensagem para o processo {destinatario.id}: {mensagem}")
        
        self.enviar_socket(destinatario.ip, destinatario.port, mensagem)

    def eleicao(self, candidatos, alreadySentList):
        if self.id in alreadySentList:
            novoLider = max(candidatos)
            print(f"Eleição completa, o novo líder é: {novoLider}")
            self.lider = novoLider
            setLiderList = [self.id]
            self.setLider(novoLider, setLiderList)
            return

        alreadySentList.append(self.id)

        if self.ativo:
            candidatos.append(self.id)

        processos[self.nextProcesso].eleicao(candidatos, alreadySentList)

    def setLider(self, mensagem, alreadySet):
        alreadySetList = alreadySet

        for ids in alreadySet:
            if self.id == ids:
                return

        self.lider(mensagem)
        alreadySetList.append(self.id)
        self.nextProcesso.setLider(mensagem, alreadySetList)

    def receber_mensagem(self, mensagem):
        time.sleep(0.5)
        if mensagem == "Iniciando Thread":
            print(f"Processo {self.id}: Iniciando Thread")
            return
        print(f"Processo {self.id}: Recebendo mensagem: {mensagem} \n")

    def enviar_socket(self, ip, port, mensagem):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((ip, port))
                s.sendall(mensagem.encode())
            except Exception as e:
                print(f"Erro ao enviar mensagem para o processo {self.id}: {str(e)}")

def receber_socket(processo, conn):
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            mensagem = data.decode()
            processo.receber_mensagem(mensagem)

num_processos = 5
processos = [
    Processo(0, "localhost", 5000),
    Processo(1, "localhost", 5001),
    Processo(2, "localhost", 5002),
    Processo(3, "localhost", 5003),
    Processo(4, "localhost", 5004)
]
for i in range(len(processos)):
    processos[i].nextProcesso = (i + 1) % len(processos)
    processos[i].lider = id_lider

threads = []
for processo in processos:
    thread = threading.Thread(target=processo.receber_mensagem, args=("Iniciando Thread",))
    thread.start()
    threads.append(thread)
    time.sleep(0.5)

print("\n")
time.sleep(1)

def start_server(processo):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((processo.ip, processo.port))
        s.listen()
        while True:
            conn, addr = s.accept()
            threading.Thread(target=receber_socket, args=(processo, conn)).start()

for processo in processos:
    threading.Thread(target=start_server, args=(processo,)).start()

processo_envia = 2
processo_recebe = 4
processos[processo_envia].enviar_mensagem(processos[processo_recebe], f"Oi processo {processo_recebe}")

processos[3].ativo = False

processo_envia = 2
processo_recebe = 1
processos[processo_envia].enviar_mensagem(processos[processo_recebe], f"Oi processo {processo_recebe}")

processo_envia = 3
processo_recebe = 2
processos[processo_envia].enviar_mensagem(processos[processo_recebe], f"Oi processo {processo_recebe}")

processo_envia = 2
processo_recebe = 3
processos[processo_envia].enviar_mensagem(processos[processo_recebe], f"Oi processo {processo_recebe}")
