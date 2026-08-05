from locktreatment.lock import LOCK          # tem que ser o mesmo LOCK para toda thread
import network as net
import threading
import json

HOST = "127.0.0.1"
PORT = 9090

# banco de dados
with open("database/db.json", "r") as file:
    bd = json.load(file)

# socket de escuta
lsock = net.criar_socket_escuta(HOST, PORT)

try:                        # o servidor rodando
    # laco principal
    while True:
        # aceitar client
        csock, client_addr = lsock.accept()
        print(f">> server connected to {client_addr}")

        # abrir uma thread
        th = threading.Thread(target = net.atender_client, args=(csock, bd))
        th.start()
except KeyboardInterrupt:   # quando o servidor for derrubado (ctrl+C), queremos que ele salve o banco de dados
    with LOCK:
        with open("database/db.json", "w") as file:
            json.dump(bd, file, indent=4, sort_keys=True)    # indent: para identar e ficar elegante // sort_keys: para ordenar alfabeticamente
finally:
    lsock.close()

