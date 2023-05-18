import threading

id_lider = 3

# Classe para representar um processo
class Processo:
    def __init__(self, id):
        self.id = id
        self.processos_indisponiveis = []
        self.ativo = True

    # Método para enviar uma mensagem para outro processo
    def enviar_mensagem(self, destinatario, mensagem):
        print(f"Processo {self.id}: Enviando mensagem para o processo {destinatario.id}: {mensagem}")
        if processos[id_lider].ativo == True:
            destinatario.receber_mensagem(mensagem)
        else:
            self.iniciar_eleicao()
            

    def iniciar_eleicao(self):
        global id_lider

        for processo in processos:
            if processo.ativo == True and processo.id > id_lider:
                id_lider = processo.id
        
        print(f"O novo processo líder é : Processo {id_lider}")


    def receber_mensagem(self, mensagem):
        global id_lider

        if mensagem == "Iniciando Thread":
            print(f"Processo {self.id}: Iniciando Thread \n")
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

# Aguardar o término de todas as threads
for thread in threads:
    thread.join()

# Iniciar o algoritmo de eleição a partir de um processo
processo_inicial = 2
print("lider atual: ",id_lider)
processos[processo_inicial].enviar_mensagem(processos[processo_inicial], f"Oi processo {processo_inicial}")

processos[id_lider].ativo = False
processos[processo_inicial].enviar_mensagem(processos[processo_inicial], f"Oi processo {processo_inicial}")
print("lider atual: ",id_lider)

