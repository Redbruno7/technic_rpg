import os

os.system('cls')

import cores
import pygame
import sys
from principal import janela_principal
import registro_sql


pygame.init()

# Fonte
fonte = pygame.font.SysFont('Unicode', 40)

padrao_cursor = pygame.SYSTEM_CURSOR_ARROW
mao_cursor = pygame.SYSTEM_CURSOR_HAND
digitar = pygame.SYSTEM_CURSOR_IBEAM



def tela_registrar(tela):
    botao_voltar = pygame.Rect(620, 600, 130, 50) # x, y, largura, altura
    botao_registrar = pygame.Rect(850, 600, 130, 50)
    nome_input = pygame.Rect(600, 150, 400, 50)
    cpf_input =  pygame.Rect(600, 270, 400, 50)
    email_input = pygame.Rect(600, 380, 400, 50)
    senha_input = pygame.Rect(600, 500, 400, 50)
    texto_nome = ''
    texto_cpf = ''
    texto_email = ''
    texto_senha = ''
    nome_ativo = False
    cpf_ativo = False
    email_ativo = False
    senha_ativo = False

    # Variáveis de controle de "rolagem" do texto
    offset_nome = 0
    offset_cpf = 0
    offset_email = 0
    offset_senha = 0

    while True:

        mouse_pos = pygame.mouse.get_pos()

        # Verifica se o mouse está sobre os campos de texto ou botão voltar
        if email_input.collidepoint(mouse_pos) or senha_input.collidepoint(mouse_pos) or cpf_input.collidepoint(mouse_pos) or nome_input.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)  # Cursor de texto
        elif botao_voltar.collidepoint(mouse_pos) or botao_registrar.collidepoint(mouse_pos):
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
                if nome_input.collidepoint(event.pos):
                    nome_ativo = True # Ativa o campo
                else:
                    nome_ativo = False # Desativa o campo
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cpf_input.collidepoint(event.pos):
                    cpf_ativo = True # Ativa o campo
                else:
                    cpf_ativo = False # Desativa o campo
            
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

            # Botão Registrar
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_registrar.collidepoint(event.pos):
                    registro_sql.registrar_usuario()
                    
            if event.type == pygame.KEYDOWN:
                if nome_ativo:
                    if event.key == pygame.K_BACKSPACE:
                        # apaga o ultimo caracter
                        texto_nome = texto_nome[:-1]
                    elif event.key == pygame.K_RETURN:
                        # Quando pressionar enter aparece o texto
                        print('Texto digitado:', texto_nome)
                    else:
                        # Adiciona o caractere pressionado ao texto
                        texto_nome += event.unicode
                
                if cpf_ativo:
                    if event.key == pygame.K_BACKSPACE:
                        # apaga o ultimo caracter
                        texto_cpf = texto_cpf[:-1]
                    elif event.key == pygame.K_RETURN:
                        # Quando pressionar enter aparece o texto
                        print('Texto digitado:', texto_cpf)
                    else:
                        # Adiciona o caractere pressionado ao texto
                        texto_cpf += event.unicode
                
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

        # Renderiza os rótulos acima dos campos de entrada
        nome = fonte.render('Nome', True, cores.PRETO)
        cpf = fonte.render('CPF', True, cores.PRETO)
        email = fonte.render('Email', True, cores.PRETO)
        senha = fonte.render('Senha', True, cores.PRETO)
        tela.blit(nome, (nome_input.x, nome_input.y - 40))
        tela.blit(cpf, (cpf_input.x, cpf_input.y - 40))
        tela.blit(email, (email_input.x, email_input.y - 40))   # Exibe "Email" acima do campo
        tela.blit(senha, (senha_input.x, senha_input.y - 40))   # Exibe "Senha" acima do campo

        # Desenha os retângulos dos campos de entrada
        pygame.draw.rect(tela, cores.OURO, nome_input, 2)
        pygame.draw.rect(tela, cores.OURO, cpf_input, 2)
        pygame.draw.rect(tela, cores.OURO, email_input, 2)      # Campo para digitar o email
        pygame.draw.rect(tela, cores.OURO, senha_input, 2)      # Campo para digitar a senha

        # Define a cor do texto digitado com base na ativação dos campos
        cor_nome = cores.PRETO if nome_ativo else cores.CINZA_CLARO
        cor_cpf = cores.PRETO if cpf_ativo else cores.CINZA_CLARO
        cor_email = cores.PRETO if email_ativo else cores.CINZA_CLARO
        cor_senha = cores.PRETO if senha_ativo else cores.CINZA_CLARO

        # Renderiza o texto digitado nos campos
        texto_renderizado_nome = fonte.render(texto_nome, True, cor_nome)
        texto_renderizado_cpf = fonte.render(texto_cpf, True, cor_cpf)
        texto_renderizado_email = fonte.render(texto_email, True, cor_email)
        texto_renderizado_senha = fonte.render(texto_senha, True, cor_senha)

        # Cálculo da centralização vertical do texto
        altura_texto_nome = texto_renderizado_nome.get_height()
        altura_texto_cpf = texto_renderizado_cpf.get_height()
        altura_texto_email = texto_renderizado_email.get_height()
        altura_texto_senha = texto_renderizado_senha.get_height()

        pos_y_nome = nome_input.centery - altura_texto_nome // 2
        pos_y_cpf = cpf_input.centery - altura_texto_cpf // 2
        pos_y_email = email_input.centery - altura_texto_email // 2
        pos_y_senha = senha_input.centery - altura_texto_senha // 2

        # Calcula deslocamento para mostrar final do texto se for maior que o campo
        offset_nome = max(0, texto_renderizado_nome.get_width() - (nome_input.width - 10))
        offset_cpf = max(0, texto_renderizado_cpf.get_width() - (cpf_input.width - 10))
        offset_email = max(0, texto_renderizado_email.get_width() - (email_input.width - 10))
        offset_senha = max(0, texto_renderizado_senha.get_width() - (senha_input.width - 10))

        # Clip e blit dos campos
        tela.set_clip(nome_input)
        tela.blit(texto_renderizado_nome, (nome_input.x + 5 - offset_nome, pos_y_nome))

        tela.set_clip(cpf_input)
        tela.blit(texto_renderizado_cpf, (cpf_input.x + 5 - offset_cpf, pos_y_cpf))

        tela.set_clip(email_input)
        tela.blit(texto_renderizado_email, (email_input.x + 5 - offset_email, pos_y_email))

        tela.set_clip(senha_input)
        tela.blit(texto_renderizado_senha, (senha_input.x + 5 - offset_senha, pos_y_senha))

        tela.set_clip(None)

        pygame.draw.rect(tela, cores.VERMELHO_ESCURO , botao_voltar)
        texto = fonte.render('Voltar', True, cores.PRETO)
        texto_rect = texto.get_rect(center=botao_voltar.center)
        tela.blit(texto, texto_rect)

        pygame.draw.rect(tela, cores.OURO, botao_registrar)
        texto = fonte.render('Registrar', True, cores.PRETO)
        texto_rect = texto.get_rect(center=botao_registrar.center)
        tela.blit(texto, texto_rect)

        # Atualiza a tela
        pygame.display.update()