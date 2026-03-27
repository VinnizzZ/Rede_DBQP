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

# Tabela de ligação: Comunidade <-> Usuários (Membros)
comunidade_membros = db.Table('comunidade_membros',
    db.Column('user_id', db.Integer, db.ForeignKey('registro.id'), primary_key=True),
    db.Column('comunidade_id', db.Integer, db.ForeignKey('comunidade.id'), primary_key=True)
)

# Tabela de ligação: Comunidade <-> Habilidades (Tags do tópico)
comunidade_habilidades = db.Table('comunidade_habilidades',
    db.Column('comunidade_id', db.Integer, db.ForeignKey('comunidade.id'), primary_key=True),
    db.Column('habilidade_id', db.Integer, db.ForeignKey('lista_habilidades.id'), primary_key=True)
)

# Tabela de ligação: Comunidade <-> Interesses (Tags do tópico)
comunidade_interesses = db.Table('comunidade_interesses',
    db.Column('comunidade_id', db.Integer, db.ForeignKey('comunidade.id'), primary_key=True),
    db.Column('interesse_id', db.Integer, db.ForeignKey('lista_interesses.id'), primary_key=True)
)

# ================================================================
# GRAFO NÃO-DIRIGIDO: Amizades (com status para pedidos pendentes)
# ================================================================
class Amizade(db.Model):
    __tablename__ = 'amizades'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('registro.id'), nullable=False)
    amigo_id = db.Column(db.Integer, db.ForeignKey('registro.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending' ou 'accepted'
    
    # Relacionamentos para acesso fácil
    remetente = db.relationship('Registro', foreign_keys=[user_id], backref='pedidos_enviados')
    destinatario = db.relationship('Registro', foreign_keys=[amigo_id], backref='pedidos_recebidos')
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'amigo_id', name='uq_amizade'),
    )

# ================================================================
# GRAFO DIRIGIDO: Seguidores (um segue o outro, unilateral)
# ================================================================
seguidores = db.Table('seguidores',
    db.Column('seguidor_id', db.Integer, db.ForeignKey('registro.id'), primary_key=True),
    db.Column('seguido_id', db.Integer, db.ForeignKey('registro.id'), primary_key=True)
)