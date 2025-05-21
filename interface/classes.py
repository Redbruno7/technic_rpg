class Usuario:
    def __init__(self, nome_usuario = '', cpf_usuario = '', email_usuario = '', senha_usuario = ''):
        """Classe Usuário

        Args:
            nome_usuario (str): _description_. Defaults to ''.
            cpf_usuario (str): _description_. Defaults to ''.
            email_usuario (str): _description_. Defaults to ''.
            senha_usuario (str): _description_. Defaults to ''.
        """
        self._nome_usuario = nome_usuario
        self._cpf_usuario = cpf_usuario
        self._email_usuario = email_usuario
        self._senha_usuario = senha_usuario


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
    def cpf_usuario(self):
        """
        Retorna valor privado
        """
        return self._cpf_usuario
    

    @cpf_usuario.setter
    def cpf_usuario(self, valor):
        """Receber valor

        Args:
            valor (str): cpf usuário

        Raises:
            ValueError: entrada vazia
        """
        if not valor.strip():
            raise ValueError('Nome de usuário deve ser preenchido.')
        self._cpf_usuario = valor.strip()


    @property
    def email_usuario(self):
        """
        Retorna valor privado
        """
        return self._email_usuario
    

    @email_usuario.setter
    def email_usuario(self, valor):
        """Receber valor

        Args:
            valor (str): email do usuário

        Raises:
            ValueError: entrada vazia
        """
        if not valor.strip():
            raise ValueError('E-mail deve ser preenchido.')
        self._email_usuario = valor.strip()


    @property
    def senha_usuario(self):
        """
        Retorna valor privado
        """
        return self._senha_usuario
    

    @senha_usuario.setter
    def senha_usuario(self, valor):
        """Receber valor

        Args:
            valor (str): senha do usuário

        Raises:
            ValueError: entrada vazia
        """
        if not valor.strip():
            raise ValueError('Senha deve ser preenchida.')
        self._senha_usuario = valor.strip()

    def form_cadastro(self):
        """
        Cadastro Usuário - Formulário
        """
        print('=' * 80)
        self.nome_usuario = input('Nome de usuário: ').strip().lower()
        self.cpf_usuario = input('CPF: ').strip()
        self.email_usuario = input('Email: ').strip().lower()
        self.senha_usuario = input('Senha: ').strip()
        print('=' * 80)
        print()