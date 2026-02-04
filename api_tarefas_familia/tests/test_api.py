"""
Testes unitarios para a API Tarefas Familia
"""
import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)


class TestRoot:
    """Testes para o endpoint raiz"""

    def test_root(self):
        """Testa endpoint raiz"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["version"] == "1.0.0"

    def test_health(self):
        """Testa endpoint de health check"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestLocais:
    """Testes para endpoints de Locais"""

    def test_listar_locais(self):
        """Testa listagem de locais"""
        response = client.get("/locais/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_criar_local(self):
        """Testa criacao de local"""
        response = client.post("/locais/", json={"Descricao": "Cozinha Teste"})
        assert response.status_code == 201
        data = response.json()
        assert data["Descricao"] == "Cozinha Teste"
        assert "idLocal" in data

    def test_obter_local_inexistente(self):
        """Testa busca de local inexistente"""
        response = client.get("/locais/99999")
        assert response.status_code == 404


class TestTarefas:
    """Testes para endpoints de Tarefas"""

    def test_listar_tarefas(self):
        """Testa listagem de tarefas"""
        response = client.get("/tarefas/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_criar_tarefa(self):
        """Testa criacao de tarefa"""
        response = client.post("/tarefas/", json={
            "Tarefa": "Lavar louca teste",
            "Descricao": "Lavar toda a louca"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["Tarefa"] == "Lavar louca teste"
        assert "idTarefa" in data

    def test_obter_tarefa_inexistente(self):
        """Testa busca de tarefa inexistente"""
        response = client.get("/tarefas/99999")
        assert response.status_code == 404


class TestUsuarios:
    """Testes para endpoints de Usuarios"""

    def test_listar_usuarios(self):
        """Testa listagem de usuarios"""
        response = client.get("/usuarios/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_criar_usuario(self):
        """Testa criacao de usuario"""
        import random
        login_teste = f"teste_{random.randint(1000, 9999)}"
        response = client.post("/usuarios/", json={
            "Nome": "Usuario Teste",
            "login": login_teste,
            "senha": "senha123"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["Nome"] == "Usuario Teste"
        assert data["login"] == login_teste
        assert "idUsuario" in data
        # Senha nao deve ser retornada
        assert "senha" not in data

    def test_obter_usuario_inexistente(self):
        """Testa busca de usuario inexistente"""
        response = client.get("/usuarios/99999")
        assert response.status_code == 404


class TestLogin:
    """Testes para endpoint de Login"""

    def test_login_usuario_inexistente(self):
        """Testa login com usuario inexistente"""
        response = client.post("/usuarios/login", json={
            "login": "usuario_que_nao_existe",
            "senha": "qualquersenha"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["sucesso"] == False
        assert "nao encontrado" in data["mensagem"].lower()

    def test_login_senha_incorreta(self):
        """Testa login com senha incorreta"""
        # Primeiro cria um usuario
        import random
        login_teste = f"login_teste_{random.randint(1000, 9999)}"
        client.post("/usuarios/", json={
            "Nome": "Teste Login",
            "login": login_teste,
            "senha": "senhaCorreta123"
        })

        # Tenta login com senha errada
        response = client.post("/usuarios/login", json={
            "login": login_teste,
            "senha": "senhaErrada"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["sucesso"] == False
        assert "incorreta" in data["mensagem"].lower()

    def test_login_sucesso(self):
        """Testa login com sucesso"""
        # Primeiro cria um usuario
        import random
        login_teste = f"login_sucesso_{random.randint(1000, 9999)}"
        client.post("/usuarios/", json={
            "Nome": "Teste Login Sucesso",
            "login": login_teste,
            "senha": "minhasenha123"
        })

        # Faz login
        response = client.post("/usuarios/login", json={
            "login": login_teste,
            "senha": "minhasenha123"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["sucesso"] == True
        assert data["usuario"] is not None
        assert data["usuario"]["login"] == login_teste


class TestCategorias:
    """Testes para endpoints de Categorias"""

    def test_listar_categorias(self):
        """Testa listagem de categorias"""
        response = client.get("/categorias/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_criar_categoria(self):
        """Testa criacao de categoria"""
        response = client.post("/categorias/", json={"category_name": "Limpeza Teste"})
        assert response.status_code == 201
        data = response.json()
        assert data["category_name"] == "Limpeza Teste"
        assert "category_id" in data


class TestTarefasUsuarios:
    """Testes para endpoints de Tarefas-Usuarios"""

    def test_listar_atribuicoes(self):
        """Testa listagem de atribuicoes"""
        response = client.get("/tarefas-usuarios/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
