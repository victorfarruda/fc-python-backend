# fc-python-backend

Backend em Python com Django e Django REST Framework, organizado com Clean Architecture.

## Pré-requisitos

- Python >= 3.14
- [uv](https://docs.astral.sh/uv/) instalado

## Instalação

Clone o repositório e instale as dependências:

```bash
git clone <url-do-repositório>
cd fc-python-backend
uv sync
```

## Executando o servidor de desenvolvimento

```bash
uv run python src/manage.py runserver
```

O servidor estará disponível em `http://127.0.0.1:8000`.

## Migrações do banco de dados

Aplicar as migrações:

```bash
uv run python src/manage.py migrate
```

Criar um superusuário (opcional):

```bash
uv run python src/manage.py createsuperuser
```

## Executando os testes

Todos os testes (unitários, integração e e2e):

```bash
uv run pytest
```

Apenas testes de uma camada específica:

```bash
# Testes unitários
uv run pytest src/core/category/tests/application/use_cases/unit/

# Testes de integração
uv run pytest src/core/category/tests/application/use_cases/integration/

# Testes do Django (views e repositório)
uv run pytest src/django_project/
```

## Linting

```bash
uv run ruff check
```

Corrigir automaticamente:

```bash
uv run ruff check --fix
```
