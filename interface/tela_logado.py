import os
import pygame
import sys
from interface import cores
from interface.janela import janela_principal


pygame.init()
os.system('cls')


def desenhar_botao(tela, botao, texto, cor_fundo, cor_texto, fonte):
    """
    Desenhar um botão com texto centralizado na tela

    Args:
        tela (pygame.Surface): superfície onde o botão será desenhado
        botao (pygame.Rect): retângulo que define a área do botão
        texto (str): texto exibido no botão
        cor_fundo (tuple): cor do fundo do botão (RGB)
        cor_texto (tuple): cor do texto (RGB)
        fonte (pygame.font.Font): fonte para renderizar o texto
    """
    pygame.draw.rect(tela, cor_fundo, botao)
    texto_render = fonte.render(texto, True, cor_texto)
    texto_rect = texto_render.get_rect(center=botao.center)
    tela.blit(texto_render, texto_rect)


def atualizar_cursor(mouse_pos, botoes, cursor_padrao, cursor_mao):
    """
    Atualizar o cursor do mouse dependendo se está sobre algum botão

    Args:
        mouse_pos (tuple): posição atual do mouse
        botoes (list of pygame.Rect): lista de botões para checar colisão
        cursor_padrao: cursor padrão do sistema
        cursor_mao: cursor de mão (hand) do sistema
    """
    if any(botao.collidepoint(mouse_pos) for botao in botoes):
        pygame.mouse.set_cursor(cursor_mao)

    else:
        pygame.mouse.set_cursor(cursor_padrao)


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
    botao_sair = pygame.Rect(650, 400, 100, 50)  # Criando o botão sair
    padrao_cursor, mao_cursor = cursores

    while True:
        mouse_pos = pygame.mouse.get_pos()
        atualizar_cursor(mouse_pos, [botao_sair], padrao_cursor, mao_cursor)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if botao_sair.collidepoint(event.pos):
                    return janela_principal(
                        tela, largura, altura, fonte, botoes, cursores, fundo)

        tela.fill(cores.BRANCO)

        desenhar_botao(
            tela, botao_sair, 'Sair', cores.VERMELHO_ESC, cores.PRETO, fonte)

        pygame.display.update()
