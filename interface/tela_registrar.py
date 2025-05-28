import os
import pygame
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
conn = sqlite3.connect(r'bd\Guedgers.db')
cursor = conn.cursor()

# Dimensões de tela fullscreen baseada no monitor do usuário

largura, altura = 1600, 800
tela = pygame.display.set_mode((largura, altura))


def tela_registrar(tela, largura, altura, fonte, botoes, cursores):
    """
    Exibe a interface gráfica para registro de novos usuários.
    Monta uma tela com campos para o usuário preencher nome, 
    CPF, e-mail e senha, além de botões para registrar ou voltar. 
    Ela gerencia a interação do usuário com o teclado e mouse, 
    validando os dados antes de registrar no banco de dados.

    Args:
        tela (pygame.Surface): Superfície principal do Pygame onde os elementos são desenhados.
        largura (int): Largura da tela.
        altura (int): Altura da tela.
        fonte (pygame.Font): Fonte usada para desenhar textos.
        botoes (dict): Dicionário com os estados ou referências dos botões da interface.
        cursores (dict): Dicionário com os cursores dos campos de entrada.

    Returns:
        None: Retorna à tela principal após registro ou ao clicar em voltar.
    """
    from interface.tela_principal import janela_principal

    # Imagem de fundo
    fundo = pygame.image.load("imgs/fundo_geral.png")
    fundo = pygame.transform.scale(fundo, (largura, altura))

    # Imagem - CRIAR CONTA
    criar = pygame.image.load("imgs/criar.png")
    criar = pygame.transform.scale(criar, (500, 500))

    # Posição dos campos e botões
    botao_voltar = pygame.Rect(620, 600, 130, 50)
    botao_registrar = pygame.Rect(850, 600, 130, 50)
    nome_input = pygame.Rect(600, 150, 400, 50)
    cpf_input = pygame.Rect(600, 270, 400, 50)
    email_input = pygame.Rect(600, 380, 400, 50)
    senha_input = pygame.Rect(600, 500, 400, 50)

    # Valores iniciais de textos, posicionamento do cursor, atividade, mensagem de erro
    texto_nome, texto_cpf, texto_email, texto_senha = '', '', '', ''
    cursor_nome, cursor_cpf, cursor_email, cursor_senha = 0, 0, 0, 0
    nome_ativo, cpf_ativo, email_ativo, senha_ativo = False, False, False, False
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

    # Método de registro de usuário
    def registrar_usuario():
        """
        Valida os dados inseridos pelo usuário e insere um novo registro no banco de dados.
        Verifica se todos os campos estão preenchidos, 
        se o CPF tem 11 dígitos e se o e-mail contém '@'. 
        Em caso de sucesso, insere os dados na tabela Usuario.

        Returns:
            bool: True se o registro for bem-sucedido, False se houver erros.
        """

        # Importar mensagem de erro
        nonlocal mensagem_erro

        # Erro - Campos vazios
        if not (texto_nome and texto_cpf and texto_email and texto_senha):
            mensagem_erro = 'Preencha todos os campos!'
            return False

        try:
            import re

            # Erro - email
            if '@' not in texto_email:
                mensagem_erro = 'E-mail inválido! Deve conter @'
                return False

            # Erro - CPF
            cpf_limpo = re.sub(r'\D', '', texto_cpf)
            if len(cpf_limpo) != 11:
                mensagem_erro = 'CPF deve ter 11 dígitos numéricos!'
                return False

            cpf_formatado = f'{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}'

            # Atualizar banco de dados
            cursor.execute(
                '''
                INSERT INTO Usuario (nome_usuario, cpf_usuario, email_usuario, senha_usuario)
                VALUES (?, ?, ?, ?)
                ''', (texto_nome, cpf_formatado, texto_email, texto_senha)
            )
        
            conn.commit()
            return True

        # Quaisquer erros - Testes
        except Exception as e:
            mensagem_erro = f'Erro ao registrar: {str(e)}'
            return False

    # Loop Principal
    while True:

        # Posição das imagens
        tela.blit(fundo, (0, 0))
        tela.blit(criar, (50, 100))

        # Invocar método - Atualizar cursor
        mouse_pos = pygame.mouse.get_pos()
        atualizar_cursor(mouse_pos, [nome_input, cpf_input, email_input, senha_input], [
                         botao_voltar, botao_registrar])

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

        # Eventos
        for event in pygame.event.get():

            # MOUSE BTN-1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    # Botão Voltar
                    if botao_voltar.collidepoint(event.pos):
                        return janela_principal(tela, largura, altura, fonte, botoes, cursores)

                    # Botão Registrar
                    if botao_registrar.collidepoint(event.pos):
                        if registrar_usuario():
                            return janela_principal(tela, largura, altura, fonte, botoes, cursores)

                    # Invocar método - Verificar campo ativo
                    nome_ativo, cpf_ativo, email_ativo, senha_ativo = verificar_campo_ativo_registro(
                        event.pos, nome_input, cpf_input, email_input, senha_input)

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
                    if registrar_usuario():
                        return janela_principal(tela, largura, altura, fonte, botoes, cursores)

                # Invocar método - Processar dígitos de registro
                else:
                    (texto_nome, texto_cpf, texto_email, texto_senha,
                     cursor_nome, cursor_cpf, cursor_email, cursor_senha) = processar_digito_registro(
                        event, nome_ativo, cpf_ativo, email_ativo, senha_ativo,
                        texto_nome, texto_cpf, texto_email, texto_senha,
                        cursor_nome, cursor_cpf, cursor_email, cursor_senha
                    )

        # Invocar método - Desenhar rótulo dos campos
        desenhar_rotulo_campo(tela, fonte, nome_input, "Nome")
        desenhar_rotulo_campo(tela, fonte, cpf_input, "CPF")
        desenhar_rotulo_campo(tela, fonte, email_input, "Email")
        desenhar_rotulo_campo(tela, fonte, senha_input, "Senha")

        # Invocar método - Preencher campos de texto
        desenhar_campo_texto(tela, fonte, nome_input,
                             texto_nome, nome_ativo, cursor_index=cursor_nome)
        desenhar_campo_texto(tela, fonte, cpf_input, texto_cpf,
                             cpf_ativo, cursor_index=cursor_cpf)
        desenhar_campo_texto(tela, fonte, email_input,
                             texto_email, email_ativo, cursor_index=cursor_email)
        desenhar_campo_texto(tela, fonte, senha_input, texto_senha,
                             senha_ativo, cursor_index=cursor_senha, ocultar=True)

        # Invocar método - Desenhar botões
        desenhar_botao(tela, botao_voltar, "Voltar", fonte, cores.SANGUE_SECO)
        desenhar_botao(tela, botao_registrar, "Registrar",
                       fonte, cores.AMARELO_OURO_VELHO)

        # Desenhar mensagem de erro
        if mensagem_erro:
            fonte_erro = pygame.font.SysFont('UNICODE', 40)
            texto_erro = fonte_erro.render(
                mensagem_erro, True, cores.BEGE)
            erro_rect = texto_erro.get_rect(center=(largura // 2, 700))
            tela.blit(texto_erro, erro_rect)

        pygame.display.update()
