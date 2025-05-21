import os

os.system('cls')

import cores
import pygame
import sys
from principal import janela_principal
from tela_logado import tela_logar


pygame.init()

padrao_cursor = pygame.SYSTEM_CURSOR_ARROW
mao_cursor = pygame.SYSTEM_CURSOR_HAND
digitar = pygame.SYSTEM_CURSOR_IBEAM

# Fonte
fonte = pygame.font.SysFont('Unicode', 40)


def tela_entrar(tela):
    botao_logar = pygame.Rect(850, 400, 100, 50)
    botao_voltar = pygame.Rect(650, 400, 100, 50) # x, y, largura, altura
    email_input = pygame.Rect(600, 150, 400, 50)
    senha_input = pygame.Rect(600, 300, 400, 50)
    texto_email = ''
    texto_senha = ''
    email_ativo = False
    senha_ativo = False

    # Variáveis de controle de "rolagem" do texto
    offset_email = 0
    offset_senha = 0

    while True:

        mouse_pos = pygame.mouse.get_pos()

        # Verifica se o mouse está sobre os campos de texto ou botão voltar
        if email_input.collidepoint(mouse_pos) or senha_input.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)  # Cursor de texto
        elif botao_voltar.collidepoint(mouse_pos) or botao_logar.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_voltar.collidepoint(event.pos):
                    return janela_principal()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_logar.collidepoint(event.pos):
                    return tela_logar()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if email_input.collidepoint(event.pos):
                    email_ativo = True # Ativa o campo
                else:
                    email_ativo = False # Desativa o campo
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if senha_input.collidepoint(event.pos):
                    senha_ativo = True # Ativa o campo
                else:
                    senha_ativo = False # Desativa o campo
            
            if event.type == pygame.KEYDOWN:
                if email_ativo:
                    if event.key == pygame.K_BACKSPACE:
                        # apaga o ultimo caracter
                        texto_email = texto_email[:-1]
                    elif event.key == pygame.K_RETURN:
                        # Quando pressionar enter aparece o texto
                        print('Texto digitado:', texto_email)
                    else:
                        # Adiciona o caractere pressionado ao texto
                        texto_email += event.unicode

                if senha_ativo:
                    if event.key == pygame.K_BACKSPACE:
                        # apaga o ultimo caracter
                        texto_senha = texto_senha[:-1]
                    elif event.key == pygame.K_RETURN:
                        # Quando pressionar enter aparece o texto
                        print('Texto digitado:', texto_senha)
                    else:
                        # Adiciona o caractere pressionado ao texto
                        texto_senha += event.unicode
        
        # Preenche a tela com a cor de fundo
        tela.fill(cores.BRANCO)

        # Renderiza os rótulos "Email" e "Senha" acima dos campos de entrada
        email = fonte.render('Email', True, cores.PRETO)
        senha = fonte.render('Senha', True, cores.PRETO)
        tela.blit(email, (email_input.x, email_input.y - 40))   # Exibe "Email" acima do campo
        tela.blit(senha, (senha_input.x, senha_input.y - 40))   # Exibe "Senha" acima do campo

        # Desenha os retângulos dos campos de entrada
        pygame.draw.rect(tela, cores.OURO, email_input, 2)      # Campo para digitar o email
        pygame.draw.rect(tela, cores.OURO, senha_input, 2)      # Campo para digitar a senha

        # Define a cor do texto digitado com base na ativação dos campos
        cor_email = cores.PRETO if email_ativo else cores.CINZA_CLARO
        cor_senha = cores.PRETO if senha_ativo else cores.CINZA_CLARO

        # Renderiza o texto digitado nos campos
        texto_renderizado_email = fonte.render(texto_email, True, cor_email)
        texto_renderizado_senha = fonte.render(texto_senha, True, cor_senha)

        pygame.draw.rect(tela, cores.VERMELHO_ESCURO , botao_voltar)
        texto = fonte.render('Voltar', True, cores.PRETO)
        texto_rect = texto.get_rect(center=botao_voltar.center)
        tela.blit(texto, texto_rect)

        pygame.draw.rect(tela, cores.OURO , botao_logar)
        texto = fonte.render('Entrar', True, cores.PRETO)
        texto_rect = texto.get_rect(center=botao_logar.center)
        tela.blit(texto, texto_rect)

        # Cálculo da centralização vertical do texto
        altura_texto_email = texto_renderizado_email.get_height()
        altura_texto_senha = texto_renderizado_senha.get_height()

        pos_y_email = email_input.centery - altura_texto_email // 2
        pos_y_senha = senha_input.centery - altura_texto_senha // 2

        # Calcula deslocamento para mostrar final do texto se for maior que o campo
        offset_email = max(0, texto_renderizado_email.get_width() - (email_input.width - 10))
        offset_senha = max(0, texto_renderizado_senha.get_width() - (senha_input.width - 10))

        # Clip e blit dos campos
        tela.set_clip(email_input)
        tela.blit(texto_renderizado_email, (email_input.x + 5 - offset_email, pos_y_email))
        tela.set_clip(senha_input)
        tela.blit(texto_renderizado_senha, (senha_input.x + 5 - offset_senha, pos_y_senha))
        tela.set_clip(None)
        
        # Atualiza a tela
        pygame.display.update()