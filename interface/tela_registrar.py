import os

os.system('cls')

import pygame
import sys
import sqlite3
from funcoes_padrao import cores
from funcoes_padrao.mtd_form import atualizar_cursor
from funcoes_padrao.mtd_form import desenhar_rotulo_campo
from funcoes_padrao.mtd_form import desenhar_campo_texto
from funcoes_padrao.mtd_form import verificar_campo_ativo_registro
from funcoes_padrao.mtd_form import desenhar_botao
from funcoes_padrao.mtd_form import processar_digito_registro

pygame.init()

# Fonte
fonte = pygame.font.SysFont('Unicode', 40)

# Definir padrões de cursor
padrao_cursor = pygame.SYSTEM_CURSOR_ARROW
mao_cursor = pygame.SYSTEM_CURSOR_HAND
digitar = pygame.SYSTEM_CURSOR_IBEAM

conn = sqlite3.connect(r'C:\TECNICO\technic_rpg\Guedgers.db')
cursor = conn.cursor()


def tela_registrar(tela, largura, altura, fonte, botoes, cursores, fundo):
    from interface.tela_principal import janela_principal


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

    mensagem_erro = ''

    backspace_timer = 0
    BACKSPACE_DELAY = 100


    def registrar_usuario():
        nonlocal mensagem_erro

        if not (texto_nome and texto_cpf and texto_email and texto_senha):
            mensagem_erro = 'Preencha todos os campos!'
            return False  # ERRO

        try:
            import re

            
            # Validação de e-mail (tem que conter '@')
            if '@' not in texto_email:
                mensagem_erro = 'E-mail inválido! Deve conter @'
                return False

            # Validação e formatação de CPF
            cpf_limpo = re.sub(r'\D', '', texto_cpf)
            if len(cpf_limpo) != 11:
                mensagem_erro = 'CPF deve ter 11 dígitos numéricos!'
                return False

            # Formatar CPF com máscara (000.000.000-00)
            cpf_formatado = f'{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}'

            cursor.execute(
                '''
                INSERT INTO Usuario (nome_usuario, cpf_usuario, email_usuario, senha_usuario)
                VALUES (?, ?, ?, ?)
                ''', (texto_nome, cpf_formatado, texto_email, texto_senha)
            )
            conn.commit()
            mensagem_erro = 'Usuário registrado com sucesso!'
            return True

        except Exception as e:
            mensagem_erro = f'Erro ao registrar: {str(e)}'
            return False
        

    while True:
        mouse_pos = pygame.mouse.get_pos()
        atualizar_cursor(mouse_pos, [nome_input, cpf_input, email_input, senha_input], [botao_voltar, botao_registrar])
        
        if email_input.collidepoint(
            mouse_pos) or senha_input.collidepoint(mouse_pos) or cpf_input.collidepoint(mouse_pos) or nome_input.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)

        elif botao_voltar.collidepoint(
            mouse_pos) or botao_registrar.collidepoint(
                mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        teclas = pygame.key.get_pressed()
        tempo_atual = pygame.time.get_ticks()

        if teclas[pygame.K_BACKSPACE]:
            if (nome_ativo or cpf_ativo or email_ativo or senha_ativo) and tempo_atual - backspace_timer > BACKSPACE_DELAY:
                if nome_ativo and texto_nome:
                    texto_nome = texto_nome[:-1]

                elif cpf_ativo and texto_cpf:
                    texto_cpf = texto_cpf[:-1]

                elif email_ativo and texto_email:
                    texto_email = texto_email[:-1]

                elif senha_ativo and texto_senha:
                    texto_senha = texto_senha[:-1]

                backspace_timer = tempo_atual

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
                        return janela_principal(tela, largura, altura, fonte, botoes, cursores, fundo)
                    
                nome_ativo, cpf_ativo, email_ativo, senha_ativo = verificar_campo_ativo_registro(event.pos, nome_input, cpf_input, email_input, senha_input)
            
            # Eventos de teclas
            if event.type == pygame.KEYDOWN:

                # Evento BACKSPACE
                if event.key == pygame.K_BACKSPACE:
                    backspace_timer = pygame.time.get_ticks() - BACKSPACE_DELAY

                # Evento TAB
                elif event.key == pygame.K_TAB:
                    if nome_ativo:
                        nome_ativo = False
                        cpf_ativo = True
                    
                    elif cpf_ativo:
                        cpf_ativo = False
                        email_ativo = True

                    elif email_ativo:
                        email_ativo = False
                        senha_ativo = True

                    elif senha_ativo:
                        senha_ativo = False
                        nome_ativo = True
                        
                    else:
                        nome_ativo = True

                else:
                    texto_nome, texto_cpf, texto_email, texto_senha = processar_digito_registro(event, nome_ativo, cpf_ativo, email_ativo, senha_ativo, texto_nome, texto_cpf, texto_email, texto_senha)
            
        tela.fill(cores.BRANCO)

        # Método - Título campo
        desenhar_rotulo_campo(tela, fonte, nome_input, "Nome")
        desenhar_rotulo_campo(tela, fonte, cpf_input, "CPF")
        desenhar_rotulo_campo(tela, fonte, email_input, "Email")
        desenhar_rotulo_campo(tela, fonte, senha_input, "Senha")

        # Método - Preencheimento do campo de texto
        desenhar_campo_texto(tela, fonte, nome_input, texto_nome, nome_ativo)
        desenhar_campo_texto(tela, fonte, cpf_input, texto_cpf, cpf_ativo)
        desenhar_campo_texto(tela, fonte, email_input, texto_email, email_ativo)
        desenhar_campo_texto(tela, fonte, senha_input, texto_senha, senha_ativo, ocultar=True)

        # Método - Desenho dos botões
        desenhar_botao(tela, botao_voltar, "Voltar", fonte, cores.VERMELHO_ESC)
        desenhar_botao(tela, botao_registrar, "Registrar", fonte, cores.OURO)

        if mensagem_erro:
            fonte_erro = pygame.font.SysFont('UNICODE', 40)
            texto_erro = fonte_erro.render(
                mensagem_erro, True, cores.VERMELHO_ESC)
            erro_rect = texto_erro.get_rect(center=(largura // 2, 700))
            tela.blit(texto_erro, erro_rect)

        pygame.display.update()