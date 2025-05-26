import pygame
from funcoes_padrao import cores


def atualizar_cursor(pos, campos, botoes):

    # Campos de texto
    if any(campo.collidepoint(pos) for campo in campos):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)

    # Botões
    elif any(botao.collidepoint(pos) for botao in botoes):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    # Padrão
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


def desenhar_rotulo_campo(tela, fonte, campo, texto):

    # Título do campo
    rotulo = fonte.render(texto, True, cores.AMARELO_OURO_VELHO)
    tela.blit(rotulo, (campo.x, campo.y - 40))


def desenhar_campo_texto(tela, fonte, retangulo, texto, ativo, cursor_index=0, ocultar=False):

    # Cores
    cor_fundo = cores.BRANCO
    cor_borda = cores.AMARELO_OURO_VELHO
    cor_texto = cores.PRETO

    # Fundo e borda
    pygame.draw.rect(tela, cor_fundo, retangulo)
    pygame.draw.rect(tela, cor_borda, retangulo, 2)

    # Ocultar senha
    texto_visivel = '*' * len(texto) if ocultar else texto

    # Texto renderizado
    texto_render = fonte.render(texto_visivel, True, cor_texto)

    # Largura visível do campo
    largura_maxima = retangulo.width - 10  # margem de 5px dos lados

    # Coordenada X do cursor no texto completo
    cursor_x_total = fonte.size(texto_visivel[:cursor_index])[0]

    # Scroll horizontal (deslocamento do texto)
    scroll_x = 0
    if cursor_x_total > largura_maxima:
        scroll_x = cursor_x_total - largura_maxima
    elif cursor_x_total < scroll_x:
        scroll_x = 0

    # Criar uma "máscara" (clipping) para evitar que o texto vaze
    tela.set_clip(retangulo)

    # Desenhar o texto com scroll aplicado
    tela.blit(texto_render, (retangulo.x + 5 - scroll_x, retangulo.y + (retangulo.height - fonte.get_height()) // 2))

    # Restaurar clipping
    tela.set_clip(None)

    # Cursor piscante
    if ativo and (pygame.time.get_ticks() // 500) % 2 == 0:
        cursor_x = retangulo.x + 5 + cursor_x_total - scroll_x
        cursor_y = retangulo.y + (retangulo.height - fonte.get_height()) // 2
        cursor_altura = fonte.get_height()
        pygame.draw.line(tela, cor_texto, (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_altura))


def desenhar_botao(tela, rect, texto, fonte, cor_fundo):

    # Desenhar botões
    pygame.draw.rect(tela, cor_fundo, rect)
    texto_render = fonte.render(texto, True, cores.PRETO)
    texto_rect = texto_render.get_rect(center=rect.center)
    tela.blit(texto_render, texto_rect)


def verificar_campo_ativo_login(pos, campo_email, campo_senha):

    # Verificar campo ativo - Login
    email_ativo = campo_email.collidepoint(pos)
    senha_ativo = campo_senha.collidepoint(pos)

    return email_ativo, senha_ativo


def verificar_campo_ativo_registro(pos, campo_nome, campo_cpf, campo_email, campo_senha):

    # Verificar campo ativo - Registro
    nome_ativo = campo_nome.collidepoint(pos)
    cpf_ativo = campo_cpf.collidepoint(pos)
    email_ativo = campo_email.collidepoint(pos)
    senha_ativo = campo_senha.collidepoint(pos)

    return nome_ativo, cpf_ativo, email_ativo, senha_ativo


def processar_digito_login(event, email_ativo, senha_ativo, texto_email, texto_senha, pos_cursor_email, pos_cursor_senha):

    # Email
    if email_ativo:

        # DEFAULT
        if len(event.unicode) > 0 and event.unicode.isprintable():
            texto_email = texto_email[:pos_cursor_email] + \
                event.unicode + texto_email[pos_cursor_email:]
            pos_cursor_email += len(event.unicode)

    # Senha
    elif senha_ativo:

        # DEFAULT
        if len(event.unicode) > 0 and event.unicode.isprintable():
            texto_senha = texto_senha[:pos_cursor_senha] + \
                event.unicode + texto_senha[pos_cursor_senha:]
            pos_cursor_senha += len(event.unicode)

    return (texto_email, texto_senha, pos_cursor_email, pos_cursor_senha)


def processar_digito_registro(event, nome_ativo, cpf_ativo, email_ativo, senha_ativo,
                              texto_nome, texto_cpf, texto_email, texto_senha,
                              pos_cursor_nome, pos_cursor_cpf, pos_cursor_email, pos_cursor_senha):

    # Nome
    if nome_ativo:

        # DEFAULT
        if len(event.unicode) > 0 and event.unicode.isprintable():
            texto_nome = texto_nome[:pos_cursor_nome] + \
                event.unicode + texto_nome[pos_cursor_nome:]
            pos_cursor_nome += len(event.unicode)

    # CPF
    elif cpf_ativo:

        # DEFAULT
        if event.unicode.isdigit() and len(texto_cpf) < 11:
            texto_cpf = texto_cpf[:pos_cursor_cpf] + \
                event.unicode + texto_cpf[pos_cursor_cpf:]
            pos_cursor_cpf += 1

    # Email
    elif email_ativo:

        # DEFAULT
        if len(event.unicode) > 0 and event.unicode.isprintable():
            texto_email = texto_email[:pos_cursor_email] + \
                event.unicode + texto_email[pos_cursor_email:]
            pos_cursor_email += len(event.unicode)

    # Senha
    elif senha_ativo:

        # DEFAULT
        if len(event.unicode) > 0 and event.unicode.isprintable():
            texto_senha = texto_senha[:pos_cursor_senha] + \
                event.unicode + texto_senha[pos_cursor_senha:]
            pos_cursor_senha += len(event.unicode)

    return (texto_nome, texto_cpf, texto_email, texto_senha,
            pos_cursor_nome, pos_cursor_cpf, pos_cursor_email, pos_cursor_senha)
