import os
from Modulos.classes import Usuario


def cls_term():
    os.system('cls')


def titulo():
    """
    Título do Projeto
    """
    print('=' * 80)
    print('RPG - CRIAÇÃO DE PERSONAGEM'.center(80))
    print('=' * 80)
    print()


def selecionar_opcao(texto, min_valor=1, max_valor=10):
    while True:
        opcao = input(texto).strip()
        try:
            opcao = int(opcao)
            if min_valor <= opcao <= max_valor:
                return opcao
            else:
                print('-' * 80)
                print('Entrada inválida. Tente novamente.')
                print('-' * 80)
        except ValueError:
            print('-' * 80)
            print('Entrada inválida. Tente novamente.')
            print('-' * 80)


def menu_1():
    """
    Acesso e Cadastro de Usuário - Menu 1
    """
    cls_term()
    print('=' * 80)
    print('Menu Principal:'.center(80))
    print('=' * 80)
    print('1. Entrar.')
    print('2. Registrar.')
    print('3. Sair.')
    print('-' * 80)

    while True:
        opcao_1 = selecionar_opcao('Escolha uma opção (1-3): ', 1, 3)

        if opcao_1 == 1:
            cls_term()
            titulo()
            # ação da opção 1

        elif opcao_1 == 2:
            cls_term()
            titulo()
            usuario = Usuario()
            while True:
                try:
                    usuario.form_cadastro()
                    break
                except ValueError as e:
                    print('-' * 80)
                    print(e)
                    print('-' * 80)

            print('=' * 80)
            print('Usuário registrado com sucesso.')
            print('-' * 80)
            input('Aperte Enter para voltar ao Menu Principal: ')
            return menu_1()

        elif opcao_1 == 3:
            print('=' * 80)
            print()
            print('=' * 80)
            print('Encerrando o sistema...')
            print('=' * 80)
            print()
            break
        else:
            print('-' * 80)
            input('Opção inválida. Aperte Enter para tentar novamente: ')
        cls_term()



def menu_2():
    """
    Acesso - Formulário
    """
    print('=' * 80)
    print('Menu:'.center(80))
    print('=' * 80)
    print('1. Car.')
    print('2. Motorcycle.')
    print('3. Truck.')
    print('4. Back.')
    print('-' * 80)