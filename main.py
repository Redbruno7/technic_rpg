import sqlite3
import os
from Modulos.menu import menu_1

# Conexao com banco de dados
conn = sqlite3.connect('C:\Bruno - Técnico DS\\technic_rpg\personagem.db')

def cls_term():
    os.system('cls')


menu_1()