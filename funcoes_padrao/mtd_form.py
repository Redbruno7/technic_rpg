import pygame
from funcoes_padrao import cores


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


def desenhar_campo_texto(tela, fonte, campo, texto, ativo, ocultar=False):
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

    # Se for o campo de senha, mostra asteriscos no lugar do texto
    texto_exibido = '*' * len(texto) if ocultar else texto

    texto_render = fonte.render(texto_exibido, True, cor)
    offset = max(0, texto_render.get_width() - (campo.width - 10))
    pos_y = campo.centery - texto_render.get_height() // 2

    tela.set_clip(campo)
    tela.blit(texto_render, (campo.x + 5 - offset, pos_y))
    tela.set_clip(None)


def verificar_campo_ativo_login(pos, campo_email, campo_senha):
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


def verificar_campo_ativo_registro(pos, campo_nome, campo_cpf, campo_email, campo_senha):
    """
    Verificar se o usuário clicou em um dos campos de entrada (e-mail ou senha)

    Args:
        pos (tuple): Posição (x, y) do clique do mouse
        campo_email (pygame.Rect): Retângulo do campo de e-mail
        campo_senha (pygame.Rect): Retângulo do campo de senha

    Returns:
        tuple: Dois valores booleanos indicando se o campo de e-mail ou senha foi ativado
    """
    nome_ativo = campo_nome.collidepoint(pos)
    cpf_ativo = campo_cpf.collidepoint(pos)
    email_ativo = campo_email.collidepoint(pos)
    senha_ativo = campo_senha.collidepoint(pos)

    return nome_ativo, cpf_ativo, email_ativo, senha_ativo


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


def processar_digito_login(event, email_ativo, senha_ativo, texto_email, texto_senha):
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


def processar_digito_registro(event, nome_ativo, cpf_ativo, email_ativo, senha_ativo, texto_nome, texto_cpf, texto_email, texto_senha):
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
    if nome_ativo:
        if event.key == pygame.K_BACKSPACE:
            texto_nome = texto_nome[:-1]

        else:
            texto_nome += event.unicode

    if cpf_ativo:
        if event.key == pygame.K_BACKSPACE:
            texto_cpf = texto_cpf[:-1]
            texto_cpf = ''.join(filter(str.isdigit, texto_cpf))

        elif event.unicode.isdigit() and len(
            texto_cpf.replace('.', '').replace('-', '')) < 11:
            texto_cpf += event.unicode
            numeros = ''.join(filter(str.isdigit, texto_cpf))

            if len(numeros) <= 3:
                texto_cpf = numeros

            elif len(numeros) <= 6:
                texto_cpf = f"{numeros[:3]}.{numeros[3:]}"

            elif len(numeros) <= 9:
                texto_cpf = f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:]}"

            else:
                texto_cpf = f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"

    elif email_ativo:
        if event.key == pygame.K_BACKSPACE:
            texto_email = texto_email[:-1]

        else:
            texto_email += event.unicode

    elif senha_ativo:
        if event.key == pygame.K_BACKSPACE:
            texto_senha = texto_senha[:-1]

        else:
            texto_senha += event.unicode

    return texto_nome, texto_cpf, texto_email, texto_senha