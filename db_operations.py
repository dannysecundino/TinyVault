def set_bd(bd, chave, valor):
    bd[chave] = valor

def get_bd(bd, chave):
    if chave in bd:
        return bd[chave]
    else:
        return None

def del_bd(bd, chave):
    if chave in bd:
        del bd[chave]
        return True
    else:
        return False
