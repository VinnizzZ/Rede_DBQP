import os
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash, current_app
from werkzeug.utils import secure_filename
from app.models import db
from app.models.user import Registro, Perfil
from app.models.preferences import Habilidade, Interesse

users_bp = Blueprint('users', __name__)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@users_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = Registro.query.get(session['user_id'])
    
    if request.method == 'POST':
        biografia = request.form.get('biografia', '')
        github_url = request.form.get('github_url', '')
        
        # Atualiza o perfil básico
        perfil = user.perfil
        if not perfil:
            perfil = Perfil(user_id=user.id)
            db.session.add(perfil)
            
        avatar_file = request.files.get('avatar')
        if avatar_file and avatar_file.filename != '':
            filename = secure_filename(avatar_file.filename)
            
            # Garante que a imagem seja salva na pasta app/static já existente
            static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
            uploads_dir = os.path.join(static_dir, 'uploads')
            os.makedirs(uploads_dir, exist_ok=True)
            
            file_path = os.path.join(uploads_dir, filename)
            avatar_file.save(file_path)
            perfil.avatar_url = f"/static/uploads/{filename}"
        elif not perfil.avatar_url:
            perfil.avatar_url = "/static/default_avatar.png"
            
        perfil.biografia = biografia
        perfil.github_url = github_url
        
        # Atualiza Habilidades (separadas por vírgula)
        habilidades_str = request.form.get('habilidades', '')
        habilidades_nomes = [h.strip() for h in habilidades_str.split(',') if h.strip()]
        
        user.habilidades = []
        for h_nome in habilidades_nomes:
            hab = Habilidade.query.filter_by(nome=h_nome).first()
            if not hab:
                hab = Habilidade(nome=h_nome)
                db.session.add(hab)
            user.habilidades.append(hab)
            
        # Atualiza Interesses (separadas por vírgula)
        interesses_str = request.form.get('interesses', '')
        interesses_nomes = [i.strip() for i in interesses_str.split(',') if i.strip()]
        
        user.interesses = []
        for i_nome in interesses_nomes:
            int_obj = Interesse.query.filter_by(nome=i_nome).first()
            if not int_obj:
                int_obj = Interesse(nome=i_nome)
                db.session.add(int_obj)
            user.interesses.append(int_obj)
            
        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('users.profile'))
        
    return render_template('profile.html', user=user)

@users_bp.route('/profile/<int:user_id>')
@login_required
def view_profile(user_id):
    if user_id == session['user_id']:
        return redirect(url_for('users.profile'))
    
    user = Registro.query.get_or_404(user_id)
    return render_template('view_profile.html', user=user)

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
    
    # Criar nodes
    for u in all_users:
        nodes.append({
            "id": u.id,
            "label": u.nome,
            "title": f"Habilidades: {', '.join([h.nome for h in u.habilidades])}\\nInteresses: {', '.join([i.nome for i in u.interesses])}",
            "group": 1 if u.id == current_user_id else 2,
            "shape": "circularImage" if u.perfil and u.perfil.avatar_url else "dot",
            "image": u.perfil.avatar_url if u.perfil and u.perfil.avatar_url else None
        })
        
    # Criar edges baseados em compartilhamentos
    for i in range(len(all_users)):
        for j in range(i + 1, len(all_users)):
            user1 = all_users[i]
            user2 = all_users[j]
            
            shared_habilidades = set([h.nome for h in user1.habilidades]) & set([h.nome for h in user2.habilidades])
            shared_interesses = set([int_obj.nome for int_obj in user1.interesses]) & set([int_obj.nome for int_obj in user2.interesses])
            
            weight = len(shared_habilidades) + len(shared_interesses)
            
            if weight > 0:
                titles = []
                if shared_habilidades:
                    titles.append(f"Hab: {', '.join(shared_habilidades)}")
                if shared_interesses:
                    titles.append(f"Int: {', '.join(shared_interesses)}")
                    
                edges.append({
                    "from": user1.id,
                    "to": user2.id,
                    "value": weight, # Thicker edge for more shared items
                    "title": " | ".join(titles)
                })
                
    return jsonify({"nodes": nodes, "edges": edges})