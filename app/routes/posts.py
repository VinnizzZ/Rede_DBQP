from flask import Blueprint

posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/')
def index():
    return "Feed da Rede Social"