import socket

# comunicacao com o client
def criar_socket_escuta(host, port):
    socket_escuta = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_escuta.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_escuta.bind((host, port))
    socket_escuta.listen(1)

    print(">> server is ready to connect\n")

    return socket_escuta

def receber_comando(sock):
    sock.sendall(b">> ")
    com = sock.recv(1024).decode("utf-8").split()

    return com

def enviar_saida(sock, saida):
    sock.sendall(saida)