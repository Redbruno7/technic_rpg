import os
from interface import cores
import pygame
import sys


pygame.init()
os.system('cls')

# Definir visuais do cursor
padrao_cursor = pygame.SYSTEM_CURSOR_ARROW
mao_cursor = pygame.SYSTEM_CURSOR_HAND
digitar = pygame.SYSTEM_CURSOR_IBEAM

# Definir fonte
fonte = pygame.font.SysFont('Unicode', 40)


def tela_entrar(tela, largura, altura, fonte, botoes, cursores, fundo):
    from interface.janela import janela_principal
    from interface.tela_logado import tela_logar

    # Dimensionar elementos visuais
    botao_logar = pygame.Rect(850, 400, 100, 50) # x, y, largura, altura
    botao_voltar = pygame.Rect(650, 400, 100, 50)
    email_input = pygame.Rect(600, 150, 400, 50)
    senha_input = pygame.Rect(600, 300, 400, 50)

    # Atribuir valores
    texto_email = ''
    texto_senha = ''

    # Criar evento de desselecionar campo
    email_ativo = False
    senha_ativo = False

    # Criar variáveis de controle de deslocamento do texto
    offset_email = 0
    offset_senha = 0

    while True:

        # Identificar posição do cursor
        mouse_pos = pygame.mouse.get_pos()

        # Identificar se cursor está sobre campo de texto
        if email_input.collidepoint(mouse_pos) or senha_input.collidepoint(mouse_pos):

            # Definir padrão para cursor "Ibeam"
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)

        # Identificar se cursor está sobre botão
        elif botao_voltar.collidepoint(mouse_pos) or botao_logar.collidepoint(mouse_pos):

            # Definir padrão para cursor "Hand"
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        # Retornar ao padrão "Arrow"
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Definir eventos de clique
        for event in pygame.event.get():

            # Finalizar programa
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                # Direcionar para tela principal
                if botao_voltar.collidepoint(event.pos):
                    return janela_principal(tela, largura, altura, fonte, botoes, cursores, fundo)
            
                # Direcionar para tela logado
                elif botao_logar.collidepoint(event.pos):
                    return tela_logar(tela, largura, altura, fonte, botoes, cursores, fundo)
                
                email_ativo = email_input.collidepoint(event.pos)
                senha_ativo = senha_input.collidepoint(event.pos)

            # Definir evento de tecla
            if event.type == pygame.KEYDOWN:

                # Verificar seleção do campo email
                if email_ativo:

                    # Definir tecla para apagar texto
                    if event.key == pygame.K_BACKSPACE:

                        # Apagar último caractere
                        texto_email = texto_email[:-1]
                    
                    # Adicionar caractere referente à tecla pressionada
                    else:
                        texto_email += event.unicode

                # Verificar seleção do campo senha
                if senha_ativo:
                    if event.key == pygame.K_BACKSPACE:
                        texto_senha = texto_senha[:-1]

                    else:
                        texto_senha += event.unicode
        
        # Preencher tela com cor de fundo
        tela.fill(cores.BRANCO)

        # Renderizar títulos dos campos - email, senha
        email = fonte.render('Email', True, cores.PRETO)
        senha = fonte.render('Senha', True, cores.PRETO)

        # Dimensionar texto dos campos
        tela.blit(email, (email_input.x, email_input.y - 40))
        tela.blit(senha, (senha_input.x, senha_input.y - 40))

        # Desenhar campos de texto
        pygame.draw.rect(tela, cores.OURO, email_input, 2)
        pygame.draw.rect(tela, cores.OURO, senha_input, 2)

        # Definir a cor do texto digitado - campo selecionado, campo não selecionado
        cor_email = cores.PRETO if email_ativo else cores.CINZA_CLARO
        cor_senha = cores.PRETO if senha_ativo else cores.CINZA_CLARO

        # Renderizar o texto digitado
        texto_renderizado_email = fonte.render(texto_email, True, cor_email)
        texto_renderizado_senha = fonte.render(texto_senha, True, cor_senha)

        # Desenhar botões - voltar, entrar
        pygame.draw.rect(tela, cores.VERMELHO_ESCURO , botao_voltar)
        pygame.draw.rect(tela, cores.OURO , botao_logar)

        # Renderizar texto dos botões
        texto_voltar = fonte.render('Voltar', True, cores.PRETO)
        texto_entrar = fonte.render('Entrar', True, cores.PRETO)

        # Centralizar texto nos botões
        texto_rect = texto_voltar.get_rect(center=botao_voltar.center)
        tela.blit(texto_voltar, texto_rect)        
        texto_rect = texto_entrar.get_rect(center=botao_logar.center)
        tela.blit(texto_entrar, texto_rect)

        # Centralizar verticalmente texto digitado
        altura_texto_email = texto_renderizado_email.get_height()
        altura_texto_senha = texto_renderizado_senha.get_height()
        pos_y_email = email_input.centery - altura_texto_email // 2
        pos_y_senha = senha_input.centery - altura_texto_senha // 2

        # Posicionar início do deslocamento para exibir final do texto digitado
        offset_email = max(0, texto_renderizado_email.get_width() - (email_input.width - 10))
        offset_senha = max(0, texto_renderizado_senha.get_width() - (senha_input.width - 10))

        # Recortar campo email
        tela.set_clip(email_input)
        tela.blit(texto_renderizado_email, (email_input.x + 5 - offset_email, pos_y_email))

        # Recortar campo senha
        tela.set_clip(senha_input)
        tela.blit(texto_renderizado_senha, (senha_input.x + 5 - offset_senha, pos_y_senha))

        # Desativar recortes
        tela.set_clip(None)
        
        # Atualizar a janela
        pygame.display.update()