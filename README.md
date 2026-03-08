# PiiCheck API

API para **detecção assíncrona de PII (Personally Identifiable Information)** em textos utilizando uma arquitetura baseada em **Flask + Celery + Redis**.
O sistema permite enviar textos para análise, processar a detecção em background e consultar os resultados posteriormente.

A aplicação foi projetada com foco em:

* processamento assíncrono
* separação em camadas
* escalabilidade
* controle de uso via rate limit
* boas práticas de desenvolvimento

---

# 1 — Descrição do projeto e execução

## Fluxo da aplicação

1. O cliente envia um arquivo de texto para análise
2. A API registra a solicitação no banco
3. Uma **task Celery** é disparada
4. O worker processa a detecção de PII
5. O resultado é salvo no banco
6. O cliente consulta o resultado posteriormente

Arquitetura simplificada:

```
Client
   |
   v
Flask API
   |
   v
Redis (fila de tarefas)
   |
   v
Celery Worker
   |
   v
Banco de dados
```

---

# Configuração de Ambiente (.env)

O projeto utiliza variáveis de ambiente para configuração.
Para facilitar a execução em um **projeto de portfólio**, o setup foi mantido **simples e rápido de configurar**.

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=supersecret
JWT_SECRET_KEY=jwtsecret

DATABASE_URL=sqlite:///app.db
```

Essas variáveis são suficientes para executar o projeto localmente.

---

## Explicação das variáveis

| Variável         | Descrição                                        |
| ---------------- | ------------------------------------------------ |
| `SECRET_KEY`     | chave usada pelo Flask para segurança de sessões |
| `JWT_SECRET_KEY` | chave usada para assinatura dos tokens JWT       |
| `DATABASE_URL`   | conexão com banco de dados                       |

Por padrão, o projeto utiliza **SQLite**, que não exige instalação adicional.

O banco será criado automaticamente no arquivo:

```id="v0iyty"
app.db
```

---


# Execução com Docker

Pré-requisitos:

* Docker
* Docker Compose

### Subir toda a aplicação

```bash
docker compose up --build
```

Serviços iniciados:

* API Flask
* Redis
* Celery Worker

API disponível em:

```
http://localhost:5000
```

### Ver logs do worker

```bash
docker compose logs worker -f
```

### Parar containers

```bash
docker compose down
```

---

# Execução sem Docker

Pré-requisitos:

* Python 3.10+
* Redis instalado

### 1 — Instalar dependências

Se estiver usando **Pipenv**:

```bash
pipenv install
```

Entrar no ambiente:

```bash
pipenv shell
```

---

### 2 — Executar Redis

```bash
redis-server
```

Redis é o **broker de mensagens** usado pelo Celery.

---

### 3 — Rodar a API

```bash
python run.py
```

---

### 4 — Rodar o worker

Em outro terminal:

```bash
celery -A app.celery_worker:celery worker --loglevel=info
```

---

# 2 — Arquitetura

## Processamento assíncrono

O projeto utiliza:

* Celery
* Redis

### Por que usar Celery?

Algumas tarefas são **custosas computacionalmente**, como análise de texto.

Executar isso diretamente na API poderia:

* bloquear requisições
* aumentar latência
* reduzir escalabilidade

Com Celery:

* a API apenas **envia a tarefa**
* o worker executa **em background**

---

## Redis como broker

Redis é usado como **fila de mensagens**.

Fluxo:

```
API → Redis → Worker
```

Quando a API cria uma task:

```
process_scan.delay(text)
```

A mensagem vai para o Redis.

O worker Celery consome essa fila e executa a função.

---

## Rate Limiting

A API utiliza:

* Flask-Limiter

Objetivo:

* evitar abuso da API
* limitar número de requisições
* proteger recursos

Exemplo de configuração:

```
10 requests por minuto por usuário
```

---

## Arquitetura em Camadas

Estrutura do projeto:

```
app/
    modules/
        auth/
        pii/
    extensions/
    config/
```

Camadas principais:

### Rotas (Controllers)

Responsáveis por:

* receber requisições
* validar dados
* chamar serviços

Exemplo:

```
app/modules/pii/pii_routes.py
```

---

### Tasks

Responsáveis pelo **processamento assíncrono**.

```
app/modules/pii/pii_tasks.py
```

Executadas pelo worker Celery.

---

### Extensões

Inicialização de componentes do Flask:

```
app/extensions/
```

Inclui:

* banco
* JWT
* rate limiter
* celery

---

### Configuração

Centralização de configurações:

```
app/config/config.py
```

---

## Linting

O projeto utiliza:

* Ruff

Objetivo:

* manter padrão de código
* evitar erros comuns
* melhorar legibilidade

Rodar lint:

```bash
ruff check .
```

Auto corrigir:

```bash
ruff check . --fix
```

---

# 3 — Banco de Dados

O projeto utiliza:

* SQLAlchemy

---

## Migrações

Migrações são gerenciadas com:

* Flask-Migrate

Baseado no **Alembic**.

### Criar migração

```bash
flask db migrate -m "create scans table"
```

### Aplicar migração

```bash
flask db upgrade
```

---

## Índices no banco

Índices são utilizados para melhorar performance de consultas.

Exemplo:

* busca por `scan_id`
* busca por `user_id`

Índices permitem:

* consultas mais rápidas
* melhor escalabilidade

---

## Estrutura típica de tabela

Exemplo simplificado:

```
scans
----
id
user_id
text
status
created_at
```

Resultados da análise ficam em tabela separada.

---

# 4 — Contribuições

## Padrão de Branch

Formato:

```
feat/<descricao>
fix/<descricao>
chore/<descricao>
```

Exemplos:

```
feat/add-pii-detector
fix/jwt-validation
chore/update-dependencies
```

---

## Padrão de Commit

Padrão **Conventional Commits**.

Formato:

```
tipo: descrição
```

Exemplos:

```
feat: add async pii scan
fix: correct celery worker import
refactor: improve api structure
```

---

# Tecnologias Utilizadas

Backend:

* Flask
* Celery
* Redis

Banco de dados:

* SQLAlchemy
* Flask-Migrate

Infraestrutura:

* Docker
* Docker Compose

Qualidade de código:

* Ruff

Autenticação:

* Flask-JWT-Extended
