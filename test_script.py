import sys
import importlib.util
spec = importlib.util.spec_from_file_location("main_app", "app.py")
main_app = importlib.util.module_from_spec(spec)
sys.modules["main_app"] = main_app
spec.loader.exec_module(main_app)

app = main_app.app
from app.models import db
from app.models.user import Registro, Perfil
from app.models.preferences import Habilidade, Interesse
from app.models.post import Post
from app.models.associations import Amizade

def test():
    with app.app_context():
        # Clear existing data for fresh test
        db.drop_all()
        db.create_all()
        
        # Cria usuarios
        u1 = Registro(nome="Alice", email="alice@test.com", senha="123")
        u2 = Registro(nome="Bob", email="bob@test.com", senha="123")
        u3 = Registro(nome="Charlie", email="charlie@test.com", senha="123")
        u4 = Registro(nome="David", email="david@test.com", senha="123")
        
        db.session.add_all([u1, u2, u3, u4])
        db.session.commit()
        
        # --- Teste de Seguidores (Grafo Dirigido) ---
        u1.seguindo.append(u2)  # Alice segue Bob
        db.session.commit()
        
        assert u2 in u1.seguindo.all()
        assert u1 in u2.seguidores_lista # Backref test
        assert u1 not in u2.seguindo.all() # Unilateral
        print("Teste de Seguidores (Grafo Dirigido) passou!")

        # --- Teste de Amizades (Grafo Não-Dirigido com Status) ---
        # Alice envia para Bob
        a1 = Amizade(user_id=u1.id, amigo_id=u2.id, status='accepted')
        # Bob envia para Charlie
        a2 = Amizade(user_id=u2.id, amigo_id=u3.id, status='accepted')
        # Charlie envia para David
        a3 = Amizade(user_id=u3.id, amigo_id=u4.id, status='accepted')
        
        db.session.add_all([a1, a2, a3])
        db.session.commit()
        
        # Verificar se as amizades estão no banco
        assert Amizade.query.count() == 3
        print("Teste de Amizades (Inserção) passou!")

        # --- Teste de Algoritmo BFS (Simulado via Helper do users.py) ---
        from app.routes.users import construir_grafo_amizades, bfs_distancia
        
        grafo = construir_grafo_amizades()
        # Grafo: Alice - Bob - Charlie - David
        
        dist_alice_bob = bfs_distancia(grafo, u1.id, u2.id)
        dist_alice_charlie = bfs_distancia(grafo, u1.id, u3.id)
        dist_alice_david = bfs_distancia(grafo, u1.id, u4.id)
        dist_bob_david = bfs_distancia(grafo, u2.id, u4.id)
        
        assert dist_alice_bob == 1
        assert dist_alice_charlie == 2
        assert dist_alice_david == 3
        assert dist_bob_david == 2
        
        print(f"BFS Distância Alice -> David: {dist_alice_david} (Esperado: 3)")
        print("Teste de BFS Distância passou!")

        # --- Teste de Sugestões (BFS até 3 hops) ---
        from app.routes.users import bfs_sugestoes
        sugestoes_alice = bfs_sugestoes(grafo, u1.id, max_dist=3)
        # Sugestões para Alice (amigo direto: Bob)
        # Charlie (dist 2) e David (dist 3) devem estar nas sugestões
        sugestoes_ids = [s[0] for s in sugestoes_alice]
        assert u3.id in sugestoes_ids
        assert u4.id in sugestoes_ids
        assert u2.id not in sugestoes_ids # Já é amigo direto
        
        print("Teste de BFS Sugestões passou!")

        print("\nTodos as validações de backend e grafos passaram com sucesso!")
        
if __name__ == "__main__":
    test()

