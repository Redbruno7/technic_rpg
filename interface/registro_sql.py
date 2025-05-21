import sqlite3
from classes import Usuario


conn = sqlite3.connect('C:\Bruno - Técnico DS\\technic_rpg\Guedgers.db')
cursor = conn.cursor()

def registrar_usuario(usuario):
    usuario = Usuario()
    usuario.form_cadastro()
    cursor.execute(
        '''
    INSERT INTO Usuario (nome_usuario, cpf_usuario, email_usuario, senha_usuario)
    VALUES (?, ?, ?, ?)
    ''', (usuario.nome_usuario, usuario.cpf_usuario, usuario.email_usuario, usuario.senha_usuario)
    )
    conn.commit()