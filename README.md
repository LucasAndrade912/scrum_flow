# Scrum Flow

Sistema de gerenciamento de projetos seguindo a metodologia Scrum.

## Funcionalidades

- **Gerenciamento de Projetos**: Crie e gerencie projetos com equipes
- **Membros do Projeto**: Adicione e remova membros dos projetos
- **Sprints**: Crie e gerencie sprints para seus projetos
- **Product Backlog**: Gerencie user stories no backlog do produto
- **Sprint Backlog**: Gerencie user stories de cada sprint
- **User Stories**: Crie user stories com formato padrão Scrum (Como/Eu quero/Para que)
- **Priorização**: Defina prioridades e story points para as user stories
- **Movimentação**: Mova user stories entre Product Backlog e Sprint Backlog

## Requisitos

- Python 3.8+
- Django 4.0+
- SQLite (padrão) ou outro banco de dados compatível

## Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd scrum_flow
```

2. Crie um ambiente virtual e ative-o:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute as migrações:
```bash
python manage.py migrate
```

5. (Opcional) Popule o banco de dados com dados de teste:
```bash
python manage.py populate_db --clear
```

### Comando populate_db

O comando `populate_db` cria dados fictícios para facilitar o desenvolvimento e testes:

```bash
python manage.py populate_db [opções]
```

**Opções disponíveis:**

- `--users N`: Número de usuários a criar (padrão: 10)
- `--projects N`: Número de projetos por usuário (padrão: 5)
- `--sprints N`: Número máximo de sprints por projeto (padrão: 3)
- `--stories N`: Número máximo de user stories por backlog (padrão: 5)
- `--clear`: Limpar dados existentes antes de popular

**Exemplos:**

```bash
# Criar dados com valores padrão
python manage.py populate_db

# Criar 5 usuários, 3 projetos cada, com até 2 sprints e 10 user stories
python manage.py populate_db --users 5 --projects 3 --sprints 2 --stories 10

# Limpar banco e criar novos dados
python manage.py populate_db --clear
```

**Credenciais de acesso:**
- Usuário: qualquer username gerado
- Senha: `senha123`

## Executar o projeto

```bash
python manage.py runserver
```

Acesse: http://localhost:8000

## Estrutura do Projeto

```
scrum_flow/
├── scrum_app/              # Aplicação principal
│   ├── forms/              # Formulários
│   ├── management/         # Comandos customizados
│   ├── migrations/         # Migrações do banco
│   ├── services/           # Lógica de negócio
│   ├── templates/          # Templates HTML
│   ├── views/              # Views
│   └── models.py           # Modelos de dados
└── scrum_flow/             # Configurações do projeto
```

## Tecnologias

- **Backend**: Django 5.1.5
- **Frontend**: Bootstrap 5.3.2, Bootstrap Icons
- **Banco de Dados**: SQLite
- **Geração de dados**: Faker

## Licença

Este projeto é de código aberto para fins educacionais.
