import socket
import commands as cmd

cabecalho = "\033[94m" + r""" _________  ___  ________       ___    ___      ___      ___ ________  ___  ___  ___   _________   
|\___   ___\\  \|\   ___  \    |\  \  /  /|    |\  \    /  /|\   __  \|\  \|\  \|\  \ |\___   ___\ 
\|___ \  \_\ \  \ \  \\ \  \   \ \  \/  / /    \ \  \  /  / | \  \|\  \ \  \\\  \ \  \\|___ \  \_| 
     \ \  \ \ \  \ \  \\ \  \   \ \    / /      \ \  \/  / / \ \   __  \ \  \\\  \ \  \    \ \  \  
      \ \  \ \ \  \ \  \\ \  \   \/  /  /        \ \    / /   \ \  \ \  \ \  \\\  \ \  \____\ \  \ 
       \ \__\ \ \__\ \__\\ \__\__/  / /           \ \__/ /     \ \__\ \__\ \_______\ \_______\ \__\
        \|__|  \|__|\|__| \|__|\___/ /             \|__|/       \|__|\|__|\|_______|\|_______|\|__|
                              \|___|/                                                              
""" + "\033[90m" + "Welcome to the Tiny Vault server! (type \\help for available commands)\n" + "\033[0m"


# comunicacao com o client
def criar_socket_escuta(host, port):
    socket_escuta = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_escuta.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_escuta.bind((host, port))
    socket_escuta.listen()                  # sem args: aceita várias pessoas

    print(">> server is ready to connect\n")

    return socket_escuta

def receber_comando(sock):
    sock.sendall(b">> ")
    com = sock.recv(1024).decode("utf-8").split()

    return com

def enviar_saida(sock, saida):
    sock.sendall(saida)

def atender_client(csock, bd):
    # se comunicando com o client
    enviar_saida(csock, "\033[H\033[J".encode("utf-8"))  # ANSI escape code to clear the screen
    enviar_saida(csock, cabecalho.encode("utf-8"))

    sair = False
    while not sair:
        comando = receber_comando(csock)

        if not comando:  # lista vazia: cliente desconectou
            break

        saida = cmd.execute(bd, comando)
        enviar_saida(csock, str(saida).encode("utf-8"))
        if saida == ">> See you later!\n":
            sair = True
    csock.close()

