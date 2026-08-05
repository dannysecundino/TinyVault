import threading    # cuidar de concorrência de threads
import json         # persistência em disco

LOCK = threading.Lock()

# 1. acesso a dicionario

def set_bd(bd, chave, valor):
    with LOCK:
        bd[chave] = valor

def get_bd(bd, chave):
    with LOCK:
        if chave in bd:
            return bd[chave]
        else:
            return None

def del_bd(bd, chave):
    with LOCK:
        if chave in bd:
            del bd[chave]
            return True
        else:
            return False

# 2. persistência em disco

def pegar_json():
    with open("data/db.json", "r") as file:
        bd = json.load(file)
    return bd

def atualizar_json(bd):
    with LOCK:
        with open("data/db.json", "w") as file:
            json.dump(bd, file, indent=4, sort_keys=True)    # indent: para identar e ficar elegante // sort_keys: para ordenar alfabeticamente
