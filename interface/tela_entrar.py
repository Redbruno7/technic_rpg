import os
import pygame
import sys
import sqlite3
from funcoes_padrao import cores
from funcoes_padrao.mtd_form import atualizar_cursor
from funcoes_padrao.mtd_form import desenhar_rotulo_campo
from funcoes_padrao.mtd_form import desenhar_campo_texto
from funcoes_padrao.mtd_form import verificar_campo_ativo_login
from funcoes_padrao.mtd_form import desenhar_botao
from funcoes_padrao.mtd_form import processar_digito_login


pygame.init()
os.system('cls')


conn = sqlite3.connect(r'C:\TECNICO\technic_rpg\Guedgers.db')

# Definir dimensão da tela
largura = 1600
altura = 800
tela = pygame.display.set_mode((largura, altura))


def tela_entrar(tela, largura, altura, fonte, botoes, cursores):
    """
    Exibir a tela de login com campos de e-mail e senha, e botões "Entrar" e "Voltar"

    Args:
        tela (pygame.Surface): Superfície principal da janela
        largura (int): Largura da janela
        altura (int): Altura da janela
        fonte (pygame.font.Font): Fonte padrão usada no layout
        botoes (list): Lista de botões (não usados diretamente aqui)
        cursores (dict): Cursores personalizados (não usados diretamente aqui)
        fundo (pygame.Surface): Imagem ou superfície de fundo (não usada diretamente aqui)

    Comportamento:
        - Permite digitação nos campos
        - Botão "Entrar" leva à tela de logado
        - Botão "Voltar" retorna à tela principal
        - Atualiza o cursor dinamicamente conforme o elemento em foco
    """    
    from interface.tela_principal import janela_principal
    from interface.tela_logado import tela_logar

    # Carregar imagem de fundo
    fundo = pygame.image.load("imgs/fundo_geral.png")
    fundo = pygame.transform.scale(fundo, (largura, altura))

    # Definir posição dos campos e botões
    botao_logar = pygame.Rect(850, 400, 100, 50)
    botao_voltar = pygame.Rect(650, 400, 100, 50)
    email_input = pygame.Rect(600, 150, 400, 50)
    senha_input = pygame.Rect(600, 300, 400, 50)

    # Definir valores textos, cursores e atividades
    texto_email, texto_senha = '', ''
    cursor_email, cursor_senha = 0, 0
    email_ativo, senha_ativo = False, False
    mensagem_erro = ''

    # Definir temporizadores para funções de tecla
    backspace_timer = 0
    BACKSPACE_DELAY = 100
    k_left_timer = 0
    K_LEFT_DELAY = 100
    k_right_timer = 0
    K_RIGHT_DELAY = 100

    # Definir método de autenticação de usuário
    def autenticar_usuario(email, senha):
        """_summary_

        Args:
            email (_type_): _description_
            senha (_type_): _description_

        Returns:
            _type_: _description_
        """
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM Usuario WHERE email_usuario=? AND senha_usuario=?",
                (email, senha)
            )
            usuario = cursor.fetchone()
            return usuario is not None

        except sqlite3.Error as e:
            nonlocal mensagem_erro
            mensagem_erro = f"Erro no banco: {str(e)}"
            return False

    # Loop principal
    while True:

        # Invocar método - Atualizar cursor
        mouse_pos = pygame.mouse.get_pos()
        atualizar_cursor(mouse_pos, [email_input, senha_input], [
                         botao_voltar, botao_logar])

        teclas = pygame.key.get_pressed()
        tempo_atual = pygame.time.get_ticks()

        # Definir evento contínuo BACKSPACE
        if teclas[pygame.K_BACKSPACE] and tempo_atual - backspace_timer > BACKSPACE_DELAY:
            if email_ativo and cursor_email > 0:
                texto_email = texto_email[:cursor_email -
                                          1] + texto_email[cursor_email:]
                cursor_email -= 1

            elif senha_ativo and cursor_senha > 0:
                texto_senha = texto_senha[:cursor_senha -
                                          1] + texto_senha[cursor_senha:]
                cursor_senha -= 1

            backspace_timer = tempo_atual

        # Definir evento contínuo K-LEFT
        if teclas[pygame.K_LEFT] and tempo_atual - k_left_timer > K_LEFT_DELAY:
            if email_ativo and cursor_email > 0:
                cursor_email -= 1

            elif senha_ativo and cursor_senha > 0:
                cursor_senha -= 1

            k_left_timer = tempo_atual

        # Definir evento contínuo K-RIGHT
        if teclas[pygame.K_RIGHT] and tempo_atual - k_right_timer > K_RIGHT_DELAY:
            if email_ativo and cursor_email > 0:
                cursor_email += 1

            elif senha_ativo and cursor_senha > 0:
                cursor_senha += 1

            k_right_timer = tempo_atual

        # Definir eventos de interação
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Evento de clique
            elif event.type == pygame.MOUSEBUTTONDOWN:

                # Botão Voltar
                if botao_voltar.collidepoint(event.pos):
                    return janela_principal(tela, largura, altura, fonte, botoes, cursores)

                # Botão Entrar
                elif botao_logar.collidepoint(event.pos):
                    if autenticar_usuario(texto_email, texto_senha):
                        return tela_logar(tela, largura, altura, fonte, botoes, cursores)

                    else:
                        mensagem_erro = "Email e/ou Senha incorretos."

                # Invocar método - Verificar campo ativo
                email_ativo, senha_ativo = verificar_campo_ativo_login(
                    event.pos, email_input, senha_input)

            # Evento de tecla
            if event.type == pygame.KEYDOWN:

                # Evento BACKSPACE
                if event.key == pygame.K_BACKSPACE:
                    backspace_timer = pygame.time.get_ticks() - BACKSPACE_DELAY

                # Evento TAB
                elif event.key == pygame.K_TAB:
                    if email_ativo:
                        email_ativo, senha_ativo = False, True

                    elif senha_ativo:
                        senha_ativo, email_ativo = False, True

                    else:
                        email_ativo = True

                # Evento seta esquerda
                elif event.key == pygame.K_LEFT:
                    k_left_timer = pygame.time.get_ticks() - K_LEFT_DELAY

                    if email_ativo and cursor_email > 0:
                        cursor_email -= 1

                    elif senha_ativo and cursor_senha > 0:
                        cursor_senha -= 1

                # Evento seta direita
                elif event.key == pygame.K_RIGHT:
                    k_right_timer = pygame.time.get_ticks() - K_RIGHT_DELAY

                    if email_ativo and cursor_email < len(texto_email):
                        cursor_email += 1

                    elif senha_ativo and cursor_senha < len(texto_senha):
                        cursor_senha += 1

                else:
                    char = event.unicode

                    if email_ativo:
                        texto_email = texto_email[:cursor_email] + \
                            char + texto_email[cursor_email:]
                        cursor_email += 1

                    elif senha_ativo:
                        texto_senha = texto_senha[:cursor_senha] + \
                            char + texto_senha[cursor_senha:]
                        cursor_senha += 1

            tela.blit(fundo, (0, 0))

        # Método - Desenhar título
        desenhar_rotulo_campo(tela, fonte, email_input, "Email")
        desenhar_rotulo_campo(tela, fonte, senha_input, "Senha")

        # Método - Preencher campo de texto
        desenhar_campo_texto(tela, fonte, email_input,
                             texto_email, email_ativo, cursor_index=cursor_email)
        desenhar_campo_texto(tela, fonte, senha_input, texto_senha,
                             senha_ativo, cursor_index=cursor_senha, ocultar=True)

        # Método - Desenhar botão
        desenhar_botao(tela, botao_voltar, "Voltar", fonte, cores.VERMELHO_ESC)
        desenhar_botao(tela, botao_logar, "Entrar", fonte, cores.OURO)

        # Desenhar mensagem de erro
        if mensagem_erro:
            fonte_erro = pygame.font.SysFont('Unicode', 40)
            texto_erro = fonte_erro.render(
                mensagem_erro, True, cores.VERMELHO_ESC)
            tela.blit(texto_erro, (610, 500))

        pygame.display.update()
