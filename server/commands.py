import db_operations as db

cabecalho = "\033[94m" + r""" _________  ___  ________       ___    ___      ___      ___ ________  ___  ___  ___   _________   
|\___   ___\\  \|\   ___  \    |\  \  /  /|    |\  \    /  /|\   __  \|\  \|\  \|\  \ |\___   ___\ 
\|___ \  \_\ \  \ \  \\ \  \   \ \  \/  / /    \ \  \  /  / | \  \|\  \ \  \\\  \ \  \\|___ \  \_| 
     \ \  \ \ \  \ \  \\ \  \   \ \    / /      \ \  \/  / / \ \   __  \ \  \\\  \ \  \    \ \  \  
      \ \  \ \ \  \ \  \\ \  \   \/  /  /        \ \    / /   \ \  \ \  \ \  \\\  \ \  \____\ \  \ 
       \ \__\ \ \__\ \__\\ \__\__/  / /           \ \__/ /     \ \__\ \__\ \_______\ \_______\ \__\
        \|__|  \|__|\|__| \|__|\___/ /             \|__|/       \|__|\|__|\|_______|\|_______|\|__|
                              \|___|/                                                              
""" + "\033[90m" + "Welcome to the Tiny Vault server! (type \\help for available commands)\n" + "\033[0m"

# funções auxiliares
def eh_argumento_unico_ou_vazio(com):
    if len(com) <= 2:
        return True
    else:
        return False

def tratar_comando(com):
    if eh_argumento_unico_ou_vazio(com):
        return

    valor = ""
    for i in range(2, len(com)):
        valor = valor + com[i]
        if i != len(com) - 1:
            valor = valor + " "

    com[2] = valor

    # atualizar com para conter apenas os 3 primeiros elementos
    atualizado_com = []
    for i in range(3):
        atualizado_com.append(com[i])
    com.clear()
    for i in range(len(atualizado_com)):
        com.append(atualizado_com[i])

# funções dos comandos
def _set(bd, com):
    saida = ""
    if len(com) < 3:
        saida = ">> Invalid command\n"
    else:
        chave = com[1]
        valor = com[2]
        db.set_bd(bd, chave, valor)
        saida = ">> Value set\n"

    return saida

def _get(bd, com):
    saida = ""
    
    if len(com) < 2:
        saida = ">> Invalid command\n"
    else:
        chave = com[1]
        valor = db.get_bd(bd, chave)
        if valor is not None:
            saida = f">> {valor}\n"
        else:
            saida = ">> Key not found\n"

    return saida

def _del (bd, com):
    saida = ""

    if len(com) < 2:
        saida = ">> Invalid command\n"
    else:
        chave = com[1]
        sucesso = db.del_bd(bd, chave)
        if sucesso:
            saida = ">> Key deleted\n"
        else:
            saida = ">> Key not found\n"

    return saida

def _list(bd):
    saida = ">> Keys in the database:\n"
    for chave in bd.keys():
        saida += f"   {chave}\n"
    return saida

def _exit ():
    saida = ">> See you later!\n"
    return saida

def _clear():
    saida = "\033[H\033[J" + cabecalho  # \033[H\033[J -> ANSI escape code to clear the screen
    return saida

def _rename(bd, com):
    saida = ""

    if len(com) < 3:
        saida = ">> Invalid command\n"
    else:
        chave_antiga = com[1]
        chave_nova = com[2]

        valor = db.get_bd(bd, chave_antiga)
        if valor == None:
            saida = f">> The key \"{chave_antiga}\" is not registered\n"
        else:
            sucesso = db.del_bd(bd, chave_antiga)       # é desnecessário guardar o sucesso, mas guardei só para fazer jus ao retorno da função
            db.set_bd(bd, chave_nova, valor)
            saida = ">> Key updated successfully\n"

    return saida

def _exists(bd, com):
    saida = ""

    chave = com[1]
    if chave in bd:
        saida = ">> YES (this key exists)\n"
    else:
        saida = ">> NO (this key doesn't exists)\n"

    return saida

def _help():
    saida = ">> Available commands:\n"
    saida += "   \\set <key> <value> - Set a value for a key\n"
    saida += "   \\get <key> - Get the value of a key\n"
    saida += "   \\del <key> - Delete a key\n"
    saida += "   \\rename <old_key> <new_key> - Rename a key\n"
    saida += "   \\exists <key> - Checks if the key exists\n"
    saida += "   \\list - List all keys in the database\n"
    saida += "   \\exit - Exit the server\n"
    saida += "   \\clear - Clear the screen\n"
    saida += "   \\help - Show this help message\n"

    return saida

def _cmdnotfound():
    saida = ">> Invalid command\n"
    return saida

# função execute
def execute(bd, com):
    print("Debug", repr(com))       # repr() retorna a representação oficial ("nua e crua") daquele objeto

    tratar_comando(com)

    saida = ""
    operacao = com[0]

    match operacao:
        case "\\set":
            saida = _set (bd, com)

        case "\\get":
            saida = _get(bd, com)

        case "\\del":
            saida = _del(bd, com)

        case "\\list":
            saida = _list(bd)

        case "\\exit":
            saida = _exit()

        case "\\clear":
            saida = _clear()

        case "\\rename":
            saida = _rename(bd, com)

        case "\\exists":
            saida = _exists(bd, com)
            
        case "\\help":
            saida = _help()

        case _:
            saida = _cmdnotfound()

    saida = "\033[3;36m" + saida + "\033[0m"      # para ficar colorido

    return saida