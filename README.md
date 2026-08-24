# Tiny Vault

Banco de dados educacional chave-valor, feito em Python puro.

Servidor de armazenamento chave-valor multi-cliente, construído inteiramente sobre a biblioteca padrão do Python (`socket`, `threading`, `json`), sem frameworks ou dependências externas. O protocolo de comandos é próprio, inspirado no [Redis](https://redis.io), mas implementado do zero como exercício de redes de computadores, concorrência e arquitetura de sistemas.

> Redis é uma marca registrada da Redis Ltd. Este projeto não possui afiliação, patrocínio ou endosso da Redis Ltd.; a referência é apenas conceitual.

---

## Stack

- **Python 3**, apenas biblioteca padrão
- `socket` — camada de transporte TCP
- `threading` — concorrência (thread por conexão) e exclusão mútua (`Lock`)
- `json` — serialização do estado do banco para disco

Nenhuma dependência externa. Todo o comportamento de rede, protocolo e persistência foi escrito manualmente, sem bibliotecas como `asyncio`, `socketserver` ou ORMs.

---

## Como rodar

Copie todo o repositório (a pasta `data`, por exemplo, é essencial por contar com o `.json` que guarda o banco de dados do servidor).

Navegue até a pasta `server/` e rode o servidor com:

```bash
python3 main.py
```

O servidor escuta em `127.0.0.1:9090`. Conecte com qualquer cliente TCP (por exemplo, o netcat):

```bash
nc 127.0.0.1 9090
```

Múltiplos clientes podem conectar ao mesmo tempo; cada conexão é atendida numa thread própria.

---

## Comandos

| Comando | Descrição |
|---|---|
| `\set <chave> <valor>` | Armazena um valor associado a uma chave |
| `\get <chave>` | Recupera o valor de uma chave |
| `\del <chave>` | Remove uma chave |
| `\swap <chave_1> <chave_2>` | Troca os valores entre duas chaves |
| `\rename <chave_antiga> <chave_nova>` | Renomeia uma chave |
| `\exists <chave>` | Checa a existência de uma chave |
| `\list` | Lista todas as chaves armazenadas |
| `\copy <chave_existente> <chave_nova>` | Copiar o valor de uma chave existente para uma nova chave |
| `\clear` | Limpa a tela do terminal |
| `\help` | Mostra os comandos disponíveis |
| `\exit` | Encerra a conexão |

Valores com espaço são suportados (`\set nome Danny Secundino` grava `"Danny Secundino"` inteiro); o parser que se encontra em `commands.py` trata tudo após a chave como valor.

---

## Arquitetura

| Módulo | Responsabilidade |
|---|---|
| `main.py` | Ponto de entrada: carrega o estado do disco (`db.pegar_json()`), sobe o socket de escuta, aceita conexões em loop e delega cada uma a uma thread. Trata `KeyboardInterrupt` para persistir o estado antes de encerrar. |
| `network.py` | Socket de escuta, leitura/escrita de dados brutos, e o handler `atender_client` que roda dentro da thread de cada cliente. |
| `commands.py` | Parsing e execução dos comandos do protocolo. |
| `db_operations.py` | Acesso ao dicionário compartilhado (protegido por um `threading.Lock` global) e toda a persistência em disco (`pegar_json`/`atualizar_json`). |

### Concorrência: thread por conexão

Cada cliente que conecta ganha sua própria thread (`threading.Thread(target=net.atender_client, ...)`), em vez de um loop de eventos (`select`/`epoll`) monitorando todos os sockets num único thread. É o modelo mais simples de implementar corretamente e o ponto de partida natural pra entender concorrência em servidores de rede, embora não escale tão bem quanto um event loop pra um número muito grande de conexões simultâneas (cada thread tem custo de memória e o SO precisa fazer context switch entre elas).

### Exclusão mútua: lock global no dicionário

Como múltiplas threads podem ler e escrever o mesmo dicionário ao mesmo tempo, todo acesso passa por um único `threading.Lock()` (`db_operations.LOCK`), garantindo que operações de `set`/`get`/`del` nunca aconteçam simultaneamente e corrompam o estado. É uma solução de granularidade grossa: correta e simples, mas serializa todo acesso ao banco, mesmo entre chaves diferentes que não têm relação nenhuma entre si. Um lock por chave (ou uma estrutura lock-free) daria mais paralelismo, mas exigiria bem mais cuidado pra não introduzir condições de corrida sutis.

### Persistência: snapshot em JSON a cada alteração

O estado é carregado de `data/db.json` na subida do servidor (`db.pegar_json()`) e salvo de volta sempre que o banco sofre alguma alteração (`\set` ou `\del`), via `db.atualizar_json(bd)`, que está inevitavelmente sujeito, em suas chamadas, o mesmo lock das operações normais pra garantir que nenhuma escrita concorrente aconteça durante o dump. Essa é uma estratégia que veio para substituir uma ideia de snapshot simples, não durável, em que a atualização do `.json` era feita somente se o servidor caísse por um `KeyboardInterrupt`. Essa não era uma boa estratégia, já que, se o processo caísse de forma anormal (kill -9, queda de energia, crash), as alterações desde a última subida se perderiam.

---

## Competências demonstradas

- Programação de sockets TCP (`socket.AF_INET`, `SOCK_STREAM`, `bind`/`listen`/`accept`)
- Concorrência: modelo thread-per-connection e sincronização com `Lock`
- Design de protocolo de aplicação orientado a texto, incluindo parsing de argumentos com espaço
- Serialização e persistência de estado com `json`
- Organização de software em módulos com responsabilidades bem separadas

---

## Roteiro

- [x] Servidor single-client com `\set`/`\get`/`\del`
- [x] Listagem de chaves e sistema de ajuda
- [x] Suporte a múltiplos clientes simultâneos (thread por conexão)
- [x] Persistência em disco (snapshot em JSON ao alterar)
- [ ] Expiração automática de chaves (TTL)
- [ ] Testes automatizados
- [ ] Novos comandos
