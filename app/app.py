# Imports externos
import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from dotenv import load_dotenv

# Imports internos
from routes.auth import auth_bp
from routes.posts import posts_bp
from routes.users import users_bp

app = Flask(__name__)

# Configuracoes banco de dados
host = os.getenv('host')
user = os.getenv('user')
password = os.getenv('password')
port = os.getenv('port')
banco = os.getenv('banco')

# Registro de blueprints Flask
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(posts_bp, url_prefix='/posts')
app.register_blueprint(users_bp, url_prefix='/users')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)