import uuid
from tkinter import messagebox

import bcrypt

from view.base import *


class Login(TelaBaseFilha):
    """    Classe para a criação da tela de login    """

    def __init__(self, parent, update_user, telafechada, nome, widthinc, heightinc):
        super().__init__(parent, None, telafechada, nome, widthinc, heightinc)
        self.update_user = update_user
        self.user = None
        # Tamanho da tela
        self.posicionar_tela(widht=250, height=150)
        # ajustar os tamanhos das colunas e linhas
        self.ajustar_colunas_linhas(8, 10)

        # Linha do Título
        self.criar(Label, name='titulo', borderwidth=2, relief='groove', text="LOGIN", font=self.fonteTitulo)
        self.instalar_em(name='titulo', row=0, column=0, rowspan=4, columnspan=8, sticky=tk.NSEW)

        # Usuário
        self.criar(Label, name='usuario_lbl', borderwidth=2, relief='groove', text="Usuário:", font=self.fonte)
        self.instalar_em(name='usuario_lbl', row=4, column=0, rowspan=2, columnspan=4, sticky=tk.NSEW)
        self.criar(Entry, name='usuario', borderwidth=2, relief='groove')
        self.instalar_em(name='usuario', row=4, column=4, rowspan=2, columnspan=4, sticky=tk.NSEW)
        self.widgets['usuario'].focus()

        # Senha
        self.criar(Label, name='senha_lbl', borderwidth=2, relief='groove', text="Senha:", font=self.fonte)
        self.instalar_em(name='senha_lbl', row=6, column=0, rowspan=2, columnspan=4, sticky=tk.NSEW)
        self.criar(Entry, name='senha', borderwidth=2, relief='groove', show='*')
        self.instalar_em(name='senha', row=6, column=4, rowspan=2, columnspan=4, sticky=tk.NSEW)

        # Botões
        self.criar(Button, name='bt_ok', text="OK", command=self.validar, fg="green", font=self.fonte)
        self.instalar_em(name='bt_ok', row=8, column=0, rowspan=2, columnspan=4, sticky=tk.NSEW)
        self.criar(Button, name='btcancelar', text="CANCELAR", command=self.sair, fg="red", font=self.fonte)
        self.instalar_em(name='btcancelar', row=8, column=4, rowspan=2, columnspan=4, sticky=tk.NSEW)

    def validar(self):
        """Função que verifica as credenciais do usuário"""
        valido = True
        usuario_nome = self.widgets['usuario'].get().upper()
        usuario_senha = self.widgets['senha'].get().upper()

        # Verifica se foram preenchidos os campos usuario/senha e coloca em vermelho caso não estejam preenchidos
        if usuario_nome == "":
            valido = False
            self.alterar_parametro('usuario', bg="red")
        else:
            self.alterar_parametro('usuario', bg="white")

        if usuario_senha == "":
            valido = False
            self.alterar_parametro('senha', bg="red")
        else:
            self.alterar_parametro('senha', bg="white")

        # Verifica se o usuário/senha estão corretos
        if valido:
            # verifica existência do usuário
            usuario = bd_consulta_valor_tabela('usuarios', 'nome', usuario_nome)

            if not usuario:
                tk.messagebox.showerror(title="Erro", message="Usuário e/ou Senha inválidos!")
            else:
                # verifica se está ativo
                if usuario[0][2] == 0:
                    tk.messagebox.showerror(title="Erro", message="Usuário está bloqueado!")
                else:
                    if not validar_senha(usuario_senha, usuario[0][3]):
                        tk.messagebox.showerror(title="Erro", message="Usuário e/ou Senha inválidos!")
                    else:
                        # verifica se é administrador, caso contrario verifica se o pc está valido para operar o sistema
                        if usuario[0][4] == 1 or verificar_mac():
                            self.update_user(usuario_nome, usuario[0][4])
                            self.sair()
                        else:
                            self.sair()
                            tk.messagebox.showerror(title="Erro", message="Computador não habilitado para operar o sistema!")


def validar_senha(senha, hash_senha):
    """Função que valida a senha repassada"""
    return bcrypt.hashpw(senha.encode('utf-8'), hash_senha.encode('utf-8')) == hash_senha.encode('utf-8')


def verificar_mac():
    """Função que verifica se o mac_address do pc está cadastrado no BD"""
    resultado = False

    if len(bd_consulta_valor_tabela('mac_address', 'mac_nome', str(hex(uuid.getnode())))) > 0:
        resultado = True

    return resultado
