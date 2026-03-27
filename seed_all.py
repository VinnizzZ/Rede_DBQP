import os
import sys
import random
import importlib.util
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

# Configurar carregamento do app
spec = importlib.util.spec_from_file_location("main_app", "app.py")
main_app = importlib.util.module_from_spec(spec)
sys.modules["main_app"] = main_app
spec.loader.exec_module(main_app)
app = main_app.app

from app.models import db
from app.models.user import Registro, Perfil
from app.models.preferences import Habilidade, Interesse
from app.models.comunidade import Comunidade, ComunidadePost
from app.models.post import Post
from app.models.associations import Amizade, seguidores

def seed():
    with app.app_context():
        print("Iniciando alimentação do banco de dados...")
        
        # 1. Definir Stacks e Interesses
        lista_habilidades = [
            "Python", "JavaScript", "Java", "C++", "C#", "Ruby", "PHP", 
            "Go", "Swift", "Kotlin", "TypeScript", "Rust", "Dart", 
            "React", "Angular", "Vue.js", "Django", "Flask", "Spring Boot", 
            "Node.js", "Express", "Docker", "Kubernetes", "AWS", "Azure",
            "SQL", "NoSQL", "Git", "Linux", "Machine Learning", "Data Science"
        ]
        
        lista_interesses = [
            "Inteligencia Artificial", "Desenvolvimento Web", "Desenvolvimento Mobile",
            "Seguranca da Informacao", "DevOps", "Cloud Computing", "Internet das Coisas",
            "Jogos Digitais", "Realidade Virtual", "Realidade Aumentada",
            "Blockchain", "Criptomoedas", "Big Data", "Data Analytics",
            "UX/UI Design", "Agile", "Scrum", "Empreendedorismo Tech",
            "Open Source", "Arquitetura de Software", "Sistemas Distribuidos"
        ]

        # Criar tags se não existirem
        habilidades_db = {h.nome: h for h in Habilidade.query.all()}
        for h in lista_habilidades:
            if h not in habilidades_db:
                new_h = Habilidade(nome=h)
                db.session.add(new_h)
                habilidades_db[h] = new_h
        
        interesses_db = {i.nome: i for i in Interesse.query.all()}
        for i in lista_interesses:
            if i not in interesses_db:
                new_i = Interesse(nome=i)
                db.session.add(new_i)
                interesses_db[i] = new_i
        
        db.session.commit()

        # 2. Criar Usuários (15 fakes)
        nomes = [
            "Alice Silva", "Bob Oliveira", "Carol Santos", "David Rocha", "Elena Costa",
            "Fabio Mendes", "Gisele Lima", "Hugo Souza", "Iris Carvalho", "Joao Gomes",
            "Karina Alves", "Leonardo Bruno", "Marta Julia", "Nato Alves", "Olivia Beatriz"
        ]
        
        hashed_password = generate_password_hash("123456")
        usuarios = []
        
        for nome in nomes:
            email = nome.lower().replace(" ", ".") + "@fake.com"
            user = Registro.query.filter_by(email=email).first()
            if not user:
                user = Registro(nome=nome, email=email, senha=hashed_password)
                db.session.add(user)
                db.session.flush()
                
                perfil = Perfil(
                    user_id=user.id,
                    biografia=f"Olá, eu sou {nome}. Desenvolvedor apaixonado por {random.choice(lista_habilidades)} e focado em {random.choice(lista_interesses)}.",
                    avatar_url=f"https://api.dicebear.com/7.x/avataaars/svg?seed={nome.replace(' ', '')}"
                )
                db.session.add(perfil)
                
                # Atribuir skills e interesses aleatórios
                habs = random.sample(list(habilidades_db.values()), random.randint(3, 6))
                ints = random.sample(list(interesses_db.values()), random.randint(3, 6))
                for h in habs: user.habilidades.append(h)
                for i in ints: user.interesses.append(i)
                
            usuarios.append(user)
        
        db.session.commit()
        print(f"Usuários criados: {len(usuarios)}")

        # 3. Criar Comunidades
        comunidades_data = [
            ("DevOps Brasil", "Comunidade para entusiastas de automação e cloud.", ["Docker", "Kubernetes", "AWS"], ["DevOps", "Cloud Computing"]),
            ("Frontend Masters", "Focado em React, Vue e design de interfaces.", ["React", "TypeScript", "JavaScript"], ["Desenvolvimento Web", "UX/UI Design"]),
            ("AI & Data Engineering", "Dados, modelos e arquitetura de inteligência.", ["Python", "SQL", "Machine Learning"], ["Inteligencia Artificial", "Big Data"]),
            ("Game Dev Junkies", "Desenvolvimento de jogos com C++ e Rust.", ["C++", "Rust"], ["Jogos Digitais", "Sistemas Distribuidos"]),
            ("Cyber Security Squad", "Segurança ofensiva e defensiva.", ["Linux", "Python", "PHP"], ["Seguranca da Informacao", "Internet das Coisas"])
        ]
        
        comunidades = []
        for nome, desc, habs, ints in comunidades_data:
            com = Comunidade.query.filter_by(nome=nome).first()
            if not com:
                criador = random.choice(usuarios)
                com = Comunidade(nome=nome, descricao=desc, criador_id=criador.id)
                db.session.add(com)
                db.session.flush()
                
                for h in habs: com.habilidades.append(habilidades_db[h])
                for i in ints: com.interesses.append(interesses_db[i])
                
                # Adicionar 5-10 membros aleatórios
                membros = random.sample(usuarios, random.randint(5, 10))
                for m in membros:
                    if m not in com.membros:
                        com.membros.append(m)
            
            comunidades.append(com)
            
        db.session.commit()
        print(f"Comunidades criadas: {len(comunidades)}")

        # 4. Criar Postagens (Feed Geral)
        posts_conteudos = [
            "Acabei de aprender como o Dijkstra funciona no DBQP! Sensacional.",
            "Alguém aí recomenda um curso bom de Rust? A performance é absurda.",
            "Docker Compose é vida. Facilita muito o setup local.",
            "Hoje o dia foi de debug no CSS... Centralizar div ainda é um desafio kkk",
            "Ansioso para o próximo evento de IA em SP!",
            "O algoritmo de Kruskal é elegante demais para achar o MST.",
            "Node.js vs Go para microserviços de alta performance, o que acham?",
            "Cloud Computing no Azure está cada vez mais intuitivo."
        ]
        
        for _ in range(30):
            u = random.choice(usuarios)
            p = Post(conteudo=random.choice(posts_conteudos), user_id=u.id, data_criacao=datetime.utcnow() - timedelta(hours=random.randint(1, 100)))
            db.session.add(p)
            
        # 5. Criar Postagens de Comunidade
        for com in comunidades:
            for _ in range(random.randint(3, 7)):
                u = random.choice(com.membros)
                cp = ComunidadePost(
                    conteudo=f"Dúvida rápida sobre o tópico da {com.nome}: " + random.choice(posts_conteudos),
                    user_id=u.id,
                    comunidade_id=com.id,
                    data_criacao=datetime.utcnow() - timedelta(hours=random.randint(1, 48))
                )
                db.session.add(cp)
        
        db.session.commit()
        print("Postagens criadas.")

        # 6. Criar Relacionamentos (Amizades e Seguidores)
        # Isso gera o grafo para os algoritmos de BFS/DFS/Dijkstra
        print("Gerando conexões sociais (grafos)...")
        
        # Amizades (Grafo Não-Dirigido)
        amizades_count = 0
        for _ in range(40):
            u1, u2 = random.sample(usuarios, 2)
            # Evitar duplicatas
            if u1.id != u2.id:
                # Ordenar IDs para garantir unicidade no banco (conforme o UniqueConstraint se houver)
                # Mas aqui o modelo usa user_id e amigo_id.
                existente = Amizade.query.filter(
                    ((Amizade.user_id == u1.id) & (Amizade.amigo_id == u2.id)) |
                    ((Amizade.user_id == u2.id) & (Amizade.amigo_id == u1.id))
                ).first()
                
                if not existente:
                    # Amizade com status 'accepted' para valer no grafo
                    amizade = Amizade(user_id=u1.id, amigo_id=u2.id, status='accepted')
                    db.session.add(amizade)
                    amizades_count += 1
        
        # Seguidores (Grafo Dirigido)
        seguidores_count = 0
        for _ in range(50):
            seguidor, seguido = random.sample(usuarios, 2)
            if seguidor.id != seguido.id:
                # Inserir direto na tabela seguidores via execute ou append se for dinâmico
                # Usando o backref/relationship 'seguindo'
                if seguido not in seguidor.seguindo:
                    seguidor.seguindo.append(seguido)
                    seguidores_count += 1
        
        db.session.commit()
        print(f"Conexões geradas: {amizades_count} amizades e {seguidores_count} seguidores.")
        
        print("\nSucesso! Banco de dados alimentado com dados randômicos complexos.")

if __name__ == "__main__":
    seed()
