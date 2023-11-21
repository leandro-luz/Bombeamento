from datetime import datetime, timedelta
from tkinter import *
from tkinter import messagebox

from database.bd import *
from view.base import *


class CadastrarClp(TelaBaseFilha):
    def __init__(self, parent, usuario, tela_fechada, nome, widthinc, heightinc):
        super().__init__(parent, usuario, tela_fechada, nome, widthinc, heightinc)
        # ajustar o tamanho da tela
        self.posicionar_tela(widht=300, height=200)

        # ajustar os tamanhos das colunas e linhas
        self.ajustar_colunas_linhas(10, 9)

        self.criar(Label, name='titulo', borderwidth=2, relief='groove', text="CADASTRAR CLP", font=self.fonteSubtitulo, pady=10)
        self.instalar_em(name='titulo', row=1, column=1, rowspan=1, columnspan=8, sticky=tk.NSEW)

        # Botões de cadastro, cadastrados, alterações
        self.criar(Label, name='lb_nome_clp', text="Nome:", font=self.fonte, fg="blue", borderwidth=2, relief='groove', anchor='e')
        self.instalar_em(name='lb_nome_clp', row=2, column=1, rowspan=1, columnspan=4, sticky=tk.NSEW)
        self.criar(Entry, name='clp', borderwidth=2, relief='groove')
        self.instalar_em(name='clp', row=2, column=5, rowspan=1, columnspan=4, sticky=tk.NSEW)
        self.widgets['clp'].focus()

        self.criar(Label, name='lb_ip', text="IP:", font=self.fonte, fg="blue", borderwidth=2, relief='groove', anchor='e')
        self.instalar_em(name='lb_ip', row=3, column=1, rowspan=1, columnspan=4, sticky=tk.NSEW)
        self.criar(Entry, name='ip', borderwidth=2, relief='groove')
        self.instalar_em(name='ip', row=3, column=5, rowspan=1, columnspan=4, sticky=tk.NSEW)

        self.criar(Label, name='lb_porta', text="Porta:", font=self.fonte, fg="blue", borderwidth=2, relief='groove', anchor='e')
        self.instalar_em(name='lb_porta', row=4, column=1, rowspan=1, columnspan=4, sticky=tk.NSEW)
        self.criar(Entry, name='porta', borderwidth=2, relief='groove')
        self.instalar_em(name='porta', row=4, column=5, rowspan=1, columnspan=4, sticky=tk.NSEW)

        self.criar(Label, name='lb_id', text="ID:", font=self.fonte, fg="blue", borderwidth=2, relief='groove', anchor='e')
        self.instalar_em(name='lb_id', row=5, column=1, rowspan=1, columnspan=4, sticky=tk.NSEW)
        self.criar(Entry, name='id', borderwidth=2, relief='groove')
        self.instalar_em(name='id', row=5, column=5, rowspan=1, columnspan=4, sticky=tk.NSEW)

        self.criar(Button, name='bt_ok', text="OK", command=self.validar, fg="green", font=self.fonte)
        self.instalar_em(name='bt_ok', row=7, column=1, rowspan=1, columnspan=4, sticky=tk.NSEW)
        self.criar(Button, name='btcancelar', text="CANCELAR", command=self.sair, fg="red", font=self.fonte)
        self.instalar_em(name='btcancelar', row=7, column=5, rowspan=1, columnspan=4, sticky=tk.NSEW)

    def validar(self):
        """Função para validar as informações para cadastrar novo usuário"""
        nome_clp = self.widgets['clp'].get().upper()
        ip = self.widgets['ip'].get().upper()
        porta = self.widgets['porta'].get().upper()
        id_ = self.widgets['id'].get().upper()

        erro = 0

        # verificar se os campos não estão vazio
        if nome_clp != '' and ip != '' and porta != '' and id_ != '':
            # consulta os usuarios existentes
            clps = bd_consultar('clps')
            # percorre por todos os clps cadastrados
            for clp in clps:
                # verifica se já existe o nome do clp
                if clp[1] == nome_clp:
                    erro = 2
                if clp[2] == ip:
                    erro = 3
                if clp[4] == id:
                    erro = 4
            # verifica se o ip tem o minimo de caracteres
            ip_ = ip.split('.')
            if len(ip_) == 4:
                if ip_[0] == '' or ip_[1] == '' or ip_[2] == '' or ip_[3] == '':
                    erro = 5
            else:
                erro = 5
            # verifica se a porta é um número
            if not porta.isnumeric():
                erro = 6
            # verifica se o id é um número
            if not id_.isnumeric():
                erro = 7

            # verificar se não existe o usuario com o mesmo nome
            if erro == 0:
                # cadastrar
                bd_registrar("clps", 'inserir_base', [[nome_clp, ip, porta, id_]])
                # registrar o evento cadastro usuario
                bd_registrar('eventos', 'inserir_base', [(get_now(), self.usuario, "CADASTRO", f"CADASTRADO O CLP - {nome_clp}")])
                # fechar a tela
                self.sair()
        else:
            erro = 1

        if erro > 0:
            if erro == 1:
                tk.messagebox.showerror(title="Erro", message="Algum campo não preenchido!")
            if erro == 2:
                tk.messagebox.showerror(title="Erro", message="Nome para o CLP já cadastrado!")
            if erro == 3:
                tk.messagebox.showerror(title="Erro", message="IP para o CLP já cadastrado!")
            if erro == 4:
                tk.messagebox.showerror(title="Erro", message="ID para o CLP já cadastrado!")
            if erro == 5:
                tk.messagebox.showerror(title="Erro", message="IP não informado corretamente!")
            if erro == 6:
                tk.messagebox.showerror(title="Erro", message="Porta informada não é um número!")
            if erro == 7:
                tk.messagebox.showerror(title="Erro", message="ID informado não é um número!")


