import threading
import time
import Pyro4

id_lider = 3

@Pyro4.expose
class Processo:
    def __init__(self, id):
        self.id = id
        self.ativo = True
        self.lider = None
        self.nextProcesso = None

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
        destinatario.receber_mensagem(mensagem)

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

        nextProcesso = Pyro4.Proxy(f"PYRONAME:processo.{self.nextProcesso}")
        nextProcesso.eleicao(candidatos, alreadySentList)

    def setLider(self, mensagem, alreadySet):
        alreadySetList = alreadySet

        for ids in alreadySet:
            if self.id == ids:
                return

        self.lider(mensagem)
        alreadySetList.append(self.id)
        nextProcesso = Pyro4.Proxy(f"PYRONAME:processo.{self.nextProcesso}")
        nextProcesso.setLider(mensagem, alreadySetList)

    def receber_mensagem(self, mensagem):
        time.sleep(0.5)
        if mensagem == "Iniciando Thread":
            print(f"Processo {self.id}: Iniciando Thread")
            return
        print(f"Processo {self.id}: Recebendo mensagem: {mensagem} \n")

# Configuração do servidor Pyro4
def setup_pyro4_server(processo):
    daemon = Pyro4.Daemon()
    uri = daemon.register(processo)
    ns = Pyro4.locateNS()
    ns.register(f"processo.{processo.id}", uri)
    print(f"Processo {processo.id}: Servidor Pyro4 iniciado.")
    daemon.requestLoop()

num_processos = 5
processos = [Processo(id) for id in range(num_processos)]

for i in range(len(processos)):
    processos[i].nextProcesso = (i + 1) % len(processos)
    processos[i].lider = id_lider

threads = []
for processo in processos:
    thread = threading.Thread(target=setup_pyro4_server, args=(processo,))
    thread.start()
    threads.append(thread)
    time.sleep(0.5)

print("\n")
time.sleep(1)

processo_envia = 2
processo_recebe = 4
processos[processo_envia].enviar_mensagem(processos[processo_recebe], f"Oi processo {processo_recebe}")

processos[3].ativo = False
processos[4].ativo = False

processo_envia = 2
processo_recebe = 1
processos[processo_envia].enviar_mensagem(processos[processo_recebe], f"Oi processo {processo_recebe}")

processo_envia = 3
processo_recebe = 2
processos[processo_envia].enviar_mensagem(processos[processo_recebe], f"Oi processo {processo_recebe}")

processo_envia = 2
processo_recebe = 3
processos[processo_envia].enviar_mensagem(processos[processo_recebe], f"Oi processo {processo_recebe}")
