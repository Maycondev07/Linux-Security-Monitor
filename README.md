# Linux Security Monitor

Monitoramento e análise de eventos de autenticação do Ubuntu Server utilizando Python.

## Sobre o projeto

Este projeto lê o arquivo de autenticação do Linux (`/var/log/auth.log`), identifica eventos relevantes e gera um relatório em texto. Foi desenvolvido como projeto de aprendizado de Python, Linux e fundamentos de cibersegurança.

## Funcionalidades

- Identifica autenticações SSH aprovadas (`Accepted password`).
- Identifica tentativas SSH recusadas (`Failed password`).
- Identifica falhas de autenticação local (`authentication failure`).
- Registra eventos de abertura de sessão do sudo.
- Extrai usuário, IP e porta de origem dos eventos SSH reconhecidos.
- Conta autenticações SSH aprovadas por endereço IP.
- Gera o relatório `log.txt`.

## Requisitos

- Ubuntu ou outra distribuição Linux que registre autenticações em `/var/log/auth.log`.
- Python 3.
- Permissão de leitura do arquivo de log.

O projeto utiliza apenas a biblioteca padrão do Python; não há dependências externas.

## Como executar

Clone o repositório:

```bash
git clone https://github.com/Maycondev07/Linux-Security-Monitor.git
cd Linux-Security-Monitor
```

Execute com permissões para ler o log:

```bash
sudo python3 create.py
```

O relatório será salvo como `log.txt` no diretório em que o programa for executado. A cada execução, o relatório é recriado para evitar misturar resultados de execuções anteriores.

## Observações

- O formato e a disponibilidade de `/var/log/auth.log` dependem da distribuição e da configuração do sistema.
- Nem todo evento de falha contém um endereço IP. Falhas locais, como autenticações no terminal ou uso do sudo, são registradas separadamente.
- Endereços como `192.168.x.x` são privados e representam a origem dentro da rede local.
- O relatório pode conter nomes de usuários e endereços IP. Não publique logs reais sem revisar e remover informações sensíveis.
- A contagem atual resume os eventos de autenticação SSH aprovados encontrados no arquivo durante aquela execução; não é um contador persistente em tempo real.

## Estrutura

```text
Linux-Security-Monitor/
├── create.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Próximos passos

- Ampliar a classificação de eventos SSH.
- Adicionar estatísticas de falhas por IP.
- Criar testes com amostras de logs anonimizadas.

## Autor

[Maycondev07](https://github.com/Maycondev07)
