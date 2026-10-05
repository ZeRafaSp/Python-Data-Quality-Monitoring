# Python Data Quality Monitoring

Projeto de monitoramento automatizado da qualidade de dados utilizando **Python**, **Pandas** e **PostgreSQL**.

O projeto simula um processo em que dados são recebidos periodicamente em um arquivo CSV, carregados em um banco de dados e posteriormente analisados para identificar problemas de qualidade.

A execução é automatizada pelo Windows Task Scheduler e gera logs, relatório do monitoramento e uma lista dos registros que apresentam problemas.

---

## Objetivo

Criar um processo simples de monitoramento capaz de identificar automaticamente problemas comuns em uma base de dados antes que ela seja utilizada para análises ou processos posteriores.

O projeto foi desenvolvido com foco em:

- Qualidade de dados
- Monitoramento
- Automação de processos
- Validação de dados
- Registro de logs
- Identificação de falhas

---

## Arquitetura

```text
                  CSV
                   │
                   ▼
          carregar_dados.py
                   │
                   ▼
              PostgreSQL
                   │
                   ▼
                main.py
                   │
          ┌────────┴────────┐
          ▼                 ▼
      Validações        Monitoramento
                            │
                            ▼
                  OK / ALERTA / FALHA
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
             Log        Relatório      CSV de
                                      problemas
```

---

## Tecnologias utilizadas

- Python
- Pandas
- PostgreSQL
- SQLAlchemy
- psycopg2
- python-dotenv
- Windows Task Scheduler
- Git / GitHub

---

## Estrutura do projeto

```text
python-data-monitoring/
│
├── data/
│   └── transacoes.csv
│
├── logs/
│   └── monitoramento.log
│
├── output/
│   ├── relatorio_monitoramento.txt
│   └── registros_com_problemas.csv
│
├── screenshots/
│
├── src/
│   ├── carregar_dados.py
│   └── main.py
│
├── .gitignore
├── executar_monitoramento.bat
└── README.md
```

> **Observação:** o arquivo `.env`, com as credenciais do banco, é criado apenas localmente e **não deve ser versionado** (ele está listado no `.gitignore`).

---

## Funcionamento

### 1. Ingestão dos dados

O arquivo `carregar_dados.py` realiza a leitura do CSV e carrega os dados no PostgreSQL.

Os dados são inicialmente lidos como texto para evitar que valores inválidos sejam alterados automaticamente durante a ingestão. Isso permite preservar dados como:

```text
2026-09-31
```

mesmo sendo uma data inválida.

Posteriormente, os campos numéricos são tratados antes da inserção no banco.

### 2. Monitoramento

O arquivo `main.py` consulta os dados armazenados no PostgreSQL e realiza as validações utilizando Pandas.

São verificadas as seguintes situações:

- Valores ausentes
- Registros duplicados
- Valores negativos
- Valores acima de um limite definido
- Status inválidos
- Datas inválidas

### 3. Classificação do monitoramento

Após as validações, o processo classifica o resultado em três situações:

| Status | Descrição |
|--------|-----------|
| **OK** | Nenhum problema encontrado. |
| **ALERTA** | Foram encontrados problemas que não são considerados críticos. |
| **FALHA** | Foram encontrados problemas críticos que precisam de atenção. |

Atualmente, **status ou datas inválidas** são considerados problemas críticos.

---

## Exemplo de resultado

Em uma das execuções do projeto foram analisados 26 registros:

```text
RELATÓRIO DE MONITORAMENTO
==========================

Registros analisados: 26
Quantidade de problemas: 9
Percentual de problemas: 34.62%

Valores ausentes: 4
Duplicidades: 1
Valores negativos: 1
Valores acima do limite: 1
Status inválidos: 1
Datas inválidas: 1

STATUS: FALHA

Problemas críticos:
Datas inválidas: 1
Status inválidos: 1

Problemas em alerta:
Valores ausentes: 4
Duplicidades: 1
Valores negativos: 1
Valores acima do limite: 1
```

Além do relatório, o sistema gera um CSV contendo os registros que apresentam problemas e o respectivo tipo de problema identificado.

---

## Automação

O projeto possui o arquivo `executar_monitoramento.bat`, que executa automaticamente as duas etapas:

1. Carregamento dos dados
2. Monitoramento

O processo pode ser executado manualmente ou configurado no **Windows Task Scheduler** para execução automática.

### Fluxo automatizado

```text
executar_monitoramento.bat
          │
          ▼
carregar_dados.py
          │
          ▼
PostgreSQL
          │
          ▼
main.py
          │
          ▼
Validações
          │
          ▼
Relatórios e logs
```

---

## Logs

Durante a execução, o sistema registra informações no arquivo `logs/monitoramento.log`.

Os logs permitem acompanhar:

- Início da execução
- Problemas encontrados
- Avisos de qualidade
- Resultado final do monitoramento

---

## Segurança

As credenciais do PostgreSQL são armazenadas em variáveis de ambiente através do arquivo `.env`.

Exemplo:

```env
DB_HOST=localhost
DB_PORT=5****
DB_NAME=data******
DB_USER=po*****
DB_PASSWORD=sua_senha
```

O arquivo `.env` está incluído no `.gitignore` para evitar que credenciais sejam enviadas para o GitHub.

---

## Como executar

### Pré-requisitos

- Python 3
- PostgreSQL
- Banco de dados `data_monitoring`
- Tabela `transacoes`

### Instalação das dependências

```bash
pip install pandas sqlalchemy psycopg2-binary python-dotenv
```

### Executar a carga

```bash
python src/carregar_dados.py
```

### Executar o monitoramento

```bash
python src/main.py
```

### Executar o processo completo

```bash
executar_monitoramento.bat
```

---

## Aprendizados

Durante o desenvolvimento deste projeto foram praticados conceitos de:

- Leitura e tratamento de dados com Pandas
- Validação de qualidade de dados
- Integração entre Python e PostgreSQL
- SQLAlchemy
- Tratamento de dados inválidos
- Monitoramento automatizado
- Geração de logs
- Geração de relatórios
- Automação com Windows Task Scheduler
- Uso de variáveis de ambiente
- Organização de projetos Python

---

## Possíveis evoluções

Algumas melhorias podem ser adicionadas futuramente:

- Armazenamento do histórico das execuções
- Dashboard de qualidade de dados
- Envio automático de notificações em caso de falha
- Mais regras de validação
- Monitoramento de múltiplas fontes de dados
- Histórico dos indicadores de qualidade

---

## Autor

**José Rafael Santos Pereira**

Analista de Dados | Business Intelligence | Data monitoring | Python | SQL | PostgreSQL

Projeto desenvolvido como parte do portfólio de estudos em Dados, Automação e Qualidade de Dados.

LinkedIn: https://www.linkedin.com/in/rafaelsantospereirarsp/

GitHub: https://github.com/ZeRafaSp/