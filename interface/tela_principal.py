import os
import pygame
import sys
from funcoes_padrao import cores
from interface import tela_entrar, tela_registrar
from funcoes_padrao.mtd_form import desenhar_botao


pygame.init()
os.system('cls')

# Dimensões de tela fullscreen baseada no monitor do usuário
info = pygame.display.Info()
largura, altura = info.current_w, info.current_h
tela = pygame.display.set_mode((largura, altura), pygame.FULLSCREEN)

# Imagem de fundo
fundo = pygame.image.load("imgs/guedgers_principal.png")
fundo = pygame.transform.scale(fundo, (largura, altura))

# Imagem - Ícone padrão
icone = pygame.image.load("imgs/icone.png")
pygame.display.set_icon(icone)

# Nome da janela padrão
pygame.display.set_caption("Guedgers")

# Fonte padrão
fonte = pygame.font.SysFont('Unicode', 40)

# Posição dos campos e botões
botao_entrar = pygame.Rect(620, 500, 370, 50)
botao_registrar = pygame.Rect(620, 600, 370, 50)
botao_sair = pygame.Rect(735, 750, 130, 50)

# Tupla - Botões
botoes = (botao_entrar, botao_registrar, botao_sair)

# Visuais cursor
padrao_cursor = pygame.SYSTEM_CURSOR_ARROW
mao_cursor = pygame.SYSTEM_CURSOR_HAND

# Unificar cursores
cursores = (padrao_cursor, mao_cursor)


def janela_principal(tela, largura, altura, fonte, botoes, cursores):
    """
    Exibe a tela principal com os botões Entrar, Registrar e Sair.

    Args:
        tela (pygame.Surface): Superfície da janela.
        largura (int): Largura da tela.
        altura (int): Altura da tela.
        fonte (pygame.font.Font): Fonte usada nos botões.
        botoes (tuple): Tupla com os retângulos dos botões.
        cursores (tuple): Tupla com os tipos de cursores.

    Returns:
        tela_entrar/tela_registrar: Redireciona para outra tela conforme botão clicado.
    """
    # Separar botões
    botao_entrar, botao_registrar, botao_sair = botoes
    padrao_cursor, mao_cursor = cursores

    # Loop principal
    while True:
        tela.blit(fundo, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        # Atualizar cursor
        if (botao_entrar.collidepoint(mouse_pos) or
            botao_registrar.collidepoint(mouse_pos) or
                botao_sair.collidepoint(mouse_pos)):

            pygame.mouse.set_cursor(mao_cursor)

        else:
            pygame.mouse.set_cursor(padrao_cursor)

        # Eventos
        for event in pygame.event.get():

            # MOUSE BTN-1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    # Botão Entrar
                    if botao_entrar.collidepoint(event.pos):
                        return tela_entrar.tela_entrar(
                            tela, largura, altura, fonte, botoes, cursores)

                    # Botão Registrar
                    if botao_registrar.collidepoint(event.pos):
                        return tela_registrar.tela_registrar(
                            tela, largura, altura, fonte, botoes, cursores)

                    # Botão Sair
                    if botao_sair.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

        # Invocar método - Desenhar botão
        desenhar_botao(tela, botao_entrar, "Entrar", fonte, cores.AMARELO_OURO_VELHO)
        desenhar_botao(tela, botao_registrar, "Registrar", fonte, cores.AMARELO_OURO_VELHO)
        desenhar_botao(tela, botao_sair, "Sair", fonte, cores.SANGUE_SECO)

        pygame.display.update()
