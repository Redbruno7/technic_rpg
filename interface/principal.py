import os
os.system('cls')  # Limpa o terminal no Windows


import cores
import pygame
import sys


# Inicializa o pygame
pygame.init()

# Define as dimensões da janela
largura = 1600
altura = 800

# Cria a tela
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Guedgers")

# Fonte
fonte = pygame.font.SysFont('Unicode', 40)

# Botão 'entrar'
botao_entrar = pygame.Rect(735, 100, 130, 50) # x, y, largura, altura
botao_registrar = pygame.Rect(735, 200, 130, 50) # x, y, largura, altura
botao_sair = pygame.Rect(735, 300, 130, 50) # x, y, largura, altura


# No topo (fora do loop), carregue os cursores padrão do pygame
padrao_cursor = pygame.SYSTEM_CURSOR_ARROW
mao_cursor = pygame.SYSTEM_CURSOR_HAND
digitar = pygame.SYSTEM_CURSOR_IBEAM


# Loop principal
def janela_principal():
    fundo = pygame.image.load("imgs\minecraft.jpg")
    fundo = pygame.transform.scale(fundo, (largura, altura))
    import tela_entrar
    import tela_registrar 
    while True:
        tela.blit(fundo, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
                # Verifica se o mouse está em cima de qualquer botão
        if (botao_entrar.collidepoint(mouse_pos) or 
            botao_registrar.collidepoint(mouse_pos) or 
            botao_sair.collidepoint(mouse_pos)):
            
            pygame.mouse.set_cursor(mao_cursor)  # Muda para cursor de mão
        else:
            pygame.mouse.set_cursor(padrao_cursor)  # Volta para o cursor padrão
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if botao_entrar.collidepoint(event.pos):
                    return tela_entrar.tela_entrar(tela)

                if botao_registrar.collidepoint(event.pos):
                    return tela_registrar.tela_registrar(tela)

                if botao_sair.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


        # # Preenche a tela com uma cor (por exemplo, branco)
        # tela.fill(cores.BRANCO)

        # Desenha o botao
        pygame.draw.rect(tela, cores.OURO , botao_entrar)
        pygame.draw.rect(tela, cores.OURO , botao_registrar)
        pygame.draw.rect(tela, cores.VERMELHO_ESCURO , botao_sair)

        # Desenha o texto no botão
        texto = fonte.render('Entrar', True, cores.PRETO)
        texto_rect = texto.get_rect(center=botao_entrar.center)
        tela.blit(texto, texto_rect)

        texto = fonte.render('Registrar', True, cores.PRETO)
        texto_rect = texto.get_rect(center=botao_registrar.center)
        tela.blit(texto, texto_rect)

        texto = fonte.render('Sair', True, cores.PRETO)
        texto_rect = texto.get_rect(center=botao_sair.center)
        tela.blit(texto, texto_rect)

        # Atualiza o display
        pygame.display.update()

if __name__ == "__main__":
    janela_principal()