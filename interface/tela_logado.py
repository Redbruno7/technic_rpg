import os

os.system('cls')

from interface import cores
import pygame
import sys


pygame.init()

# Define as dimensões da janela
largura = 1600
altura = 800

# Cria a tela
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Guedgers")

padrao_cursor = pygame.SYSTEM_CURSOR_ARROW
mao_cursor = pygame.SYSTEM_CURSOR_HAND
# digitar = pygame.SYSTEM_CURSOR_IBEAM

fonte = pygame.font.SysFont('Unicode', 40)

def tela_logar(tela, largura, altura, fonte, botoes, cursores, fundo):
    from interface.janela import janela_principal


    botao_sair = pygame.Rect(650, 400, 100, 50) # x, y, largura, altura

    while True:

        mouse_pos = pygame.mouse.get_pos()

        # Verifica se o mouse está sobre os campos de texto ou botão voltar
        # if email_input.collidepoint(mouse_pos) or senha_input.collidepoint(mouse_pos):
        # pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)  # Cursor de texto
        if botao_sair.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if botao_sair.collidepoint(event.pos):
                    return janela_principal(tela, largura, altura, fonte, botoes, cursores, fundo)

        # Preenche a tela com a cor de fundo
        tela.fill(cores.BRANCO)

        pygame.draw.rect(tela, cores.VERMELHO_ESCURO , botao_sair)
        texto = fonte.render('Sair', True, cores.PRETO)
        texto_rect = texto.get_rect(center=botao_sair.center)
        tela.blit(texto, texto_rect)

        # Atualiza o display
        pygame.display.update()
