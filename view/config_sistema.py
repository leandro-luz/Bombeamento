from tkinter import *
from tkinter import messagebox

from database.bd import *
from view.base import *


class AlterarConfigSistema(TelaBaseFilha):
    def __init__(self, parent, usuario, tela_fechada, logout_user, nome, widthinc, heightinc):
        super().__init__(parent, usuario, tela_fechada, nome, widthinc, heightinc)
        self.logout_user = logout_user

        # ajustar o tamanho da tela
        self.posicionar_tela(widht=450, height=300)
        # ajustar os tamanhos das colunas e linhas
        self.ajustar_colunas_linhas(10, 10)

        self.excluir = BooleanVar()

        self.criar(Label, name='titulo', borderwidth=2, relief='groove', text="CONFIGURAÇÕES DO CONTROLE DE ILUMINAÇÃO", font=self.fonteSubtitulo,
                   pady=10)
        self.instalar_em(name='titulo', row=1, column=1, rowspan=1, columnspan=9, sticky=tk.NSEW)

        self.criar(Label, name='subtitulo', borderwidth=2, relief='groove', text="AJUSTE NOS TEMPORIZADORES", font=self.fonte, pady=10)
        self.instalar_em(name='subtitulo', row=2, column=1, rowspan=1, columnspan=9, sticky=tk.NSEW)

        self.criar(Label, name='lb_tl_aberta', text="Tempo tela aberta (minutos):", font=self.fonte, fg="blue", borderwidth=2, relief='groove',
                   anchor='e')
        self.instalar_em(name='lb_tl_aberta', row=3, column=1, rowspan=1, columnspan=3, sticky=tk.NSEW)
        self.criar(Entry, name='tela_aberta', borderwidth=2, relief='groove')
        self.instalar_em(name='tela_aberta', row=3, column=4, rowspan=1, columnspan=2, sticky=tk.NSEW)
        self.widgets['tela_aberta'].focus()

        self.criar(Label, name='lb_login', text="Tempo de login ativo (minutos):", font=self.fonte, fg="blue", borderwidth=2, relief='groove',
                   anchor='e')
        self.instalar_em(name='lb_login', row=4, column=1, rowspan=1, columnspan=3, sticky=tk.NSEW)
        self.criar(Entry, name='login', borderwidth=2, relief='groove')
        self.instalar_em(name='login', row=4, column=4, rowspan=1, columnspan=2, sticky=tk.NSEW)

        self.criar(Label, name='lb_atualizacao', text="Tempo de ciclo para atualizações (segundos):", font=self.fonte, fg="blue", borderwidth=2,
                   relief='groove', anchor='e')
        self.instalar_em(name='lb_atualizacao', row=5, column=1, rowspan=1, columnspan=3, sticky=tk.NSEW)
        self.criar(Entry, name='atualizacao', borderwidth=2, relief='groove')
        self.instalar_em(name='atualizacao', row=5, column=4, rowspan=1, columnspan=2, sticky=tk.NSEW)

        self.criar(Label, name='lb_operacao', text="Tempo de ciclo para operações (minutos):", font=self.fonte, fg="blue", borderwidth=2,
                   relief='groove', anchor='e')
        self.instalar_em(name='lb_operacao', row=6, column=1, rowspan=1, columnspan=3, sticky=tk.NSEW)
        self.criar(Entry, name='operacao', borderwidth=2, relief='groove')
        self.instalar_em(name='operacao', row=6, column=4, rowspan=1, columnspan=2, sticky=tk.NSEW)

        self.criar(Button, name='bt_ok', text="OK", command=self.validar, fg="green", font=self.fonte)
        self.instalar_em(name='bt_ok', row=8, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar(Button, name='btcancelar', text="CANCELAR", command=self.sair, fg="red", font=self.fonte)
        self.instalar_em(name='btcancelar', row=8, column=3, rowspan=1, columnspan=1, sticky=tk.NSEW)

        self.preencher_valores()

    def preencher_valores(self):
        """Função local de preencher os valores da tela ao inicializar"""
        valor = bd_consultar("sistema")[0]
        self.alterar_valor('tela_aberta', valor[1])
        self.alterar_valor('login', valor[2])
        self.alterar_valor('atualizacao', valor[3])
        self.alterar_valor('operacao', valor[4])

    def validar(self):
        """Função para validar as informações para atualizar clp"""

        tela_aberta = self.widgets['tela_aberta'].get().upper()
        login = self.widgets['login'].get().upper()
        atualizacao = self.widgets['atualizacao'].get().upper()
        operacao = self.widgets['operacao'].get().upper()

        erro = 0
        # Verifica se foi selecionado o clp
        if tela_aberta != "" and login != "" and atualizacao != "" and operacao != "":
            # verifica se os campos são númericos

            if not tela_aberta.isnumeric():
                erro = 2
            if not login.isnumeric():
                erro = 3
            if not atualizacao.isnumeric():
                erro = 4
            if not operacao.isnumeric():
                erro = 5

            # se não houver erro
            if erro == 0:
                # cadastrar
                bd_registrar("sistema", 'atualizar_base', [[tela_aberta, login, atualizacao, operacao]])

                # registrar o evento cadastro usuario
                bd_registrar('eventos', 'inserir_base',
                             [(get_now(), self.usuario, "SETUP", f"ALTERADO - "
                                                                 f"Tela_Aberta:{tela_aberta}, Tempo_Login:{login}, "
                                                                 f"Tempo_Atualização:{atualizacao}, Tempo_Operação:{operacao}")])

                # fechar a tela
                self.logout_user("AUTOMATICAMENTE")
        else:
            erro = 1

        if erro > 0:
            if erro == 1:
                tk.messagebox.showerror(title="Erro", message="Algum campo não preenchido!")
            if erro == 2:
                tk.messagebox.showerror(title="Erro", message="Tempo informado de TELA ABERTA não é um número")
            if erro == 3:
                tk.messagebox.showerror(title="Erro", message="Tempo informado de LOGIN ATIVO não é um número")
            if erro == 4:
                tk.messagebox.showerror(title="Erro", message="Tempo informado de CILO DE ATUALIZAÇÃO não é um número")
            if erro == 5:
                tk.messagebox.showerror(title="Erro", message="Tempo informado de CICLO DE OPERAÇÃO não é um número")
