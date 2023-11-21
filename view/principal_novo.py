import time
import uuid
from datetime import datetime, timedelta
from threading import *
from tkinter import *
from tkinter import messagebox

from PIL import Image, ImageTk

from database.bd import *
from database.sql import sql_consultar_clp_areas
from utils.conexao import escrever_clp
from utils.times import get_now
from view.comunicacao import CadastrarClp, AlterarClp, ListarClp, CadastrarIO, ListarIO, AlterarIO
from view.config_reservatorios import ConfigReservatorio
from view.config_sistema import AlterarConfigSistema
from view.historico import Historico
from view.login import Login
from view.usuario import CadastrarUsuario, AlterarUsuario, ListarUsuario

# Variavel global
threads = True


class TelaVazia:
    """Classe de tela vazia"""
    status = False
    nome = 'telavazia'

    def verificar_tela_aberta(self):
        pass

    def sair(self):
        pass


class TelaPrincipal(tk.Tk):
    """Classe para montagem da tela principal"""

    def __init__(self):
        super().__init__()
        self.carregar_variaveis()
        self.montagem_tela()
        self.alterar_limites()
        self.ativar_desativar_botoes(ativar=False)

        # Registro de inicio do sistema
        bd_registrar('eventos', 'inserir_base', [(get_now(), "Null", "ACESSO", "Sistema de Controle e Monitoramente de Bombeamento INICIADO")])

    def montagem_tela(self):
        """Função que mosta a tela principal"""
        # dimensões do canvas igual ao da tela
        self.criar(Canvas, name='canvas', width=self.widthTela, height=self.heightTela)
        self.instalar_em(name="canvas", x=0, y=0)

        # Titulo
        self.criar_texto("canvas", 650, -50, "CONTROLE E MONITORAMENTO - BOMBEAMENTO", self.fontetitulo, "c")

        # Versão
        self.criar(Label, name='versao', text="ELT.001 - 01/11/2023")
        self.instalar_em(name="versao", x=10, y=1)
        # Total de Falhas
        self.criar(Label, name='total_falhas', text=self.falhas, anchor="w")
        self.instalar_em(name='total_falhas', x=10, y=20)
        # Data-hora
        self.criar(Label, name='time', text="dd/mm/yyyy - hh/mm/ssss")
        self.instalar_em(name="time", x=10, y=40)
        # Usuário
        self.criar(Label, name='usuario_nome', text=self.usuario, font=self.fonte, anchor="w")
        self.instalar_em(name='usuario_nome', x=10, y=60)
        # Botão Login
        self.criar(Button, name='bt_login', text="LOGIN", width=13, height=1, command=lambda: self.login_user("login"))
        self.instalar_em(name='bt_login', x=1200 + self.off_x, y=10)

        # Linhas
        self.criar_linha("canvas", "l1", 90, 25, 530, 25, 'gray', 10)
        self.criar_linha("canvas", "l2", 530, 20, 530, 50, 'gray', 10)
        self.criar_linha("canvas", "l3", 425, 20, 425, 50, 'gray', 10)
        self.criar_linha("canvas", "l4", 305, 20, 305, 50, 'gray', 10)
        self.criar_linha("canvas", "l5", 200, 20, 200, 50, 'gray', 10)

        self.criar_linha("canvas", "l6", 95, 20, 95, 450, 'gray', 10)
        self.criar_linha("canvas", "l7", 90, 425, 290, 425, 'gray', 10)
        self.criar_linha("canvas", "l8", 195, 420, 195, 450, 'gray', 10)
        self.criar_linha("canvas", "l9", 295, 420, 295, 450, 'gray', 10)

        self.criar_linha("canvas", "l10", 775, 425, 1080, 425, 'gray', 10)
        self.criar_linha("canvas", "l11", 875, 425, 875, 480, 'gray', 10)
        self.criar_linha("canvas", "l12", 975, 425, 975, 480, 'gray', 10)
        self.criar_linha("canvas", "l13", 1075, 420, 1075, 480, 'gray', 10)
        self.criar_linha("canvas", "l14", 870, 475, 900, 475, 'gray', 10)
        self.criar_linha("canvas", "l15", 970, 475, 1000, 475, 'gray', 10)
        self.criar_linha("canvas", "l16", 1070, 475, 1100, 475, 'gray', 10)

        self.criar_linha("canvas", "l17", 875, 20, 875, 405, 'gray35', 10)
        self.criar_linha("canvas", "l18", 870, 25, 1005, 25, 'gray35', 10)
        self.criar_linha("canvas", "l19", 1000, 20, 1000, 50, 'gray35', 10)
        self.criar_linha("canvas", "l20", 910, 400, 910, 450, 'gray35', 10)
        self.criar_linha("canvas", "l21", 1010, 400, 1010, 450, 'gray35', 10)
        self.criar_linha("canvas", "l22", 1110, 395, 1110, 450, 'gray35', 10)
        self.criar_linha("canvas", "l23", 870, 400, 1115, 400, 'gray35', 10)

        # # Reservatório
        self.criar_retangulo("canvas", 149, 49, 250, 250, '#249794', 'black')
        self.criar_retangulo("canvas", 254, 49, 355, 250, '#249794', 'black')
        self.criar_retangulo("canvas", 374, 49, 475, 250, '#249794', 'red')
        self.criar_retangulo("canvas", 479, 49, 580, 250, '#249794', 'red')
        self.criar_retangulo("canvas", 924, 49, 1075, 250, '#249794', 'black')
        self.criar_retangulo("canvas", 649, 249, 800, 450, '#249794', 'black')

        # Textos
        self.criar_texto("canvas", 150, 255, "RSV-I", self.fonte, "nw")
        self.criar_texto("canvas", 255, 255, "RSV-II", self.fonte, "nw")
        self.criar_texto("canvas", 375, 255, "RSV-III", self.fonte, "nw")
        self.criar_texto("canvas", 480, 255, "RSV-IV", self.fonte, "nw")
        self.criar_texto("canvas", 650, 455, "RSV-VI", self.fonte, "nw")
        self.criar_texto("canvas", 925, 255, "RSV-V", self.fonte, "nw")

        # nível em percentual de cada reservatório
        self.criar(Label, name='nivel_percentil_reservatorio_1', text="5%", font=self.fontenivel, bg='cadetblue', anchor='w')
        self.instalar_em(name="nivel_percentil_reservatorio_1", x=180 + self.off_x, y=280 + self.off_y)
        self.criar_com_imagem(Button, name='bt_config_reservatorio_1', render=self.img3_configuracao, image=self.img3_configuracao,
                              command=lambda: self.configuracao_reservatorio("reservatorio_1"))
        self.instalar_em(name='bt_config_reservatorio_1', x=150 + self.off_x, y=280 + self.off_y)

        self.criar(Label, name='nivel_percentil_reservatorio_2', text="25%", font=self.fontenivel, bg='cadetblue', anchor='w')
        self.instalar_em(name="nivel_percentil_reservatorio_2", x=280 + self.off_x, y=280 + self.off_y)
        self.criar_com_imagem(Button, name='bt_config_reservatorio_2', render=self.img3_configuracao, image=self.img3_configuracao,
                              command=lambda: self.configuracao_reservatorio("reservatorio_2"))
        self.instalar_em(name='bt_config_reservatorio_2', x=250 + self.off_x, y=280 + self.off_y)

        self.criar(Label, name='nivel_percentil_reservatorio_3', text="25%", font=self.fontenivel, bg='cadetblue', anchor='w')
        self.instalar_em(name="nivel_percentil_reservatorio_3", x=405 + self.off_x, y=280 + self.off_y)
        self.criar_com_imagem(Button, name='bt_config_reservatorio_3', render=self.img3_configuracao, image=self.img3_configuracao,
                              command=lambda: self.configuracao_reservatorio("reservatorio_3"))
        self.instalar_em(name='bt_config_reservatorio_3', x=375 + self.off_x, y=280 + self.off_y)

        self.criar(Label, name='nivel_percentil_reservatorio_4', text="25%", font=self.fontenivel, bg='cadetblue', anchor='w')
        self.instalar_em(name="nivel_percentil_reservatorio_4", x=510 + self.off_x, y=280 + self.off_y)
        self.criar_com_imagem(Button, name='bt_config_reservatorio_4', render=self.img3_configuracao, image=self.img3_configuracao,
                              command=lambda: self.configuracao_reservatorio("reservatorio_4"))
        self.instalar_em(name='bt_config_reservatorio_4', x=480 + self.off_x, y=280 + self.off_y)

        self.criar(Label, name='nivel_percentil_reservatorio_5', text="50%", font=self.fontenivel, bg='cadetblue')
        self.instalar_em(name="nivel_percentil_reservatorio_5", x=955 + self.off_x, y=280 + self.off_y)
        self.criar_com_imagem(Button, name='bt_config_reservatorio_5', render=self.img3_configuracao, image=self.img3_configuracao,
                              command=lambda: self.configuracao_reservatorio("reservatorio_5"))
        self.instalar_em(name='bt_config_reservatorio_5', x=925 + self.off_x, y=280 + self.off_y)

        self.criar(Label, name='nivel_percentil_reservatorio_6', text="100%", font=self.fontenivel, bg='cadetblue')
        self.instalar_em(name="nivel_percentil_reservatorio_6", x=680 + self.off_x, y=480 + self.off_y)
        self.criar_com_imagem(Button, name='bt_config_reservatorio_6', render=self.img3_configuracao, image=self.img3_configuracao,
                              command=lambda: self.configuracao_reservatorio("reservatorio_6"))
        self.instalar_em(name='bt_config_reservatorio_6', x=650 + self.off_x, y=480 + self.off_y)

        self.criar(Frame, name="nivel_reservatorio_1", width=100, height=200 * 0.95, bg='gray')
        self.instalar_em(name="nivel_reservatorio_1", x=150 + self.off_x, y=50 + self.off_y)
        self.criar(Frame, name="nivel_reservatorio_2", width=100, height=200 * 0.75, bg='gray')
        self.instalar_em(name="nivel_reservatorio_2", x=255 + self.off_x, y=50 + self.off_y)
        self.criar(Frame, name="nivel_reservatorio_3", width=100, height=200 * 0.75, bg='gray')
        self.instalar_em(name="nivel_reservatorio_3", x=375 + self.off_x, y=50 + self.off_y)
        self.criar(Frame, name="nivel_reservatorio_4", width=100, height=200 * 0.75, bg='gray')
        self.instalar_em(name="nivel_reservatorio_4", x=480 + self.off_x, y=50 + self.off_y)
        self.criar(Frame, name="nivel_reservatorio_5", width=150, height=200 * 0.50, bg='gray')
        self.instalar_em(name="nivel_reservatorio_5", x=925 + self.off_x, y=50 + self.off_y)
        self.criar(Frame, name="nivel_reservatorio_6", width=150, height=200 * 0.25, bg='gray')
        self.instalar_em(name="nivel_reservatorio_6", x=650 + self.off_x, y=250 + self.off_y)

        self.criar_com_imagem(Label, name='img_reservatorio_1', render=self.img_reservatorio_bloqueado, image=self.img_reservatorio_bloqueado)
        self.instalar_em(name='img_reservatorio_1', x=150 + self.off_x, y=50 + self.off_y)
        self.criar_com_imagem(Label, name='img_reservatorio_2', render=self.img_reservatorio_bloqueado, image=self.img_reservatorio_bloqueado)
        self.instalar_em(name='img_reservatorio_2', x=255 + self.off_x, y=50 + self.off_y)
        self.criar_com_imagem(Label, name='img_reservatorio_3', render=self.img_reservatorio_bloqueado, image=self.img_reservatorio_bloqueado)
        self.instalar_em(name='img_reservatorio_3', x=375 + self.off_x, y=50 + self.off_y)
        self.criar_com_imagem(Label, name='img_reservatorio_4', render=self.img_reservatorio_bloqueado, image=self.img_reservatorio_bloqueado)
        self.instalar_em(name='img_reservatorio_4', x=480 + self.off_x, y=50 + self.off_y)
        self.criar_com_imagem(Label, name='img_reservatorio_5', render=self.img_reservatorio_bloqueado, image=self.img_reservatorio_bloqueado)
        self.instalar_em(name='img_reservatorio_5', x=925 + self.off_x, y=50 + self.off_y)
        self.criar_com_imagem(Label, name='img_reservatorio_6', render=self.img_reservatorio_bloqueado, image=self.img_reservatorio_bloqueado)
        self.instalar_em(name='img_reservatorio_6', x=650 + self.off_x, y=250 + self.off_y)

        self.criar_com_imagem(Label, name='img_poco_cut', render=self.img_poco_desligado, image=self.img_poco_desligado, borderwidth=2, relief='flat')
        self.instalar_em(name='img_poco_cut', x=50 + self.off_x, y=450 + self.off_y)
        self.criar_com_imagem(Label, name='img_poco_a1', render=self.img_poco_ligado, image=self.img_poco_ligado, borderwidth=2, relief='flat')
        self.instalar_em(name='img_poco_a1', x=150 + self.off_x, y=450 + self.off_y)
        self.criar_com_imagem(Label, name='img_poco_sci', render=self.img_poco_alarme, image=self.img_poco_alarme, borderwidth=2, relief='flat')
        self.instalar_em(name='img_poco_sci', x=250 + self.off_x, y=450 + self.off_y)

        self.criar_com_imagem(Label, name='img_bomba_sci_1', render=self.img_bomba_alarme, image=self.img_bomba_alarme)
        self.instalar_em(name='img_bomba_sci_1', x=885 + self.off_x, y=450 + self.off_y)
        self.criar_com_imagem(Label, name='img_bomba_sci_2', render=self.img_bomba_ligada, image=self.img_bomba_ligada)
        self.instalar_em(name='img_bomba_sci_2', x=985 + self.off_x, y=450 + self.off_y)
        self.criar_com_imagem(Label, name='img_bomba_sci_3', render=self.img_bomba_desligada, image=self.img_bomba_desligada)
        self.instalar_em(name='img_bomba_sci_3', x=1085 + self.off_x, y=450 + self.off_y)

        # botões operacao_manual
        self.criar(Button, name='bt_poco_cut', text="POÇO CUT", width=13, height=1, command=lambda: self.operacao_ligar("poco_cut"))
        self.instalar_em(name='bt_poco_cut', x=50 + self.off_x, y=505 + self.off_y)
        self.criar_com_imagem(Button, name='bt_modo_poco_cut', render=self.img2_modo_manual, image=self.img2_modo_manual,
                              command=lambda: self.operacao_manual("poco_cut"))
        self.instalar_em(name='bt_modo_poco_cut', x=50 + self.off_x, y=530 + self.off_y)
        self.criar_com_imagem(Button, name='bt_controle_poco_cut', render=self.img2_controle_remoto, image=self.img2_controle_remoto)
        self.instalar_em(name='bt_controle_poco_cut', x=95 + self.off_x, y=530 + self.off_y)

        self.criar(Button, name='bt_poco_a1', text="POÇO A1", width=13, height=1, command=lambda: self.operacao_ligar("poco_a1"))
        self.instalar_em(name='bt_poco_a1', x=150 + self.off_x, y=505 + self.off_y)
        self.criar_com_imagem(Button, name='bt_modo_poco_a1', render=self.img2_modo_manual, image=self.img2_modo_manual,
                              command=lambda: self.operacao_manual("poco_a1"))
        self.instalar_em(name='bt_modo_poco_a1', x=150 + self.off_x, y=530 + self.off_y)
        self.criar_com_imagem(Button, name='bt_controle_poco_a1', render=self.img2_controle_remoto, image=self.img2_controle_remoto)
        self.instalar_em(name='bt_controle_poco_a1', x=195 + self.off_x, y=530 + self.off_y)
        #
        self.criar(Button, name='bt_poco_sci', text="POÇO SCI", width=13, height=1, command=lambda: self.operacao_ligar("poco_sci"))
        self.instalar_em(name='bt_poco_sci', x=250 + self.off_x, y=505 + self.off_y)
        self.criar_com_imagem(Button, name='bt_modo_poco_sci', render=self.img2_modo_manual, image=self.img2_modo_manual,
                              command=lambda: self.operacao_manual("poco_sci"))
        self.instalar_em(name='bt_modo_poco_sci', x=250 + self.off_x, y=530 + self.off_y)
        self.criar_com_imagem(Button, name='bt_controle_poco_sci', render=self.img2_controle_remoto, image=self.img2_controle_remoto)
        self.instalar_em(name='bt_controle_poco_sci', x=295 + self.off_x, y=530 + self.off_y)

        self.criar(Button, name='bt_bomba_sci_1', text="BOMBA 01", width=13, height=1, command=lambda: self.operacao_ligar("bomba_sci_1"))
        self.instalar_em(name='bt_bomba_sci_1', x=870 + self.off_x, y=505 + self.off_y)
        self.criar_com_imagem(Button, name='bt_modo_bomba_sci_1', render=self.img2_modo_manual, image=self.img2_modo_manual,
                              command=lambda: self.operacao_manual("bomba_sci_1"))
        self.instalar_em(name='bt_modo_bomba_sci_1', x=870 + self.off_x, y=530 + self.off_y)
        self.criar_com_imagem(Button, name='bt_controle_bomba_sci_1', render=self.img2_controle_remoto, image=self.img2_controle_remoto)
        self.instalar_em(name='bt_controle_bomba_sci_1', x=915 + self.off_x, y=530 + self.off_y)

        self.criar(Button, name='bt_bomba_sci_2', text="BOMBA 02", width=13, height=1, command=lambda: self.operacao_ligar("bomba_sci_2"))
        self.instalar_em(name='bt_bomba_sci_2', x=970 + self.off_x, y=505 + self.off_y)
        self.criar_com_imagem(Button, name='bt_modo_bomba_sci_2', render=self.img2_modo_manual, image=self.img2_modo_manual,
                              command=lambda: self.operacao_manual("bomba_sci_2"))
        self.instalar_em(name='bt_modo_bomba_sci_2', x=970 + self.off_x, y=530 + self.off_y)
        self.criar_com_imagem(Button, name='bt_controle_bomba_sci_2', render=self.img2_controle_remoto, image=self.img2_controle_remoto)
        self.instalar_em(name='bt_controle_bomba_sci_2', x=1015 + self.off_x, y=530 + self.off_y)

        self.criar(Button, name='bt_bomba_sci_3', text="BOMBA 03", width=13, height=1, command=lambda: self.operacao_ligar("bomba_sci_3"))
        self.instalar_em(name='bt_bomba_sci_3', x=1070 + self.off_x, y=505 + self.off_y)
        self.criar_com_imagem(Button, name='bt_modo_bomba_sci_3', render=self.img2_modo_manual, image=self.img2_modo_manual,
                              command=lambda: self.operacao_manual("bomba_sci_3"))
        self.instalar_em(name='bt_modo_bomba_sci_3', x=1070 + self.off_x, y=530 + self.off_y)
        self.criar_com_imagem(Button, name='bt_controle_bomba_sci_3', render=self.img2_controle_remoto, image=self.img2_controle_remoto)
        self.instalar_em(name='bt_controle_bomba_sci_3', x=1115 + self.off_x, y=530 + self.off_y)

        # Linhas de alarmes minimo e maximo
        self.reservatorio_1_al_max = self.criar_linha("canvas", 'reservatorio_1_alarme_maximo', 145, 60, 150, 60, 'red', 3)
        self.reservatorio_1_al_min = self.criar_linha("canvas", 'reservatorio_1_alarme_minimo', 145, 240, 150, 240, 'red', 3)
        self.reservatorio_1_op_max = self.criar_linha("canvas", 'reservatorio_1_nivel_maximo', 145, 80, 150, 80, 'blue', 3)
        self.reservatorio_1_op_min = self.criar_linha("canvas", 'reservatorio_1_nivel_minimo', 145, 200, 150, 200, 'blue', 3)

        self.reservatorio_2_al_max = self.criar_linha("canvas", 'reservatorio_2_alarme_maximo', 355, 60, 360, 60, 'red', 3)
        self.reservatorio_2_al_min = self.criar_linha("canvas", 'reservatorio_2_alarme_minimo', 355, 240, 360, 240, 'red', 3)
        self.reservatorio_2_op_max = self.criar_linha("canvas", 'reservatorio_2_nivel_maximo', 355, 80, 360, 80, 'blue', 3)
        self.reservatorio_2_op_min = self.criar_linha("canvas", 'reservatorio_2_nivel_minimo', 355, 200, 360, 200, 'blue', 3)

        self.reservatorio_3_al_max = self.criar_linha("canvas", 'reservatorio_3_alarme_maximo', 370, 60, 375, 60, 'red', 3)
        self.reservatorio_3_al_min = self.criar_linha("canvas", 'reservatorio_3_alarme_minimo', 370, 240, 375, 240, 'red', 3)
        self.reservatorio_3_op_max = self.criar_linha("canvas", 'reservatorio_3_nivel_maximo', 370, 80, 375, 80, 'blue', 3)
        self.reservatorio_3_op_min = self.criar_linha("canvas", 'reservatorio_3_nivel_minimo', 370, 200, 375, 200, 'blue', 3)

        self.reservatorio_4_al_max = self.criar_linha("canvas", 'reservatorio_4_alarme_maximo', 580, 60, 585, 60, 'red', 3)
        self.reservatorio_4_al_min = self.criar_linha("canvas", 'reservatorio_4_alarme_minimo', 580, 240, 585, 240, 'red', 3)
        self.reservatorio_4_op_max = self.criar_linha("canvas", 'reservatorio_4_nivel_maximo', 580, 80, 585, 80, 'blue', 3)
        self.reservatorio_4_op_min = self.criar_linha("canvas", 'reservatorio_4_nivel_minimo', 580, 200, 585, 200, 'blue', 3)

        self.reservatorio_5_al_max = self.criar_linha("canvas", 'reservatorio_5_alarme_maximo', 919, 60, 925, 60, 'red', 3)
        self.reservatorio_5_al_min = self.criar_linha("canvas", 'reservatorio_5_alarme_minimo', 919, 240, 925, 240, 'red', 3)
        self.reservatorio_5_op_max = self.criar_linha("canvas", 'reservatorio_5_nivel_maximo', 919, 80, 925, 80, 'blue', 3)
        self.reservatorio_5_op_min = self.criar_linha("canvas", 'reservatorio_5_nivel_minimo', 919, 200, 925, 200, 'blue', 3)

        self.reservatorio_6_al_max = self.criar_linha("canvas", 'reservatorio_6_alarme_maximo', 644, 260, 650, 260, 'red', 3)
        self.reservatorio_6_al_min = self.criar_linha("canvas", 'reservatorio_6_alarme_minimo', 644, 440, 650, 440, 'red', 3)
        self.reservatorio_6_op_max = self.criar_linha("canvas", 'reservatorio_6_nivel_maximo', 644, 280, 650, 280, 'blue', 3)
        self.reservatorio_6_op_min = self.criar_linha("canvas", 'reservatorio_6_nivel_minimo', 644, 400, 650, 400, 'blue', 3)

    def carregar_variaveis(self):
        """Função que carrega as variáveis para a tela principal"""
        self.versao = "ELT.001 - 1/11/2023"
        self.usuario = ""
        self.falhas = ""
        self.acessado = False
        self.tela = TelaVazia()
        self.cliquebotao = datetime.now()

        self.title('ASGA')
        # Configuração o sair do windows
        self.protocol("WM_DELETE_WINDOW", self.sair)

        self.resizable(False, False)

        # Fontes
        self.fonte = ("Verdana", "8", "bold")
        self.fontenivel = ("Verdana", "10", "bold")
        self.fontetitulo = ("Verdana", "20", "bold")

        self.off_x = 0
        self.off_y = 70

        # Lista de ferramentas na tela
        self.__widgets = {}

        # consultar valor de tela aberta no BD
        valor = bd_consultar("sistema")[0]
        self.tempoacessado = datetime.now() + timedelta(minutes=valor[2])

        self.widthTela = 1300
        self.heightTela = 650
        # tamanho da splash
        self.posicionar_tela(widht=self.widthTela, height=self.heightTela)

        # Tamanho da tela
        self.widthInc = 0
        self.heightInc = 0

        self.img_reservatorio_alarme = ''
        self.img_reservatorio_normal = ''
        self.img_reservatorio_bloqueado = ''
        self.img_poco_alarme = ''
        self.img_poco_ligado = ''
        self.img_poco_desligado = ''
        self.img_bomba_alarme = ''
        self.img_bomba_ligada = ''
        self.img_bomba_desligada = ''
        self.img_desconectado = ''
        self.carregar_imagens('img_', 50, 50)

        self.img2_modo_automatico = ''
        self.img2_modo_manual = ''
        self.img2_controle_remoto = ''
        self.img2_controle_local = ''
        self.carregar_imagens('img2_', 35, 35)

        self.img3_configuracao = ''
        self.carregar_imagens('img3_', 15, 15)

        self.inserir_menu()

    def criar_retangulo(self, canvas, __x0, __y0, __x1, __y1, fill, outline):
        self.__widgets[canvas].create_rectangle(__x0 + self.off_x, __y0 + self.off_y, __x1 + self.off_x, __y1 + self.off_y, fill=fill,
                                                outline=outline)

    def criar_texto(self, canvas, __x, __y, text, font, anchor):
        self.__widgets[canvas].create_text(__x + self.off_x, __y + self.off_y, text=text, font=font, anchor=anchor)

    def criar_linha(self, canvas, name, __x0, __y0, __x1, __y1, fill, width):
        return self.__widgets[canvas].create_line(__x0 + self.off_x, __y0 + self.off_y, __x1 + self.off_x, __y1 + self.off_y, fill=fill, width=width)

    def criar(self, widget, **kwargs):
        """Função que criar uma ferramenta na tela"""
        w = widget(self, **kwargs)
        name = kwargs.get("name", str(w))
        self.__widgets[name] = w
        return name

    def instalar_em(self, name, **kwargs):
        """Função que instala a ferramenta em uma posição na tela"""
        self.__widgets[name].place(**kwargs)

    def carregar_imagens(self, prefixo, largura, comprimento):
        """Função para carregar a imagem"""
        for imagem in bd_consultar("imagens"):
            setattr(self, prefixo + imagem[1], ImageTk.PhotoImage(Image.open(imagem[2]).resize((largura, comprimento))))

    def alterar_imagem(self, nome, imagem):
        """Altera a imagem de uma ferramenta"""
        self.__widgets[nome].image = imagem

    def criar_com_imagem(self, widget, render, **kwargs):
        """Função que criar uma ferramenta na tela"""
        w = widget(self, **kwargs)
        w.image = render

        name = kwargs.get("name", str(w))
        self.__widgets[name] = w
        return name

    def inserir_menu(self):
        """Função para criar o menu"""
        self.menubar = Menu(self, font=self.fonte)

        user_menu = Menu(self.menubar, tearoff=0, font=self.fonte)
        user_menu.add_command(label="Adicionar", command=lambda: self.crud("cadastrar", "usuario"), font=self.fonte)
        user_menu.add_command(label="Alterar", command=lambda: self.crud("alterar", "usuario"), font=self.fonte)
        user_menu.add_command(label="Listar", command=lambda: self.crud("listar", "usuario"), font=self.fonte)
        self.menubar.add_cascade(label="Usuário", menu=user_menu, font=self.fonte)
        self.menubar.entryconfig("Usuário", state='disabled', font=self.fonte)

        comm_menu = Menu(self, tearoff=0, font=self.fonte)
        comm_menu.add_command(label="Adicionar", command=lambda: self.crud("cadastrar", "clp"), font=self.fonte)
        comm_menu.add_command(label="Alterar", command=lambda: self.crud("alterar", "clp"), font=self.fonte)
        comm_menu.add_command(label="Listar", command=lambda: self.crud("listar", "clp"), font=self.fonte)

        io_menu = Menu(self, tearoff=0, font=self.fonte)
        io_menu.add_command(label="Adicionar", command=lambda: self.crud("cadastrar", "io"), font=self.fonte)
        io_menu.add_command(label="Alterar", command=lambda: self.crud("alterar", "io"), font=self.fonte)
        io_menu.add_command(label="Listar", command=lambda: self.crud("listar", "io"), font=self.fonte)

        clp_menu = Menu(self, tearoff=0, font=self.fonte)
        self.menubar.add_cascade(label="Comunicação", menu=clp_menu, font=self.fonte)
        self.menubar.entryconfig("Comunicação", state='disabled')

        clp_menu.add_cascade(label="CLP", menu=comm_menu, font=self.fonte)
        clp_menu.add_cascade(label="Entradas/Saídas", menu=io_menu, font=self.fonte)

        sistema_menu = Menu(self, tearoff=0, font=self.fonte)
        sistema_menu.add_command(label="Alterar", command=lambda: self.crud("sistema", 'sistema'), font=self.fonte)
        sistema_menu.add_command(label="Habilitar_PC", command=self.habilitar_computador, font=self.fonte)
        self.menubar.add_cascade(label="Sistema", menu=sistema_menu, font=self.fonte)
        self.menubar.entryconfig("Sistema", state='disabled')

        historico_menu = Menu(self, tearoff=0, font=self.fonte)
        historico_menu.add_command(label="Listar", command=lambda: self.crud("historico", 'historico'), font=self.fonte)
        self.menubar.add_cascade(label="Histórico", menu=historico_menu, font=self.fonte)
        self.menubar.entryconfig("Histórico", state='disabled')

        self.config(menu=self.menubar)

    def sair(self):
        """Função para saida do sistema"""
        if tk.messagebox.askokcancel("Sair da Aplicação", "Quer sair do Sistema de Controle e Monitoramento de Bombeamento?"):
            bd_registrar('eventos', 'inserir_base', [(get_now(), "Null", "ACESSO", "Sistema de Controle e Monitoramente de Bombeamento FECHADO")])
            "Finalizar os ciclos de threads"
            finalizar_ciclos()
            "Fechar a tela"
            self.destroy()

    def ciclo_relogio(self):
        """ Função para atualização do relógio na tela principal e filhas """
        # Atualiza a hora
        self.alterar_parametro("time", text=get_now())

        # Atualizar totalizador de falhas
        falhas = bd_consulta_generica(sql_consultar_eventos_acao('FALHAS'))
        self.alterar_parametro("total_falhas", text=f"TOTAL DE FALHAS: {len(falhas)}")

        # Verificar se o tempo de login não está expirado
        if self.acessado and datetime.now() > self.tempoacessado:
            self.logout_user("automaticamente")

        # # atualiza as imagens das areas
        self.atualizar_imagem_areas()

        # coletar informações da posição da tela
        self.ajustar_posicao_tela()

        # # se existir uma tela aberta, atualiza as imagens da tela filha
        if self.tela.status:
            self.tela.verificar_tela_aberta()
            # self.tela.atualizar_bt()

    def ajustar_posicao_tela(self):
        """Função que coleta a posição da tela principal"""
        posicoes = self.winfo_geometry().split('+')
        self.widthInc = posicoes[1]
        self.heightInc = posicoes[2]

    def login_user(self, nome):
        """Função para acessar o usuário ao sistema"""
        # Se não tiver nenhum usuario acessando o sistema, libera a tela de login
        if not self.acessado:
            tl_login = Login(self, self.update_user, self.tela_fechada, nome, self.widthInc, self.heightInc)
            tl_login.grab_set()
        else:
            self.logout_user("manualmente")

    def logout_user(self, tipo):
        """Função para alterar os variaveis da tela ao sair o usuario do acesso"""

        bd_registrar('eventos', 'inserir_base', [(get_now(), self.usuario, "ACESSO", f"Usuário: {self.usuario} saiu do sistema {tipo}")])
        self.fechar_telas()
        self.usuario = None
        self.acessado = False
        self.alterar_parametro("usuario_nome", text="")
        self.alterar_parametro("bt_login", text='LOGIN')

        # Desabilitar os botões
        self.ativar_desativar_botoes(ativar=False)

    def tela_fechada(self):
        """Função para registrar quando a tela filha e fechada por ela"""
        self.tela = TelaVazia()

    def fechar_telas(self):
        """Função que fecha a tela filha aberta"""
        if self.tela:
            self.tela.sair()

    def update_user(self, usuario, perfil):
        """Atualizar as informações dos usuário que acessou o sistema"""
        self.usuario = usuario
        self.acessado = True
        valor = bd_consultar("sistema")[0]
        # Colocar o tempo máximo de login ativado
        self.tempoacessado = datetime.now() + timedelta(minutes=valor[2])

        self.alterar_parametro("bt_login", text='LOGOUT')
        self.alterar_parametro("usuario_nome", text=usuario)
        self.alterar_parametro("usuario_nome", text=usuario)

        # Habilitar os botões
        self.ativar_desativar_botoes(ativar=True, perfil=perfil)

        # Registra o acesso do usuário nos eventos
        bd_registrar('eventos', 'inserir_base', [(get_now(), self.usuario, "ACESSO", f"Usuário: {self.usuario} acessou o sistema")])

    def retornar_valor_parametro(self, nome, *args):
        """Função que retorna o valor do parametro selecionado"""
        return self.__widgets[nome].config(*args)

    def alterar_parametro(self, name, **kwargs):
        """Função que alterar algum parametro de uma ferramenta"""
        self.__widgets[name].config(**kwargs)

    def alterar_limites(self):
        lista = bd_consultar('reservatorios')
        # Percorre por todos reservatórios
        for item in lista:
            # coleta os valores
            nome = item[1]
            op_min = self.calcular_posicao(item[2], nome)
            op_max = self.calcular_posicao(item[3], nome)
            al_min = self.calcular_posicao(item[5], nome)
            al_max = self.calcular_posicao(item[6], nome)
            x_ref = item[9]
            # ajustar a posicao
            if nome == "reservatorio_1":
                self.__widgets["canvas"].coords(self.reservatorio_1_op_min, x_ref, op_min, x_ref + 5, op_min)
                self.__widgets["canvas"].coords(self.reservatorio_1_op_max, x_ref, op_max, x_ref + 5, op_max)
                self.__widgets["canvas"].coords(self.reservatorio_1_al_min, x_ref, al_min, x_ref + 5, al_min)
                self.__widgets["canvas"].coords(self.reservatorio_1_al_max, x_ref, al_max, x_ref + 5, al_max)
            if nome == "reservatorio_2":
                self.__widgets["canvas"].coords(self.reservatorio_2_op_min, x_ref, op_min, x_ref + 5, op_min)
                self.__widgets["canvas"].coords(self.reservatorio_2_op_max, x_ref, op_max, x_ref + 5, op_max)
                self.__widgets["canvas"].coords(self.reservatorio_2_al_min, x_ref, al_min, x_ref + 5, al_min)
                self.__widgets["canvas"].coords(self.reservatorio_2_al_max, x_ref, al_max, x_ref + 5, al_max)
            if nome == "reservatorio_3":
                self.__widgets["canvas"].coords(self.reservatorio_3_op_min, x_ref, op_min, x_ref + 5, op_min)
                self.__widgets["canvas"].coords(self.reservatorio_3_op_max, x_ref, op_max, x_ref + 5, op_max)
                self.__widgets["canvas"].coords(self.reservatorio_3_al_min, x_ref, al_min, x_ref + 5, al_min)
                self.__widgets["canvas"].coords(self.reservatorio_3_al_max, x_ref, al_max, x_ref + 5, al_max)
            if nome == "reservatorio_4":
                self.__widgets["canvas"].coords(self.reservatorio_4_op_min, x_ref, op_min, x_ref + 5, op_min)
                self.__widgets["canvas"].coords(self.reservatorio_4_op_max, x_ref, op_max, x_ref + 5, op_max)
                self.__widgets["canvas"].coords(self.reservatorio_4_al_min, x_ref, al_min, x_ref + 5, al_min)
                self.__widgets["canvas"].coords(self.reservatorio_4_al_max, x_ref, al_max, x_ref + 5, al_max)
            if nome == "reservatorio_5":
                self.__widgets["canvas"].coords(self.reservatorio_5_op_min, x_ref, op_min, x_ref + 5, op_min)
                self.__widgets["canvas"].coords(self.reservatorio_5_op_max, x_ref, op_max, x_ref + 5, op_max)
                self.__widgets["canvas"].coords(self.reservatorio_5_al_min, x_ref, al_min, x_ref + 5, al_min)
                self.__widgets["canvas"].coords(self.reservatorio_5_al_max, x_ref, al_max, x_ref + 5, al_max)
            if nome == "reservatorio_6":
                self.__widgets["canvas"].coords(self.reservatorio_6_op_min, x_ref, op_min, x_ref + 5, op_min)
                self.__widgets["canvas"].coords(self.reservatorio_6_op_max, x_ref, op_max, x_ref + 5, op_max)
                self.__widgets["canvas"].coords(self.reservatorio_6_al_min, x_ref, al_min, x_ref + 5, al_min)
                self.__widgets["canvas"].coords(self.reservatorio_6_al_max, x_ref, al_max, x_ref + 5, al_max)

    def calcular_posicao(self, valor, nome):
        y_ref = 49
        if nome == "reservatorio_6":
            y_ref = 249
        return 200 - 200 * (valor / 100) + y_ref + self.off_y

    def atualizar_imagem_areas(self):
        """Função para atualizar as imagens da tela"""
        # Consulta no banco de dados as situações atualizadas

        lista = bd_consultar('areas')
        # Percorre por todas as areas
        for item in lista:
            tipo = True  # bomba
            nome = item[1].lower()
            modo = item[2]
            ligado = item[3]
            alarme = item[4]
            conexao = item[5]
            controle = item[6]

            # formata o nome do local da imagem
            nome_imagem_1 = "img_" + nome
            nome_imagem_2 = "bt_modo_" + nome
            nome_imagem_3 = "bt_controle_" + nome

            if nome.split("_")[0] == "poco":
                tipo = False

            # se estiver desconectado
            if conexao == 0:
                imagem_1 = self.img_desconectado
            else:
                if alarme == 1:
                    if tipo:
                        imagem_1 = self.img_bomba_alarme
                    else:
                        imagem_1 = self.img_poco_alarme
                else:
                    if ligado == 1:
                        if tipo:
                            imagem_1 = self.img_bomba_ligada
                        else:
                            imagem_1 = self.img_poco_ligado
                    else:
                        if tipo:
                            imagem_1 = self.img_bomba_desligada
                        else:
                            imagem_1 = self.img_poco_desligado
            # se está em modo é automatico/manual
            if modo == 'AUTOMATICO':
                imagem_2 = self.img2_modo_automatico
                auto = "disabled"
            else:
                imagem_2 = self.img2_modo_manual
                auto = "active"

            # se o controle é remoto/local
            if controle == 1:
                imagem_3 = self.img2_controle_remoto
            else:
                imagem_3 = self.img2_controle_local

            # verifica se está logado
            if self.acessado:
                # Ativando /desativando o botão da area
                self.alterar_parametro("bt_" + nome, state=auto)

            self.alterar_imagem(nome_imagem_1, imagem_1)
            self.alterar_parametro(nome_imagem_1, image=imagem_1)
            self.alterar_imagem(nome_imagem_2, imagem_2)
            self.alterar_parametro(nome_imagem_2, image=imagem_2)
            self.alterar_imagem(nome_imagem_3, imagem_3)
            self.alterar_parametro(nome_imagem_3, image=imagem_3)

        lista = bd_consultar('reservatorios')
        # Percorre por todos reservatórios
        for item in lista:
            nome = "img_" + item[1]
            percent = "nivel_percentil_" + item[1]
            nivel = "nivel_" + item[1]
            nivel_atual = item[4]
            alarme_min = item[5]
            alarme_max = item[6]
            bloqueado = item[10]

            if bloqueado == 0:
                imagem = self.img_reservatorio_bloqueado
            else:
                imagem = self.img_reservatorio_normal
                # verifica o nível
                if alarme_min > nivel_atual or nivel_atual > alarme_max:
                    imagem = self.img_reservatorio_alarme

            self.alterar_parametro(nome, image=imagem)
            self.alterar_parametro(percent, text=str(nivel_atual) + "%")
            self.alterar_parametro(nivel, height=200 * (1 - nivel_atual / 100))

    def operacao_automatico(self):
        # """Função para operar as areas que estiverem em modo automático """
        reservatorios_cut = ['reservatorio_1', 'reservatorio_2', 'reservatorio_3', 'reservatorio_4']
        reservatorios_sci = ['reservatorio_5']
        reservatorios_sci_critico = ['reservatorio_6']
        bombas_reservatorios_cut = ['poco_cut', 'poco_a1', 'poco_sci']
        bombas_reservatorios_sci = ['bomba_sci_1', 'bomba_sci_2', 'bomba_sci_3']

        # status sem alteração
        reservatorio_cut_status = 0
        reservatorio_sci_status = 0
        reservatorios_ativos_cut = 0
        reservatorios_ativos_sci = 0
        bombas_sci_bloqueadas = False
        nivel_atual_cut = 0
        nivel_atual_sci = 0

        lista = bd_consultar('reservatorios')
        nivel_cut_max = 100
        nivel_cut_min = 0
        nivel_sci_max = 100
        nivel_sci_min = 0
        for item in lista:
            nome = item[1]
            operacao_min = item[2]
            operacao_max = item[3]
            nivel_atual = item[4]
            bloqueado = item[10]

            if nome in reservatorios_cut:
                if bloqueado == 0:
                    continue
                else:
                    # contagem de reservatórios ativos
                    reservatorios_ativos_cut += bloqueado
                    nivel_atual_cut = nivel_atual
                    if operacao_max < nivel_cut_max:
                        nivel_cut_max = operacao_max
                    if operacao_min > nivel_cut_min:
                        nivel_cut_min = operacao_min

            if nome in reservatorios_sci:
                if bloqueado == 0:
                    continue
                else:
                    reservatorios_ativos_sci += bloqueado
                    nivel_atual_sci = nivel_atual
                    if operacao_max < nivel_sci_max:
                        nivel_sci_max = operacao_max
                    if operacao_min > nivel_sci_min:
                        nivel_sci_min = operacao_min

            if nome in reservatorios_sci_critico:
                if nivel_atual <= operacao_min:
                    bombas_sci_bloqueadas = True

        if nivel_atual_cut >= nivel_cut_max or reservatorios_ativos_cut == 0:
            reservatorio_cut_status = -1
        elif nivel_atual_cut <= nivel_cut_min:
            reservatorio_cut_status = 1

        if nivel_atual_sci >= nivel_sci_max or reservatorios_ativos_sci == 0:
            reservatorio_sci_status = -1
        elif nivel_atual_sci <= nivel_sci_min:
            reservatorio_sci_status = 1

        lista = bd_consultar('areas')
        for item in lista:
            nome = item[1]
            modo = item[2]
            ligado = item[3]
            alarme = item[4]
            conexao = item[5]
            controle = item[6]

            if conexao == 1:
                if alarme == 0:
                    if controle == 1:
                        if modo == 'AUTOMATICO':
                            # BOMBAS CUT
                            if nome in bombas_reservatorios_cut:
                                if reservatorio_cut_status == 1:
                                    if ligado == 0:
                                        # ligar
                                        bd_registrar("areas", "atualizar_operacao", [(1, nome)])
                                if reservatorio_cut_status == -1:
                                    if ligado == 1:
                                        # desligar
                                        bd_registrar("areas", "atualizar_operacao", [(0, nome)])
                            # BOMBAS SCI
                            if nome in bombas_reservatorios_sci:
                                if reservatorio_sci_status == 1:
                                    if not bombas_sci_bloqueadas:
                                        if ligado == 0:
                                            # ligar
                                            bd_registrar("areas", "atualizar_operacao", [(1, nome)])
                                if reservatorio_sci_status == -1:
                                    if ligado == 1:
                                        # desligar
                                        bd_registrar("areas", "atualizar_operacao", [(0, nome)])

    def crud(self, tipo, tabela):
        """Função para abetura das telas do menu administrador"""
        if tipo == "cadastrar":
            if tabela == "usuario":
                self.tela = CadastrarUsuario(self, self.usuario, self.tela_fechada, tabela, self.widthInc, self.heightInc)
            if tabela == "clp":
                self.tela = CadastrarClp(self, self.usuario, self.tela_fechada, tabela, self.widthInc, self.heightInc)
            if tabela == "io":
                self.tela = CadastrarIO(self, self.usuario, self.tela_fechada, tabela, self.widthInc, self.heightInc)
        if tipo == "alterar":
            if tabela == "usuario":
                self.tela = AlterarUsuario(self, self.usuario, self.tela_fechada, tabela, self.widthInc, self.heightInc)
            if tabela == "clp":
                self.tela = AlterarClp(self, self.usuario, self.tela_fechada, tabela, self.widthInc, self.heightInc)
            if tabela == "io":
                self.tela = AlterarIO(self, self.usuario, self.tela_fechada, tabela, self.widthInc, self.heightInc)
        if tipo == "listar":
            if tabela == "usuario":
                self.tela = ListarUsuario(self, self.usuario, self.tela_fechada, tabela, self.widthInc, self.heightInc)
            if tabela == "clp":
                self.tela = ListarClp(self, self.usuario, self.tela_fechada, tabela, self.widthInc, self.heightInc)
            if tabela == "io":
                self.tela = ListarIO(self, self.usuario, self.tela_fechada, tabela, self.widthInc, self.heightInc)
        if tipo == "historico":
            self.tela = Historico(self, self.usuario, self.tela_fechada, tabela, self.widthInc, self.heightInc)
        if tipo == "sistema":
            self.tela = AlterarConfigSistema(self, self.usuario, self.tela_fechada, self.logout_user, tabela, self.widthInc, self.heightInc)
        self.tela.grab_set()

    def atualizar_bd(self):
        """  Função para realizar o teste de conexão com o clps e atualizar as informações no BD  """
        # gerar a lista de areas
        lista = bd_consultar('areas')
        adicionar_reserva_cut = 0
        adicionar_reserva_sci = 0
        adicionar_reserva_sci_critico = 0

        for item in lista:
            nome = item[1]
            modo = item[2]
            ligado = item[3]
            alarme = item[4]
            conexao = item[5]
            controle = item[6]
            #     bd_registrar("areas", "atualizar_geral", [(modo_t, ligado_t, alarme_t, conexao_t, controle_t, nome)])

            bombas_reservatorios_cut = ['poco_cut', 'poco_a1', 'poco_sci']
            bombas_reservatorios_sci = ['bomba_sci_1', 'bomba_sci_2', 'bomba_sci_3']

            if ligado == 1:
                if nome in bombas_reservatorios_cut:
                    adicionar_reserva_cut += 5
                if nome in bombas_reservatorios_sci:
                    adicionar_reserva_sci += 5

        for reserva in bd_consultar("reservatorios"):
            reservatorios_cut = ['reservatorio_1', 'reservatorio_2', 'reservatorio_3', 'reservatorio_4']
            reservatorios_sci = ['reservatorio_5']
            reservatorio_sci_critico = ['reservatorio_6']
            nome = reserva[1]
            valor = reserva[4]
            nivel_critico = reserva[5]
            decaimento = 0
            adicionar = 0

            # decaimento
            if valor > 0:
                decaimento = 5
                if (valor - decaimento) < 0:
                    decaimento = valor

            # adicionar
            if nome in reservatorios_cut:
                if valor > nivel_critico:
                    adicionar_reserva_sci_critico = 10
                adicionar = adicionar_reserva_cut
            if nome in reservatorios_sci:
                adicionar = adicionar_reserva_sci
            if nome in reservatorio_sci_critico:
                adicionar = adicionar_reserva_sci_critico

            # total
            total = valor + adicionar - decaimento
            if total > 100:
                total = 100

            bd_registrar("reservatorios", "atualizar_nivel_atual", [(total, nome)])

    def operacao_ligar(self, nome):
        """Função que realiza as operações MANUALMENTE de ligar/desligar"""
        # busca no BD pelo nome a situação(ligado/desligado) atual do local
        status_atual = bd_consultar_operacao_area(nome)
        clp_saidas = []
        status_nome = ''

        # verifica se está permitido o clique dentro do prazo
        if datetime.now() > self.cliquebotao:
            # realiza a inversão de situação
            if status_atual[0] == 1:
                # realizar a pergunta de confirmação de desligamento
                if tk.messagebox.askokcancel("Desligar", "Têm certeza que quer desligar está bomba?"):
                    status_nome = "DESLIGADO MANUALMENTE"
                    bd_registrar("areas", "atualizar_operacao", [(0, nome)])
                    # clp_saidas = bd_consulta_generica(sql_consultar_clp_areas(nome, 'DESLIGAR'))
            else:
                status_nome = "LIGADO MANUALMENTE"
                bd_registrar("areas", "atualizar_operacao", [(1, nome)])
                # clp_saidas = bd_consulta_generica(sql_consultar_clp_areas(nome, 'LIGAR'))

            # # verifica se existe algum área para desligar
            # if clp_saidas:
            #     # Enviar as informações ao clp para ligar ou desligar
            #     for clp in clp_saidas:
            #         # realiza a ação de ligar
            #         if escrever_clp(host=clp[1], port=clp[2], endereco=clp[3]):
            #             # grava no BD o log do evento
            #             bd_registrar('eventos', 'inserir_base', [(get_now(), self.usuario, "OPERAÇÃO", f"{status_nome} - {nome}")])

            # atualizando o tempo entre cliques
            self.cliquebotao = datetime.now() + timedelta(seconds=2)

    def operacao_manual(self, nome):
        """Função que alterar o modo de operação manual/automático"""
        # conferir o valor atual
        status_atual = bd_consulta_valor_tabela('areas', 'nome', nome)[0]

        # inverter o valor
        if status_atual[2] == 'AUTOMATICO':
            valor = "MANUAL"
        else:
            valor = "AUTOMATICO"

        # salvar o valor final
        bd_registrar("areas", "atualizar_modo", [(valor, nome)])
        bd_registrar('eventos', 'inserir_base',
                     [(get_now(), self.usuario, "CONFIGURAÇÃO_AREA", f"Alterado o modo de operação manualmente para {valor} de {nome}")])

    def operacao_local(self, nome):
        """Função que alterar o modo de operação local/remoto"""
        # Confirmação de alteração de modo
        if tk.messagebox.askokcancel("Local/Remoto", "Têm certeza que quer alterar o modo está área?"):
            # conferir o valor atual
            status_atual = bd_consulta_valor_tabela('areas', 'nome', nome)[0]
            # realiza a inversão de situação
            if status_atual[9] == 1:
                status_nome = "LOCAL"
                endereco = 9
            else:
                status_nome = "REMOTO"
                endereco = 10

            # lista dos clps vinculado a area
            clp_saidas = bd_consulta_generica(sql_consultar_clp_areas(nome, 'LIGAR'))
            # Enviar as informações ao clp para ligar ou desligar
            for clp in clp_saidas:
                # realiza a ação de ligar
                if escrever_clp(host=clp[1], port=clp[2], endereco=endereco):
                    # grava no BD o log do evento
                    bd_registrar('eventos', 'inserir_base', [(get_now(), self.usuario, "CONFIGURAÇÃO_AREA",
                                                              f"Alterado o controle de operação manualmente para {status_nome} de {nome}")])

    def posicionar_tela(self, widht, height):
        """Função para posicionamento da tela"""
        self.geometry(f'{widht}x{height}+{0}+{0}')

    def ativar_desativar_botoes(self, ativar, perfil=0):
        """Função para ativar e desativar os botões da tela principal"""

        acao = 'disabled'
        menu = False
        # verifica se é para ativar os botões
        if ativar:
            # perfil administrador
            if perfil == 1:
                menu = True
                acao = 'active'
            # perfil operador
            if perfil == 3:
                acao = 'active'

        self.ativar_desativar_menu(menu)

        self.alterar_parametro("bt_poco_cut", state=acao)
        self.alterar_parametro("bt_poco_a1", state=acao)
        self.alterar_parametro("bt_poco_sci", state=acao)
        self.alterar_parametro("bt_modo_poco_cut", state=acao)
        self.alterar_parametro("bt_modo_poco_a1", state=acao)
        self.alterar_parametro("bt_modo_poco_sci", state=acao)
        self.alterar_parametro("bt_controle_poco_cut", state=acao)
        self.alterar_parametro("bt_controle_poco_a1", state=acao)
        self.alterar_parametro("bt_controle_poco_sci", state=acao)
        self.alterar_parametro("bt_bomba_sci_1", state=acao)
        self.alterar_parametro("bt_bomba_sci_2", state=acao)
        self.alterar_parametro("bt_bomba_sci_3", state=acao)
        self.alterar_parametro("bt_modo_bomba_sci_1", state=acao)
        self.alterar_parametro("bt_modo_bomba_sci_2", state=acao)
        self.alterar_parametro("bt_modo_bomba_sci_3", state=acao)
        self.alterar_parametro("bt_controle_bomba_sci_1", state=acao)
        self.alterar_parametro("bt_controle_bomba_sci_2", state=acao)
        self.alterar_parametro("bt_controle_bomba_sci_3", state=acao)
        self.alterar_parametro("bt_config_reservatorio_1", state=acao)
        self.alterar_parametro("bt_config_reservatorio_2", state=acao)
        self.alterar_parametro("bt_config_reservatorio_3", state=acao)
        self.alterar_parametro("bt_config_reservatorio_4", state=acao)
        self.alterar_parametro("bt_config_reservatorio_5", state=acao)
        self.alterar_parametro("bt_config_reservatorio_6", state=acao)

    def ativar_desativar_menu(self, ativar):
        """Função para ativar e desativar o menu da tela principal"""
        if ativar:
            self.menubar.entryconfig("Usuário", state='active')
            self.menubar.entryconfig("Comunicação", state='active')
            self.menubar.entryconfig("Sistema", state='active')
            self.menubar.entryconfig("Histórico", state='active')
        else:
            self.menubar.entryconfig("Usuário", state='disabled')
            self.menubar.entryconfig("Comunicação", state='disabled')
            self.menubar.entryconfig("Sistema", state='disabled')
            self.menubar.entryconfig("Histórico", state='disabled')

    def habilitar_computador(self):
        """Função que insere o mac_address no banco de dados"""
        valor = str(hex(uuid.getnode()))

        # verifica se mac_address já está cadastrada no BD
        if bd_consulta_valor_tabela('mac_address', 'mac_nome', valor):
            tk.messagebox.showerror(title="Erro", message="Computador já está habilitado!")
        else:
            bd_registrar("mac_address", 'inserir_base', [[(valor)]])
            bd_registrar('eventos', 'inserir_base', [(get_now(), self.usuario, "CADASTRO", f"CADASTRADO NOVO MAC_ADDRESS - {valor}")])

            # força as thread a iniciarem
            inicializar_ciclos(self)
            tk.messagebox.showinfo(title="Sucesso", message="Computador habilitado!")

    def configuracao_reservatorio(self, nome_reservatorio):
        telaconfiguracao = ConfigReservatorio(self, self.usuario, self.alterar_limites, nome_reservatorio, self.widthInc, self.heightInc)
        telaconfiguracao.grab_set()


