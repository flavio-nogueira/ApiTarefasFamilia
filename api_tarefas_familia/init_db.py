"""
Script para inicializar o banco de dados
"""
import pymysql

# Configuracoes de conexao
HOST = "76.13.69.127"
PORT = 3306
USER = "dbamysql"
PASSWORD = "@Fn.2026@"
DATABASE = "dbApiTarefasFamilia"


def init_database():
    # Conecta sem especificar banco para criar o database
    conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD)
    cursor = conn.cursor()

    print(f"Conectado ao MySQL em {HOST}:{PORT}")

    # Cria o banco de dados
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")
    cursor.execute(f"USE {DATABASE}")
    print(f"Banco de dados '{DATABASE}' criado/selecionado")

    # Drop tabelas na ordem correta (por causa das FKs)
    print("Removendo tabelas existentes...")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    cursor.execute("DROP TABLE IF EXISTS tarefa_usuario")
    cursor.execute("DROP TABLE IF EXISTS Tarefa")
    cursor.execute("DROP TABLE IF EXISTS Local")
    cursor.execute("DROP TABLE IF EXISTS usuario")
    cursor.execute("DROP TABLE IF EXISTS category")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

    # Cria tabela Local
    print("Criando tabela Local...")
    cursor.execute("""
        CREATE TABLE Local (
            idLocal INT NOT NULL AUTO_INCREMENT,
            Descricao VARCHAR(45) NOT NULL,
            PRIMARY KEY (idLocal)
        ) ENGINE=InnoDB
    """)

    # Cria tabela Tarefa
    print("Criando tabela Tarefa...")
    cursor.execute("""
        CREATE TABLE Tarefa (
            idTarefa INT NOT NULL AUTO_INCREMENT,
            Tarefa VARCHAR(45) NOT NULL,
            Descricao VARCHAR(100),
            Local_idLocal INT,
            PRIMARY KEY (idTarefa),
            CONSTRAINT fk_tarefa_local FOREIGN KEY (Local_idLocal)
                REFERENCES Local(idLocal) ON DELETE SET NULL ON UPDATE CASCADE
        ) ENGINE=InnoDB
    """)

    # Cria tabela usuario
    print("Criando tabela usuario...")
    cursor.execute("""
        CREATE TABLE usuario (
            idUsuario INT NOT NULL AUTO_INCREMENT,
            Nome VARCHAR(45) NOT NULL,
            login VARCHAR(45) NOT NULL,
            senha VARCHAR(255) NOT NULL,
            PRIMARY KEY (idUsuario),
            UNIQUE KEY login_UNIQUE (login)
        ) ENGINE=InnoDB
    """)

    # Cria tabela tarefa_usuario
    print("Criando tabela tarefa_usuario...")
    cursor.execute("""
        CREATE TABLE tarefa_usuario (
            id INT NOT NULL AUTO_INCREMENT,
            usuario_idUsuario INT NOT NULL,
            Tarefa_idTarefa INT NOT NULL,
            Data DATE,
            Periodo VARCHAR(45),
            Feito TINYINT DEFAULT 0,
            DataHoraConclusao VARCHAR(45),
            PRIMARY KEY (id),
            CONSTRAINT fk_tarefa_usuario_usuario FOREIGN KEY (usuario_idUsuario)
                REFERENCES usuario(idUsuario) ON DELETE CASCADE ON UPDATE CASCADE,
            CONSTRAINT fk_tarefa_usuario_tarefa FOREIGN KEY (Tarefa_idTarefa)
                REFERENCES Tarefa(idTarefa) ON DELETE CASCADE ON UPDATE CASCADE
        ) ENGINE=InnoDB
    """)

    # Cria tabela category
    print("Criando tabela category...")
    cursor.execute("""
        CREATE TABLE category (
            category_id INT NOT NULL AUTO_INCREMENT,
            category_name VARCHAR(45) NOT NULL,
            PRIMARY KEY (category_id)
        ) ENGINE=InnoDB
    """)

    conn.commit()

    # Lista tabelas criadas
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print("\nTabelas criadas:")
    for table in tables:
        print(f"  - {table[0]}")

    cursor.close()
    conn.close()
    print("\nBanco de dados inicializado com sucesso!")


if __name__ == "__main__":
    try:
        init_database()
    except Exception as e:
        print(f"Erro: {e}")
