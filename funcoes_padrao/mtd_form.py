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


def desenhar_campo_texto(tela, fonte, retangulo, texto, ativo, cursor_index=0, ocultar=False):
    cor_fundo = cores.BRANCO
    cor_borda = cores.OURO
    pygame.draw.rect(tela, cor_fundo, retangulo)
    pygame.draw.rect(tela, cor_borda, retangulo, 2)

    if ocultar:
        texto_render = fonte.render('*' * len(texto), True, (0, 0, 0))
    else:
        texto_render = fonte.render(texto, True, (0, 0, 0))

    tela.blit(texto_render, (retangulo.x + 5, retangulo.y + 5))

    if ativo:
        cursor_x = retangulo.x + 5 + fonte.size(texto[:cursor_index])[0]
        cursor_y = retangulo.y + 5
        cursor_altura = fonte.get_height()
        pygame.draw.line(tela, (0, 0, 0), (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_altura))


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


def processar_digito_login(event, email_ativo, senha_ativo, texto_email, pos_cursor_email, pos_cursor_senha):
    """
    Processa digitação, incluindo movimentação do cursor com setas esquerda e direita
    e edição do texto nos campos ativos.

    Args:
        event (pygame.Event): Evento de tecla pressionada
        *_ativo (bool): Flags indicando qual campo está ativo
        texto_* (str): Texto atual dos campos
        pos_cursor_* (int): Posição atual do cursor nos textos

    Returns:
        tuple: (texto_nome, texto_cpf, texto_email, texto_senha,
                pos_cursor_nome, pos_cursor_cpf, pos_cursor_email, pos_cursor_senha)
    """

    def inserir_char(texto, pos, char):
        return texto[:pos] + char + texto[pos:], pos + 1

    def apagar_char(texto, pos):
        if pos > 0:
            texto = texto[:pos-1] + texto[pos:]
            pos -= 1
        return texto, pos

    def mover_cursor_esquerda(pos):
        return max(0, pos - 1)

    def mover_cursor_direita(pos, texto):
        return min(len(texto), pos + 1)

    if email_ativo:
        if event.key == pygame.K_BACKSPACE:
            texto_email, pos_cursor_email = apagar_char(texto_email, pos_cursor_email)

        elif event.key == pygame.K_LEFT:
            pos_cursor_email = mover_cursor_esquerda(pos_cursor_email)

        elif event.key == pygame.K_RIGHT:
            pos_cursor_email = mover_cursor_direita(pos_cursor_email, texto_email)

        else:
            texto_email, pos_cursor_email = inserir_char(texto_email, pos_cursor_email, event.unicode)

    elif senha_ativo:
        if event.key == pygame.K_BACKSPACE:
            texto_senha, pos_cursor_senha = apagar_char(texto_senha, pos_cursor_senha)
            
        elif event.key == pygame.K_LEFT:
            pos_cursor_senha = mover_cursor_esquerda(pos_cursor_senha)

        elif event.key == pygame.K_RIGHT:
            pos_cursor_senha = mover_cursor_direita(pos_cursor_senha, texto_senha)
            
        else:
            texto_senha, pos_cursor_senha = inserir_char(texto_senha, pos_cursor_senha, event.unicode)

    return (texto_email, texto_senha, pos_cursor_email, pos_cursor_senha)


