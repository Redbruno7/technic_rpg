import os
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
os.system('cls')

# Definir Fonte
fonte = pygame.font.SysFont('Unicode', 40)

# Conectar Banco de dados
conn = sqlite3.connect(r'C:\TECNICO\technic_rpg\Guedgers.db')
cursor = conn.cursor()


# Definir dimensão da tela
largura = 1600
altura = 800
tela = pygame.display.set_mode((largura, altura))


def tela_registrar(tela, largura, altura, fonte, botoes, cursores):
    from interface.tela_principal import janela_principal

    # Carregar imagem de fundo
    fundo = pygame.image.load("imgs/fundo_geral.png")
    fundo = pygame.transform.scale(fundo, (largura, altura))

    # Definir posição dos campos e botões
    botao_voltar = pygame.Rect(620, 600, 130, 50)
    botao_registrar = pygame.Rect(850, 600, 130, 50)
    nome_input = pygame.Rect(600, 150, 400, 50)
    cpf_input = pygame.Rect(600, 270, 400, 50)
    email_input = pygame.Rect(600, 380, 400, 50)
    senha_input = pygame.Rect(600, 500, 400, 50)

    # Definir valores textos, cursores e atividades
    texto_nome, texto_cpf, texto_email, texto_senha = '', '', '', ''
    cursor_nome, cursor_cpf, cursor_email, cursor_senha = 0, 0, 0, 0
    nome_ativo, cpf_ativo, email_ativo, senha_ativo = False, False, False, False
    mensagem_erro = ''

    # Definir temporizadores para funções de tecla
    backspace_timer = 0
    BACKSPACE_DELAY = 100

    # Definir método de registro de usuário
    def registrar_usuario():

        # Importar mensagem de erro
        nonlocal mensagem_erro

        # Definir mensagem de erro
        if not (texto_nome and texto_cpf and texto_email and texto_senha):
            mensagem_erro = 'Preencha todos os campos!'
            return False

        try:
            import re
            if '@' not in texto_email:
                mensagem_erro = 'E-mail inválido! Deve conter @'
                return False

            cpf_limpo = re.sub(r'\D', '', texto_cpf)
            if len(cpf_limpo) != 11:
                mensagem_erro = 'CPF deve ter 11 dígitos numéricos!'
                return False

            cpf_formatado = f'{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}'

            cursor.execute(
                '''
                INSERT INTO Usuario (nome_usuario, cpf_usuario, email_usuario, senha_usuario)
                VALUES (?, ?, ?, ?)
                ''', (texto_nome, cpf_formatado, texto_email, texto_senha)
            )
            conn.commit()
            return True

        except Exception as e:
            mensagem_erro = f'Erro ao registrar: {str(e)}'
            return False

    # Loop Principal
    while True:

        # Invocar método - Atualizar cursor
        mouse_pos = pygame.mouse.get_pos()
        atualizar_cursor(mouse_pos, [nome_input, cpf_input, email_input, senha_input], [
                         botao_voltar, botao_registrar])

        teclas = pygame.key.get_pressed()
        tempo_atual = pygame.time.get_ticks()

        # Definir evento contínuo BACKSPACE
        if teclas[pygame.K_BACKSPACE] and tempo_atual - backspace_timer > BACKSPACE_DELAY:
            if nome_ativo and cursor_nome > 0:
                texto_nome = texto_nome[:cursor_nome -
                                        1] + texto_nome[cursor_nome:]
                cursor_nome -= 1

            elif cpf_ativo and cursor_cpf > 0:
                texto_cpf = texto_cpf[:cursor_cpf-1] + texto_cpf[cursor_cpf:]
                cursor_cpf -= 1

            elif email_ativo and cursor_email > 0:
                texto_email = texto_email[:cursor_email -
                                          1] + texto_email[cursor_email:]
                cursor_email -= 1

            elif senha_ativo and cursor_senha > 0:
                texto_senha = texto_senha[:cursor_senha -
                                          1] + texto_senha[cursor_senha:]
                cursor_senha -= 1

            backspace_timer = tempo_atual

        # Definir eventos de interação
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Evento de clique
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Botão Voltar
                if botao_voltar.collidepoint(event.pos):
                    return janela_principal(tela, largura, altura, fonte, botoes, cursores)

                # Botão Registrar
                if botao_registrar.collidepoint(event.pos):
                    if registrar_usuario():
                        return janela_principal(tela, largura, altura, fonte, botoes, cursores)
                    
                    else:
                        mensagem_erro = "Preencha todos os campos"

                # Invocar método - Verificar campo ativo
                nome_ativo, cpf_ativo, email_ativo, senha_ativo = verificar_campo_ativo_registro(
                    event.pos, nome_input, cpf_input, email_input, senha_input)

            # Evento de tecla
            if event.type == pygame.KEYDOWN:

                # Evento BACKSPACE
                if event.key == pygame.K_BACKSPACE:
                    backspace_timer = pygame.time.get_ticks() - BACKSPACE_DELAY

                # Evento TAB
                elif event.key == pygame.K_TAB:
                    if nome_ativo:
                        nome_ativo, cpf_ativo = False, True

                    elif cpf_ativo:
                        cpf_ativo, email_ativo = False, True

                    elif email_ativo:
                        email_ativo, senha_ativo = False, True

                    elif senha_ativo:
                        senha_ativo, nome_ativo = False, True

                    else:
                        nome_ativo = True

                # Processa digitação, backspace e setas
                else:
                    (texto_nome, texto_cpf, texto_email, texto_senha,
                    cursor_nome, cursor_cpf, cursor_email, cursor_senha) = processar_digito_registro(
                        event, nome_ativo, cpf_ativo, email_ativo, senha_ativo,
                        texto_nome, texto_cpf, texto_email, texto_senha,
                        cursor_nome, cursor_cpf, cursor_email, cursor_senha
                    )

            # Setar tela de fundo
            tela.blit(fundo, (0, 0))

        # Método - Título campo
        desenhar_rotulo_campo(tela, fonte, nome_input, "Nome")
        desenhar_rotulo_campo(tela, fonte, cpf_input, "CPF")
        desenhar_rotulo_campo(tela, fonte, email_input, "Email")
        desenhar_rotulo_campo(tela, fonte, senha_input, "Senha")

        # Método - Preencher campo
        desenhar_campo_texto(tela, fonte, nome_input,
                             texto_nome, nome_ativo, cursor_index=cursor_nome)
        desenhar_campo_texto(tela, fonte, cpf_input, texto_cpf,
                             cpf_ativo, cursor_index=cursor_cpf)
        desenhar_campo_texto(tela, fonte, email_input,
                             texto_email, email_ativo, cursor_index=cursor_email)
        desenhar_campo_texto(tela, fonte, senha_input, texto_senha,
                             senha_ativo, cursor_index=cursor_senha, ocultar=True)

        # Método - Definir botões
        desenhar_botao(tela, botao_voltar, "Voltar", fonte, cores.VERMELHO_ESC)
        desenhar_botao(tela, botao_registrar, "Registrar", fonte, cores.OURO)

        if mensagem_erro:
            fonte_erro = pygame.font.SysFont('UNICODE', 40)
            texto_erro = fonte_erro.render(
                mensagem_erro, True, cores.VERMELHO_ESC)
            erro_rect = texto_erro.get_rect(center=(largura // 2, 700))
            tela.blit(texto_erro, erro_rect)

        pygame.display.update()
