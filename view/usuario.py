from tkinter import *
from tkinter import messagebox

import bcrypt

from view.base import *


class CadastrarUsuario(TelaBaseFilha):
    def __init__(self, parent, usuario, tela_fechada, nome, widthinc, heightinc):
        super().__init__(parent, usuario, tela_fechada, nome, widthinc, heightinc)
        # ajustar o tamanho da tela
        self.posicionar_tela(widht=400, height=250)
        # ajustar os tamanhos das colunas e linhas
        self.ajustar_colunas_linhas(5, 10)

        self.criar(Label, name='titulo', borderwidth=2, relief='groove', text="CADASTRAR USUÁRIO", font=self.fonteTitulo, pady=10)
        self.instalar_em(name='titulo', row=1, column=1, rowspan=1, columnspan=3, sticky=tk.NSEW)

        # Botões de cadastro, cadastrados, alterações
        self.criar(Label, name='lb_nome_usuario', text="Nome:", font=self.fonte, fg="blue", borderwidth=2, relief='groove', anchor='e')
        self.instalar_em(name='lb_nome_usuario', row=2, column=1, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar(Entry, name='usuario', borderwidth=2, relief='groove')
        self.instalar_em(name='usuario', row=2, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.widgets['usuario'].focus()

        self.criar(Label, name='lb_perfil_usuario', text="Perfil:", font=self.fonte, fg="blue", borderwidth=2, relief='groove', anchor='e')
        self.instalar_em(name='lb_perfil_usuario', row=3, column=1, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar_lista('sb_perfil', 'lt_perfil', lista=bd_consultar("perfis"), row1=3, col_lb=2, colspan_lb=1, col_sb=3, colspan_sb=1)

        self.criar(Label, name='lb_senha', text="Senha:", font=self.fonte, fg="blue", borderwidth=2, relief='groove', anchor='e')
        self.instalar_em(name='lb_senha', row=4, column=1, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar(Entry, name='senha', borderwidth=2, relief='groove', show='*')
        self.instalar_em(name='senha', row=4, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW)

        self.criar(Label, name='lb_senha_confirm', text="Confirme a Senha:", font=self.fonte, fg="blue", borderwidth=2, relief='groove', anchor='e')
        self.instalar_em(name='lb_senha_confirm', row=5, column=1, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar(Entry, name='senha_confirm', borderwidth=2, relief='groove', show='*')
        self.instalar_em(name='senha_confirm', row=5, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW)

        self.criar(Button, name='bt_ok', text="OK", command=self.validar, fg="green", font=self.fonte)
        self.instalar_em(name='bt_ok', row=7, column=1, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar(Button, name='btcancelar', text="CANCELAR", command=self.sair, fg="red", font=self.fonte)
        self.instalar_em(name='btcancelar', row=7, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW)

    def validar(self):
        """Função para validar as informações para cadastrar novo usuário"""
        nome_usuario = self.widgets['usuario'].get().upper()
        perfil_contador = self.widgets['lt_perfil'].curselection()
        senha = self.widgets['senha'].get()
        senha_confirm = self.widgets['senha_confirm'].get()
        erro = False

        # verificar se os campos não estão vazio
        if nome_usuario != '' and len(perfil_contador) > 0 and senha != '' and senha_confirm != '':
            # consulta os usuarios existentes
            usuarios = bd_consultar('usuarios')
            for usuario in usuarios:
                if usuario[1] == nome_usuario:
                    erro = True
            # verificar se não existe o usuario com o mesmo nome
            if not erro:
                # verificar se as senhas são iguais
                if senha == senha_confirm:
                    perfil = bd_consulta_valor_tabela("perfis", "nome", self.item_selecionado(self.widgets['lt_perfil']))[0]
                    perfil_id = perfil[0]
                    perfil_nome = perfil[1]

                    # criptografar a senha
                    hash_senha = bcrypt.hashpw(senha.upper().encode('utf-8'), bcrypt.gensalt())

                    # cadastrar
                    bd_registrar("usuarios", 'inserir_base', [(nome_usuario, 1, perfil_id, hash_senha)])
                    # registrar o evento cadastro usuario
                    bd_registrar('eventos', 'inserir_base', [(get_now(), self.usuario,
                                                              "CADASTRO", f"CADASTRADO O USUARIO - {nome_usuario} - {perfil_nome}")])
                    # fechar a tela
                    self.sair()
                else:
                    tk.messagebox.showerror(title="Erro", message="Senhas não são iguais!")
            else:
                tk.messagebox.showerror(title="Erro", message="Usuário já cadastrado!")
        else:
            tk.messagebox.showerror(title="Erro", message="Falta preencher algum campo!")


class ListarUsuario(TelaBaseFilha):
    def __init__(self, parent, usuario, tela_fechada, nome, widthinc, heightinc):
        super().__init__(parent, usuario, tela_fechada, nome, widthinc, heightinc)
        # ajustar o tamanho da tela largura x altura
        self.posicionar_tela(widht=300, height=250)
        # ajustar os tamanhos das colunas e linhas
        self.ajustar_colunas_linhas(5, 7)

        self.criar(Label, name='titulo', borderwidth=2, relief='groove', text="LISTA DE USUÁRIOS", font=self.fonteTitulo, pady=10)
        self.instalar_em(name='titulo', row=1, column=1, rowspan=1, columnspan=1, sticky=tk.NSEW)

        self.criar(Label, name='subtitulo', borderwidth=2, relief='groove', text="NOME - PERFIL", font=self.fonteSubtitulo, pady=10)
        self.instalar_em(name='subtitulo', row=2, column=1, rowspan=1, columnspan=1, sticky=tk.NSEW)

        self.criar_lista('sb_usuarios', 'lt_usuarios', lista=bd_consulta_lista_usuario(),
                         row1=3, col_lb=1, colspan_lb=1, col_sb=2, colspan_sb=1)

        self.criar(Button, name='bt_sair', text="SAIR", command=self.sair, fg="red", font=self.fonte)
        self.instalar_em(name='bt_sair', row=5, column=1, rowspan=1, columnspan=1, sticky=tk.NSEW)


class AlterarUsuario(TelaBaseFilha):
    def __init__(self, parent, usuario, tela_fechada, nome, widthinc, heightinc):
        super().__init__(parent, usuario, tela_fechada, nome, widthinc, heightinc)
        # ajustar o tamanho da tela
        self.posicionar_tela(widht=450, height=300)
        # ajustar os tamanhos das colunas e linhas
        self.ajustar_colunas_linhas(6, 9)

        self.excluir = BooleanVar()

        self.criar(Label, name='titulo', borderwidth=2, relief='groove', text="ALTERAR DADOS DO USUÁRIO", font=self.fonteTitulo, pady=10)
        self.instalar_em(name='titulo', row=1, column=1, rowspan=1, columnspan=4, sticky=tk.NSEW)

        self.criar(Checkbutton, name='rd_excluir', text="Excluir? ", variable=self.excluir, onvalue=True, offvalue=False,
                   font=self.fonte, fg="blue", borderwidth=2, relief='groove', anchor='e')
        self.instalar_em(name='rd_excluir', row=2, column=1, rowspan=1, columnspan=1, sticky=tk.NSEW)

        self.criar(Label, name='lb_nome_usuario', text="Nome:", font=self.fonte,
                   fg="blue", borderwidth=2, relief='groove', anchor='e')
        self.instalar_em(name='lb_nome_usuario', row=2, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar_lista('sb_usuario', 'lt_usuario', lista=bd_consultar("usuarios"),
                         row1=2, col_lb=3, colspan_lb=1, col_sb=4, colspan_sb=1)

        self.criar(Label, name='lb_perfil_usuario', text="Perfil:", font=self.fonte, fg="blue", borderwidth=2, relief='groove', anchor='e')
        self.instalar_em(name='lb_perfil_usuario', row=3, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar_lista('sb_perfil', 'lt_perfil', lista=bd_consultar("perfis"),
                         row1=3, col_lb=3, colspan_lb=1, col_sb=4, colspan_sb=1)

        self.criar(Label, name='lb_senha', text="Senha:", font=self.fonte, fg="blue", borderwidth=2, relief='groove', anchor='e')
        self.instalar_em(name='lb_senha', row=4, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar(Entry, name='senha', borderwidth=2, relief='groove', show='*')
        self.instalar_em(name='senha', row=4, column=3, rowspan=1, columnspan=1, sticky=tk.NSEW)

        self.criar(Label, name='lb_senha_confirm', text="Confirme a Senha:", font=self.fonte, fg="blue", borderwidth=2, relief='groove', anchor='e')
        self.instalar_em(name='lb_senha_confirm', row=5, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar(Entry, name='senha_confirm', borderwidth=2, relief='groove', show='*')
        self.instalar_em(name='senha_confirm', row=5, column=3, rowspan=1, columnspan=1, sticky=tk.NSEW)

        self.criar(Button, name='bt_ok', text="OK", command=self.validar, fg="green", font=self.fonte)
        self.instalar_em(name='bt_ok', row=7, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar(Button, name='btcancelar', text="CANCELAR", command=self.sair, fg="red", font=self.fonte)
        self.instalar_em(name='btcancelar', row=7, column=3, rowspan=1, columnspan=1, sticky=tk.NSEW)

    def validar(self):
        """Função para validar as informações para atualizar usuário"""
        usuario_nome = self.item_selecionado(self.widgets['lt_usuario'])
        perfil_contador = self.widgets['lt_perfil'].curselection()

        # verifica se foi selecionado o usuario
        if usuario_nome != "":
            # verificar se e exclusão
            if self.excluir.get():
                # excluir o usuário
                bd_excluir_item("usuarios", usuario_nome)
                # registrar o evento cadastro usuario
                bd_registrar('eventos', 'inserir_base', [(get_now(), self.usuario, "CADASTRO", f"EXCLUIDO O USUARIO - {usuario_nome}")])
                # fechar a tela
                self.sair()
            else:
                # verificar se os campos não estão vazio
                senha = self.widgets['senha'].get()
                senha_confirm = self.widgets['senha_confirm'].get()
                if len(perfil_contador) > 0 and senha != '' and senha_confirm != '':
                    # buscar no  perfil
                    perfil = bd_consulta_valor_tabela("perfis", "nome", self.item_selecionado(self.widgets['lt_perfil']))[0]
                    perfil_id = perfil[0]
                    # verificar se as senhas são iguais
                    if senha == senha_confirm:

                        # criptografar a senha
                        hash_senha = bcrypt.hashpw(senha.upper().encode('utf-8'), bcrypt.gensalt())

                        # alterar dados do usuário
                        bd_registrar("usuarios", 'atualizar_usuario', [(1, perfil_id, hash_senha, usuario_nome)])
                        # registrar o evento cadastro usuario
                        bd_registrar('eventos', 'inserir_base', [(get_now(), self.usuario, "CADASTRO", f"ALTERADO O USUARIO - {usuario_nome}")])
                        # fechar a tela
                        self.sair()
                    else:
                        tk.messagebox.showerror(title="Erro", message="Senhas não são iguais!")
                else:
                    tk.messagebox.showerror(title="Erro", message="Faltando o preenchimento/seleção de algum campo!")
        else:
            tk.messagebox.showerror(title="Erro", message="Não selecionado o usuário!")
