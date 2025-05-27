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

# Conectar Banco de dados
conn = sqlite3.connect(r'C:\guilherme\technic_rpg\Guedgers.db')
cursor = conn.cursor()

# Definir dimensão da tela
largura = 1600
altura = 800
tela = pygame.display.set_mode((largura, altura))


def tela_editar(tela, largura, altura, fonte, botoes, cursores, email_original):
    from interface.tela_logado import tela_logar

    # Carregar imagem de fundo
    fundo = pygame.image.load("imgs/fundo_geral.png")
    fundo = pygame.transform.scale(fundo, (largura, altura))

    # Definir posição dos campos e botões
    botao_voltar = pygame.Rect(620, 600, 130, 50)
    botao_alterar = pygame.Rect(850, 600, 130, 50)
    novo_nome = pygame.Rect(600, 150, 400, 50)
    novo_cpf = pygame.Rect(600, 270, 400, 50)
    novo_email = pygame.Rect(600, 380, 400, 50)
    novo_senha = pygame.Rect(600, 500, 400, 50)


    # aqui deixa os campos da edicao pré-preenchidos
    cursor.execute('SELECT nome_usuario, cpf_usuario, email_usuario, senha_usuario FROM Usuario WHERE email_usuario = ?', (email_original,))
    resultado = cursor.fetchone()

    if resultado:
        texto_nome, texto_cpf, texto_email, texto_senha = resultado
    else:
        texto_nome, texto_cpf, texto_email, texto_senha = '', '', '', ''

    cursor_nome = len(texto_nome)
    cursor_cpf = len(texto_cpf)
    cursor_email = len(texto_email)
    cursor_senha = len(texto_senha)

    nome_ativo, cpf_ativo, email_ativo, senha_ativo = False, False, False, False
    mensagem_erro = ''

    # Definir temporizadores para funções de tecla
    backspace_timer = 0
    BACKSPACE_DELAY = 100
    delete_timer = 0
    DELETE_DELAY = 100
    left_timer = 0
    LEFT_DELAY = 100
    right_timer = 0
    RIGHT_DELAY = 100

    # Definir método de registro de usuário
    def alterar_usuario():
        

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


            cursor.execute('''
                UPDATE Usuario
                SET nome_usuario = ?, cpf_usuario = ?, email_usuario = ?, senha_usuario = ?
                WHERE email_usuario = ?
            ''', (texto_nome, cpf_formatado, texto_email, texto_senha, email_original))

            usuario = cursor.fetchone()
            conn.commit()
            return True

        except Exception as e:
            mensagem_erro = f'Erro ao registrar: {str(e)}'
            return False

    # Loop Principal
    while True:

        # Invocar método - Atualizar cursor
        mouse_pos = pygame.mouse.get_pos()
        atualizar_cursor(mouse_pos, [novo_nome, novo_cpf, novo_email, novo_senha], [
                         botao_voltar, botao_alterar])

        teclas = pygame.key.get_pressed()
        tempo_atual = pygame.time.get_ticks()

        # BACKSPACE contínuo
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

        # DELETE contínuo
        if teclas[pygame.K_DELETE] and tempo_atual - delete_timer > DELETE_DELAY:
            if nome_ativo and cursor_nome > 0:
                texto_nome = texto_nome[:cursor_nome] + \
                    texto_nome[cursor_nome + 1:]

            elif cpf_ativo and cursor_cpf > 0:
                texto_cpf = texto_cpf[:cursor_cpf] + texto_cpf[cursor_cpf + 1:]

            elif email_ativo and cursor_email > 0:
                texto_email = texto_email[:cursor_email] + \
                    texto_email[cursor_email + 1:]

            elif senha_ativo and cursor_senha > 0:
                texto_senha = texto_senha[:cursor_senha] + \
                    texto_senha[cursor_senha + 1:]

            delete_timer = tempo_atual

        # K-LEFT contínuo
        if teclas[pygame.K_LEFT] and tempo_atual - left_timer > LEFT_DELAY:
            if nome_ativo and cursor_nome > 0:
                cursor_nome -= 1

            elif cpf_ativo and cursor_cpf > 0:
                cursor_cpf -= 1

            elif email_ativo and cursor_email > 0:
                cursor_email -= 1

            elif senha_ativo and cursor_senha > 0:
                cursor_senha -= 1

            left_timer = tempo_atual

        # K-RIGHT contínuo
        if teclas[pygame.K_RIGHT] and tempo_atual - right_timer > RIGHT_DELAY:
            if nome_ativo and cursor_nome < len(texto_nome):
                cursor_nome += 1

            elif cpf_ativo and cursor_cpf < len(texto_cpf):
                cursor_cpf += 1

            elif email_ativo and cursor_email < len(texto_email):
                cursor_email += 1

            elif senha_ativo and cursor_senha < len(texto_senha):
                cursor_senha += 1

            right_timer = tempo_atual

        # Definir eventos de interação
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Evento de clique
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Botão Voltar
                if botao_voltar.collidepoint(event.pos):                              
                    return tela_logar(tela, largura, altura, fonte, botoes, cursores, email_original)

                # Botão Registrar
                if botao_alterar.collidepoint(event.pos):
                    if alterar_usuario():                                                 
                        return tela_logar(tela, largura, altura, fonte, botoes, cursores, texto_email)

                # Invocar método - Verificar campo ativo
                nome_ativo, cpf_ativo, email_ativo, senha_ativo = verificar_campo_ativo_registro(
                    event.pos, novo_nome, novo_cpf, novo_email, novo_senha)

            # Evento de tecla
            if event.type == pygame.KEYDOWN:

                # Evento BACKSPACE
                if event.key == pygame.K_BACKSPACE:
                    backspace_timer = pygame.time.get_ticks() - BACKSPACE_DELAY

                # DELETE
                if event.key == pygame.K_DELETE:
                    delete_timer = pygame.time.get_ticks() - DELETE_DELAY

                # K-LEFT
                if event.key == pygame.K_LEFT:
                    left_timer = pygame.time.get_ticks() - LEFT_DELAY

                # K-RIGHT
                if event.key == pygame.K_RIGHT:
                    right_timer = pygame.time.get_ticks() - RIGHT_DELAY

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

                # ENTER
                elif event.key == pygame.K_RETURN:
                    if alterar_usuario():
                        return tela_logar(tela, largura, altura, fonte, botoes, cursores)

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
        desenhar_rotulo_campo(tela, fonte, novo_nome, "Nome")
        desenhar_rotulo_campo(tela, fonte, novo_cpf, "CPF")
        desenhar_rotulo_campo(tela, fonte, novo_email, "Email")
        desenhar_rotulo_campo(tela, fonte, novo_senha, "Senha")

        # Método - Preencher campo
        desenhar_campo_texto(tela, fonte, novo_nome,
                             texto_nome, nome_ativo, cursor_index=cursor_nome)
        desenhar_campo_texto(tela, fonte, novo_cpf, texto_cpf,
                             cpf_ativo, cursor_index=cursor_cpf)
        desenhar_campo_texto(tela, fonte, novo_email,
                             texto_email, email_ativo, cursor_index=cursor_email)
        desenhar_campo_texto(tela, fonte, novo_senha, texto_senha,
                             senha_ativo, cursor_index=cursor_senha, ocultar=True)

        # Método - Definir botões
        desenhar_botao(tela, botao_voltar, "Voltar", fonte, cores.SANGUE_SECO)
        desenhar_botao(tela, botao_alterar, "Alterar", fonte, cores.AMARELO_OURO_VELHO)

        if mensagem_erro:
            fonte_erro = pygame.font.SysFont('UNICODE', 40)
            texto_erro = fonte_erro.render(
                mensagem_erro, True, cores.BEGE)
            erro_rect = texto_erro.get_rect(center=(largura // 2, 700))
            tela.blit(texto_erro, erro_rect)

        pygame.display.update()
