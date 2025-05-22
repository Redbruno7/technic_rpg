import pygame

# Iniciar pygame
pygame.init()

# Definir e atribuir dimensões da tela
largura = 1600
altura = 800
tela = pygame.display.set_mode((largura, altura))

# Nomear tela
pygame.display.set_caption("Guedgers")

# Definir fonte
fonte = pygame.font.SysFont('Unicode', 40)

# Dimensionar botões
botao_entrar = pygame.Rect(735, 100, 130, 50)
botao_registrar = pygame.Rect(735, 200, 130, 50)
botao_sair = pygame.Rect(735, 300, 130, 50)

# Unificar botões
botoes = (botao_entrar, botao_registrar, botao_sair)

# Definir visuais para cursor
padrao_cursor = pygame.SYSTEM_CURSOR_ARROW
mao_cursor = pygame.SYSTEM_CURSOR_HAND

# Unificar cursores
cursores = (padrao_cursor, mao_cursor)

# Definir imagem de de fundo
fundo = pygame.image.load("imgs/minecraft.jpg")
fundo = pygame.transform.scale(fundo, (largura, altura))