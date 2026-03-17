# Imports externos
import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

# Imports internos
from app.models import db, init_models
from app.routes.auth import auth_bp
from app.routes.posts import posts_bp
from app.routes.users import users_bp

app = Flask(__name__)
load_dotenv()

# Configuracoes banco de dados
host = os.getenv('host')
user = os.getenv('user')
password = os.getenv('password')
port = os.getenv('port')
banco = os.getenv('banco')

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{user}:{password}@{host}/{banco}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco com a estrutura modular
init_models(app)

with app.app_context():
    db.create_all()

# Registro de blueprints Flask
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(posts_bp, url_prefix='/posts')
app.register_blueprint(users_bp, url_prefix='/users')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)