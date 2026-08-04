import network as net
import threading

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
    
    th = threading.Thread(target = net.atender_client, args=(csock, bd))
    th.start()
lsock.close()

