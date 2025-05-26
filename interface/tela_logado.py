import os
import pygame
import sys
from funcoes_padrao import cores
from funcoes_padrao.mtd_form import desenhar_botao
from interface.tela_principal import janela_principal


pygame.init()
os.system('cls')

largura = 1600
altura = 800
tela = pygame.display.set_mode((largura, altura))


def tela_logar(tela, largura, altura, fonte, botoes, cursores):

    # Carregar imagem de fundo
    fundo = pygame.image.load("imgs/fundo_logado.png")
    fundo = pygame.transform.scale(fundo, (largura, altura))

    botao_sair = pygame.Rect(650, 400, 100, 50)
    padrao_cursor, mao_cursor = cursores

    while True:
        tela.blit(fundo, (0, 0))
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
                
        # Setar tela de fundo
        tela.blit(fundo, (0, 0))

        desenhar_botao(tela, botao_sair, "Sair", fonte, cores.VERMELHO_ESC)

        pygame.display.update()
