import pygame
import sys
from funcoes_padrao import cores
from interface import tela_entrar, tela_registrar
from funcoes_padrao.mtd_form import desenhar_botao

# Iniciar pygame
pygame.init()

# Definir e atribuir dimensões da tela
largura = 1600
altura = 800
tela = pygame.display.set_mode((largura, altura))

# Nomear tela
pygame.display.set_caption("Guedgers")

# Definir fonte
fonte = pygame.font.SysFont('Unicode', 40)

# Dimensionar botões
botao_entrar = pygame.Rect(735, 100, 130, 50)
botao_registrar = pygame.Rect(735, 200, 130, 50)
botao_sair = pygame.Rect(735, 300, 130, 50)

# Unificar botões
botoes = (botao_entrar, botao_registrar, botao_sair)

# Definir visuais para cursor
padrao_cursor = pygame.SYSTEM_CURSOR_ARROW
mao_cursor = pygame.SYSTEM_CURSOR_HAND

# Unificar cursores
cursores = (padrao_cursor, mao_cursor)

# Definir imagem de de fundo
fundo = pygame.image.load("imgs/minecraft.jpg")
fundo = pygame.transform.scale(fundo, (largura, altura))


def janela_principal(tela, largura, altura, fonte, botoes, cursores, fundo):
    """
    Controlar a tela principal do programa, exibir botões para entrar, registrar e sair, além de gerenciar eventos do mouse e troca de telas

    Args:
        tela (pygame.Surface): Surface do pygame onde tudo é desenhado
        largura (int): Largura da janela
        altura (int): Altura da janela
        fonte (pygame.font.Font): Fonte usada para os textos nos botões
        botoes (tuple): Tupla com 3 pygame.Rect, representando os botões Entrar, Registrar e Sair
        cursores (tuple): Tupla com dois cursores pygame, cursor padrão e cursor "mão"
        fundo (pygame.Surface): Imagem usada como fundo da janela

    Returns:
        None ou pygame.Surface: Retorna a surface da tela de login ou registro ao clicar nos botões correspondentes, ou finaliza o programa ao clicar em sair
    """
    botao_entrar, botao_registrar, botao_sair = botoes
    padrao_cursor, mao_cursor = cursores

    while True:
        tela.blit(fundo, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        if (botao_entrar.collidepoint(mouse_pos) or 
            botao_registrar.collidepoint(mouse_pos) or 
            botao_sair.collidepoint(mouse_pos)):

            pygame.mouse.set_cursor(mao_cursor)

        else:
            pygame.mouse.set_cursor(padrao_cursor)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if botao_entrar.collidepoint(event.pos):
                    return tela_entrar.tela_entrar(
                        tela, largura, altura, fonte, botoes, cursores, fundo)
                
                if botao_registrar.collidepoint(event.pos):
                    return tela_registrar.tela_registrar(
                        tela, largura, altura, fonte, botoes, cursores, fundo)
                
                if botao_sair.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        desenhar_botao(tela, botao_entrar, "Entrar", fonte, cores.OURO)
        desenhar_botao(tela, botao_registrar, "Registrar", fonte, cores.OURO)
        desenhar_botao(tela, botao_sair, "Sair", fonte, cores.VERMELHO_ESC)

        pygame.display.update()