import os
import pygame
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

# Conectar Banco de dados
conn = sqlite3.connect(r'C:\TECNICO\technic_rpg\Guedgers.db')
cursor = conn.cursor()

# Dimensões de tela fullscreen baseada no monitor do usuário
info = pygame.display.Info()
largura, altura = info.current_w, info.current_h
tela = pygame.display.set_mode((largura, altura), pygame.FULLSCREEN)


def tela_entrar(tela, largura, altura, fonte, botoes, cursores):
    """
    Exibe a tela de login para o usuário, permitindo autenticação via email e senha.

    Args:
        tela (pygame.Surface): A superfície da janela principal onde os elementos são desenhados.
        largura (int): A largura da tela em pixels.
        altura (int): A altura da tela em pixels.
        fonte (pygame.font.Font): Fonte padrão utilizada para os textos.
        botoes (list): Lista de retângulos representando botões interativos.
        cursores (list): Lista de retângulos que representam campos de entrada ativos.

    Returns:
        tela_logar (function): Redireciona para a tela do usuário logado, se a autenticação for bem-sucedida.
        janela_principal (function): Retorna à tela principal caso o botão "Voltar" seja clicado.
    """
    from interface.tela_principal import janela_principal
    from interface.tela_logado import tela_logar

    # Imagem de fundo
    fundo = pygame.image.load("imgs/fundo_geral.png")
    fundo = pygame.transform.scale(fundo, (largura, altura))

    # Imagem - LOGIN
    login = pygame.image.load("imgs/login.png")
    login = pygame.transform.scale(login, (300, 300))

    # Posição dos campos e botões
    botao_logar = pygame.Rect(850, 550, 100, 50)
    botao_voltar = pygame.Rect(650, 550, 100, 50)
    email_input = pygame.Rect(600, 300, 400, 50)
    senha_input = pygame.Rect(600, 450, 400, 50)

    # Valores iniciais de textos, posicionamento do cursor, atividade, mensagem de erro
    texto_email, texto_senha = '', ''
    cursor_email, cursor_senha = 0, 0
    email_ativo, senha_ativo = False, False
    mensagem_erro = ''

    # Temporizadores para teclas pressionadas
    backspace_timer = 0
    BACKSPACE_DELAY = 100
    delete_timer = 0
    DELETE_DELAY = 100
    left_timer = 0
    LEFT_DELAY = 100
    right_timer = 0
    RIGHT_DELAY = 100

    # Método de autenticação de usuário
    def autenticar_usuario(email, senha):
        """
        Verifica se o email e a senha informados correspondem a um usuário existente no banco de dados.

        Args:
            email (str): Email digitado pelo usuário.
            senha (str): Senha digitada pelo usuário.

        Returns:
            bool: True se o usuário for autenticado com sucesso, False caso contrário.
        """

        # Selecionar registro no banco de dados
        try:
            cursor.execute(
                "SELECT * FROM Usuario WHERE email_usuario=? AND senha_usuario=?",
                (email, senha)
            )

            usuario = cursor.fetchone()
            return usuario is not None
        
        # Quaisquer erros - Testes
        except sqlite3.Error as e:
            nonlocal mensagem_erro
            mensagem_erro = f"Erro no banco: {str(e)}"
            return False

    # Loop principal
    while True:

        # Posição das imagens
        tela.blit(fundo, (0, 0))
        tela.blit(login, (650, 0))

        # Invocar método - Atualizar cursor
        mouse_pos = pygame.mouse.get_pos()
        atualizar_cursor(mouse_pos, [email_input, senha_input], [
                         botao_voltar, botao_logar])

        teclas = pygame.key.get_pressed()
        tempo_atual = pygame.time.get_ticks()

        # BACKSPACE contínuo
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

        # DELETE contínuo
        if teclas[pygame.K_DELETE] and tempo_atual - delete_timer > DELETE_DELAY:
            if email_ativo and cursor_email > 0:
                texto_email = texto_email[:cursor_email] + \
                    texto_email[cursor_email + 1:]

            elif senha_ativo and cursor_senha > 0:
                texto_senha = texto_senha[:cursor_senha] + \
                    texto_senha[cursor_senha + 1:]

            delete_timer = tempo_atual

        # K-LEFT contínuo
        if teclas[pygame.K_LEFT] and tempo_atual - left_timer > LEFT_DELAY:
            if email_ativo and cursor_email > 0:
                cursor_email -= 1

            elif senha_ativo and cursor_senha > 0:
                cursor_senha -= 1

            left_timer = tempo_atual

        # K-RIGHT contínuo
        if teclas[pygame.K_RIGHT] and tempo_atual - right_timer > RIGHT_DELAY:
            if email_ativo and cursor_email < len(texto_email):
                cursor_email += 1

            elif senha_ativo and cursor_senha < len(texto_senha):
                cursor_senha += 1

            right_timer = tempo_atual

        # Eventos
        for event in pygame.event.get():

            # MOUSE BTN-1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    # Botão Voltar
                    if botao_voltar.collidepoint(event.pos):
                        return janela_principal(tela, largura, altura, fonte, botoes, cursores)

                    # Botão Entrar
                    elif botao_logar.collidepoint(event.pos):
                        if autenticar_usuario(texto_email, texto_senha):
                            return tela_logar(tela, largura, altura, fonte, botoes, cursores, texto_email)

                        # Mensagem de erro padrão
                        else:
                            mensagem_erro = "Email e/ou Senha incorretos."

                    # Invocar método - Verificar campo ativo
                    email_ativo, senha_ativo = verificar_campo_ativo_login(
                        event.pos, email_input, senha_input)

            # Teclas
            if event.type == pygame.KEYDOWN:

                # BACKSPACE
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

                # TAB
                elif event.key == pygame.K_TAB:
                    if email_ativo:
                        email_ativo, senha_ativo = False, True

                    elif senha_ativo:
                        senha_ativo, email_ativo = False, True

                    else:
                        email_ativo = True

                # ENTER
                elif event.key == pygame.K_RETURN:
                    if autenticar_usuario(texto_email, texto_senha):
                        return tela_logar(tela, largura, altura, fonte, botoes, cursores, texto_email)
                    else:
                        mensagem_erro = "Email e/ou Senha incorretos."

                # Invocar método - Processar dígitos de login
                else:
                    (texto_email, texto_senha, cursor_email, cursor_senha) = processar_digito_login(
                        event, email_ativo, senha_ativo, texto_email, texto_senha, cursor_email, cursor_senha
                    )

        # Invocar método - Desenhar rótulo dos campos
        desenhar_rotulo_campo(tela, fonte, email_input, "Email")
        desenhar_rotulo_campo(tela, fonte, senha_input, "Senha")

        # Invocar método - Preencher campos de texto
        desenhar_campo_texto(tela, fonte, email_input,
                             texto_email, email_ativo, cursor_index=cursor_email)
        desenhar_campo_texto(tela, fonte, senha_input, texto_senha,
                             senha_ativo, cursor_index=cursor_senha, ocultar=True)

        # Invocar método - Desenhar botões
        desenhar_botao(tela, botao_voltar, "Voltar", fonte, cores.SANGUE_SECO)
        desenhar_botao(tela, botao_logar, "Entrar",
                       fonte, cores.AMARELO_OURO_VELHO)

        # Desenhar mensagem de erro
        if mensagem_erro:
            fonte_erro = pygame.font.SysFont('Unicode', 40)
            texto_erro = fonte_erro.render(
                mensagem_erro, True, cores.BEGE)
            tela.blit(texto_erro, (610, 500))

        pygame.display.update()
