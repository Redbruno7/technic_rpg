import pygame
import sys
from interface import tela_entrar, tela_registrar, cores


def desenhar_botao(tela, cor, botao, texto, fonte, cor_texto):

    # Desenhar botão
    pygame.draw.rect(tela, cor, botao)

    # Inserir texto
    txt_render = fonte.render(texto, True, cor_texto)

    # Centralizar texto
    tela.blit(txt_render, txt_render.get_rect(center=botao.center))


def janela_principal(tela, largura, altura, fonte, botoes, cursores, fundo):

    # Unificar variáveis - botões, cursores
    botao_entrar, botao_registrar, botao_sair = botoes
    padrao_cursor, mao_cursor = cursores

    # Criar loop principal
    while True:

        # Localizar início da imagem de fundo
        tela.blit(fundo, (0, 0))

        # Identificar posição do cursor
        mouse_pos = pygame.mouse.get_pos()

        # Identificar se cursor está sobre botão
        if (botao_entrar.collidepoint(mouse_pos) or 
            botao_registrar.collidepoint(mouse_pos) or 
            botao_sair.collidepoint(mouse_pos)):

            # Definir padrão para cursor "Hand"
            pygame.mouse.set_cursor(mao_cursor)

        # Retorna ao cursor padrão
        else:
            pygame.mouse.set_cursor(padrao_cursor)

        # Definir eventos de clique
        for event in pygame.event.get():

            # Finalizar programa
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                # Direcionar para tela de login
                if botao_entrar.collidepoint(event.pos):
                    return tela_entrar.tela_entrar(tela, largura, altura, fonte, botoes, cursores, fundo)
                
                # Direcionar para tela de registro
                if botao_registrar.collidepoint(event.pos):
                    return tela_registrar.tela_registrar(tela, largura, altura, fonte, botoes, cursores, fundo)
                
                # Finalizar programa
                if botao_sair.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        # Invocar função - desenhar_botao()
        desenhar_botao(tela, cores.OURO, botao_entrar, 'Entrar', fonte, cores.PRETO)
        desenhar_botao(tela, cores.OURO, botao_registrar, 'Registrar', fonte, cores.PRETO)
        desenhar_botao(tela, cores.VERMELHO_ESCURO, botao_sair, 'Sair', fonte, cores.PRETO)

        # Atualizar o display
        pygame.display.update()
        