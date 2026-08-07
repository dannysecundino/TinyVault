import db_operations as db
import network as net
import threading

HOST = "127.0.0.1"
PORT = 9090

if __name__ == "__main__":          # isso serve para que essa parte rode só se este arquivo for rodado como o principal
    # banco de dados
    bd = db.pegar_json()

    # socket de escuta
    lsock = net.criar_socket_escuta(HOST, PORT)

    # laco principal
    while True:
        # aceitar client
        csock, client_addr = lsock.accept()
        print(f">> server connected to {client_addr}")

        # abrir uma thread
        th = threading.Thread(target = net.atender_client, args=(csock, bd))
        th.start()
    lsock.close()
