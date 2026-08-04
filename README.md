# Tiny Vault

Banco de dados educacional chave-valor, desenvolvido em Python puro.

O Tiny Vault é um servidor de armazenamento chave-valor em memória construído utilizando apenas a biblioteca padrão do Python. O objetivo do projeto é servir como ferramenta de estudo para compreender, na prática, conceitos de programação em Python, redes de computadores e arquitetura cliente-servidor.

A comunicação entre cliente e servidor é implementada diretamente sobre sockets TCP, sem frameworks ou dependências externas, utilizando um protocolo de comandos simples inspirado no Redis.

> Redis é uma marca registrada da Redis Ltd. Este projeto não possui qualquer afiliação, patrocínio ou endosso da Redis Ltd.; a referência é utilizada apenas para fins educacionais.

---

## Objetivos

Este projeto foi desenvolvido com foco em aprendizado, buscando aplicar conhecimentos em:

- programação em Python;
- programação orientada a módulos;
- comunicação em redes utilizando sockets TCP;
- arquitetura cliente-servidor;
- desenvolvimento de protocolos de aplicação;
- manipulação de estruturas de dados em memória.

Além de consolidar conceitos de Redes de Computadores, o projeto também contribui para o desenvolvimento de familiaridade com a biblioteca padrão do Python, demonstrando que é possível implementar aplicações de rede completas sem recorrer a bibliotecas externas.

---

## Como rodar

Inicie o servidor:

```bash
python3 server.py
```

O servidor escutará em:

```
127.0.0.1:9090
```

Para conectar, utilize qualquer cliente TCP, por exemplo o Netcat:

```bash
nc 127.0.0.1 9090
```

---

## Comandos disponíveis

| Comando | Descrição |
|---------|-----------|
| `\set <chave> <valor>` | Armazena um valor associado a uma chave |
| `\get <chave>` | Recupera o valor armazenado |
| `\del <chave>` | Remove uma chave do banco |
| `\list` | Lista todas as chaves existentes |
| `\clear` | Limpa a tela do terminal |
| `\help` | Exibe os comandos disponíveis |
| `\exit` | Encerra a conexão com o servidor |

---

## Arquitetura

O projeto está organizado em módulos independentes, cada um responsável por uma parte da aplicação.

### `server.py`

Responsável pelo ciclo de vida do servidor:

- criação do socket de escuta;
- aceitação de conexões TCP;
- recebimento dos comandos enviados pelo cliente;
- envio das respostas.

### `network.py`

Implementa toda a camada de comunicação da aplicação:

- criação do socket TCP;
- envio e recebimento de mensagens;
- abstração da comunicação entre cliente e servidor.

### `commands.py`

Implementa o protocolo de comandos.

É responsável por:

- interpretar a entrada recebida;
- validar argumentos;
- executar cada operação;
- produzir a resposta enviada ao cliente.

### `db_operations.py`

Camada de acesso ao armazenamento.

Atualmente utiliza um `dict` do Python como banco de dados em memória, encapsulando operações de inserção, consulta e remoção.

---

## Conceitos aplicados

Durante o desenvolvimento foram utilizados diversos conceitos estudados em disciplinas de programação e redes, como:

- sockets TCP (`socket.AF_INET` e `SOCK_STREAM`);
- comunicação cliente-servidor;
- protocolo de aplicação baseado em texto;
- parsing de comandos;
- abstração por módulos;
- manipulação de estruturas de dados (`dict`);
- tratamento de conexões;
- organização de software.

Embora simples, o projeto reproduz parte da lógica encontrada em servidores reais, permitindo compreender o fluxo de comunicação entre aplicações distribuídas.

---

## Próximos passos

- [x] Servidor single-client
- [x] Comandos `SET`, `GET`, `DEL`
- [x] Listagem de chaves
- [x] Sistema de ajuda
- [ ] Suporte a múltiplos clientes simultaneamente
- [ ] Persistência em disco
- [ ] Expiração automática de chaves (TTL)
- [ ] Testes automatizados
- [ ] Implementação de novos comandos

---

## Licença

Este projeto está licenciado sob a licença **MIT**.
