import commands as cmd
import network as net

HOST = "127.0.0.1"
PORT = 9090

# banco de dados
bd = dict()

# socket de escuta
lsock = net.criar_socket_escuta(HOST, PORT)

# laco principal
while True:
    # aceitar client
    csock, client_addr = lsock.accept()
    print(f">> server connected to {client_addr}")
    
    # se comunicando com o client
    net.enviar_saida(csock, "\033[H\033[J".encode("utf-8"))  # ANSI escape code to clear the screen
    net.enviar_saida(csock, ">> Welcome to the Redis server! (type \\help for available commands)\n".encode("utf-8"))
    sair = False
    while not sair:
        comando = net.receber_comando(csock)

        if not comando:  # lista vazia = cliente desconectou
            break
        
        saida = cmd.execute(bd, comando)
        net.enviar_saida(csock, str(saida).encode("utf-8"))
        if saida == ">> See you later!\n":
            sair = True
    csock.close()
lsock.close()