def processar_digito_registro(event, nome_ativo, cpf_ativo, email_ativo, senha_ativo,
                             texto_nome, texto_cpf, texto_email, texto_senha,
                             pos_cursor_nome, pos_cursor_cpf, pos_cursor_email, pos_cursor_senha):
    """
    Processa digitação, incluindo movimentação do cursor com setas esquerda e direita
    e edição do texto nos campos ativos.

    Args:
        event (pygame.Event): Evento de tecla pressionada
        *_ativo (bool): Flags indicando qual campo está ativo
        texto_* (str): Texto atual dos campos
        pos_cursor_* (int): Posição atual do cursor nos textos

    Returns:
        tuple: (texto_nome, texto_cpf, texto_email, texto_senha,
                pos_cursor_nome, pos_cursor_cpf, pos_cursor_email, pos_cursor_senha)
    """

    def inserir_char(texto, pos, char):
        return texto[:pos] + char + texto[pos:], pos + 1

    def apagar_char(texto, pos):
        if pos > 0:
            texto = texto[:pos-1] + texto[pos:]
            pos -= 1
        return texto, pos

    def mover_cursor_esquerda(pos):
        return max(0, pos - 1)

    def mover_cursor_direita(pos, texto):
        return min(len(texto), pos + 1)

    if nome_ativo:
        if event.key == pygame.K_BACKSPACE:
            texto_nome, pos_cursor_nome = apagar_char(texto_nome, pos_cursor_nome)
        elif event.key == pygame.K_LEFT:
            pos_cursor_nome = mover_cursor_esquerda(pos_cursor_nome)
        elif event.key == pygame.K_RIGHT:
            pos_cursor_nome = mover_cursor_direita(pos_cursor_nome, texto_nome)
        else:
            texto_nome, pos_cursor_nome = inserir_char(texto_nome, pos_cursor_nome, event.unicode)

    elif cpf_ativo:
        if event.key == pygame.K_BACKSPACE:
            texto_cpf, pos_cursor_cpf = apagar_char(texto_cpf, pos_cursor_cpf)
            # Remover caracteres não numéricos e ajustar formatação após apagar
            numeros = ''.join(filter(str.isdigit, texto_cpf))
            if len(numeros) <= 3:
                texto_cpf = numeros
            elif len(numeros) <= 6:
                texto_cpf = f"{numeros[:3]}.{numeros[3:]}"
            elif len(numeros) <= 9:
                texto_cpf = f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:]}"
            else:
                texto_cpf = f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"
            pos_cursor_cpf = min(pos_cursor_cpf, len(texto_cpf))  # Ajusta cursor se necessário
        elif event.key == pygame.K_LEFT:
            pos_cursor_cpf = mover_cursor_esquerda(pos_cursor_cpf)
        elif event.key == pygame.K_RIGHT:
            pos_cursor_cpf = mover_cursor_direita(pos_cursor_cpf, texto_cpf)
        elif event.unicode.isdigit() and len(''.join(filter(str.isdigit, texto_cpf))) < 11:
            # Insere o dígito na posição do cursor
            texto_cpf, pos_cursor_cpf = inserir_char(texto_cpf, pos_cursor_cpf, event.unicode)
            # Reformatar o texto
            numeros = ''.join(filter(str.isdigit, texto_cpf))
            if len(numeros) <= 3:
                texto_cpf = numeros
            elif len(numeros) <= 6:
                texto_cpf = f"{numeros[:3]}.{numeros[3:]}"
            elif len(numeros) <= 9:
                texto_cpf = f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:]}"
            else:
                texto_cpf = f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"
            pos_cursor_cpf = min(pos_cursor_cpf, len(texto_cpf))

    elif email_ativo:
        if event.key == pygame.K_BACKSPACE:
            texto_email, pos_cursor_email = apagar_char(texto_email, pos_cursor_email)
        elif event.key == pygame.K_LEFT:
            pos_cursor_email = mover_cursor_esquerda(pos_cursor_email)
        elif event.key == pygame.K_RIGHT:
            pos_cursor_email = mover_cursor_direita(pos_cursor_email, texto_email)
        else:
            texto_email, pos_cursor_email = inserir_char(texto_email, pos_cursor_email, event.unicode)

    elif senha_ativo:
        if event.key == pygame.K_BACKSPACE:
            texto_senha, pos_cursor_senha = apagar_char(texto_senha, pos_cursor_senha)
        elif event.key == pygame.K_LEFT:
            pos_cursor_senha = mover_cursor_esquerda(pos_cursor_senha)
        elif event.key == pygame.K_RIGHT:
            pos_cursor_senha = mover_cursor_direita(pos_cursor_senha, texto_senha)
        else:
            texto_senha, pos_cursor_senha = inserir_char(texto_senha, pos_cursor_senha, event.unicode)

    return (texto_nome, texto_cpf, texto_email, texto_senha,
            pos_cursor_nome, pos_cursor_cpf, pos_cursor_email, pos_cursor_senha)