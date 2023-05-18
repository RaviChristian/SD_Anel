import threading
import time

id_lider = 3

# Classe para representar um processo
class Processo:
    def __init__(self, id):
        self.id = id
        self.processos_indisponiveis = []
        self.ativo = True

    # Método para enviar uma mensagem para outro processo
    def enviar_mensagem(self, destinatario, mensagem):
        time.sleep(0.5)
        print(f"Processo {self.id}: Enviando mensagem para o processo {destinatario.id}: {mensagem}")
        if processos[id_lider].ativo == True:
            destinatario.receber_mensagem(mensagem)
        else:
            print(f"O processo {destinatario.id} não pode receber a mensagem, pois o líder está inativo.")
            print("Iniciando uma nova eleição de líder \n")
            self.iniciar_eleicao()
            

    def iniciar_eleicao(self):
        global id_lider

        for processo in processos:
            if processo.ativo == True and processo.id > id_lider:
                id_lider = processo.id
        
        print(f"O novo processo líder é : Processo {id_lider}\n")


    def receber_mensagem(self, mensagem):
        time.sleep(0.5)
        global id_lider

        if mensagem == "Iniciando Thread":
            print(f"Processo {self.id}: Iniciando Thread")
            return
        
        print(f"Processo {self.id}: Recebendo mensagem: {mensagem} \n")



# Número de processos no anel
num_processos = 5

# Criar os objetos de processo
processos = [Processo(id) for id in range(num_processos)]

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

processos[id_lider].ativo = False

processo_envia = 2
processo_recebe = 1

processos[processo_envia].enviar_mensagem(processos[processo_recebe], f"Oi processo {processo_recebe}")
#print("lider atual: ",id_lider)


processo_envia = 3
processo_recebe = 2

processos[processo_envia].enviar_mensagem(processos[processo_recebe], f"Oi processo {processo_recebe}")
#print("lider atual: ",id_lider)