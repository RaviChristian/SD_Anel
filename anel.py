import threading
import time

id_lider = 3

# Classe para representar um processo
class Processo:
    def __init__(self, id):
        self.id = id
        self.ativo = True
        self.lider = None
        self.nextProcesso = None

    # Método para enviar uma mensagem para outro processo
    def enviar_mensagem(self, destinatario, mensagem):
        time.sleep(0.5)
        if destinatario.lider == destinatario.id and destinatario.ativo == False:
            print(f"Processo {self.id}: Enviando mensagem para o processo {destinatario.id}: {mensagem}")
            print(f"O processo {destinatario.id} é o lider e está inativo.")
            print("Iniciando uma nova eleição de líder \n")
            idEleicao = []
            idAlreadySent = []   
            self.eleicao(idEleicao,idAlreadySent)
            
        print(f"Processo {self.id}: Enviando mensagem para o processo {destinatario.id}: {mensagem}")


    def eleicao(self,candidatos,alreadySentList):
        if self.id in alreadySentList:
            novoLider = max(candidatos)
            print(f"Eleição completa, o novo lider é : {novoLider}")
            self.lider = novoLider
            setLiderList = [self.id]
            self.setLider(novoLider,setLiderList)
            return

        alreadySentList.append(self.id)

        if self.ativo == True:
            candidatos.append(self.id)
        
        processos[self.nextProcesso].eleicao(candidatos,alreadySentList)

    def setLider(self,mensagem,alreadySet):
        alreadySetList = alreadySet

        for ids in alreadySet:
            if self.id == ids:
                return
        
        self.lider(mensagem)
        alreadySetList.append(self.id)
        self.nextProcesso.setLider(mensagem,alreadySetList)

    def receber_mensagem(self, mensagem):

        time.sleep(0.5)

        if mensagem == "Iniciando Thread":
            print(f"Processo {self.id}: Iniciando Thread")
            return
        
        
            
        print(f"Processo {self.id}: Recebendo mensagem: {mensagem} \n")



# Número de processos no anel
num_processos = 5

# Criar os objetos de processo
processos = [Processo(id) for id in range(num_processos)]
for i in range(len(processos)):
    processos[i].nextProcesso = (i + 1) % len(processos)
    processos[i].lider = id_lider

# Iniciar as threads para cada processo
threads = []
for processo in processos:
    thread = threading.Thread(target=processo.receber_mensagem, args=("Iniciando Thread",))
    thread.start()
    threads.append(thread)
    time.sleep(0.5)

print("\n")
time.sleep(1)
# Iniciar o algoritmo de eleição a partir de um processo
processo_envia = 2
processo_recebe = 4
#print("lider atual: ",id_lider)
processos[processo_envia].enviar_mensagem(processos[processo_recebe], f"Oi processo {processo_recebe}")

processos[3].ativo = False
processos[4].ativo = False

processo_envia = 2
processo_recebe = 1

processos[processo_envia].enviar_mensagem(processos[processo_recebe], f"Oi processo {processo_recebe}")
#print("lider atual: ",id_lider)


processo_envia = 3
processo_recebe = 2

processos[processo_envia].enviar_mensagem(processos[processo_recebe], f"Oi processo {processo_recebe}")
#print("lider atual: ",id_lider)

processo_envia = 2
processo_recebe = 3

processos[processo_envia].enviar_mensagem(processos[processo_recebe], f"Oi processo {processo_recebe}")
#print("lider atual: ",id_lider)