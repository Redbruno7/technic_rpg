import os
import sqlite3
import pygame
import sys
from funcoes_padrao import cores
from funcoes_padrao.mtd_form import desenhar_rotulo_campo
from funcoes_padrao.mtd_form import desenhar_botao
from interface.tela_principal import janela_principal
from interface.tela_editar import tela_editar


pygame.init()
os.system('cls')

largura = 1600
altura = 800
tela = pygame.display.set_mode((largura, altura))


# Conectar Banco de dados
conn = sqlite3.connect(r'C:\guilherme\technic_rpg\Guedgers.db')
cursor = conn.cursor()


def tela_logar(tela, largura, altura, fonte, botoes, cursores, email_original):

    # Carregar imagem de fundo
    fundo = pygame.image.load("imgs/fundo_logado.png")
    fundo = pygame.transform.scale(fundo, (largura, altura))

    guedgers = pygame.image.load("imgs/guedgers.png")

    bem_vindo = pygame.image.load("imgs/info.png")
    bem_vindo = pygame.transform.scale(bem_vindo , (300, 300))



    botao_sair = pygame.Rect(250, 550, 100, 50)
    botao_editar = pygame.Rect(100, 550, 100, 50)
    padrao_cursor, mao_cursor = cursores

    def exibir_usuario():
        cursor.execute(
            '''
            SELECT nome_usuario, cpf_usuario, email_usuario, senha_usuario
            FROM Usuario
            WHERE email_usuario = ?
            ''',
            (email_original,)
        )
        usuario = cursor.fetchone()

        if usuario:
            nome, cpf, email, senha = usuario
        else:
            nome, cpf, email, senha = "Desconhecido", "", "", ""

        fonte_info = pygame.font.SysFont('Unicode', 50)

        texto_nome = fonte_info.render(f"Nome: {nome}", True, cores.BEGE)
        texto_cpf = fonte_info.render(f"CPF: {cpf}", True, cores.BEGE)
        texto_email = fonte_info.render(f"E-mail: {email}", True, cores.BEGE)
        texto_senha = fonte_info.render(f"Senha: {senha}", True, cores.BEGE)

        # Desenhar na tela
        tela.blit(texto_nome, (100, 300))
        tela.blit(texto_cpf, (100, 350))
        tela.blit(texto_email, (100, 400))
        tela.blit(texto_senha, (100, 450))

    while True:
        tela.blit(fundo, (0, 0))
        tela.blit(guedgers, (500, 100))
        tela.blit(bem_vindo, (80, 50))

        mouse_pos = pygame.mouse.get_pos()

        if (botao_sair.collidepoint(mouse_pos)):

            pygame.mouse.set_cursor(mao_cursor)

        else:
            pygame.mouse.set_cursor(padrao_cursor)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if botao_sair.collidepoint(event.pos):
                    return janela_principal(
                        tela, largura, altura, fonte, botoes, cursores)
            

                if botao_editar.collidepoint(event.pos):
                    return tela_editar(
                        tela, largura, altura, fonte, botoes, cursores, email_original)

        desenhar_botao(tela, botao_sair, "Sair", fonte, cores.SANGUE_SECO)
        desenhar_botao(tela, botao_editar, "Editar", fonte, cores.AMARELO_OURO_VELHO)
        exibir_usuario()
        pygame.display.update()