class ListarClp(TelaBaseFilha):
    def __init__(self, parent, usuario, tela_fechada, nome, widthinc, heightinc):
        super().__init__(parent, usuario, tela_fechada, nome, widthinc, heightinc)
        # ajustar o tamanho da tela largura x altura
        self.posicionar_tela(widht=300, height=350)
        # ajustar os tamanhos das colunas e linhas
        self.ajustar_colunas_linhas(7, 13)

        self.criar(Label, name='titulo', borderwidth=2, relief='groove', text="LISTA DE CLP", font=self.fonteSubtitulo, pady=10)
        self.instalar_em(name='titulo', row=1, column=1, rowspan=1, columnspan=4, sticky=tk.NSEW)
        self.criar(Label, name='subtitulo', borderwidth=2, relief='groove', text="NOME - IP - PORTA - ID - ATIVO ", font=self.fonteSubtitulo)
        self.instalar_em(name='subtitulo', row=2, column=1, rowspan=1, columnspan=4, sticky=tk.NSEW)

        self.criar_lista('sb_clp', 'lt_clp', lista=bd_consulta_generica(sql_consultar_clps_concatenada), pos_lista=0,
                         row1=3, rowspan_lb=5, col_lb=1, colspan_lb=4, col_sb=5, colspan_sb=1)

        self.criar(Button, name='bt_sair', text="SAIR", command=self.sair, fg="red", font=self.fonte)
        self.instalar_em(name='bt_sair', row=10, column=1, rowspan=1, columnspan=1, sticky=tk.NSEW)


