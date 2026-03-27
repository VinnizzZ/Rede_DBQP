# Rede DBQP — DataBase Qualitativa Pessoal

## Visão Geral

A **Rede DBQP** é uma rede social voltada para programadores e profissionais de tecnologia. A plataforma conecta usuários com base em suas **habilidades técnicas** e **interesses profissionais**, utilizando **teoria dos grafos** para calcular conexões, recomendar comunidades e visualizar a rede de relacionamentos.

## Stack Tecnológica

| Camada       | Tecnologia                           |
|--------------|--------------------------------------|
| Backend      | Python 3 + Flask                     |
| ORM          | Flask-SQLAlchemy                     |
| Banco de Dados | SQLite (dev) / MySQL (produção)    |
| Frontend     | HTML5, CSS3, Jinja2                  |
| Visualização de Grafos | vis.js (vis-network)      |
| Autenticação | Werkzeug (hash de senhas) + Session  |
| Fontes       | Google Fonts (Inter)                 |
| Ícones       | Font Awesome                         |

## Estrutura do Projeto

```
Rede_DBQP/
├── app.py                  # Entry point — configuração Flask e registro de Blueprints
├── populate_db.py          # Script para criar usuários fictícios com perfis randomizados
├── seed_communities.py     # Script para criar comunidades pré-definidas
├── reduce_fakes.py         # Script para limpeza de dados falsos
├── requirements.txt        # Dependências Python
├── .env                    # Variáveis de ambiente (DB, secret key)
│
└── app/
    ├── __init__.py          # Inicializa SQLAlchemy
    │
    ├── models/
    │   ├── user.py          # Registro (usuário) + Perfil
    │   ├── preferences.py   # Habilidade + Interesse
    │   ├── comunidade.py    # Comunidade + ComunidadePost
    │   ├── post.py          # Post (feed geral)
    │   └── associations.py  # Tabelas de ligação (many-to-many)
    │
    ├── routes/
    │   ├── auth.py          # Login, Registro, Logout
    │   ├── posts.py         # Feed de posts
    │   ├── users.py         # Perfil, edição, Network (grafo)
    │   └── communities.py   # Comunidades, recomendações, posts internos
    │
    ├── templates/           # Templates Jinja2 (HTML)
    └── static/              # CSS, JS, imagens
```

## Módulos Principais

### 1. Autenticação (`auth.py`)
- Registro de novos usuários com hash de senha (Werkzeug)
- Login/Logout via sessão Flask

### 2. Perfil de Usuário (`users.py`)
- Edição de biografia, avatar e GitHub
- Cadastro de **habilidades** e **interesses** (separados por vírgula)
- Visualização de perfis de outros usuários

### 3. Feed de Posts (`posts.py`)
- Criação e listagem de posts em ordem cronológica inversa

### 4. Network — Grafo de Conexões (`users.py`)
- API REST (`/api/network_data`) que gera um grafo de similaridade entre usuários
- Visualização interativa com **vis.js** usando layout Barnes-Hut
- Arestas representam habilidades/interesses compartilhados, com espessura proporcional

### 5. Comunidades (`communities.py`)
- Criação de comunidades (fóruns) com tags de habilidades/interesses
- Sistema de recomendação baseado em sobreposição de tags
- Divisão em **Recomendadas** (matching com perfil) e **Todas as Comunidades**
- Posts internos por membros

## Banco de Dados — Modelo Relacional

```
Registro (usuário)
  ├──> Perfil (1:1)
  ├──> Posts (1:N)
  ├──> Habilidades (N:N via user_habilidades)
  ├──> Interesses (N:N via user_interesses)
  ├──> Comunidades inscritas (N:N via comunidade_membros)
  └──> Comunidades criadas (1:N)

Comunidade
  ├──> Habilidades (N:N via comunidade_habilidades)
  ├──> Interesses (N:N via comunidade_interesses)
  ├──> Membros (N:N via comunidade_membros)
  └──> ComunidadePosts (1:N)
```

## Como Executar

```bash
# 1. Criar e ativar ambiente virtual
python -m venv .venv
.venv\Scripts\activate       # Windows

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar variáveis de ambiente (.env)
# Copiar de env-example.md

# 4. Popular banco (opcional)
python populate_db.py
python seed_communities.py

# 5. Executar
python app.py
```

O servidor estará em `http://127.0.0.1:5000`.
