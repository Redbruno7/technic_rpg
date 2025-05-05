class Usuario:
    def __init__(self, nome_usuario = '', email = '', senha = ''):
        """Classe Usuário

        Args:
            nome_usuario (str): _description_. Defaults to ''.
            email (str): _description_. Defaults to ''.
            senha (str): _description_. Defaults to ''.
        """
        self._nome_usuario = nome_usuario
        self._email = email
        self._senha = senha


    @property
    def nome_usuario(self):
        """
        Retorna valor privado
        """
        return self._nome_usuario
    

    @nome_usuario.setter
    def nome_usuario(self, valor):
        """Receber valor

        Args:
            valor (str): nome de usuário

        Raises:
            ValueError: entrada vazia
        """
        if not valor.strip():
            raise ValueError('Nome de usuário deve ser preenchido.')
        self._nome_usuario = valor.strip()


    @property
    def email(self):
        """
        Retorna valor privado
        """
        return self._email
    

    @email.setter
    def email(self, valor):
        """Receber valor

        Args:
            valor (str): email do usuário

        Raises:
            ValueError: entrada vazia
        """
        if not valor.strip():
            raise ValueError('E-mail deve ser preenchido.')
        self._email = valor.strip()


    @property
    def senha(self):
        """
        Retorna valor privado
        """
        return self._senha
    

    @senha.setter
    def senha(self, valor):
        """Receber valor

        Args:
            valor (str): senha do usuário

        Raises:
            ValueError: entrada vazia
        """
        if not valor.strip():
            raise ValueError('Senha deve ser preenchida.')
        self._senha = valor.strip()

    def form_cadastro(self):
        """
        Cadastro Usuário - Formulário
        """
        print('=' * 80)
        self.nome_usuario = input('Nome de usuário: ').strip().lower()
        self.email = input('Email: ').strip().lower()
        self.senha = input('Senha: ').strip()
        print('=' * 80)
        print()