class AlterarClp(TelaBaseFilha):
    def __init__(self, parent, usuario, tela_fechada, nome, widthinc, heightinc):
        super().__init__(parent, usuario, tela_fechada, nome, widthinc, heightinc)
        # ajustar o tamanho da tela
        self.posicionar_tela(widht=400, height=350)
        # ajustar os tamanhos das colunas e linhas
        self.ajustar_colunas_linhas(6, 10)

        self.excluir = BooleanVar()

        self.criar(Label, name='titulo', borderwidth=2, relief='groove', text="ALTERAR DADOS DO CLP", font=self.fonteSubtitulo, pady=10)
        self.instalar_em(name='titulo', row=1, column=1, rowspan=1, columnspan=4, sticky=tk.NSEW)

        self.criar(Checkbutton, name='rd_excluir', text="Excluir? ", variable=self.excluir, onvalue=True, offvalue=False,
                   font=self.fonte, fg="blue", borderwidth=2, relief='groove', anchor='e')
        self.instalar_em(name='rd_excluir', row=2, column=1, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar(Label, name='lb_lista', text="Lista:", font=self.fonte, fg="blue", borderwidth=2, relief='groove', anchor='e')
        self.instalar_em(name='lb_lista', row=2, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar_lista('sb_clp', 'lt_clp', lista=bd_consultar("clps"), row1=2, col_lb=3, colspan_lb=1, col_sb=4, colspan_sb=1)

        self.criar(Label, name='lb_nome_clp', text="Nome:", font=self.fonte, fg="blue", borderwidth=2, relief='groove', anchor='e')
        self.instalar_em(name='lb_nome_clp', row=3, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar(Entry, name='clp', borderwidth=2, relief='groove')
        self.instalar_em(name='clp', row=3, column=3, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.widgets['clp'].focus()

        self.criar(Label, name='lb_ip', text="IP:", font=self.fonte, fg="blue", borderwidth=2, relief='groove', anchor='e')
        self.instalar_em(name='lb_ip', row=4, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar(Entry, name='ip', borderwidth=2, relief='groove')
        self.instalar_em(name='ip', row=4, column=3, rowspan=1, columnspan=1, sticky=tk.NSEW)

        self.criar(Label, name='lb_porta', text="Porta:", font=self.fonte, fg="blue", borderwidth=2, relief='groove', anchor='e')
        self.instalar_em(name='lb_porta', row=5, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar(Entry, name='porta', borderwidth=2, relief='groove')
        self.instalar_em(name='porta', row=5, column=3, rowspan=1, columnspan=1, sticky=tk.NSEW)

        self.criar(Label, name='lb_id', text="ID:", font=self.fonte, fg="blue", borderwidth=2, relief='groove', anchor='e')
        self.instalar_em(name='lb_id', row=6, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar(Entry, name='id', borderwidth=2, relief='groove')
        self.instalar_em(name='id', row=6, column=3, rowspan=1, columnspan=1, sticky=tk.NSEW)

        self.criar(Button, name='bt_ok', text="OK", command=self.validar, fg="green", font=self.fonte)
        self.instalar_em(name='bt_ok', row=8, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar(Button, name='btcancelar', text="CANCELAR", command=self.sair, fg="red", font=self.fonte)
        self.instalar_em(name='btcancelar', row=8, column=3, rowspan=1, columnspan=1, sticky=tk.NSEW)

    def validar(self):
        """Função para validar as informações para atualizar clp"""
        nome_clp_old = self.item_selecionado(self.widgets['lt_clp'])
        nome_clp = self.widgets['clp'].get().upper()
        ip = self.widgets['ip'].get().upper()
        porta = self.widgets['porta'].get().upper()
        id_ = self.widgets['id'].get().upper()

        erro = 0
        # Verifica se foi selecionado o clp
        if nome_clp_old != "":
            # Verificar se e exclusão
            if self.excluir.get():
                # Excluir o usuário
                bd_excluir_item("clps", nome_clp_old)
                # registrar o evento cadastro usuario
                bd_registrar('eventos', 'inserir_base', [(get_now(), self.usuario, "CADASTRO", f"EXCLUIDO O CLP - {nome_clp_old})")])
                # Fechar a tela
                self.sair()
            else:
                # verificar se os campos não estão vazio
                if nome_clp != '' and ip != '' and porta != '' and id_ != '':
                    # Consulta do id do clp
                    clp_old = bd_consulta_valor_tabela("clps", "nome", nome_clp_old)[0]
                    clp_old_id = clp_old[0]

                    # Consulta os usuarios existentes
                    clps = bd_consultar('clps')
                    # Percorre por todos os clps cadastrados
                    for clp in clps:
                        # Verifica os clp diferente do selecionado
                        if clp[0] != clp_old_id:
                            # verifica se já existe o nome do clp
                            if clp[1] == nome_clp:
                                erro = 2
                            if clp[2] == ip:
                                erro = 3
                            if clp[4] == id:
                                erro = 4
                    # Verifica se o ip tem o minimo de caracteres
                    ip_ = ip.split('.')
                    if len(ip_) == 4:
                        if ip_[0] == '' or ip_[1] == '' or ip_[2] == '' or ip_[3] == '':
                            erro = 5
                    else:
                        erro = 5
                    # verifica se a porta é um número
                    if not porta.isnumeric():
                        erro = 6
                    # verifica se o id é um número
                    if not id_.isnumeric():
                        erro = 7

                    # verificar se não existe o usuario com o mesmo nome
                    if erro == 0:
                        # cadastrar
                        bd_registrar("clps", 'atualizar_clp', [[nome_clp, ip, porta, id_, nome_clp_old]])

                        # registrar o evento cadastro usuario
                        bd_registrar('eventos', 'inserir_base', [(get_now(), self.usuario, "CADASTRO", f"ALTERADO OS DADOS DO CLP - {nome_clp}")])
                        # fechar a tela
                        self.sair()
        else:
            erro = 1

        if erro > 0:
            if erro == 1:
                tk.messagebox.showerror(title="Erro", message="Algum campo não preenchido!")
            if erro == 2:
                tk.messagebox.showerror(title="Erro", message="Nome para o CLP já cadastrado!")
            if erro == 3:
                tk.messagebox.showerror(title="Erro", message="IP para o CLP já cadastrado!")
            if erro == 4:
                tk.messagebox.showerror(title="Erro", message="ID para o CLP já cadastrado!")
            if erro == 5:
                tk.messagebox.showerror(title="Erro", message="IP não informado corretamente!")
            if erro == 6:
                tk.messagebox.showerror(title="Erro", message="Porta informada não é um número!")
            if erro == 7:
                tk.messagebox.showerror(title="Erro", message="ID informado não é um número!")


class CadastrarIO(TelaBaseFilha):
    def __init__(self, parent, usuario, tela_fechada, nome, widthinc, heightinc):
        super().__init__(parent, usuario, tela_fechada, nome, widthinc, heightinc)
        # ajustar o tamanho da tela
        self.posicionar_tela(widht=400, height=350)
        # ajustar os tamanhos das colunas e linhas
        self.ajustar_colunas_linhas(10, 10)

        self.criar(Label, name='titulo', borderwidth=2, relief='groove', text="CADASTRAR ENTRADAS E SAÍDAS DO CLP", font=self.fonteSubtitulo, pady=10)
        self.instalar_em(name='titulo', row=1, column=1, rowspan=1, columnspan=9, sticky=tk.NSEW)

        # Botões de cadastro, cadastrados, alterações
        self.criar(Label, name='lb_nome_io', text="Nome:", font=self.fonte, fg="blue", borderwidth=2, relief='groove', anchor='e')
        self.instalar_em(name='lb_nome_io', row=2, column=1, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar(Entry, name='io', borderwidth=2, relief='groove')
        self.instalar_em(name='io', row=2, column=2, rowspan=1, columnspan=8, sticky=tk.NSEW)
        self.widgets['io'].focus()

        self.criar(Label, name='lb_endereco', text="Endereço Memória:", font=self.fonte, fg="blue", borderwidth=2, relief='groove', anchor='e')
        self.instalar_em(name='lb_endereco', row=3, column=1, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar(Entry, name='endereco', borderwidth=2, relief='groove')
        self.instalar_em(name='endereco', row=3, column=2, rowspan=1, columnspan=8, sticky=tk.NSEW)

        self.criar(Label, name='lb_tipo_io', text="Tipo I/O:", font=self.fonte, fg="blue", borderwidth=2, relief='groove', anchor='e')
        self.instalar_em(name='lb_tipo_io', row=4, column=1, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar_lista('sb_tipos', 'lt_tipos', lista=bd_consultar("tipos_io"), row1=4, col_lb=2, colspan_lb=7, col_sb=9, colspan_sb=1)

        self.criar(Label, name='lb_clps', text="CLP:", font=self.fonte, fg="blue", borderwidth=2, relief='groove', anchor='e')
        self.instalar_em(name='lb_clps', row=5, column=1, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar_lista('sb_clps', 'lt_clps', lista=bd_consultar("clps"), row1=5, col_lb=2, colspan_lb=7, col_sb=9, colspan_sb=1)

        self.criar(Label, name='lb_areas', text="ÁREA:", font=self.fonte, fg="blue", borderwidth=2, relief='groove', anchor='e')
        self.instalar_em(name='lb_areas', row=6, column=1, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar_lista('sb_areas', 'lt_areas', lista=bd_consultar("areas"), row1=6, col_lb=2, colspan_lb=7, col_sb=9, colspan_sb=1)

        self.criar(Button, name='bt_ok', text="OK", command=self.validar, fg="green", font=self.fonte)
        self.instalar_em(name='bt_ok', row=8, column=1, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar(Button, name='btcancelar', text="CANCELAR", command=self.sair, fg="red", font=self.fonte)
        self.instalar_em(name='btcancelar', row=8, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW)

    def validar(self):
        """Função para validar as informações para cadastrar nova entrada/saida"""
        nome_io = self.widgets['io'].get().upper()
        nome_endereco = self.widgets['endereco'].get().upper()
        tipo_nome = self.item_selecionado(self.widgets['lt_tipos'])
        clp_nome = self.item_selecionado(self.widgets['lt_clps'])
        area_nome = self.item_selecionado(self.widgets['lt_areas'])
        erro = False

        # verificar se os campos não estão vazio
        if nome_io != '' and nome_endereco != '' and tipo_nome != '' and clp_nome != '' and area_nome != '':
            # consultar o id do clp
            clp = bd_consulta_valor_tabela("clps", "nome", clp_nome)[0]
            clp_id = clp[0]

            # consulta os enderecos existentes
            ios = bd_consulta_generica(sql_consultar_entradas_saidas)
            # verificar se não existe o usuario com o mesmo nome
            for io in ios:
                # verifica se o nome do IO já está cadastrado
                if io[1] == nome_io:
                    erro = 1
                # verifica os registros vinculado ao clp selecionado
                if io[3] == clp_nome:
                    # verifica se o endereço do IO já está cadastrado
                    if io[2] == nome_endereco:
                        erro = 2
            # se não houver repetições
            if erro == 0:
                # consulta o id do tipo_io
                tipo = bd_consulta_valor_tabela("tipos_io", "nome", tipo_nome)[0]
                tipo_id = tipo[0]
                # consulta o id da area
                area = bd_consulta_valor_tabela("areas", "nome", area_nome.lower())[0]
                area_id = area[0]

                # registra uma nova entrada_saida
                bd_registrar("entradas_saidas", 'inserir_base', [(nome_io, nome_endereco, tipo_id, clp_id, area_id)])
                # registrar o evento cadastro usuario
                bd_registrar('eventos', 'inserir_base',
                             [(get_now(), self.usuario, "CADASTRO", f"CADASTRADO A {nome_io} do tipo {tipo_nome} no CLP {clp_nome}")])
                # fechar a tela
                self.sair()
        else:
            erro = 3

        # Mensagens de erros
        if erro > 0:
            if erro == 1:
                tk.messagebox.showerror(title="Erro", message="Este nome já está cadastrado!")
            if erro == 2:
                tk.messagebox.showerror(title="Erro", message="Já cadastrada este endereço de memória para o CLP selecionado!")
            if erro == 3:
                tk.messagebox.showerror(title="Erro", message="Algum campo não preenchido ou selecionado!")


class ListarIO(TelaBaseFilha):
    def __init__(self, parent, usuario, tela_fechada, nome, widthinc, heightinc):
        super().__init__(parent, usuario, tela_fechada, nome, widthinc, heightinc)
        # ajustar o tamanho da tela largura x altura
        self.posicionar_tela(widht=600, height=400)
        # ajustar os tamanhos das colunas e linhas
        self.ajustar_colunas_linhas(10, 15)

        self.criar(Label, name='titulo', borderwidth=2, relief='groove', text="LISTA DE ENTRADAS E SAÍDAS", font=self.fonteSubtitulo, pady=10)
        self.instalar_em(name='titulo', row=1, column=1, rowspan=1, columnspan=7, sticky=tk.NSEW)
        self.criar(Label, name='subtitulo', borderwidth=2, relief='groove', text="NOME - ID - CLP - TIPO - ÁREA", font=self.fonteSubtitulo,
                   anchor='w')
        self.instalar_em(name='subtitulo', row=2, column=1, rowspan=1, columnspan=7, sticky=tk.NSEW)

        self.criar_lista('sb_io', 'lt_io', lista=bd_consulta_generica(sql_consultar_entradas_saidas_concatenada),
                         row1=3, col_lb=1, rowspan_lb=10, rowspan_sb=10, colspan_lb=7, col_sb=8, colspan_sb=1)

        self.criar(Button, name='bt_sair', text="SAIR", command=self.sair, fg="red", font=self.fonte)
        self.instalar_em(name='bt_sair', row=14, column=1, rowspan=1, columnspan=1, sticky=tk.NSEW)


class AlterarIO(TelaBaseFilha):
    def __init__(self, parent, usuario, tela_fechada, nome, widthinc, heightinc):
        super().__init__(parent, usuario, tela_fechada, nome, widthinc, heightinc)
        # ajustar o tamanho da tela
        self.posicionar_tela(widht=600, height=350)
        # ajustar o tempo de tela aberta
        valor = bd_consultar("sistema")[0]
        self.tempotela = datetime.now() + timedelta(minutes=valor[1])
        # ajustar os tamanhos das colunas e linhas
        self.ajustar_colunas_linhas(6, 11)

        self.excluir = BooleanVar()

        self.criar(Label, name='titulo', borderwidth=2, relief='groove', text="ALTERAR DADOS DAS ENTRADAS E SAÍDAS", font=self.fonteSubtitulo,
                   pady=10)
        self.instalar_em(name='titulo', row=1, column=1, rowspan=1, columnspan=4, sticky=tk.NSEW)

        self.criar(Label, name='lb_nome_lista', text="Lista:", font=self.fonte, fg="blue", borderwidth=2, relief='groove', anchor='e')
        self.instalar_em(name='lb_nome_lista', row=2, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW)

        self.criar_lista('sb_io', 'lt_io', lista=bd_consulta_generica(sql_consultar_entradas_saidas), pos_lista=1,
                         row1=2, col_lb=3, colspan_lb=1, col_sb=4, colspan_sb=1)
        self.criar(Checkbutton, name='rd_excluir', text="Excluir? ", variable=self.excluir, onvalue=True, offvalue=False,
                   font=self.fonte, fg="blue", borderwidth=2, relief='groove', anchor='e')
        self.instalar_em(name='rd_excluir', row=2, column=1, rowspan=1, columnspan=1, sticky=tk.NSEW)

        self.criar(Label, name='lb_nome_io', text="Nome:", font=self.fonte, fg="blue", borderwidth=2, relief='groove', anchor='e')
        self.instalar_em(name='lb_nome_io', row=3, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar(Entry, name='io', borderwidth=2, relief='groove')
        self.instalar_em(name='io', row=3, column=3, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.widgets['io'].focus()

        self.criar(Label, name='lb_endereco', text="Endereço Memória:", font=self.fonte, fg="blue", borderwidth=2, relief='groove', anchor='e')
        self.instalar_em(name='lb_endereco', row=4, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar(Entry, name='endereco', borderwidth=2, relief='groove')
        self.instalar_em(name='endereco', row=4, column=3, rowspan=1, columnspan=1, sticky=tk.NSEW)

        self.criar(Label, name='lb_tipo_io', text="Tipo I/O:", font=self.fonte, fg="blue", borderwidth=2, relief='groove', anchor='e')
        self.instalar_em(name='lb_tipo_io', row=5, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar_lista('sb_tipos', 'lt_tipos', lista=bd_consultar("tipos_io"), row1=5, col_lb=3, colspan_lb=1, col_sb=4, colspan_sb=1)

        self.criar(Label, name='lb_clps', text="CLP:", font=self.fonte, fg="blue", borderwidth=2, relief='groove', anchor='e')
        self.instalar_em(name='lb_clps', row=6, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar_lista('sb_clps', 'lt_clps', lista=bd_consultar("clps"), row1=6, col_lb=3, colspan_lb=1, col_sb=4, colspan_sb=1)

        self.criar(Label, name='lb_areas', text="ÁREA:", font=self.fonte, fg="blue", borderwidth=2, relief='groove', anchor='e')
        self.instalar_em(name='lb_areas', row=7, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar_lista('sb_areas', 'lt_areas', lista=bd_consultar("areas"), row1=7, col_lb=3, colspan_lb=1, col_sb=4, colspan_sb=1)

        self.criar(Button, name='bt_ok', text="OK", command=self.validar, fg="green", font=self.fonte)
        self.instalar_em(name='bt_ok', row=9, column=2, rowspan=1, columnspan=1, sticky=tk.NSEW)
        self.criar(Button, name='btcancelar', text="CANCELAR", command=self.sair, fg="red", font=self.fonte)
        self.instalar_em(name='btcancelar', row=9, column=3, rowspan=1, columnspan=1, sticky=tk.NSEW)

    def validar(self):
        """Função para validar as informações para atualizar clp"""
        io_nome_old = self.item_selecionado(self.widgets['lt_io'])
        nome_io_novo = self.widgets['io'].get().upper()
        nome_endereco_novo = self.widgets['endereco'].get().upper()
        tipo_nome_novo = self.item_selecionado(self.widgets['lt_tipos'])
        clp_nome_novo = self.item_selecionado(self.widgets['lt_clps'])
        area_nome_novo = self.item_selecionado(self.widgets['lt_areas'])

        erro = 0
        # verifica se foi selecionado o clp
        if io_nome_old != '':
            # verificar se e exclusão
            if self.excluir.get():
                # excluir o usuário
                bd_excluir_item("entradas_saidas", io_nome_old)
                # registrar o evento cadastro usuario
                bd_registrar('eventos', 'inserir_base', [(get_now(), self.usuario, "CADASTRO", f"EXCLUIDO A ENTRADA/SAÍDA - {io_nome_old})")])
                # fechar a tela
                self.sair()
            else:
                # verificar se os campos não estão vazio
                if nome_io_novo != '' and nome_endereco_novo != '' and tipo_nome_novo != '' and clp_nome_novo != '' and area_nome_novo != '':
                    # consultar o id do clp
                    clp = bd_consulta_valor_tabela("clps", "nome", clp_nome_novo)[0]
                    clp_id = clp[0]
                    # consultar o id do io
                    io_old = bd_consulta_valor_tabela("entradas_saidas", "nome", io_nome_old)[0]
                    io_old_id = io_old[0]

                    # consulta os enderecos existentes
                    ios = bd_consulta_generica(sql_consultar_entradas_saidas)
                    # verificar se não existe o usuario com o mesmo nome
                    for io in ios:
                        # percorre por todos os outros ios cadastrados
                        if io[0] != io_old_id:
                            # verifica se não existe nome igual
                            if io[1] == nome_io_novo:
                                erro = 2
                            # verifica os registros vinculado ao clp selecionado
                            if io[2] == clp_nome_novo:
                                # verifica se o endereço do IO já está cadastrado
                                if io[1] == nome_endereco_novo:
                                    erro = 3

                    # se não houver erro
                    if erro == 0:
                        # alterar
                        tipo = bd_consulta_valor_tabela("tipos_io", "nome", self.item_selecionado(self.widgets['lt_tipos']))[0]
                        tipo_id = tipo[0]
                        # consulta o id da area
                        area = bd_consulta_valor_tabela("areas", "nome", area_nome_novo.lower())[0]
                        area_id = area[0]
                        # alterar a registro do io
                        bd_registrar("entradas_saidas", 'atualizar_entradas_saidas',
                                     [(nome_io_novo, nome_endereco_novo, tipo_id, clp_id, area_id, io_nome_old)])
                        # registrar o evento cadastro usuario
                        bd_registrar('eventos', 'inserir_base',
                                     [(get_now(), self.usuario, "CADASTRO",
                                       f"ALTERADO OS DADOS DA ENTRADA_SAIDA {nome_io_novo} do tipo {tipo_nome_novo} no CLP {clp_nome_novo}")])
                        # fechar a tela
                        self.sair()
        else:
            erro = 1

        # Mensagens de erro
        if erro > 0:
            if erro == 1:
                tk.messagebox.showerror(title="Erro", message="Não selecionado o usuário!")
            if erro == 2:
                tk.messagebox.showerror(title="Erro", message="Já existe este nome cadastrado!")
            if erro == 3:
                tk.messagebox.showerror(title="Erro", message="Já cadastrada este endereço de memória para o CLP selecionado!")
