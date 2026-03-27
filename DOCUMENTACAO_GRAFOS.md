# Documentação de Grafos — Rede DBQP

## Sumário

1. [Introdução](#1-introdução)
2. [Modelagem do Grafo Bipartido (Usuário ↔ Tags)](#2-modelagem-do-grafo-bipartido-usuário--tags)
3. [Grafo de Similaridade entre Usuários (Network)](#3-grafo-de-similaridade-entre-usuários-network)
4. [Sistema de Recomendação de Comunidades](#4-sistema-de-recomendação-de-comunidades)
5. [Algoritmos e Complexidade](#5-algoritmos-e-complexidade)
6. [Visualização com vis.js e Barnes-Hut](#6-visualização-com-visjs-e-barnes-hut)

---

## 1. Introdução

O projeto utiliza **teoria dos grafos** como base para três sistemas fundamentais:

| Sistema | Tipo de Grafo | Onde é usado |
|---------|---------------|--------------|
| Modelo de dados (tags) | Grafo bipartido não-direcionado | Banco de dados (tabelas de associação) |
| Network de conexões | Grafo ponderado não-direcionado | Página "Network" (`/users/network`) |
| Recomendação de comunidades | Grafo bipartido implícito | Página "Comunidades" (`/communities/`) |

---

## 2. Modelagem do Grafo Bipartido (Usuário ↔ Tags)

### 2.1 Estrutura

O banco de dados modela um **grafo bipartido** onde existem dois conjuntos de vértices disjuntos:

- **Conjunto U** = Usuários (tabela `registro`)
- **Conjunto T** = Tags, subdividido em:
  - **T_h** = Habilidades (tabela `lista_habilidades`)
  - **T_i** = Interesses (tabela `lista_interesses`)

As **arestas** são armazenadas nas tabelas de associação (many-to-many):

```
user_habilidades:     Registro ←→ Habilidade
user_interesses:      Registro ←→ Interesse
comunidade_habilidades: Comunidade ←→ Habilidade
comunidade_interesses:  Comunidade ←→ Interesse
```

### 2.2 Representação Formal

```
G_bipartido = (U ∪ T, E)

Onde:
  U = {u₁, u₂, ..., uₙ}     (usuários)
  T = T_h ∪ T_i               (habilidades + interesses)
  E = {(u, t) | u ∈ U, t ∈ T, u possui tag t}
```

### 2.3 Implementação no Código

**Arquivo:** `app/models/associations.py`

```python
# Tabela de ligação: Usuários <-> Habilidades
user_habilidades = db.Table('user_habilidades',
    db.Column('user_id', db.Integer, db.ForeignKey('registro.id'), primary_key=True),
    db.Column('lista_habilidade_id', db.Integer, db.ForeignKey('lista_habilidades.id'), primary_key=True)
)
```

Cada linha nesta tabela representa uma **aresta** no grafo bipartido.

### 2.4 Diagrama

```
         Usuários (U)                    Tags (T)
        ┌──────────┐               ┌──────────────┐
        │  Lucas   │──────────────│   Python     │
        │          │──────┐       │              │
        └──────────┘      │       └──────────────┘
                          │       ┌──────────────┐
        ┌──────────┐      └──────│   React      │──────┐
        │ Fernanda │──────────────│              │      │
        │          │──────┐       └──────────────┘      │
        └──────────┘      │       ┌──────────────┐      │
                          └──────│   Web Dev    │      │
        ┌──────────┐              │              │      │
        │  Rafael  │──────────────│              │      │
        │          │──────────────└──────────────┘      │
        └──────────┘       ┌────────────────────────────┘
                           │      ┌──────────────┐
                           └─────│   Node.js    │
                                  └──────────────┘
```

---

## 3. Grafo de Similaridade entre Usuários (Network)

### 3.1 Conceito

A partir do grafo bipartido, é derivado um **grafo de projeção unipartido** onde os vértices são exclusivamente **usuários** e as arestas representam **similaridade** (tags em comum).

```
G_network = (U, E')

Onde:
  E' = {(uᵢ, uⱼ, w) | w = |tags(uᵢ) ∩ tags(uⱼ)| > 0}
  w = peso da aresta (quantidade de tags compartilhadas)
```

### 3.2 Algoritmo de Construção

**Arquivo:** `app/routes/users.py` — função `network_data()`

O grafo é construído com **busca combinatória de força bruta** (all-pairs comparison):

```python
# Pseudocódigo do algoritmo
para cada par (userᵢ, userⱼ) onde i < j:
    hab_compartilhadas = habilidades(userᵢ) ∩ habilidades(userⱼ)
    int_compartilhados = interesses(userᵢ) ∩ interesses(userⱼ)
    
    peso = |hab_compartilhadas| + |int_compartilhados|
    
    se peso > 0:
        criar aresta(userᵢ → userⱼ, peso=peso)
```

### 3.3 Implementação Real

```python
for i in range(len(all_users)):
    for j in range(i + 1, len(all_users)):
        user1 = all_users[i]
        user2 = all_users[j]
        
        shared_habilidades = set([h.nome for h in user1.habilidades]) & set([h.nome for h in user2.habilidades])
        shared_interesses = set([i.nome for i in user1.interesses]) & set([i.nome for i in user2.interesses])
        
        weight = len(shared_habilidades) + len(shared_interesses)
        
        if weight > 0:
            edges.append({
                "from": user1.id,
                "to": user2.id,
                "value": weight,  # Espessura da aresta proporcional
                "title": "Hab: ... | Int: ..."
            })
```

### 3.4 Detalhes da Busca

| Aspecto | Detalhe |
|---------|---------|
| **Tipo de busca** | Comparação de todos os pares (all-pairs) |
| **Estrutura percorrida** | Lista de adjacência implícita (projeção do grafo bipartido) |
| **Operação central** | Interseção de conjuntos (`set.intersection`) |
| **Complexidade temporal** | O(n² × k), onde n = nº de usuários, k = nº médio de tags |
| **Complexidade espacial** | O(n²) no pior caso (grafo completo) |
| **Geração de nós** | Iteração linear O(n) sobre todos os usuários |
| **Geração de arestas** | Loop aninhado com i < j, evitando arestas duplicadas |

### 3.5 Estrutura do Grafo Resultante

Cada **nó** contém:
```json
{
    "id": 1,
    "label": "Lucas Mendes",
    "title": "Habilidades: Python, React\nInteresses: Web Dev, IA",
    "group": 1,           // 1 = usuário logado (destaque), 2 = outros
    "shape": "circularImage",
    "image": "/static/uploads/avatar.png"
}
```

Cada **aresta** contém:
```json
{
    "from": 1,
    "to": 3,
    "value": 4,           // 4 tags em comum → aresta mais grossa
    "title": "Hab: Python, React | Int: Web Dev, IA"
}
```

---

## 4. Sistema de Recomendação de Comunidades

### 4.1 Conceito

O sistema de recomendação opera sobre um **segundo grafo bipartido implícito** que conecta o usuário às comunidades através da sobreposição de tags:

```
G_rec = (U ∪ C, E_rec)

Onde:
  U = {u_atual}                          (o usuário logado)
  C = {c₁, c₂, ..., cₘ}                (comunidades que o usuário NÃO participa)
  E_rec = {(u, c, score) | score > 0}   (arestas ponderadas pelo score)
```

### 4.2 Cálculo do Score de Compatibilidade

**Arquivo:** `app/routes/communities.py` — função `list_communities()`

```
score(u, c) = |interesses(u) ∩ interesses(c)| + |habilidades(u) ∩ habilidades(c)|
```

### 4.3 Algoritmo Completo

```python
# 1. Extrair tags do usuário
meus_interesses   = {i.nome para cada i em user.interesses}
minhas_habilidades = {h.nome para cada h em user.habilidades}

# 2. Para cada comunidade disponível (que o usuário NÃO participa)
para cada comunidade c em todas_comunidades:
    se c NÃO está em minhas_comunidades:
        
        # 3. Calcular interseções (operação de conjuntos)
        over_int = meus_interesses ∩ interesses(c)
        over_hab = minhas_habilidades ∩ habilidades(c)
        
        # 4. Score = soma das cardinalidades
        score = |over_int| + |over_hab|

# 5. Ordenar por score decrescente
sugeridas.sort(key=score, reverse=True)

# 6. Dividir em dois grupos
recomendadas = [c para (score, c) em sugeridas se score > 0]
outras       = [c para (score, c) em sugeridas se score == 0]
```

### 4.4 Classificação Final

| Categoria | Critério | Exibição |
|-----------|----------|----------|
| **Recomendadas** | `score > 0` (pelo menos 1 tag em comum) | Seção superior, borda verde, botão primário |
| **Todas as Comunidades** | `score == 0` (nenhuma tag em comum) | Seção inferior, estilo padrão |

### 4.5 Destaque Visual de Tags

As tags de cada comunidade são renderizadas com **estilo condicional**:

- **Tag compatível** (presente no perfil do usuário): fundo verde, borda verde, emoji ⭐, texto em negrito
- **Tag normal** (não presente no perfil): fundo neutro transparente, borda cinza

```python
# Dados passados ao template para a lógica condicional:
meus_interesses    → set de nomes de interesses do usuário
minhas_habilidades → set de nomes de habilidades do usuário
```

```html
{% if h.nome in minhas_habilidades %}
    <span style="... background verde, borda verde ...">⭐ {{ h.nome }}</span>
{% else %}
    <span style="... fundo neutro, borda cinza ...">{{ h.nome }}</span>
{% endif %}
```

### 4.6 Complexidade

| Aspecto | Detalhe |
|---------|---------|
| **Tipo de busca** | Varredura linear sobre comunidades + interseção de conjuntos |
| **Complexidade temporal** | O(m × k), onde m = nº de comunidades, k = nº médio de tags |
| **Ordenação** | O(m log m) pelo score (Timsort do Python) |
| **Complexidade total** | O(m × k + m log m) |

---

## 5. Algoritmos e Complexidade

### 5.1 Resumo dos Algoritmos Utilizados

| Algoritmo | Onde é usado | Tipo | Complexidade |
|-----------|-------------|------|-------------|
| **All-Pairs Intersection** | Grafo de Network | Força bruta com interseção de conjuntos | O(n² × k) |
| **Tag Overlap Scoring** | Recomendação de comunidades | Interseção de conjuntos + ordenação | O(m × k + m log m) |
| **Barnes-Hut Simulation** | Layout do grafo no frontend | Simulação de N-corpos com quadtree | O(n log n) por iteração |
| **Set Intersection** | Operação fundamental em ambos | Interseção de hash sets Python | O(min(|A|, |B|)) |

### 5.2 Interseção de Conjuntos — Operação Central

Ambos os sistemas de grafos dependem fundamentalmente da **interseção de conjuntos** (`set.intersection` do Python):

```python
shared = set_A & set_B   # Equivale a set_A.intersection(set_B)
```

- Internamente, Python usa **hash tables** para representar sets
- A interseção itera sobre o menor conjunto e verifica pertinência no maior
- Complexidade: **O(min(|A|, |B|))** em caso médio

### 5.3 Projeção do Grafo Bipartido

A construção do grafo de Network é, formalmente, uma **projeção unimodal** do grafo bipartido:

```
Dado G_bipartido = (U ∪ T, E):

G_projeção = (U, E')
onde (uᵢ, uⱼ) ∈ E' ⟺ ∃ t ∈ T tal que (uᵢ, t) ∈ E e (uⱼ, t) ∈ E

Peso: w(uᵢ, uⱼ) = |N(uᵢ) ∩ N(uⱼ)|
      onde N(u) = vizinhos de u no grafo bipartido
```

---

## 6. Visualização com vis.js e Barnes-Hut

### 6.1 Biblioteca

A visualização do grafo utiliza a biblioteca **vis.js** (módulo `vis-network`), carregada via CDN:

```html
<script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
```

### 6.2 Algoritmo de Layout — Barnes-Hut

O posicionamento dos nós no canvas é calculado pelo algoritmo **Barnes-Hut**, uma otimização da simulação de N-corpos:

#### Como funciona:

1. **Modelo de forças:** Cada nó exerce repulsão sobre todos os outros (como partículas com carga elétrica). As arestas funcionam como molas que atraem os nós conectados.

2. **Quadtree:** Em vez de calcular a força entre cada par de nós (O(n²)), o Barnes-Hut agrupa nós distantes em uma **árvore quadrante** (quadtree) e aproxima a força gravitacional do grupo inteiro, reduzindo a complexidade para **O(n log n)**.

3. **Iterações de estabilização:** O grafo é simulado por múltiplas iterações até convergir para um layout estável.

#### Parâmetros Configurados:

```javascript
physics: {
    barnesHut: {
        gravitationalConstant: -4000,  // Repulsão entre nós (negativo = repulsão)
        centralGravity: 0.1,           // Atração para o centro do canvas
        springLength: 250,             // Comprimento natural das molas (arestas)
        springConstant: 0.01,          // Rigidez das molas
        damping: 0.09                  // Amortecimento (evita oscilação infinita)
    },
    stabilization: {
        iterations: 150                // Nº de iterações antes de mostrar o grafo
    }
}
```

| Parâmetro | Efeito |
|-----------|--------|
| `gravitationalConstant` | Quanto menor (mais negativo), mais os nós se repelem → grafo mais espalhado |
| `centralGravity` | Puxa tudo para o centro, evitando que nós "fujam" para fora da tela |
| `springLength` | Distância ideal entre nós conectados |
| `springConstant` | Quão forte uma aresta puxa seus nós para a distância ideal |
| `damping` | Reduz a velocidade dos nós a cada iteração (estabiliza) |
| `iterations` | Mais iterações = layout mais estável, porém mais tempo de carregamento |

### 6.3 Interatividade

| Recurso | Implementação |
|---------|---------------|
| **Hover em nós** | Mostra tooltip com habilidades e interesses do usuário |
| **Hover em arestas** | Mostra as tags compartilhadas entre os dois usuários |
| **Clique em nó** | Redireciona para o perfil do usuário clicado |
| **Espessura de aresta** | Proporcional ao peso (nº de tags compartilhadas) |
| **Cores** | Nó do usuário logado = verde (#47D15A), outros = escuro |

### 6.4 Fluxo de Dados

```
1. Cliente acessa /users/network
        │
        ▼
2. Página carrega e faz fetch('/users/api/network_data')
        │
        ▼
3. Backend (Python):
   a) Carrega todos os usuários do banco
   b) Gera nós (atributos visuais)
   c) Compara all-pairs → calcula interseções → gera arestas
   d) Retorna JSON {nodes: [...], edges: [...]}
        │
        ▼
4. Frontend (JavaScript):
   a) Cria vis.DataSet com nós e arestas
   b) Inicializa vis.Network com configurações Barnes-Hut
   c) Executa 150 iterações de simulação de forças
   d) Renderiza grafo interativo no canvas
```

---

## Referências Teóricas

- **Grafo Bipartido**: Bondy, J.A. & Murty, U.S.R. — *Graph Theory* (2008)
- **Projeção Unimodal**: Newman, M.E.J. — *Networks: An Introduction* (2010)
- **Barnes-Hut**: Barnes, J. & Hut, P. — *A hierarchical O(N log N) force-calculation algorithm* (1986)
- **vis.js**: [visjs.github.io/vis-network](https://visjs.github.io/vis-network/docs/network/)
