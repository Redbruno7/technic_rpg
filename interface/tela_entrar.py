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
    from interface.tela_principal import janela_principal
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

    backspace_timer = 0
    BACKSPACE_DELAY = 100


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
        atualizar_cursor(mouse_pos, [email_input, senha_input], [botao_voltar, botao_logar])

        teclas = pygame.key.get_pressed()
        tempo_atual = pygame.time.get_ticks()

        if teclas[pygame.K_BACKSPACE]:
            if (email_ativo or senha_ativo) and tempo_atual - backspace_timer > BACKSPACE_DELAY:
                if email_ativo and texto_email:
                    texto_email = texto_email[:-1]

                elif senha_ativo and texto_senha:
                    texto_senha = texto_senha[:-1]

                backspace_timer = tempo_atual

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if botao_voltar.collidepoint(event.pos):
                    return janela_principal(tela, largura, altura, fonte, botoes, cursores, fundo)
                
                elif botao_logar.collidepoint(event.pos):
                    if autenticar_usuario(texto_email, texto_senha):
                        return tela_logar(tela, largura, altura, fonte, botoes, cursores, fundo)
                    
                    else:
                        mensagem_erro = "Email e/ou Senha incorretos."

                email_ativo, senha_ativo = verificar_campo_ativo_login(event.pos, email_input, senha_input)

            # Evento de tecla
            if event.type == pygame.KEYDOWN:

                # Evento BACKSPACE
                if event.key == pygame.K_BACKSPACE:
                    backspace_timer = pygame.time.get_ticks() - BACKSPACE_DELAY

                # Evento TAB
                elif event.key == pygame.K_TAB:
                    if email_ativo:
                        email_ativo = False
                        senha_ativo = True

                    elif senha_ativo:
                        senha_ativo = False
                        email_ativo = True

                    else:
                        email_ativo = True

                else:
                    texto_email, texto_senha = processar_digito_login(event, email_ativo, senha_ativo, texto_email, texto_senha)


        
        tela.fill(cores.BRANCO)

        desenhar_rotulo_campo(tela, fonte, email_input, "Email")
        desenhar_rotulo_campo(tela, fonte, senha_input, "Senha")

        desenhar_campo_texto(tela, fonte, email_input, texto_email, email_ativo)
        desenhar_campo_texto(tela, fonte, senha_input, texto_senha, senha_ativo, ocultar=True)

        desenhar_botao(tela, botao_voltar, "Voltar", fonte, cores.VERMELHO_ESC)
        desenhar_botao(tela, botao_logar, "Entrar", fonte, cores.OURO)

        if mensagem_erro:
            fonte_erro = pygame.font.SysFont('Unicode', 40)
            texto_erro = fonte_erro.render(mensagem_erro, True, cores.VERMELHO_ESC)
            tela.blit(texto_erro, (610, 500))
        
        pygame.display.update()