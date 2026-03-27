# Rede DBQP — DataBase Qualitativa Pessoal

## 🌐 Visão Geral
A **Rede DBQP** é uma plataforma social avançada para desenvolvedores que transcende o modelo tradicional de conexões. Ela utiliza **Teoria dos Grafos** de alto nível para mapear afinidades técnicas, sugerir trilhas de aprendizado e visualizar a dinâmica de influência em tempo real. Cada interação — seguidor, amigo ou stack compartilhada — alimenta um ecossistema de dados processados por algoritmos clássicos e modernos.

---

## 🚀 Funcionalidades Principais

### 1. Inteligência de Rede (Graph-Powered)
- **Mapa de Conexões**: Visualização interativa usando **vis.js** com motor de física **ForceAtlas2**.
- **Esqueleto da Rede (MST)**: Destaque visual das conexões de similaridade mais fortes que estruturam a plataforma.
- **Clusters de Influência (SCC)**: Agrupamento automático de usuários com base em ciclos de seguidores, identificando "bolhas" técnicas e de autoridade.

### 2. Algoritmos Sociais
- **Caminho de Afinidade (Dijkstra)**: No perfil de qualquer desenvolvedor, você pode calcular a rota técnica mais curta até ele, baseada em habilidades compartilhadas.
- **Sugestão BFS**: Sistema de recomendações de amigos de 2º e 3º grau com base em distância geodésica no grafo social.
- **Trilha de Estudo (Topological Sort)**: Geração de um caminho lógico de aprendizado baseado no **DAG de Tecnologias** (do geral para o específico).

### 3. Ecossistema Social
- **Comunidades Inteligentes**: Recomendação de comunidades baseada em sobreposição semântica de tags.
- **Posts e Interação**: Feed global e fóruns internos por comunidade com suporte a formatação markdown.
- **Sistema Híbrido de Seguidores**: Suporte a grafos dirigidos (seguidores) e não-dirigidos (amizades aceitas).

---

## 🛠️ Stack Tecnológica

| Camada | Tecnologia | Papel |
| :--- | :--- | :--- |
| **Backend** | Python 3 + Flask | Core da aplicação e APIs de grafos |
| **ORM** | SQLAlchemy | Gerenciamento de entidades e associações complexas |
| **Database** | SQLite | Persistência de dados relacionais e grafos |
| **Frontend** | Jinja2 + CSS3 (Modern Dark) | Interface premium com estética "Cyber-Professional" |
| **Graph Engine** | Vis-Network | Renderização dinâmica e simulação de física |
| **Algoritmos** | BFS, DFS, Dijkstra, Kruskal, Tarjan | Processamento lógico e analítico da rede |

---

## 📂 Arquitetura do Projeto

```text
Rede_DBQP/
├── app.py                  # Servidor principal e configuração do ecossistema
├── seed_all.py             # Gerador de massa de dados (15+ usuários, posts, grafos)
├── DOCUMENTACAO_GRAFOS.md  # Detalhamento acadêmico e técnico dos algoritmos
├── requirements.txt        # Dependências do projeto
└── app/
    ├── models/             # Definição estrutural (User, Post, Community, Associations)
    ├── routes/             # Lógica de rotas (Auth, Social, Graph APIs)
    ├── static/             # Assets, CSS Customizado e Scripts JS
    └── templates/          # Interfaces HTML modernizadas
```

---

## ⚡ Como Começar

1. **Setup do Ambiente**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # ou .venv\Scripts\activate no Windows
   pip install -r requirements.txt
   ```

2. **Alimentação da Base**:
   ```bash
   # Popula o sistema com usuários, posts, comunidades e conexões de grafo
   python seed_all.py
   ```

3. **Execução**:
   ```bash
   python app.py
   ```
   Acesse: `http://127.0.0.1:5000`

---

## 📈 Próximos Passos
- Implementação de algoritmos de **Centralidade (PageRank)** para identificar especialistas.
- Chat em tempo real entre amigos.
- Integração profunda com APIs do GitHub para auto-preenchimento de habilidades.

---
© 2026 DBQP Project - Documentação Técnica do Sistema
