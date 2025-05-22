import pygame
import sys
from interface import tela_entrar, tela_registrar, cores


def desenhar_botao(tela, cor, botao, texto, fonte, cor_texto):
    """
    Desenhar um botão na tela com texto centralizado

    Args:
    - tela: surface do pygame onde o botão será desenhado
    - cor: cor de fundo do botão (tupla RGB)
    - botao: retângulo (pygame.Rect) representando a área do botão
    - texto: string a ser exibida dentro do botão
    - fonte: objeto pygame.font.Font usado para renderizar o texto
    - cor_texto: cor do texto (tupla RGB)
    """
    pygame.draw.rect(tela, cor, botao)
    txt_render = fonte.render(texto, True, cor_texto)
    tela.blit(txt_render, txt_render.get_rect(center=botao.center))


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

        desenhar_botao(
            tela, cores.OURO, botao_entrar, 'Entrar', fonte, cores.PRETO
            )
        desenhar_botao(
            tela, cores.OURO, botao_registrar, 'Registrar', fonte, cores.PRETO
            )
        desenhar_botao(
            tela, cores.VERMELHO_ESC, botao_sair, 'Sair', fonte, cores.PRETO
            )

        pygame.display.update()