import sqlite3


conn = sqlite3.connect('C:\Bruno - Técnico DS\\technic_rpg\Guedgers.db')
cursor = conn.cursor()

cursor.execute(
    '''
CREATE TABLE IF NOT EXISTS Admin(
    id_admin INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_admin TEXT NOT NULL,
    cpf_admin TEXT UNIQUE NOT NULL,
    email_admin TEXT UNIQUE NOT NULL,
    senha_admin TEXT NOT NULL
)
'''
)

cursor.execute(
    '''
CREATE TABLE IF NOT EXISTS Usuario(
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_usuario TEXT NOT NULL,
    cpf_usuario TEXT UNIQUE NOT NULL,
    email_usuario TEXT UNIQUE NOT NULL,
    senha_usuario TEXT NOT NULL
)
'''
)

cursor.execute(
    '''
CREATE TABLE IF NOT EXISTS Produto(
    id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_produto TEXT NOT NULL,
    valor REAL NOT NULL
)
'''
)

cursor.execute(
    '''
CREATE TABLE IF NOT EXISTS GerenciaUnica(
    id_gerencia INTEGER PRIMARY KEY AUTOINCREMENT,
    id_admin INTEGER,
    id_usuario INTEGER,
    categoria_gerencia TEXT NOT NULL,
    FOREIGN KEY (id_admin) REFERENCES Admin (id_admin),
    FOREIGN KEY (id_usuario) REFERENCES Usuario (id_usuario)
)
'''
)

cursor.execute(
    '''
CREATE TABLE IF NOT EXISTS CompraUnica(
    id_compra INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER,
    id_produto INTEGER,
    tipo_pagamento TEXT NOT NULL,
    quantidade TEXT DEFAULT 1,
    valor_total REAL NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuario (id_usuario),
    FOREIGN KEY (id_produto) REFERENCES Produto (id_produto)
)
'''
)

cursor.execute(
    '''
INSERT INTO Admin (nome_admin, cpf_admin, email_admin, senha_admin) VALUES
('Bruno Rodgers', '123.456.789-12', 'bruno.rodgers@email.com', '1234'),
('Guilherme Gerheim', '987.654.321-98', 'guilherme.gerheim', '4321')
'''
)

cursor.execute(
    '''
INSERT INTO Produto (nome_produto, valor) VALUES
('120 Guedgers Coins', '9,90'),
('250 Guedgers Coins', '19,90'),
('525 Guedgers Coins', '39,90'),
('1100 Guedgers Coins', '79,90'),
('3000 Guedgers Coins', '189,90')
'''
)


conn.commit()
conn.close()