import os
import heapq
from collections import deque
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash, current_app
from werkzeug.utils import secure_filename
from app.models import db
from app.models.user import Registro, Perfil
from app.models.preferences import Habilidade, Interesse
from app.models.associations import Amizade

users_bp = Blueprint('users', __name__)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# ================================================================
# ALGORITMOS DE GRAFO AVANÇADOS
# ================================================================

# 1. DIJKSTRA — Menor caminho ponderado (Afinidade)
def dijkstra_afinidade(grafo_ponderado, origem_id, destino_id):
    """
    Calcula o caminho de maior afinidade entre dois usuários.
    O 'peso' da aresta no grafo de afinidade é 10 / similarity.
    """
    distances = {node: float('infinity') for node in grafo_ponderado}
    distances[origem_id] = 0
    pq = [(0, origem_id)]
    predecessors = {origem_id: None}

    while pq:
        current_dist, current_node = heapq.heappop(pq)

        if current_node == destino_id:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = predecessors.get(current_node)
            return path[::-1], current_dist

        if current_dist > distances[current_node]:
            continue

        for neighbor, weight in grafo_ponderado.get(current_node, {}).items():
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
    
    return None, float('infinity')

# 2. KRUSKAL — Árvore Geradora Mínima (MST / Backbone)
class DSU:
    def __init__(self, nodes):
        self.parent = {node: node for node in nodes}
    def find(self, i):
        if self.parent[i] == i: return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            self.parent[root_i] = root_j
            return True
        return False

def kruskal_mst(nodes, edges):
    """
    Extrai a Árvore Geradora Máxima (Maximum Spanning Tree) 
    baseada no peso da similaridade (similaridade alta = aresta prioritária).
    """
    # Sort edges by weight descending for Maximum Spanning Tree
    sorted_edges = sorted(edges, key=lambda x: x['value'], reverse=True)
    dsu = DSU(nodes)
    mst_edges = []
    
    for edge in sorted_edges:
        if dsu.union(edge['from'], edge['to']):
            mst_edges.append(edge)
            
    return mst_edges

# 3. TARJAN — Componentes Fortemente Conexas (SCC)
def find_sccs(all_users):
    """
    Identifica Componentes Fortemente Conexas no grafo dirigido de seguidores.
    """
    index_counter = 0
    stack = []
    lowlink = {}
    index = {}
    on_stack = {}
    sccs = []

    # Construir grafo de adjacência a partir dos registros
    adj = {u.id: [s.id for s in u.seguindo.all()] for u in all_users}

    def strongconnect(v):
        nonlocal index_counter
        index[v] = index_counter
        lowlink[v] = index_counter
        index_counter += 1
        stack.append(v)
        on_stack[v] = True

        for w in adj.get(v, []):
            if w not in index:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif on_stack[w]:
                lowlink[v] = min(lowlink[v], index[w])

        if lowlink[v] == index[v]:
            new_scc = []
            while True:
                w = stack.pop()
                on_stack[w] = False
                new_scc.append(w)
                if w == v: break
            sccs.append(new_scc)

    for u in all_users:
        if u.id not in index:
            strongconnect(u.id)
            
    return sccs

# 4. ORDENAÇÃO TOPOLÓGICA — Trilha de Aprendizado (DAG)
def build_skill_dag(all_skills):
    """
    Cria um DAG de skills baseado em popularidade. 
    Skill A -> Skill B se A é mais popular que B (hierarquia Geral -> Específico).
    """
    # Contar usuários por skill
    skill_counts = {s.nome: len(s.usuarios) for s in all_skills}
    # Criar arestas se houver sobreposição de usuários (quem tem a rara geralmente tem a comum)
    adj = {s.nome: [] for s in all_skills}
    in_degree = {s.nome: 0 for s in all_skills}
    
    sorted_skills = sorted(all_skills, key=lambda x: skill_counts[x.nome], reverse=True)
    
    for i in range(len(sorted_skills)):
        s1 = sorted_skills[i]
        for j in range(i + 1, len(sorted_skills)):
            s2 = sorted_skills[j]
            # Se s1 é muito mais popular que s2, s1 -> s2
            if skill_counts[s1.nome] > (skill_counts[s2.nome] * 1.5):
                adj[s1.nome].append(s2.nome)
                in_degree[s2.nome] += 1
                
    return adj, in_degree

