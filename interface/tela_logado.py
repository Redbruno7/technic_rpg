import os
import pygame
import sys
from funcoes_padrao import cores
from funcoes_padrao.mtd_form import desenhar_botao
from interface.tela_principal import janela_principal


pygame.init()
os.system('cls')


def tela_logar(tela, largura, altura, fonte, botoes, cursores, fundo):
    """
    Criar tela de login simples com botão 'Sair' que retorna para a janela principal

    Args:
        tela (pygame.Surface): superfície onde a tela será desenhada
        largura (int): largura da janela
        altura (int): altura da janela
        fonte (pygame.font.Font): fonte para textos
        botoes (tuple): tupla com botões necessários (pode incluir botao_sair)
        cursores (tuple): tupla com cursores (cursor padrão e cursor mão)
        fundo (pygame.Surface): imagem ou cor de fundo da tela

    Returns:
        Função retornada pela janela principal (retorna outra tela ou fecha)
    """
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
                        tela, largura, altura, fonte, botoes, cursores, fundo)

        tela.fill(cores.BRANCO)

        desenhar_botao(tela, botao_sair, "Sair", fonte, cores.VERMELHO_ESC)

        pygame.display.update()
