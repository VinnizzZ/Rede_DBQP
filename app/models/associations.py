from . import db

# Tabela de ligação: Usuários <-> Habilidades
user_habilidades = db.Table('user_habilidades',
    db.Column('user_id', db.Integer, db.ForeignKey('registro.id'), primary_key=True),
    db.Column('lista_habilidade_id', db.Integer, db.ForeignKey('lista_habilidades.id'), primary_key=True)
)

# Tabela de ligação: Usuários <-> Interesses
user_interesses = db.Table('user_interesses',
    db.Column('user_id', db.Integer, db.ForeignKey('registro.id'), primary_key=True),
    db.Column('lista_interesse_id', db.Integer, db.ForeignKey('lista_interesses.id'), primary_key=True)
)