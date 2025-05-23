import os
import pygame
import sys
import sqlite3
from interface import cores


pygame.init()
os.system('cls')


conn = sqlite3.connect(r'C:\Bruno - Técnico DS\technic_rpg\Guedgers.db')


def atualizar_cursor(pos, campos, botoes):
    """
    Atualizar o cursor do mouse com base na posição atual

    Args:
        pos (tuple): Posição (x, y) atual do mouse
        campos (list): Lista de retângulos representando os campos de texto
        botoes (list): Lista de retângulos representando os botões
    """
    if any(campo.collidepoint(pos) for campo in campos):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)

    elif any(botao.collidepoint(pos) for botao in botoes):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


def verificar_campo_ativo(pos, campo_email, campo_senha):
    """
    Verificar se o usuário clicou em um dos campos de entrada (e-mail ou senha)

    Args:
        pos (tuple): Posição (x, y) do clique do mouse
        campo_email (pygame.Rect): Retângulo do campo de e-mail
        campo_senha (pygame.Rect): Retângulo do campo de senha

    Returns:
        tuple: Dois valores booleanos indicando se o campo de e-mail ou senha foi ativado
    """
    email_ativo = campo_email.collidepoint(pos)
    senha_ativo = campo_senha.collidepoint(pos)

    return email_ativo, senha_ativo


def processar_digito(event, email_ativo, senha_ativo, texto_email, texto_senha):
    """
    Processar a digitação do teclado nos campos de texto

    Args:
        event (pygame.Event): Evento de tecla pressionada
        email_ativo (bool): Indica se o campo de e-mail está ativo
        senha_ativo (bool): Indica se o campo de senha está ativo
        texto_email (str): Texto atual no campo de e-mail
        texto_senha (str): Texto atual no campo de senha

    Returns:
        tuple: Texto atualizado dos campos de e-mail e senha
    """
    if email_ativo:
        if event.key == pygame.K_BACKSPACE:
            texto_email = texto_email[:-1]

        else:
            texto_email += event.unicode

    elif senha_ativo:
        if event.key == pygame.K_BACKSPACE:
            texto_senha = texto_senha[:-1]

        else:
            texto_senha += event.unicode

    return texto_email, texto_senha


def desenhar_rotulo_campo(tela, fonte, campo, texto):
    """
    Desenhar um rótulo (título) acima de um campo de entrada

    Args:
        tela (pygame.Surface): Superfície onde será desenhado
        fonte (pygame.font.Font): Fonte do texto
        campo (pygame.Rect): Retângulo do campo de entrada
        texto (str): Texto do rótulo
    """
    rotulo = fonte.render(texto, True, cores.PRETO)
    tela.blit(rotulo, (campo.x, campo.y - 40))


def desenhar_campo_texto(tela, fonte, campo, texto, ativo):
    """
    Desenhar um campo de texto com o conteúdo digitado

    Args:
        tela (pygame.Surface): Superfície onde será desenhado
        fonte (pygame.font.Font): Fonte do texto
        campo (pygame.Rect): Retângulo do campo de entrada
        texto (str): Texto a ser exibido
        ativo (bool): Indica se o campo está ativo (selecionado)
    """
    cor = cores.PRETO if ativo else cores.CINZA_CLARO
    pygame.draw.rect(tela, cores.OURO, campo, 2)

    texto_render = fonte.render(texto, True, cor)
    offset = max(0, texto_render.get_width() - (campo.width - 10))
    pos_y = campo.centery - texto_render.get_height() // 2

    tela.set_clip(campo)
    tela.blit(texto_render, (campo.x + 5 - offset, pos_y))
    tela.set_clip(None)


def desenhar_botao(tela, rect, texto, fonte, cor_fundo):
    """
    Desenhar um botão com texto centralizado

    Args:
        tela (pygame.Surface): Superfície onde será desenhado
        rect (pygame.Rect): Retângulo do botão
        texto (str): Texto do botão
        fonte (pygame.font.Font): Fonte do texto
        cor_fundo (tuple): Cor de fundo do botão
    """
    pygame.draw.rect(tela, cor_fundo, rect)
    texto_render = fonte.render(texto, True, cores.PRETO)
    texto_rect = texto_render.get_rect(center=rect.center)
    tela.blit(texto_render, texto_rect)


def tela_entrar(tela, largura, altura, fonte, botoes, cursores, fundo):
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
    from interface.janela import janela_principal
    from interface.tela_logado import tela_logar

    botao_logar = pygame.Rect(850, 400, 100, 50)
    botao_voltar = pygame.Rect(650, 400, 100, 50)
    email_input = pygame.Rect(600, 150, 400, 50)
    senha_input = pygame.Rect(600, 300, 400, 50)

    texto_email = ''
    texto_senha = ''

    email_ativo = False
    senha_ativo = False

    mensagem_erro = ''


    def autenticar_usuario(email, senha):
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


    while True:
        mouse_pos = pygame.mouse.get_pos()
        atualizar_cursor(
            mouse_pos, [email_input, senha_input], [botao_voltar, botao_logar]
            )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_voltar.collidepoint(event.pos):
                    return janela_principal(
                        tela, largura, altura, fonte, botoes, cursores, fundo)
                
                elif botao_logar.collidepoint(event.pos):
                    if autenticar_usuario(texto_email, texto_senha):
                        return tela_logar(tela, largura, altura, fonte, botoes, cursores, fundo)
                    else:
                        mensagem_erro = "Email e/ou Senha incorretos."

                
                email_ativo, senha_ativo = verificar_campo_ativo(
                    event.pos, email_input, senha_input)

            if event.type == pygame.KEYDOWN:
                texto_email, texto_senha = processar_digito(
                    event, email_ativo, senha_ativo, texto_email, texto_senha)

        
        tela.fill(cores.BRANCO)

        desenhar_rotulo_campo(tela, fonte, email_input, "Email")
        desenhar_rotulo_campo(tela, fonte, senha_input, "Senha")

        desenhar_campo_texto(tela, fonte, email_input, texto_email, email_ativo)
        desenhar_campo_texto(tela, fonte, senha_input, texto_senha, senha_ativo)

        desenhar_botao(tela, botao_voltar, "Voltar", fonte, cores.VERMELHO_ESC)
        desenhar_botao(tela, botao_logar, "Entrar", fonte, cores.OURO)

        if mensagem_erro:
            fonte_erro = pygame.font.SysFont('Unicode', 40)
            texto_erro = fonte_erro.render(mensagem_erro, True, cores.VERMELHO_ESC)
            tela.blit(texto_erro, (610, 500))
        
        pygame.display.update()