def topological_sort_skills(adj, in_degree, user_skills):
    """Ordenação topológica das skills que o usuário ainda não possui."""
    queue = deque([k for k, v in in_degree.items() if v == 0])
    topo_order = []
    user_skills_names = [s.nome for s in user_skills]
    
    while queue:
        u = queue.popleft()
        if u not in user_skills_names:
            topo_order.append(u)
        
        for v in adj.get(u, []):
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    return topo_order

# ================================================================
# HELPERS — BFS (Mantidos)
# ================================================================

def construir_grafo_amizades():
    amizades = Amizade.query.filter_by(status='accepted').all()
    grafo = {}
    for a in amizades:
        grafo.setdefault(a.user_id, set()).add(a.amigo_id)
        grafo.setdefault(a.amigo_id, set()).add(a.user_id)
    return grafo

def bfs_distancia(grafo, origem_id, destino_id):
    if origem_id == destino_id: return 0
    visited = set()
    queue = deque([(origem_id, 0)])
    while queue:
        atual, dist = queue.popleft()
        if atual == destino_id: return dist
        if atual in visited: continue
        visited.add(atual)
        for vizinho in grafo.get(atual, []):
            if vizinho not in visited:
                queue.append((vizinho, dist + 1))
    return -1

def get_status_amizade(user_id, outro_id):
    amizade = Amizade.query.filter(
        ((Amizade.user_id == user_id) & (Amizade.amigo_id == outro_id)) |
        ((Amizade.user_id == outro_id) & (Amizade.amigo_id == user_id))
    ).first()
    if not amizade: return 'none'
    if amizade.status == 'accepted': return 'accepted'
    if amizade.user_id == user_id: return 'pending_sent'
    return 'pending_received'

# ================================================================
# ROTAS
# ================================================================

@users_bp.route('/profile')
@login_required
def profile():
    user = Registro.query.get(session['user_id'])
    pedidos_pendentes = Amizade.query.filter_by(amigo_id=user.id, status='pending').all()
    
    amizades_aceitas = Amizade.query.filter(
        ((Amizade.user_id == user.id) | (Amizade.amigo_id == user.id)),
        Amizade.status == 'accepted'
    ).all()
    amigos = [Registro.query.get(a.amigo_id if a.user_id == user.id else a.user_id) for a in amizades_aceitas]
    
    return render_template('view_profile.html', user=user,
                           pedidos_pendentes=pedidos_pendentes,
                           amigos=amigos,
                           num_seguindo=user.seguindo.count(),
                           num_seguidores=len(user.seguidores_lista),
                           is_own_profile=True)

@users_bp.route('/profile/<int:user_id>')
@login_required
def view_profile(user_id):
    if user_id == session['user_id']: return redirect(url_for('users.profile'))
    user = Registro.query.get_or_404(user_id)
    current_user = Registro.query.get(session['user_id'])
    
    status_amizade = get_status_amizade(current_user.id, user_id)
    esta_seguindo = current_user.seguindo.filter_by(id=user_id).first() is not None
    
    grafo = construir_grafo_amizades()
    distancia = bfs_distancia(grafo, current_user.id, user_id)
    
    amizades_aceitas = Amizade.query.filter(
        ((Amizade.user_id == user_id) | (Amizade.amigo_id == user_id)),
        Amizade.status == 'accepted'
    ).all()
    amigos = [Registro.query.get(a.amigo_id if a.user_id == user_id else a.user_id) for a in amizades_aceitas]

    return render_template('view_profile.html', user=user,
                           status_amizade=status_amizade,
                           esta_seguindo=esta_seguindo,
                           distancia=distancia,
                           amigos=amigos,
                           num_seguindo=user.seguindo.count(),
                           num_seguidores=len(user.seguidores_lista),
                           is_own_profile=False)

@users_bp.route('/network')
@login_required
def network():
    user = Registro.query.get(session['user_id'])
    return render_template('network.html', current_user=user)

