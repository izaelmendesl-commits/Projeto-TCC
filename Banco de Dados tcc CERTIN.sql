-- 1. Apaga o banco antigo para não dar conflito
DROP DATABASE IF EXISTS avisos_sistema;

-- 2. Cria o banco do zero
CREATE DATABASE avisos_sistema;
USE avisos_sistema;

CREATE TABLE cursos (
    codcurso INT PRIMARY KEY,
    descricao VARCHAR(200) NOT NULL
);

-- Aqui está o segredo: VARCHAR(10) para aceitar "3A", "3I", etc.
CREATE TABLE turmas (
    codturma VARCHAR(10) PRIMARY KEY, 
    codcurso INT NOT NULL,
    FOREIGN KEY (codcurso) REFERENCES cursos(codcurso)
);

CREATE TABLE alunos (
    matricula INT PRIMARY KEY,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    nome_completo VARCHAR(255) NOT NULL,
    codturma VARCHAR(10) NOT NULL, 
    email VARCHAR(100) NOT NULL,
    FOREIGN KEY (codturma) REFERENCES turmas(codturma)
);

CREATE TABLE aviso (
    codaviso INT PRIMARY KEY,
    datacadastro DATE NOT NULL,
    dataenvio DATE NOT NULL,
    aviso TEXT NOT NULL
);

CREATE TABLE turma_aviso (
    codaviso INT NOT NULL,
    codturma VARCHAR(10) NOT NULL, 
    PRIMARY KEY (codaviso, codturma),
    FOREIGN KEY (codaviso) REFERENCES aviso(codaviso),
    FOREIGN KEY (codturma) REFERENCES turmas(codturma)
);