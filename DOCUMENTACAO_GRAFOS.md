# Documentação de Grafos — DBQP (Advanced Edition)

Esta documentação detalha a implementação técnica, algoritmos e fundamentos teóricos que sustentam a inteligência de rede da plataforma DBQP.

---

## 🌳 1. Estruturas de Dados Fundamentais

A plataforma utiliza três estruturas de grafos principais para representar as interações sociais e técnicas:

| Estrutura | Tipo | Representação | Pesos |
| :--- | :--- | :--- | :--- |
| **Grafo Social (Amizades)** | Não-Dirigido | $G = (V, E)$ | Unweighted (distância geodésica) |
| **Grafo de Seguidores** | Dirigido | $D = (V, A)$ | Unweighted (fluxo de autoridade) |
| **Grafo de Similaridade** | Não-Dirigido | $S = (V, E, W)$ | Weighted (similaridade de skills/interesses) |

---

## 🧪 2. Algoritmos Implementados

### 2.1 BFS (Breadth-First Search) — Distância Social
O BFS é utilizado no grafo de amizades para calcular o menor caminho (unweighted) entre dois usuários.
- **Sugestões de Amigos**: Realizamos uma busca em largura limitada a profundidade 3 ($k=3$) a partir do usuário logado.
- **Complexidade**: $O(V + E)$.

### 2.2 DFS (Depth-First Search) & Algoritmo de Tarjan — SCC
Utilizamos um DFS recursivo para implementar o **Algoritmo de Tarjan**, identificando **Componentes Fortemente Conexas (SCC)** no grafo de seguidores.
- **Aplicação**: No mapa da rede, usuários pertencentes ao mesmo ciclo de influência (onde todos se alcançam via seguidores) são coloridos com o mesmo ID de grupo.
- **Complexidade**: $O(V + E)$ (passagem única).

### 2.3 Dijkstra — Melhor Caminho de Afinidade
Para encontrar a "rota técnica mais curta" entre usuários no grafo de similaridade, utilizamos o **Algoritmo de Dijkstra**.
- **Ponderação**: $W = 10 / (total\_tags\_comum + 0.1)$.
- **Objetivo**: Minimizar o custo da rota priorizando arestas com maior similaridade bi-direcional.
- **Complexidade**: $O(E \log V)$ (usando Priority Queue/Heap).

### 2.4 Kruskal — MST (Maximum Spanning Tree)
Extraímos a **Árvore Geradora Máxima** da rede de similaridade para identificar o backbone estrutural da plataforma.
- **Lógica**: Ordenamos as arestas por peso (similaridade) e usamos **DSU (Disjoint Set Union)** para reconstruir a árvore sem ciclos.
- **Visualização**: O MST é destacado em verde brilhante na interface, mostrando as conexões críticas da rede.
- **Complexidade**: $O(E \log E)$.

### 2.5 Ordenação Topológica — Trilha de Estudo (DAG)
As tecnologias são organizadas em um **Grafo Direcionado Acíclico (DAG)** baseado na popularidade relativa.
- **Hierarquia**: Se uma $Tech\_A$ é mais popular que $Tech\_B$, existe um arco $A \to B$.
- **Algoritmo de Kahn**: Gera uma ordem linear (ordenação topológica) que sugere ao usuário quais tecnologias aprender primeiro para "nivelar" com a média da rede.
- **Complexidade**: $O(V + E)$.

---

## 🎨 3. Visualização e Física (ForceAtlas2)

Para garantir a clareza visual em redes densas, migramos para o motor de física **ForceAtlas2**.
- **Filtragem de Ruído**: No backend, arestas com similaridade $< 2$ que não pertencem ao MST são ocultadas para reduzir o clutter visual.
- **Estabilidade**: O ForceAtlas2 aplica forças de repulsão baseadas no grau do nó e forças de atração baseadas no peso da aresta, resultando em clusters orgânicos e bem definidos.

---

## 📚 4. Referências Acadêmicas
1. **Dijkstra, E. W.** (1959). *A note on two problems in connexion with graphs*.
2. **Tarjan, R. E.** (1972). *Depth-first search and linear graph algorithms*.
3. **Kruskal, J. B.** (1956). *On the shortest spanning subtree of a graph*.
4. **Kahn, A. B.** (1962). *Topological sorting of large networks*.

---
© 2026 DBQP Graph Engineering Dept.
