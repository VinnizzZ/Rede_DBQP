from flask import Blueprint, render_template, request

# Criamos o Blueprint para Autenticação
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    return render_template('login.html')

@auth_bp.route('/register', methods=['POST'])
def register():
    # Lógica de cadastro aqui
    return "Usuário cadastrado!"