import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar

from database.bd import verificar_banco
from view.principal_novo import TelaPrincipal
from view.principal_novo import inicializar_ciclos


def main_window():
    """Função que inicia a tela do sistema"""
    app = TelaPrincipal()
    # app = ConfigReservatorio()
    inicializar_ciclos(app)
    app.mainloop()


def splash():
    """Função que inicia a tela do splash"""
    splash_ = Tk()
    # tamanho da splash
    width_of_windows = 400
    height_of_windows = 250
    screen_width = splash_.winfo_screenwidth()
    screen_heigh = splash_.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (width_of_windows / 2))
    y_coordinate = int((screen_heigh / 2) - (height_of_windows / 2))

    # posicionamento do splash
    splash_.geometry(f"{width_of_windows}x{height_of_windows}+{x_coordinate}+{y_coordinate}")

    # ocultar os titulos e botões do splash
    splash_.overrideredirect(True)

    # barrra de progresso
    splash_.progress = Progressbar(splash_, style="red.Horizontal.TProgressbar", orient=HORIZONTAL, length=400, mode='determinate')
    splash_.progress.place(x=0, y=235)

    # adding Frame
    Frame(splash_, width=400, height=240, bg='#249794').place(x=0, y=0)

    splash_.start = Button(splash_, width=10, height=1, text="INICIAR", command=lambda: inicializar_sistema(splash_), border=0, fg='#249794')
    splash_.start.place(x=170, y=200)

    # labels
    l1 = Label(splash_, text='CONTROLE', fg='white', bg='#249794')
    lst1 = ('Calibri (Body)', 18, 'bold')
    l1.configure(font=lst1)
    l1.place(x=30, y=60)

    l2 = Label(splash_, text='MONITORAMENTO', fg='white', bg='#249794')
    lst2 = ('Calibri (Body)', 18)
    l2.configure(font=lst2)
    l2.place(x=120, y=90)

    l3 = Label(splash_, text='BOMBEAMENTO', fg='white', bg='#249794')
    lst3 = ('Calibri (Body)', 13)
    l3.configure(font=lst3)
    l3.place(x=250, y=120)

    l4 = Label(splash_, text='ELT-001', fg='white', bg='#249794')
    lst4 = ('Calibri (Body)', 10)
    l4.configure(font=lst4)
    l4.place(x=340, y=150)

    splash_.texto = Label(splash_, text='', fg='white', bg='#249794', width=65, anchor="w")
    lst4 = ('Calibri (Body)', 8)
    splash_.texto.configure(font=lst4)
    splash_.texto.place(x=0, y=221)

    # loop da tela
    splash_.mainloop()


def incrementar_contador(splash_, valor, texto):
    """Função que altera o valor do progressbar"""
    splash_.progress['value'] = valor
    splash_.texto['text'] = texto
    splash_.update_idletasks()


def inicializar_sistema(splash_):
    """Função que verifica o banco e inicializa a tela principal"""
    # bloqueia o botão de start
    splash_.start['state'] = 'disabled'
    splash_.start['bg'] = '#249794'
    splash_.update_idletasks()

    l5 = Label(splash_, text='carregando...', fg='white', bg='#249794', anchor="w")
    lst5 = ('Calibri (Body)', 8)
    l5.configure(font=lst5)
    l5.place(x=0, y=200)

    # verifica o banco de dados
    if verificar_banco(splash_, incrementar_contador):
        # fecha a tela do splash
        splash_.destroy()
        # inicia a tela do programa
        main_window()
    else:
        tk.messagebox.showerror(title="Erro", message="Erro ao iniciar o sistema")
