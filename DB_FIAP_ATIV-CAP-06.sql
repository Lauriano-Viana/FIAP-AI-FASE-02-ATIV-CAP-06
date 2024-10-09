-- Tabela sensores: armazena dados dos sensores de pragas e doenças
CREATE TABLE sensores (
    id_sensor NUMBER PRIMARY KEY,
    tipo VARCHAR2(50),
    descricao VARCHAR2(100),
    area NUMBER(5,2)
    localizacao VARCHAR2(50)
);
-- Sequência para gerar IDs automáticos para a tabela sensores
CREATE SEQUENCE seq_sensores START WITH 1 INCREMENT BY 1;


-- Tabela produtos: armazena dados dos produtos aplicados a ser usados no CIP
CREATE TABLE produtos (
    id_produto NUMBER PRIMARY KEY,
    nome VARCHAR2(100),
    tipo VARCHAR2(100),         
    dosagem_min NUMBER(5,2),
    dosagem_max NUMBER(5,2)
);
-- Sequência para gerar IDs automáticos para a tabela sensores
CREATE SEQUENCE seq_produtos START WITH 1 INCREMENT BY 1;


-- Tabela leituras: armazena leituras dos sensores de pragas e doenças
CREATE TABLE leituras (
    id_leitura NUMBER PRIMARY KEY,
    id_sensor NUMBER,         
    valor NUMBER(5,2),                         
    data_leitura TIMESTAMP DEFAULT SYSDATE 
    FOREIGN KEY (id_sensor) REFERENCES sensores(id_sensor) 
);
-- Sequência para gerar IDs automáticos
CREATE SEQUENCE seq_leituras START WITH 1 INCREMENT BY 1;


-- Tabela aplicacao_produtos: armazena os ajustes de aplicação 
CREATE TABLE aplicacao_produtos (
    id_aplicacao NUMBER PRIMARY KEY, 
    id_sensor NUMBER,     
    id_leitura NUMBER,
    id_produto NUMBER,
    nome VARCHAR2(100),
    tipo VARCHAR2(100),
    vl_leitura NUMBER(5,2),                     
    quantidade_aplicacao NUMBER(5,2),                
    data_aplicacao TIMESTAMP DEFAULT SYSDATE, 
    FOREIGN KEY (id_sensor) REFERENCES sensores(id_sensor),
    FOREIGN KEY (id_leitura) REFERENCES leituras(id_leitura),
    FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
    
);
-- -- Sequência para gerar IDs automáticos para a tabela aplicacao_produtos
CREATE SEQUENCE seq_aplicacao_produtos START WITH 1 INCREMENT BY 1;


