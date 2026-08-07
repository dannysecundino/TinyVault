import db_operations as db

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
    
def execute(bd, com):
    tratar_comando(com)

    saida = ""
    operacao = com[0]

    if operacao == "\\set":
        if len(com) < 3:
            saida = ">> Invalid command\n"
        else:
            chave = com[1]
            valor = com[2]
            db.set_bd(bd, chave, valor)
            saida = ">> Value set\n"

    elif operacao == "\\get":
        if len(com) < 2:
            saida = ">> Invalid command\n"
        else:
            chave = com[1]
            valor = db.get_bd(bd, chave)
            if valor is not None:
                saida = f">> {valor}\n"
            else:
                saida = ">> Key not found\n"

    elif operacao == "\\del":
        if len(com) < 2:
            saida = ">> Invalid command\n"
        else:
            chave = com[1]
            sucesso = db.del_bd(bd, chave)
            if sucesso:
                saida = ">> Key deleted\n"
            else:
                saida = ">> Key not found\n"

    elif operacao == "\\list":
        saida = ">> Keys in the database:\n"
        for chave in bd.keys():
            saida += f"   {chave}\n"

    elif operacao == "\\exit":
        saida = ">> See you later!\n"

    elif operacao == "\\clear":
        saida = "\033[H\033[J"  # ANSI escape code to clear the screen

    elif operacao == "\\rename":
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

    elif operacao == "\\help":
        saida = ">> Available commands:\n"
        saida += "   \\set <key> <value> - Set a value for a key\n"
        saida += "   \\get <key> - Get the value of a key\n"
        saida += "   \\del <key> - Delete a key\n"
        saida += "   \\rename <old_key> <new_key> - Rename a key\n"
        saida += "   \\list - List all keys in the database\n"
        saida += "   \\exit - Exit the server\n"
        saida += "   \\clear - Clear the screen\n"
        saida += "   \\help - Show this help message\n"

    else:
        saida = ">> Invalid command\n"

    return saida