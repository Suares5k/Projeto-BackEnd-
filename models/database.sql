CREATE DATABASE sghss_db;
USE sghss_db;

CREATE TABLE pacientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    data_nascimento DATE
);

CREATE TABLE consultas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT,
    data_consulta DATETIME NOT NULL,
    medico VARCHAR(100) NOT NULL,
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
);

CREATE TABLE prontuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT,
    data_registro DATETIME NOT NULL,
    descricao TEXT NOT NULL,
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
);