def inicializar_ciclos(principal):
    """Função que inicializa a thread para a atualizacao do relogio"""

    # coleta o mac_id do computador
    valor = str(hex(uuid.getnode()))

    # verifica se mac_address está cadastrada no BD
    if bd_consulta_valor_tabela('mac_address', 'mac_nome', valor):
        t1 = Thread(name='atualizar_relogio', target=lambda: thread_atualizar_relogio(principal))
        t1.daemon = True
        t1.start()

        t2 = Thread(name='atualizar_bd', target=lambda: thread_atualizar_bd(principal))
        t2.daemon = True
        t2.start()

        t3 = Thread(name='operacao', target=lambda: thread_operacao(principal))
        t3.daemon = True
        t3.start()
    else:
        tk.messagebox.showerror(title="Erro", message="Computador não está habilitado, contacte o administrador!")


def thread_operar(principal, posicao):
    """Função que gera uma thread para uma operação ligar/desligar"""
    t4 = Thread(name='operar', target=lambda: principal.operacao_ligar(posicao))
    t4.start()


def finalizar_ciclos():
    """Função para finalizar os threads"""
    globals()["threads"] = False


def thread_atualizar_relogio(principal):
    """Função que atualiza o relogio"""
    while globals()["threads"]:
        principal.ciclo_relogio()
        time.sleep(1)


def thread_atualizar_bd(principal):
    """Função que atualiza o banco de dados"""
    while globals()["threads"]:
        principal.atualizar_bd()
        time.sleep(bd_consultar("sistema")[0][3])


def thread_operacao(principal):
    """Função que realiza as operações em modo automatico"""
    while globals()["threads"]:
        principal.operacao_automatico()
        time.sleep(bd_consultar("sistema")[0][4])