@users_bp.route('/api/network_data')
@login_required
def network_data():
    current_user_id = session['user_id']
    all_users = Registro.query.all()
    
    nodes = []
    edges = []
    
    # 1. SCC para o grafo de Seguidores
    sccs = find_sccs(all_users)
    scc_map = {}
    for i, scc in enumerate(sccs):
        for uid in scc: scc_map[uid] = i
    
    for u in all_users:
        node = {
            "id": u.id,
            "label": u.nome,
            "title": f"SCC Group: {scc_map.get(u.id)}",
            "group": scc_map.get(u.id, 0) + 2, # Offset group for coloring
            "shape": "circularImage" if u.perfil and u.perfil.avatar_url else "dot"
        }
        if u.perfil and u.perfil.avatar_url:
            node["image"] = u.perfil.avatar_url
            
        nodes.append(node)
        
    for i in range(len(all_users)):
        for j in range(i + 1, len(all_users)):
            u1, u2 = all_users[i], all_users[j]
            sim = len(set([h.nome for h in u1.habilidades]) & set([h.nome for h in u2.habilidades])) + \
                  len(set([i.nome for i in u1.interesses]) & set([i.nome for i in u2.interesses]))
            if sim > 0:
                edges.append({"from": u1.id, "to": u2.id, "value": sim, "is_mst": False})
                
    # 2. MST (Maximum Spanning Tree)
    uids = [u.id for u in all_users]
    mst_edges = kruskal_mst(uids, edges)
    mst_set = set([(e['from'], e['to']) for e in mst_edges])
    
    # 3. Filtrar arestas para limpeza visual
    # Mantemos arestas se forem do MST OU se tiverem peso/sim >= 2
    filtered_edges = []
    for e in edges:
        is_mst = (e['from'], e['to']) in mst_set
        if is_mst:
            e['color'] = {'color': '#47D15A', 'width': 3} # MST brilhante
            e['is_mst'] = True
            filtered_edges.append(e)
        elif e['value'] >= 2:
            # Arestas comuns mas fortes ficam mais discretas
            e['color'] = {'color': 'rgba(255, 255, 255, 0.1)', 'width': 1}
            e['is_mst'] = False
            filtered_edges.append(e)
            
    return jsonify({"nodes": nodes, "edges": filtered_edges})

@users_bp.route('/api/affinity_path/<int:target_id>')
@login_required
def api_affinity_path(target_id):
    current_id = session['user_id']
    all_users = Registro.query.all()
    
    # Construir grafo ponderado de similaridade
    grafo_sim = {}
    for i in range(len(all_users)):
        for j in range(i + 1, len(all_users)):
            u1, u2 = all_users[i], all_users[j]
            sim = len(set([h.nome for h in u1.habilidades]) & set([h.nome for h in u2.habilidades])) + \
                  len(set([int_obj.nome for int_obj in u1.interesses]) & set([int_obj.nome for int_obj in u2.interesses]))
            if sim > 0:
                weight = 10 / sim # Higher similarity = Lower weight for Dijkstra
                grafo_sim.setdefault(u1.id, {})[u2.id] = weight
                grafo_sim.setdefault(u2.id, {})[u1.id] = weight
    
    path, score = dijkstra_afinidade(grafo_sim, current_id, target_id)
    if not path: return jsonify({"error": "No affinity path found"}), 404
    
    path_details = [{"id": uid, "nome": Registro.query.get(uid).nome} for uid in path]
    return jsonify({"path": path_details, "score": score})

@users_bp.route('/api/learning_path')
@login_required
def api_learning_path():
    user = Registro.query.get(session['user_id'])
    all_skills = Habilidade.query.all()
    
    adj, in_degree = build_skill_dag(all_skills)
    topo_order = topological_sort_skills(adj, in_degree, user.habilidades)
    
    return jsonify({"learning_path": topo_order[:5]})

# --- Outras rotas (mantidas sem alteração de funcionalidade, apenas migrando pro novo users.bp) ---
@users_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = Registro.query.get(session['user_id'])
    if request.method == 'POST':
        biografia, github_url = request.form.get('biografia', ''), request.form.get('github_url', '')
        perfil = user.perfil or Perfil(user_id=user.id)
        if not user.perfil: db.session.add(perfil)
        avatar_file = request.files.get('avatar')
        if avatar_file and avatar_file.filename != '':
            filename = secure_filename(avatar_file.filename)
            static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
            uploads_dir = os.path.join(static_dir, 'uploads')
            os.makedirs(uploads_dir, exist_ok=True)
            avatar_file.save(os.path.join(uploads_dir, filename))
            perfil.avatar_url = f"/static/uploads/{filename}"
        elif not perfil.avatar_url: perfil.avatar_url = "/static/default_avatar.png"
        perfil.biografia, perfil.github_url = biografia, github_url
        habilidades_nomes = [h.strip() for h in request.form.get('habilidades', '').split(',') if h.strip()]
        user.habilidades = []
        for n in habilidades_nomes:
            hab = Habilidade.query.filter_by(nome=n).first() or Habilidade(nome=n)
            if not hab.id: db.session.add(hab)
            user.habilidades.append(hab)
        interesses_nomes = [i.strip() for i in request.form.get('interesses', '').split(',') if i.strip()]
        user.interesses = []
        for n in interesses_nomes:
            int_obj = Interesse.query.filter_by(nome=n).first() or Interesse(nome=n)
            if not int_obj.id: db.session.add(int_obj)
            user.interesses.append(int_obj)
        db.session.commit()
        flash('Perfil atualizado!', 'success')
        return redirect(url_for('users.profile'))
    return render_template('profile.html', user=user)

