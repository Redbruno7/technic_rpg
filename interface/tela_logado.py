import os
import sqlite3
import pygame
from funcoes_padrao import cores
from funcoes_padrao.mtd_form import desenhar_botao
from interface.tela_principal import janela_principal
from interface.tela_editar import tela_editar


pygame.init()
os.system('cls')

# Conectar Banco de dados
conn = sqlite3.connect(r'bd\Guedgers.db')
cursor = conn.cursor()

# Dimensões de tela fullscreen baseada no monitor do usuário
largura, altura = 1600, 800
tela = pygame.display.set_mode((largura, altura))



def tela_logar(tela, largura, altura, fonte, botoes, cursores, email_original):
    """
    Exibe a tela do usuário logado, mostrando suas informações pessoais e opções de navegação.

    Args:
        tela (pygame.Surface): Superfície da janela principal onde os elementos serão desenhados.
        largura (int): Largura da janela em pixels.
        altura (int): Altura da janela em pixels.
        fonte (pygame.font.Font): Fonte padrão utilizada para os textos e botões.
        botoes (list): Lista de retângulos para os botões interativos (não utilizado diretamente aqui, mas pode ser útil).
        cursores (tuple): Tupla com cursores personalizados (cursor padrão e cursor de mão).
        email_original (str): Email do usuário logado, usado para buscar os dados no banco de dados.

    Returns:
        function: Redireciona para a `janela_principal` se o botão "Sair" for clicado,
                  ou para a `tela_editar` se o botão "Editar" for clicado.
    """

    # Imagem de fundo
    fundo = pygame.image.load("imgs/fundo_logado.png")
    fundo = pygame.transform.scale(fundo, (largura, altura))

    # Imagem - GUEDGERS
    guedgers = pygame.image.load("imgs/guedgers.png")

    # Imagem - INFORMAÇÕES DA CONTA
    bem_vindo = pygame.image.load("imgs/info.png")
    bem_vindo = pygame.transform.scale(bem_vindo, (500, 500))

    # Posição dos campos e botões
    botao_sair = pygame.Rect(250, 550, 100, 50)
    botao_editar = pygame.Rect(100, 550, 100, 50)
    padrao_cursor, mao_cursor = cursores

    # Método de exibição de usuário
    def exibir_usuario():
        """
        Busca no banco de dados as informações do usuário logado e exibe na tela:
        Nome, CPF, Email e Senha.

        Usa o email passado para a função `tela_logar` como referência de busca.
        As informações são renderizadas com a fonte 'Unicode' e desenhadas na tela.
        """

        # Selecionar registro no banco de dados
        cursor.execute(
            '''
            SELECT nome_usuario, cpf_usuario, email_usuario, senha_usuario
            FROM Usuario
            WHERE email_usuario = ?
            ''',
            (email_original,)
        )

        usuario = cursor.fetchone()

        # Separar dados
        if usuario:
            nome, cpf, email, senha = usuario

        # Fonte
        fonte_info = pygame.font.SysFont('Unicode', 50)

        # Desenhar Informações
        texto_nome = fonte_info.render(f"Nome: {nome}", True, cores.BEGE)
        texto_cpf = fonte_info.render(f"CPF: {cpf}", True, cores.BEGE)
        texto_email = fonte_info.render(f"E-mail: {email}", True, cores.BEGE)
        texto_senha = fonte_info.render(f"Senha: {senha}", True, cores.BEGE)

        # Posicionar informações
        tela.blit(texto_nome, (100, 300))
        tela.blit(texto_cpf, (100, 350))
        tela.blit(texto_email, (100, 400))
        tela.blit(texto_senha, (100, 450))

    # Loop principal
    while True:

        # Posição das imagens
        tela.blit(fundo, (0, 0))
        tela.blit(guedgers, (500, 100))
        tela.blit(bem_vindo, (50, -100))

        # Atualizar cursor
        mouse_pos = pygame.mouse.get_pos()
        if (botao_editar.collidepoint(mouse_pos) or
            botao_sair.collidepoint(mouse_pos)):

            pygame.mouse.set_cursor(mao_cursor)

        else:
            pygame.mouse.set_cursor(padrao_cursor)

        # Eventos
        for event in pygame.event.get():

            # MOUSE BTN-1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    # Botão Sair
                    if botao_sair.collidepoint(event.pos):
                        return janela_principal(
                            tela, largura, altura, fonte, botoes, cursores)

                    # Botão Editar
                    if botao_editar.collidepoint(event.pos):
                        return tela_editar(
                            tela, largura, altura, fonte, botoes, cursores, email_original)

        # Invocar método - Desenhar botões
        desenhar_botao(tela, botao_sair, "Sair", fonte, cores.SANGUE_SECO)
        desenhar_botao(tela, botao_editar, "Editar",
                       fonte, cores.AMARELO_OURO_VELHO)

        # Invocar método - Exibir informações do usuário
        exibir_usuario()

        pygame.display.update()
