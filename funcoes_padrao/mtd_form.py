import pygame
from funcoes_padrao import cores


def atualizar_cursor(pos, campos, botoes):
    """
    Atualiza o cursor do mouse com base na posição e nos elementos interativos.

    Args:
        pos (tuple): Posição atual do mouse (x, y).
        campos (list): Lista de campos de texto (pygame.Rect).
        botoes (list): Lista de botões (pygame.Rect).
    """

    # Campo de texto
    if any(campo.collidepoint(pos) for campo in campos):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)

    # Botões
    elif any(botao.collidepoint(pos) for botao in botoes):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    # Padrão
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


def desenhar_rotulo_campo(tela, fonte, campo, texto):
    """
    Desenha o rótulo acima de um campo de entrada de texto.

    Args:
        tela (Surface): Superfície onde será desenhado.
        fonte (Font): Fonte usada no texto.
        campo (Rect): Retângulo que representa o campo de entrada.
        texto (str): Texto do rótulo.
    """

    # Rótulo do campo
    rotulo = fonte.render(texto, True, cores.AMARELO_OURO_VELHO)
    tela.blit(rotulo, (campo.x, campo.y - 40))


def desenhar_campo_texto(tela, fonte, retangulo, texto, ativo, cursor_index=0, ocultar=False):
    """
    Desenha um campo de entrada de texto com suporte ao cursor e ocultação (senha).

    Args:
        tela (Surface): Superfície onde será desenhado.
        fonte (Font): Fonte usada para o texto.
        retangulo (Rect): Retângulo do campo.
        texto (str): Texto atual dentro do campo.
        ativo (bool): Define se o campo está ativo (com foco).
        cursor_index (int, optional): Posição do cursor no texto. Defaults to 0.
        ocultar (bool, optional): Oculta o texto (usa asteriscos). Defaults to False.
    """
    
    # Cores do campo de texto
    cor_fundo = cores.CINZA_MUITO_CLARO
    cor_borda = cores.AMARELO_OURO_VELHO
    cor_texto = cores.PRETO

    # Fundo e borda
    pygame.draw.rect(tela, cor_fundo, retangulo)
    pygame.draw.rect(tela, cor_borda, retangulo, 2)

    # Ocultar senha
    texto_visivel = '*' * len(texto) if ocultar else texto

    # Texto renderizado
    texto_render = fonte.render(texto_visivel, True, cor_texto)

    # Largura visível do campo - Margem de 5px dos lados
    largura_maxima = retangulo.width - 10

    # Coordenada do cursor no campo
    cursor_x_total = fonte.size(texto_visivel[:cursor_index])[0]

    # Deslocamento horizontal do texto
    scroll_x = 0
    if cursor_x_total > largura_maxima:
        scroll_x = cursor_x_total - largura_maxima
    elif cursor_x_total < scroll_x:
        scroll_x = 0

    # Recortar área de digitação do campo
    tela.set_clip(retangulo)

    # Desenhar o texto com deslocamento aplicado
    tela.blit(texto_render, (retangulo.x + 5 - scroll_x,
              retangulo.y + (retangulo.height - fonte.get_height()) // 2))

    # Restaurar recorte
    tela.set_clip(None)

    # Animação do cursor
    if ativo and (pygame.time.get_ticks() // 500) % 2 == 0:
        cursor_x = retangulo.x + 5 + cursor_x_total - scroll_x
        cursor_y = retangulo.y + (retangulo.height - fonte.get_height()) // 2
        cursor_altura = fonte.get_height()
        pygame.draw.line(tela, cor_texto, (cursor_x, cursor_y),
                         (cursor_x, cursor_y + cursor_altura))


def desenhar_botao(tela, rect, texto, fonte, cor_fundo):
    """
    Desenha um botão com texto centralizado.

    Args:
        tela (Surface): Superfície onde será desenhado.
        rect (Rect): Retângulo do botão.
        texto (str): Texto do botão.
        fonte (Font): Fonte usada no texto.
        cor_fundo (Color): Cor de fundo do botão.
    """

    # Desenhar botões
    pygame.draw.rect(tela, cor_fundo, rect)
    texto_render = fonte.render(texto, True, cores.PRETO)
    texto_rect = texto_render.get_rect(center=rect.center)
    tela.blit(texto_render, texto_rect)


def verificar_campo_ativo_login(pos, campo_email, campo_senha):
    """
    Verifica se o clique do mouse está em um dos campos de login.

    Args:
        pos (tuple): Posição do mouse (x, y).
        campo_email (Rect): Retângulo do campo de e-mail.
        campo_senha (Rect): Retângulo do campo de senha.

    Returns:
        tuple: (bool, bool) indicando se cada campo está ativo.
    """

    # Verificar campo ativo - Login
    email_ativo = campo_email.collidepoint(pos)
    senha_ativo = campo_senha.collidepoint(pos)

    return email_ativo, senha_ativo


def verificar_campo_ativo_registro(pos, campo_nome, campo_cpf, campo_email, campo_senha):
    """
    Verifica se o clique do mouse está em um dos campos do formulário de registro.

    Args:
        pos (tuple): Posição do mouse (x, y).
        campo_nome (Rect): Retângulo do campo de nome.
        campo_cpf (Rect): Retângulo do campo de CPF.
        campo_email (Rect): Retângulo do campo de e-mail.
        campo_senha (Rect): Retângulo do campo de senha.

    Returns:
        tuple: Quatro valores booleanos indicando quais campos estão ativos.
    """

    # Verificar campo ativo - Registro
    nome_ativo = campo_nome.collidepoint(pos)
    cpf_ativo = campo_cpf.collidepoint(pos)
    email_ativo = campo_email.collidepoint(pos)
    senha_ativo = campo_senha.collidepoint(pos)

    return nome_ativo, cpf_ativo, email_ativo, senha_ativo


def processar_digito_login(event, email_ativo, senha_ativo, texto_email, texto_senha, pos_cursor_email, pos_cursor_senha):
    """
    Processa a digitação nos campos de e-mail e senha da tela de login.

    Args:
        event (Event): Evento de tecla pressionada.
        email_ativo (bool): Se o campo de e-mail está ativo.
        senha_ativo (bool): Se o campo de senha está ativo.
        texto_email (str): Texto atual do campo de e-mail.
        texto_senha (str): Texto atual do campo de senha.
        pos_cursor_email (int): Posição do cursor no campo de e-mail.
        pos_cursor_senha (int): Posição do cursor no campo de senha.

    Returns:
        tuple: Texto e posição atualizados de ambos os campos.
    """

    # Email
    if email_ativo:

        # Padrão
        if len(event.unicode) > 0 and event.unicode.isprintable():
            texto_email = texto_email[:pos_cursor_email] + \
                event.unicode + texto_email[pos_cursor_email:]
            pos_cursor_email += len(event.unicode)

    # Senha
    elif senha_ativo:

        # Padrão
        if len(event.unicode) > 0 and event.unicode.isprintable():
            texto_senha = texto_senha[:pos_cursor_senha] + \
                event.unicode + texto_senha[pos_cursor_senha:]
            pos_cursor_senha += len(event.unicode)

    return (texto_email, texto_senha, pos_cursor_email, pos_cursor_senha)


def processar_digito_registro(event, nome_ativo, cpf_ativo, email_ativo, senha_ativo,
                              texto_nome, texto_cpf, texto_email, texto_senha,
                              pos_cursor_nome, pos_cursor_cpf, pos_cursor_email, pos_cursor_senha):
    """
    Processa a digitação nos campos do formulário de registro.

    Args:
        event (Event): Evento de tecla pressionada.
        nome_ativo (bool): Se o campo de nome está ativo.
        cpf_ativo (bool): Se o campo de CPF está ativo.
        email_ativo (bool): Se o campo de e-mail está ativo.
        senha_ativo (bool): Se o campo de senha está ativo.
        texto_nome (str): Texto atual do campo de nome.
        texto_cpf (str): Texto atual do campo de CPF.
        texto_email (str): Texto atual do campo de e-mail.
        texto_senha (str): Texto atual do campo de senha.
        pos_cursor_nome (int): Posição do cursor no campo de nome.
        pos_cursor_cpf (int): Posição do cursor no campo de CPF.
        pos_cursor_email (int): Posição do cursor no campo de e-mail.
        pos_cursor_senha (int): Posição do cursor no campo de senha.

    Returns:
        tuple: Textos e posições dos cursores atualizados para todos os campos.
    """
    
    # Nome
    if nome_ativo:

        # Padrão
        if len(event.unicode) > 0 and event.unicode.isprintable():
            texto_nome = texto_nome[:pos_cursor_nome] + \
                event.unicode + texto_nome[pos_cursor_nome:]
            pos_cursor_nome += len(event.unicode)

    # CPF
    elif cpf_ativo:

        # Padrão
        if event.unicode.isdigit() and len(texto_cpf) < 11:
            texto_cpf = texto_cpf[:pos_cursor_cpf] + \
                event.unicode + texto_cpf[pos_cursor_cpf:]
            pos_cursor_cpf += 1

    # Email
    elif email_ativo:

        # Padrão
        if len(event.unicode) > 0 and event.unicode.isprintable():
            texto_email = texto_email[:pos_cursor_email] + \
                event.unicode + texto_email[pos_cursor_email:]
            pos_cursor_email += len(event.unicode)

    # Senha
    elif senha_ativo:

        # Padrão
        if len(event.unicode) > 0 and event.unicode.isprintable():
            texto_senha = texto_senha[:pos_cursor_senha] + \
                event.unicode + texto_senha[pos_cursor_senha:]
            pos_cursor_senha += len(event.unicode)

    return (texto_nome, texto_cpf, texto_email, texto_senha,
            pos_cursor_nome, pos_cursor_cpf, pos_cursor_email, pos_cursor_senha)
