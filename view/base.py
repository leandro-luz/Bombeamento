import datetime
from datetime import datetime, timedelta
from tkinter import *

from PIL import Image, ImageTk

from database.bd import *
from utils.conexao import escrever_clp


class TelaBaseFilha(tk.Toplevel):
    tempotela = ""
    nome = ""
    status = True

    def __init__(self, parent, usuario, tela_fechada, nome, widthinc, heightinc):
        super().__init__(parent)
        # ATRIBUTOS
        self.usuario = usuario
        self.tela_fechada = tela_fechada
        self.nome = nome
        self.widthInc = widthinc
        self.heightInc = heightinc
        # consultar valor de ciclo de operações no BD
        valor = bd_consultar("sistema")[0]
        # Colocar o tempo máximo de tela aberta
        self.tempotela = datetime.now() + timedelta(minutes=valor[1]) + timedelta(seconds=5)

        # Lista de ferramentas na tela
        self.widgets = {}

        # FORMATACAO DA TELA
        # Configuração o sair do windows
        self.protocol("WM_DELETE_WINDOW", self.sair)
        # Permissão para redimensionamento pelo usuário
        self.resizable(False, False)
        # Titulo na aba
        self.title('ASGA')
        # Fontes
        self.fonteTitulo = ("Verdana", "14", "bold")
        self.fonteSubtitulo = ("Verdana", "10", "bold")
        self.fonte = ("Verdana", "8", "bold")

        # Tamanho da tela
        # self.geometry('800x600')

        # Carregamento das imagens
        self.img_alarme = ''
        self.img_desabilitado = ''
        self.img_desligado = ''
        self.img_ligado_completo = ''
        self.img_ligado_parcial = ''
        self.img_desconectado = ''
        self.img_local = ''
        self.img_configuracao = ''

    def posicionar_tela(self, widht, height):
        """Função para posicionamento da tela"""
        self.geometry(f'{widht}x{height}+{self.widthInc}+{self.heightInc}')

    def ajustar_colunas_linhas(self, colunas, linhas):
        """Função para ajustar os tamanhos das colunas e linhas"""
        # Padronização dos tamanhos das colunas e linhas
        for i in range(colunas):
            self.columnconfigure(i, weight=1)
        for i in range(linhas):
            self.rowconfigure(i, weight=1)

    def verificar_tela_aberta(self):
        """Função de ciclica de atualização da tela"""
        # Verificar se o tempo de tela aberta expirou
        if datetime.now() > self.tempotela:
            self.sair()

    def criar(self, widget, **kwargs):
        """Função que criar uma ferramenta na tela"""
        w = widget(self, **kwargs)
        name = kwargs.get("name", str(w))
        self.widgets[name] = w
        return name

    def instalar_em(self, name, **kwargs):
        """Função que instala a ferramenta em uma posição na tela"""
        self.widgets[name].grid(**kwargs)

    def criar_com_imagem(self, widget, render, **kwargs):
        """Função que criar uma ferramenta na tela"""
        # criar a ferramenta
        w = widget(self, **kwargs)
        # vincula a imagem na ferramenta
        w.image = render
        # retira o nome da lista de argumentos
        name = kwargs.get("name", str(w))
        # registra o nome da ferramenta
        self.widgets[name] = w
        return name

    def carregar_imagens(self, prefixo, largura, comprimento):
        """Função que carrega as imagens conforme as dimensões repassadas"""
        for imagem in bd_consultar("imagens"):
            setattr(self, prefixo + imagem[1], ImageTk.PhotoImage(Image.open(imagem[2]).resize((largura, comprimento))))

    def alterar_imagem(self, nome, imagem):
        """Altera a imagem de uma ferramenta"""
        self.widgets[nome].image = imagem

    def alterar_parametro(self, name, **kwargs):
        """Função que alterar algum parametro de uma ferramenta"""
        self.widgets[name].config(**kwargs)

    def alterar_valor(self, name, valor):
        """Função que alterar texto de um entrada de valores"""
        self.widgets[name].delete(0, END)
        self.widgets[name].insert(0, valor)

    def operacao(self, nome):
        """Função que realiza as operações MANUALMENTE de ligar/desligar"""
        # busca no BD pelo nome a situação(ligado/desligado) atual do local
        status_atual = bd_consultar_operacao_area(nome)
        # realiza a inversão de situação
        if status_atual[0] == 1:
            status_nome = "DESLIGADO MANUALMENTE"
            clp_saidas = bd_consulta_generica(sql_consultar_clp_areas(nome, 'DESLIGAR'))
        else:
            status_nome = "LIGADO MANUALMENTE"
            clp_saidas = bd_consulta_generica(sql_consultar_clp_areas(nome, 'LIGAR'))

        # Enviar as informações ao clp para ligar ou desligar
        for clp in clp_saidas:
            # realiza a ação de ligar
            if escrever_clp(host=clp[1], port=clp[2], endereco=clp[3]):
                # grava no BD o log do evento
                bd_registrar('eventos', 'inserir_base', [(get_now(), self.usuario, "OPERAÇÃO", f"{status_nome} - {nome}")])

    def alterar_status(self, nome, status):
        """Função que altera as configurações do botão de acordo com o status"""

        if status == 0:
            # Desligado
            self.alterar_imagem("img_" + nome, self.img_desligado)
            self.alterar_parametro("img_" + nome, image=self.img_desligado)
        else:
            # Ligado
            self.alterar_imagem("img_" + nome, self.img_ligado_completo)
            self.alterar_parametro("img_" + nome, image=self.img_ligado_completo)

    def atualizar_bt(self):
        """Função que atualiza todos os botões da tela"""
        # Percorrendo por todas as areas da tela
        posicoes = bd_consultar_config_area(self.nome)
        for posicao in posicoes:
            # Verifica o tipo de operação (manual/automatico)
            if posicao[3] == "MANUAL":
                auto = "active"
            else:
                auto = "disabled"
            # Ativando /desativando o botão da area
            self.alterar_parametro("bt_" + posicao[0], state=auto)
            # Alterando a cor/imagem do botão
            self.alterar_status(posicao[0], posicao[4])

            imagem = self.img_desligado
            # Verifica se está com desconectado
            if posicao[6] == 1:
                imagem = self.img_desconectado
            else:
                # Verifica se está com alarme
                if posicao[5] == 1:
                    imagem = self.img_alarme
                else:
                    # Verifica se está ligado parcialmente
                    if posicao[7] == 1:
                        imagem = self.img_ligado_parcial
                    else:
                        # Verifica se está ligado por completo
                        if posicao[4] == 1:
                            imagem = self.img_ligado_completo

            self.alterar_imagem("img_" + posicao[0], imagem)
            self.alterar_parametro("img_" + posicao[0], image=imagem)

    def sair(self):
        """Fechar a tela """
        # registrar na tela principal o fechamento da tela
        self.tela_fechada()
        # fechar a tela
        self.destroy()

    def criar_lista(self, scrol_name, lt_name, lista, row1, col_lb, colspan_lb, col_sb, colspan_sb, pos_lista=1,
                    tipolista="texto", minimo=1, rowspan_lb=1, rowspan_sb=1):
        """Função para criar lista"""
        self.criar(Scrollbar, name=scrol_name, orient=VERTICAL, width=minimo)
        self.criar(Listbox, name=lt_name, yscrollcommand=self.widgets[scrol_name].set, selectmode=SINGLE, exportselection=0, height=minimo)

        # inclusão dos itens no listbox
        for item in lista:
            if tipolista == "numero":
                self.widgets[lt_name].insert(END, "{:02d}".format(item))
            else:
                self.widgets[lt_name].insert(END, item[pos_lista].upper())

        self.instalar_em(name=lt_name, row=row1, column=col_lb, rowspan=rowspan_lb, columnspan=colspan_lb, sticky=tk.NSEW)
        self.widgets[scrol_name].config(command=self.widgets[lt_name].yview)
        self.instalar_em(name=scrol_name, row=row1, column=col_sb, rowspan=rowspan_sb, columnspan=colspan_sb, sticky=tk.NSEW)

    @staticmethod
    def item_selecionado(lista: [Listbox]):
        """Retorna o valor selecionado de um listbox"""
        for i in lista.curselection():
            return lista.get(i)

    def ajustar_posicao_tela(self):
        """Função que coleta a posição da tela principal"""
        posicoes = self.winfo_geometry().split('+')
        self.widthInc = posicoes[1]
        self.heightInc = posicoes[2]
