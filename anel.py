import threading

id_lider = 3

# Classe para representar um processo
class Processo:
    def __init__(self, id):
        self.id = id
        self.processos_indisponiveis = []  # Lista de processos indisponíveis
        self.ativo = True

    # Método para enviar uma mensagem para outro processo
    def enviar_mensagem(self, destinatario, mensagem):
        print(f"Processo {self.id}: Enviando mensagem para o processo {destinatario.id}: {mensagem}")
        if processos[id_lider].ativo == True:
            destinatario.receber_mensagem(mensagem)
        else:
            self.iniciar_eleicao()
            
        # Implemente aqui a lógica de envio da mensagem ao processo destinatário
        # Por exemplo, chamar o método receber_mensagem() do objeto do processo destinatário
        # Certifique-se de tratar de forma adequada a exclusão mútua ao acessar a id_lider do destinatário

        # Exemplo de implementação: chamar o método receber_mensagem() do objeto destinatário diretamente

    # Método para receber uma mensagem de outro processo

    def iniciar_eleicao(self):
        global id_lider

        for processo in processos:
            if processo.ativo == True and processo.id > id_lider:
                id_lider = processo.id
        
        print(f"O novo processo líder é : Processo {id_lider}")

#        if mensagem.startswith("eleicao:"):
#            mensagem_parts = mensagem.split(":")
#            if len(mensagem_parts) >= 2 and mensagem_parts[1]:
#                id_recebido = int(mensagem_parts[1])

#                if id_lider is None or id_recebido > id_lider:
#                    id_lider = id_recebido
#                    print(f"O novo processo líder é : Processo{id_lider}")
#                    return

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

# Configurar processos indisponíveis (exemplo: processo 1 está indisponível)
processos[1].processos_indisponiveis = [1]

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




# Definimos um líder inicial
# Eleição vai iniciar quando: Processos cairem.
# Caso o líder esteja inativo, faremos uma nova eleição.

#Como vai funcionar a eleição : Percorreremos o array de processos, e todos mandarão seu id, o maior id será o novo líder.
#Percorrer de trás pra frente, o maior id disponível sera o lider.
