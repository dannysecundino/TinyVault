# Tiny Vault

Banco de dados educacional chave-valor, feito em Python puro.

Um servidor de armazenamento chave-valor em memória, com protocolo de comandos e camada de rede escritos do zero usando a biblioteca `socket` padrão do Python, sem frameworks nem dependências externas. Inspirado no [Redis](https://redis.io), como exercício de arquitetura de sistemas: protocolo próprio, servidor e persistência.

> Redis é uma marca registrada da Redis Ltd. Este projeto não tem afiliação, patrocínio ou endosso da Redis Ltd.; a menção é apenas referencial.

## Como rodar

```bash
python3 server.py
```

O servidor sobe em `127.0.0.1:9090` por padrão. Conecte com qualquer cliente TCP, por exemplo `netcat`:

```bash
nc 127.0.0.1 9090
```

## Comandos

| Comando | Descrição |
|---|---|
| `\set <chave> <valor>` | Grava um valor associado a uma chave |
| `\get <chave>` | Retorna o valor de uma chave |
| `\del <chave>` | Remove uma chave |
| `\list` | Lista todas as chaves armazenadas |
| `\clear` | Limpa a tela do terminal |
| `\help` | Mostra a lista de comandos disponíveis |
| `\exit` | Encerra a conexão |

## Arquitetura

O projeto é dividido em três módulos:

- **`network.py`** — criação do socket de escuta, aceitação de conexões e envio/recebimento de dados brutos.
- **`commands.py`** — parsing e execução dos comandos do protocolo.
- **`db_operations.py`** — operações sobre o armazenamento em memória (atualmente um `dict` do Python).

## Roteiro

- [x] Servidor single-client com `SET`/`GET`/`DEL`
- [ ] Suporte a múltiplos clientes simultâneos
- [ ] Persistência em disco
- [ ] Expiração de chaves (TTL)

## Licença

MIT.
