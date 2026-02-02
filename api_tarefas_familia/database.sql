-- Script para criar o banco de dados dbApiTarefasFamilia
-- Baseado no diagrama ER fornecido
-- IDs são gerados automaticamente (AUTO_INCREMENT)

CREATE DATABASE IF NOT EXISTS dbApiTarefasFamilia;
USE dbApiTarefasFamilia;

-- Tabela Local
-- idLocal é gerado automaticamente na inclusão
DROP TABLE IF EXISTS tarefa_usuario;
DROP TABLE IF EXISTS Tarefa;
DROP TABLE IF EXISTS Local;
DROP TABLE IF EXISTS usuario;
DROP TABLE IF EXISTS category;

CREATE TABLE Local (
    idLocal INT NOT NULL AUTO_INCREMENT,
    Descricao VARCHAR(45) NOT NULL,
    PRIMARY KEY (idLocal)
) ENGINE=InnoDB AUTO_INCREMENT=1;

-- Tabela Tarefa
-- idTarefa é gerado automaticamente na inclusão
CREATE TABLE Tarefa (
    idTarefa INT NOT NULL AUTO_INCREMENT,
    Tarefa VARCHAR(45) NOT NULL,
    Descricao VARCHAR(100),
    Local_idLocal INT,
    PRIMARY KEY (idTarefa),
    CONSTRAINT fk_tarefa_local FOREIGN KEY (Local_idLocal)
        REFERENCES Local(idLocal) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1;

-- Tabela usuario
-- idUsuario é gerado automaticamente na inclusão
CREATE TABLE usuario (
    idUsuario INT NOT NULL AUTO_INCREMENT,
    Nome VARCHAR(45) NOT NULL,
    login VARCHAR(45) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    PRIMARY KEY (idUsuario),
    UNIQUE KEY login_UNIQUE (login)
) ENGINE=InnoDB AUTO_INCREMENT=1;

-- Tabela tarefa_usuario (relacionamento N:N entre tarefa e usuario)
-- id é gerado automaticamente na inclusão
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
) ENGINE=InnoDB AUTO_INCREMENT=1;

-- Tabela category
-- category_id é gerado automaticamente na inclusão
CREATE TABLE category (
    category_id INT NOT NULL AUTO_INCREMENT,
    category_name VARCHAR(45) NOT NULL,
    PRIMARY KEY (category_id)
) ENGINE=InnoDB AUTO_INCREMENT=1;

-- Índices para melhorar performance
CREATE INDEX idx_tarefa_local ON Tarefa(Local_idLocal);
CREATE INDEX idx_tarefa_usuario_usuario ON tarefa_usuario(usuario_idUsuario);
CREATE INDEX idx_tarefa_usuario_tarefa ON tarefa_usuario(Tarefa_idTarefa);
