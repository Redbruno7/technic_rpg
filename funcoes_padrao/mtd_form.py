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
    # Cores
    cor_fundo = cores.BRANCO
    cor_borda = cores.OURO
    cor_texto = cores.PRETO  # Se tiver definido em cores.py

    # Fundo e borda do campo
    pygame.draw.rect(tela, cor_fundo, retangulo)
    pygame.draw.rect(tela, cor_borda, retangulo, 2)

    # Aplicar ocultação se for senha
    texto_visivel = '*' * len(texto) if ocultar else texto

    # Texto renderizado
    texto_render = fonte.render(texto_visivel, True, cor_texto)
    tela.blit(texto_render, (retangulo.x + 5, retangulo.y + (retangulo.height - fonte.get_height()) // 2))

    # Desenhar cursor se ativo
    if ativo:
        
        # Corrigir índice se maior que o texto
        cursor_index = min(cursor_index, len(texto))

        # Calcular posição x do cursor
        cursor_x = retangulo.x + 5 + fonte.size(texto_visivel[:cursor_index])[0]
        cursor_y = retangulo.y + (retangulo.height - fonte.get_height()) // 2
        cursor_altura = fonte.get_height()

        # Cursor piscando
        if (pygame.time.get_ticks() // 500) % 2 == 0:  # Pisca a cada ~0,5s
            pygame.draw.line(tela, cor_texto, (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_altura))


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
            texto_email, pos_cursor_email = apagar_char(
                texto_email, pos_cursor_email)

        elif event.key == pygame.K_LEFT:
            pos_cursor_email = mover_cursor_esquerda(pos_cursor_email)

        elif event.key == pygame.K_RIGHT:
            pos_cursor_email = mover_cursor_direita(
                pos_cursor_email, texto_email)

        else:
            texto_email, pos_cursor_email = inserir_char(
                texto_email, pos_cursor_email, event.unicode)

    elif senha_ativo:
        if event.key == pygame.K_BACKSPACE:
            texto_senha, pos_cursor_senha = apagar_char(
                texto_senha, pos_cursor_senha)

        elif event.key == pygame.K_LEFT:
            pos_cursor_senha = mover_cursor_esquerda(pos_cursor_senha)

        elif event.key == pygame.K_RIGHT:
            pos_cursor_senha = mover_cursor_direita(
                pos_cursor_senha, texto_senha)

        else:
            texto_senha, pos_cursor_senha = inserir_char(
                texto_senha, pos_cursor_senha, event.unicode)

    return (texto_email, texto_senha, pos_cursor_email, pos_cursor_senha)


def calcular_posicao_formatada_cpf(numeros, pos_cursor_numeros):
    """
    Converte a posição do cursor na string 'numeros' (sem pontuação)
    para a posição correspondente na string formatada (com pontos e traço).
    """
    i_n = 0  # índice nos números
    i_f = 0  # índice na string formatada

    while i_n < len(numeros) and i_n < pos_cursor_numeros:
        if i_n == 3 or i_n == 6:
            i_f += 1  # ponto
        elif i_n == 9:
            i_f += 1  # traço
        i_n += 1
        i_f += 1

    return i_f


def formatar_cpf_com_cursor(numeros, pos_cursor_digito):
    """
    Formata o CPF e retorna:
    - texto formatado com pontos e traço
    - posição visual do cursor no texto formatado
    """
    texto_formatado = ""
    cursor_visual = 0
    pos_digito = 0

    for i, digito in enumerate(numeros):
        if pos_digito == pos_cursor_digito:
            cursor_visual = len(texto_formatado)

        texto_formatado += digito
        pos_digito += 1

        # Adiciona formatação conforme o número de dígitos
        if i == 2 or i == 5:
            texto_formatado += "."
        elif i == 8:
            texto_formatado += "-"

    # Caso cursor esteja no final
    if pos_cursor_digito == len(numeros):
        cursor_visual = len(texto_formatado)

    return texto_formatado, cursor_visual


def processar_digito_registro(event, nome_ativo, cpf_ativo, email_ativo, senha_ativo,
                              texto_nome, texto_cpf, texto_email, texto_senha,
                              pos_cursor_nome, pos_cursor_cpf, pos_cursor_email, pos_cursor_senha):
    """
    Processa a digitação nos campos de texto do formulário de registro, com suporte a cursor e formatação.

    Returns:
        tuple: textos atualizados e posições dos cursores
    """
    import re

    # NOME
    if nome_ativo:
        if event.key == pygame.K_BACKSPACE and pos_cursor_nome > 0:
            texto_nome = texto_nome[:pos_cursor_nome - 1] + texto_nome[pos_cursor_nome:]
            pos_cursor_nome -= 1

        elif event.key == pygame.K_LEFT and pos_cursor_nome > 0:
            pos_cursor_nome -= 1

        elif event.key == pygame.K_RIGHT and pos_cursor_nome < len(texto_nome):
            pos_cursor_nome += 1

        elif len(event.unicode) > 0 and event.unicode.isprintable():
            texto_nome = texto_nome[:pos_cursor_nome] + event.unicode + texto_nome[pos_cursor_nome:]
            pos_cursor_nome += len(event.unicode)

    # CPF
    elif cpf_ativo:
        numeros = ''.join(filter(str.isdigit, texto_cpf))

        if event.key == pygame.K_BACKSPACE:
            if pos_cursor_cpf > 0:
                numeros = numeros[:pos_cursor_cpf - 1] + numeros[pos_cursor_cpf:]
                pos_cursor_cpf -= 1

        elif event.key == pygame.K_LEFT:
            if pos_cursor_cpf > 0:
                pos_cursor_cpf -= 1

        elif event.key == pygame.K_RIGHT:
            if pos_cursor_cpf < len(numeros):
                pos_cursor_cpf += 1

        elif event.unicode.isdigit():
            if len(numeros) < 11:
                numeros = numeros[:pos_cursor_cpf] + event.unicode + numeros[pos_cursor_cpf:]
                pos_cursor_cpf += 1

        # Chamar função para formatar e ajustar posição visual
        texto_cpf, cursor_cpf = formatar_cpf_com_cursor(numeros, pos_cursor_cpf)

    # EMAIL
    elif email_ativo:
        if event.key == pygame.K_BACKSPACE and pos_cursor_email > 0:
            texto_email = texto_email[:pos_cursor_email - 1] + texto_email[pos_cursor_email:]
            pos_cursor_email -= 1

        elif event.key == pygame.K_LEFT and pos_cursor_email > 0:
            pos_cursor_email -= 1

        elif event.key == pygame.K_RIGHT and pos_cursor_email < len(texto_email):
            pos_cursor_email += 1

        elif len(event.unicode) > 0 and event.unicode.isprintable():
            texto_email = texto_email[:pos_cursor_email] + event.unicode + texto_email[pos_cursor_email:]
            pos_cursor_email += len(event.unicode)

    # SENHA
    elif senha_ativo:
        if event.key == pygame.K_BACKSPACE and pos_cursor_senha > 0:
            texto_senha = texto_senha[:pos_cursor_senha - 1] + texto_senha[pos_cursor_senha:]
            pos_cursor_senha -= 1

        elif event.key == pygame.K_LEFT and pos_cursor_senha > 0:
            pos_cursor_senha -= 1

        elif event.key == pygame.K_RIGHT and pos_cursor_senha < len(texto_senha):
            pos_cursor_senha += 1

        elif len(event.unicode) > 0 and event.unicode.isprintable():
            texto_senha = texto_senha[:pos_cursor_senha] + event.unicode + texto_senha[pos_cursor_senha:]
            pos_cursor_senha += len(event.unicode)

    return (texto_nome, texto_cpf, texto_email, texto_senha,
            pos_cursor_nome, pos_cursor_cpf, pos_cursor_email, pos_cursor_senha)
