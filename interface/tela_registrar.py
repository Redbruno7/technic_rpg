import os

os.system('cls')

from interface import cores
import pygame
import sys
import sqlite3

pygame.init()

# Fonte
fonte = pygame.font.SysFont('Unicode', 40)

# Definir padrões de cursor
padrao_cursor = pygame.SYSTEM_CURSOR_ARROW
mao_cursor = pygame.SYSTEM_CURSOR_HAND
digitar = pygame.SYSTEM_CURSOR_IBEAM

conn = sqlite3.connect(r'C:\Bruno - Técnico DS\technic_rpg\Guedgers.db')
cursor = conn.cursor()


def tela_registrar(tela, largura, altura, fonte, botoes, cursores, fundo):
    from interface.janela import janela_principal


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

    offset_nome = 0
    offset_cpf = 0
    offset_email = 0
    offset_senha = 0

    mensagem_erro = ''

    def registrar_usuario():
        nonlocal mensagem_erro

        if not (texto_nome and texto_cpf and texto_email and texto_senha):
            mensagem_erro = 'Preencha todos os campos!'
            return False  # ERRO

        try:
            cursor.execute(
                '''
                INSERT INTO Usuario (nome_usuario, cpf_usuario, email_usuario, senha_usuario)
                VALUES (?, ?, ?, ?)
                ''', (texto_nome, texto_cpf, texto_email, texto_senha)
            )
            conn.commit()
            mensagem_erro = 'Usuário registrado com sucesso!'
            return True  # SUCESSO

        except Exception as e:
            mensagem_erro = f'Erro ao registrar: {str(e)}'
            return False

    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        if email_input.collidepoint(mouse_pos) or senha_input.collidepoint(mouse_pos) or cpf_input.collidepoint(mouse_pos) or nome_input.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)

        elif botao_voltar.collidepoint(mouse_pos) or botao_registrar.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                nome_ativo = nome_input.collidepoint(event.pos)
                cpf_ativo = cpf_input.collidepoint(event.pos)
                email_ativo = email_input.collidepoint(event.pos)
                senha_ativo = senha_input.collidepoint(event.pos)

                if botao_voltar.collidepoint(event.pos):
                    return janela_principal(tela, largura, altura, fonte, botoes, cursores, fundo)
                
                if botao_registrar.collidepoint(event.pos):
                    sucesso = registrar_usuario()

                    if sucesso:
                        conn.close()
                        return janela_principal(tela, largura, altura, fonte, botoes, cursores, fundo)
                    
            if event.type == pygame.KEYDOWN:
                if nome_ativo:
                    if event.key == pygame.K_BACKSPACE:
                        texto_nome = texto_nome[:-1]

                    elif event.key == pygame.K_RETURN:
                        print('Texto digitado:', texto_nome)

                    else:
                        texto_nome += event.unicode
                
                if cpf_ativo:
                    if event.key == pygame.K_BACKSPACE:
                        texto_cpf = texto_cpf[:-1]

                    elif event.key == pygame.K_RETURN:
                        print('Texto digitado:', texto_cpf)

                    else:
                        texto_cpf += event.unicode
                
                if email_ativo:
                    if event.key == pygame.K_BACKSPACE:
                        texto_email = texto_email[:-1]

                    elif event.key == pygame.K_RETURN:
                        print('Texto digitado:', texto_email)

                    else:
                        texto_email += event.unicode
                
                if senha_ativo:
                    if event.key == pygame.K_BACKSPACE:
                        texto_senha = texto_senha[:-1]

                    elif event.key == pygame.K_RETURN:
                        print('Texto digitado:', texto_senha)

                    else:
                        texto_senha += event.unicode
            
        tela.fill(cores.BRANCO)

        nome = fonte.render('Nome', True, cores.PRETO)
        cpf = fonte.render('CPF', True, cores.PRETO)
        email = fonte.render('Email', True, cores.PRETO)
        senha = fonte.render('Senha', True, cores.PRETO)
        tela.blit(nome, (nome_input.x, nome_input.y - 40))
        tela.blit(cpf, (cpf_input.x, cpf_input.y - 40))
        tela.blit(email, (email_input.x, email_input.y - 40))
        tela.blit(senha, (senha_input.x, senha_input.y - 40))

        pygame.draw.rect(tela, cores.OURO, nome_input, 2)
        pygame.draw.rect(tela, cores.OURO, cpf_input, 2)
        pygame.draw.rect(tela, cores.OURO, email_input, 2)
        pygame.draw.rect(tela, cores.OURO, senha_input, 2)

        cor_nome = cores.PRETO if nome_ativo else cores.CINZA_CLARO
        cor_cpf = cores.PRETO if cpf_ativo else cores.CINZA_CLARO
        cor_email = cores.PRETO if email_ativo else cores.CINZA_CLARO
        cor_senha = cores.PRETO if senha_ativo else cores.CINZA_CLARO

        texto_renderizado_nome = fonte.render(texto_nome, True, cor_nome)
        texto_renderizado_cpf = fonte.render(texto_cpf, True, cor_cpf)
        texto_renderizado_email = fonte.render(texto_email, True, cor_email)
        senha_ofuscada = '*' * len(texto_senha)
        texto_renderizado_senha = fonte.render(senha_ofuscada, True, cor_senha)

        altura_texto_nome = texto_renderizado_nome.get_height()
        altura_texto_cpf = texto_renderizado_cpf.get_height()
        altura_texto_email = texto_renderizado_email.get_height()
        altura_texto_senha = texto_renderizado_senha.get_height()

        pos_y_nome = nome_input.centery - altura_texto_nome // 2
        pos_y_cpf = cpf_input.centery - altura_texto_cpf // 2
        pos_y_email = email_input.centery - altura_texto_email // 2
        pos_y_senha = senha_input.centery - altura_texto_senha // 2

        offset_nome = max(0, texto_renderizado_nome.get_width() - (nome_input.width - 10))
        offset_cpf = max(0, texto_renderizado_cpf.get_width() - (cpf_input.width - 10))
        offset_email = max(0, texto_renderizado_email.get_width() - (email_input.width - 10))
        offset_senha = max(0, texto_renderizado_senha.get_width() - (senha_input.width - 10))

        tela.set_clip(nome_input)
        tela.blit(texto_renderizado_nome, (nome_input.x + 5 - offset_nome, pos_y_nome))
        tela.set_clip(cpf_input)
        tela.blit(texto_renderizado_cpf, (cpf_input.x + 5 - offset_cpf, pos_y_cpf))
        tela.set_clip(email_input)
        tela.blit(texto_renderizado_email, (email_input.x + 5 - offset_email, pos_y_email))
        tela.set_clip(senha_input)
        tela.blit(texto_renderizado_senha, (senha_input.x + 5 - offset_senha, pos_y_senha))

        tela.set_clip(None)

        pygame.draw.rect(tela, cores.VERMELHO_ESC , botao_voltar)
        texto = fonte.render('Voltar', True, cores.PRETO)
        texto_rect = texto.get_rect(center=botao_voltar.center)
        tela.blit(texto, texto_rect)

        pygame.draw.rect(tela, cores.OURO, botao_registrar)
        texto = fonte.render('Registrar', True, cores.PRETO)
        texto_rect = texto.get_rect(center=botao_registrar.center)
        tela.blit(texto, texto_rect)

        if mensagem_erro:
            fonte_erro = pygame.font.SysFont('UNICODE', 40)
            texto_erro = fonte_erro.render(mensagem_erro, True, cores.VERMELHO_ESC)
            erro_rect = texto_erro.get_rect(center=(largura // 2, 700))
            tela.blit(texto_erro, erro_rect)

        pygame.display.update()