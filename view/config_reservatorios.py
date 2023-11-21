from tkinter import *
from tkinter import messagebox

from database.bd import *


class ConfigReservatorio(tk.Toplevel):
    """Classe para montagem da tela principal"""

    def __init__(self, parent, usuario, alterar_limites, nome_reservatorio, widthinc, heightinc):
        super().__init__(parent)
        self.carregar_variaveis(usuario, alterar_limites, nome_reservatorio, widthinc, heightinc)
        self.montagem_tela()
        self.carregar_valores()

    def carregar_variaveis(self, usuario, alterar_limites, nome_reservatorio, widthinc, heightinc):
        self.title('CONFIGURAÇÃO NÍVEIS')
        # Configuração o sair do windows
        self.protocol("WM_DELETE_WINDOW", self.sair)
        self.nome = nome_reservatorio
        self.alterar_limites = alterar_limites
        self.usuario = usuario
        self.bloquear = 0
        self.resizable(False, False)

        # Lista de ferramentas na tela
        self.__widgets = {}

        self.widthInc = widthinc
        self.heightInc = heightinc

        self.widthTela = 380
        self.heightTela = 250
        self.fontetitulo = ("Verdana", "14", "bold")
        self.fonteSubtitulo = ("Verdana", "10")
        self.fonte = ("Verdana", "12")
        self.widthEntry = 7

        self.posicionar_tela(self.widthTela, self.heightTela)

    def montagem_tela(self):
        # dimensões do canvas igual ao da tela
        canvas = Canvas(self, width=self.widthTela, height=self.heightTela)
        canvas.pack()
        # Titulo
        canvas.create_text(60, 20, text=self.nome.upper(), font=self.fontetitulo, anchor="w")
        # subtitulo min e max
        canvas.create_text(200, 60, text="Mínimo(%)", anchor="w", font=self.fonteSubtitulo)
        canvas.create_text(280, 60, text="Máximo(%)", anchor="w", font=self.fonteSubtitulo)

        canvas.create_text(20, 90, text="Níveis de Alarme", anchor="w", font=self.fonte)
        self.criar(Entry, name='alarme_minimo', width=self.widthEntry, font=self.fonte)
        self.instalar_em(name='alarme_minimo', x=200, y=80)
        self.criar(Entry, name='alarme_maximo', width=self.widthEntry, font=self.fonte)
        self.instalar_em(name='alarme_maximo', x=280, y=80)

        canvas.create_text(20, 130, text="Níveis de Operação", anchor="w", font=self.fonte)
        self.criar(Entry, name='operacao_minimo', width=self.widthEntry, font=self.fonte)
        self.instalar_em(name='operacao_minimo', x=200, y=120)
        self.criar(Entry, name='operacao_maximo', width=self.widthEntry, font=self.fonte)
        self.instalar_em(name='operacao_maximo', x=280, y=120)

        canvas.create_text(20, 170, text="Offset", anchor="w", font=self.fonte)
        self.criar(Entry, name='offset_minimo', width=self.widthEntry, font=self.fonte)
        self.instalar_em(name='offset_minimo', x=200, y=160)
        self.criar(Entry, name='offset_maximo', width=self.widthEntry, font=self.fonte)
        self.instalar_em(name='offset_maximo', x=280, y=160)

        self.criar(Button, name='bt_bloqueio', text="BLOQUEAR", width=12, height=1, font=self.fonteSubtitulo, fg='blue',
                   command=self.bloquear_reservatorio)
        self.instalar_em(name='bt_bloqueio', x=20, y=200)
        self.criar(Button, name='bt_atualizar', text="ATUALIZAR", width=12, height=1, font=self.fonteSubtitulo, bg='green', command=self.validar)
        self.instalar_em(name='bt_atualizar', x=135, y=200)
        self.criar(Button, name='bt_cancelar', text="CANCELAR", width=12, height=1, font=self.fonteSubtitulo, bg='red', command=self.sair)
        self.instalar_em(name='bt_cancelar', x=250, y=200)

    def bloquear_reservatorio(self):
        valor = 0
        texto = 'DESBLOQUEADO'
        if self.bloquear == 0:
            valor = 1
            texto = 'BLOQUEADO'

        # registrar o bloqueio ou o desbloqueio do reservatório
        bd_registrar("reservatorios", 'atualizar_bloqueio', [[valor, self.nome]])
        # registrar o evento cadastro usuario
        bd_registrar('eventos', 'inserir_base', [(get_now(), self.usuario, "OPERAÇÃO", f"O {self.nome} foi {texto}")])
        self.sair()

    def validar(self):
        # coleta os valores
        al_min = self.__widgets['alarme_minimo'].get()
        al_max = self.__widgets['alarme_maximo'].get()
        op_min = self.__widgets['operacao_minimo'].get()
        op_max = self.__widgets['operacao_maximo'].get()
        off_min = self.__widgets['offset_minimo'].get()
        off_max = self.__widgets['offset_maximo'].get()

        # verificar se os campos estão preenchidos
        # verificar se os campos não númericos
        verificacao = self.verificar_valor(al_min, True)
        verificacao += self.verificar_valor(al_max, True)
        verificacao += self.verificar_valor(op_min, True)
        verificacao += self.verificar_valor(op_max, True)
        verificacao += self.verificar_valor(off_min, False)
        verificacao += self.verificar_valor(off_max, False)
        verificacao += self.verificar_valores(op_min, op_max, al_min, al_max)

        # salvar
        if verificacao == 0:
            # cadastrar
            bd_registrar("reservatorios", 'atualizar_niveis', [[op_min, op_max, al_min, al_max, off_min, off_max, self.nome]])

            # registrar o evento cadastro usuario
            bd_registrar('eventos', 'inserir_base',
                         [(get_now(), self.usuario, "CONFIGURACAO",
                           f"Alterado os valores -Al_min:{al_min}-Al_max:{al_max}-{op_min}-{op_max}-{off_min}-{off_max}")])
            self.alterar_limites()
            self.sair()
        else:
            tk.messagebox.showerror(title="Erro", message="Valor não preenchido ou fora dos limites!")

    def verificar_valor(self, valor, limite_negativo):
        resultado = 1
        if valor:
            if self.converterNumero(valor):
                valor = int(valor)
                if valor <= 100:
                    if limite_negativo:
                        if valor >= 0:
                            resultado = 0
                    else:
                        resultado = 0
        return resultado

    def verificar_valores(self, op_min, op_max, al_min, al_max):
        resultado = 0
        if op_min >= op_max or al_min >= al_max:
            resultado = 1
        return resultado

    @staticmethod
    def converterNumero(valor):
        try:
            int(valor)
            return True
        except:
            return False

    def carregar_valores(self):
        # carregar valores do reservatorio
        valores = bd_consulta_valor_tabela('reservatorios', 'nome', self.nome)[0]
        self.alterar_valor("operacao_minimo", valores[2])
        self.alterar_valor("operacao_maximo", valores[3])
        self.alterar_valor("alarme_minimo", valores[5])
        self.alterar_valor("alarme_maximo", valores[6])
        self.alterar_valor("offset_minimo", valores[7])
        self.alterar_valor("offset_maximo", valores[8])
        self.bloquear = valores[10]
        if self.bloquear == 0:
            texto = "DESBLOQUEAR"
            fg = 'blue'
        else:
            texto = "BLOQUEAR"
            fg = 'red'
        self.alterar_parametro("bt_bloqueio", text=texto, fg=fg)

    def sair(self):
        """Fechar a tela"""
        self.destroy()

    def criar(self, widget, **kwargs):
        """Função que criar uma ferramenta na tela"""
        w = widget(self, **kwargs)
        name = kwargs.get("name", str(w))
        self.__widgets[name] = w
        return name

    def instalar_em(self, name, **kwargs):
        """Função que instala a ferramenta em uma posição na tela"""
        self.__widgets[name].place(**kwargs)

    def alterar_parametro(self, name, **kwargs):
        """Função que alterar algum parametro de uma ferramenta"""
        self.__widgets[name].config(**kwargs)

    def alterar_valor(self, name, valor):
        """Função que alterar texto de um entrada de valores"""
        self.__widgets[name].delete(0, END)
        self.__widgets[name].insert(0, valor)

    def posicionar_tela(self, widht, height):
        """Função para posicionamento da tela"""
        self.geometry(f'{widht}x{height}+{self.widthInc}+{self.heightInc}')