@users_bp.route('/friend/request/<int:user_id>', methods=['POST'])
@login_required
def friend_request(user_id):
    curr = session['user_id']
    if curr == user_id: return redirect(url_for('users.profile'))
    if Amizade.query.filter(((Amizade.user_id==curr)&(Amizade.amigo_id==user_id))|((Amizade.user_id==user_id)&(Amizade.amigo_id==curr))).first():
        return redirect(url_for('users.view_profile', user_id=user_id))
    db.session.add(Amizade(user_id=curr, amigo_id=user_id, status='pending'))
    db.session.commit()
    flash('Pedido enviado!', 'success')
    return redirect(url_for('users.view_profile', user_id=user_id))

@users_bp.route('/friend/accept/<int:user_id>', methods=['POST'])
@login_required
def friend_accept(user_id):
    a = Amizade.query.filter_by(user_id=user_id, amigo_id=session['user_id'], status='pending').first()
    if a: a.status = 'accepted'; db.session.commit(); flash('Amizade aceita!', 'success')
    return redirect(url_for('users.profile'))

@users_bp.route('/friend/reject/<int:user_id>', methods=['POST'])
@login_required
def friend_reject(user_id):
    a = Amizade.query.filter_by(user_id=user_id, amigo_id=session['user_id'], status='pending').first()
    if a: db.session.delete(a); db.session.commit(); flash('Pedido rejeitado.', 'success')
    return redirect(url_for('users.profile'))

@users_bp.route('/friend/remove/<int:user_id>', methods=['POST'])
@login_required
def friend_remove(user_id):
    curr = session['user_id']
    a = Amizade.query.filter(((Amizade.user_id==curr)&(Amizade.amigo_id==user_id))|((Amizade.user_id==user_id)&(Amizade.amigo_id==curr))).filter_by(status='accepted').first()
    if a: db.session.delete(a); db.session.commit(); flash('Amizade removida.', 'success')
    return redirect(url_for('users.view_profile', user_id=user_id))

@users_bp.route('/follow/<int:user_id>', methods=['POST'])
@login_required
def follow(user_id):
    curr = Registro.query.get(session['user_id'])
    target = Registro.query.get_or_404(user_id)
    if curr.id != target.id and not curr.seguindo.filter_by(id=user_id).first():
        curr.seguindo.append(target); db.session.commit(); flash(f'Seguindo {target.nome}!', 'success')
    return redirect(url_for('users.view_profile', user_id=user_id))

@users_bp.route('/unfollow/<int:user_id>', methods=['POST'])
@login_required
def unfollow(user_id):
    curr = Registro.query.get(session['user_id'])
    target = Registro.query.get_or_404(user_id)
    if curr.seguindo.filter_by(id=user_id).first():
        curr.seguindo.remove(target); db.session.commit(); flash(f'Deixou de seguir {target.nome}.', 'success')
    return redirect(url_for('users.view_profile', user_id=user_id))

@users_bp.route('/api/friend_suggestions')
@login_required
def api_friend_suggestions():
    curr = session['user_id']
    g = construir_grafo_amizades()
    s_raw = bfs_sugestoes(g, curr, max_dist=3)
    p_ids = set([p.amigo_id for p in Amizade.query.filter_by(user_id=curr).all()] + [p.user_id for p in Amizade.query.filter_by(amigo_id=curr).all()])
    s = []
    for uid, dist in s_raw:
        if uid not in p_ids:
            u = Registro.query.get(uid)
            if u: s.append({"id":u.id,"nome":u.nome,"distancia":dist,"avatar_url":u.perfil.avatar_url if u.perfil else "/static/default_avatar.png","habilidades":[h.nome for h in u.habilidades[:3]],"interesses":[i.nome for i in u.interesses[:3]]})
    return jsonify({"suggestions": s})

def bfs_sugestoes(grafo, origem_id, max_dist=3):
    v, q = set(), deque([(origem_id, 0)])
    s, amigos = [], grafo.get(origem_id, set())
    while q:
        curr, dist = q.popleft()
        if dist > max_dist: break
        if curr in v: continue
        v.add(curr)
        if curr!=origem_id and curr not in amigos: s.append((curr, dist))
        if dist < max_dist:
            for n in grafo.get(curr, []):
                if n not in v: q.append((n, dist+1))
    return s
