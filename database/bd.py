import sqlite3
from utils.times import get_now
from database.sql import *
from sqlite3 import Error
from tkinter import messagebox
import tkinter as tk


class BD:
    name_banco = "database.db"
    conn = ""
    cursor = ""

    # Lista das tabelas no Banco de dados
    lista_tabelas = [
        # TIPOS DE EVENTOS
        {'nome': 'tipos_evento', 'verificar': sql_verificar_tipos_eventos, 'criar': sql_criar_tipos_eventos,
         'inserir_valores': sql_inserir_valores_tipos_eventos, 'inserir_base': sql_inserir_base_tipos_eventos},
        # EVENTO
        {'nome': 'eventos', 'verificar': sql_verificar_eventos, 'criar': sql_criar_eventos,
         'inserir_valores': sql_inserir_valores_eventos, 'inserir_base': sql_inserir_base_eventos},
        # PERFIL
        {'nome': 'perfis', 'verificar': sql_verificar_perfis, 'criar': sql_criar_perfis,
         'inserir_valores': sql_inserir_valores_perfis, 'inserir_base': sql_inserir_base_perfis},
        # BOOLEANO
        {'nome': 'booleanos', 'verificar': sql_verificar_booleanos, 'criar': sql_criar_booleanos,
         'inserir_valores': sql_inserir_valores_booleanos, 'inserir_base': sql_inserir_base_booleanos},
        # USUARIOS
        {'nome': 'usuarios', 'verificar': sql_verificar_usuarios, 'criar': sql_criar_usuarios,
         'inserir_valores': sql_inserir_valores_usuarios, 'inserir_base': sql_inserir_base_usuarios,
         'atualizar_usuario': sql_atualizar_valores_usuario, 'consultar_usuario': sql_consultar_usuario},
        # AREAS
        {'nome': 'areas', 'verificar': sql_verificar_areas, 'criar': sql_criar_areas,
         'inserir_valores': sql_inserir_valores_areas, 'inserir_base': sql_inserir_base_areas,
         'atualizar_operacao': sql_atualizar_operacao_areas,
         'atualizar_conexao': sql_atualizar_conexao_areas, 'atualizar_local': sql_atualizar_local_areas,
         'atualizar_falha': sql_atualizar_alarme_areas, 'atualizar_modo': sql_atualizar_modo_areas,
         'atualizar_geral': sql_atualizar_operacao_geral},
        # IMAGENS
        {'nome': 'imagens', 'verificar': sql_verificar_imagens, 'criar': sql_criar_imagens,
         'inserir_valores': sql_inserir_valores_imagens, 'inserir_base': sql_inserir_base_imagens},
        # CLP
        {'nome': 'clps', 'verificar': sql_verificar_clps, 'criar': sql_criar_clps,
         'inserir_valores': sql_inserir_valores_clps, 'inserir_base': sql_inserir_base_clps,
         'atualizar_clp': sql_atualizar_clp, 'atualizar_clp_ativo': sql_atualizar_clp_ativo},
        # TIPO DE IO
        {'nome': 'tipos_io', 'verificar': sql_verificar_tipos_io, 'criar': sql_criar_tipos_io,
         'inserir_valores': sql_inserir_valores_tipos_io, 'inserir_base': sql_inserir_base_tipos_io},
        # ENTRADAS_SAIDAS DO CLP
        {'nome': 'entradas_saidas', 'verificar': sql_verificar_entradas_saidas, 'criar': sql_criar_entradas_saidas,
         'inserir_valores': sql_inserir_valores_entradas_saidas, 'inserir_base': sql_inserir_base_entradas_saidas,
         'atualizar_entradas_saidas': sql_atualizar_entradas_saidas},
        # PARAMETROS DO SISTEMA
        {'nome': 'sistema', 'verificar': sql_verificar_sistema, 'criar': sql_criar_sistema,
         'inserir_valores': sql_inserir_valores_sistema, 'inserir_base': sql_inserir_base_sistema,
         'atualizar_base': sql_atualizar_valores_sistema},
        # MAC_ADDRESS
        {'nome': 'mac_address', 'verificar': sql_verificar_mac_address, 'criar': sql_criar_mac_address,
         'inserir_valores': sql_inserir_valores_mac_address, 'inserir_base': sql_inserir_base_mac_address},
        # DIA_SEMANA
        {'nome': 'dias_semana', 'verificar': sql_verificar_dias_semana, 'criar': sql_criar_dias_semana,
         'inserir_valores': sql_inserir_valores_dias_semana, 'inserir_base': sql_inserir_base_dias_semana},
        # RESERVATÓRIO
        {'nome': 'reservatorios', 'verificar': sql_verificar_reservatorios, 'criar': sql_criar_reservatorios,
         'inserir_valores': sql_inserir_valores_reservatorios, 'inserir_base': sql_inserir_base_reservatorios,
         'atualizar_nivel_atual': sql_atualizar_nivel_atual_reservatorios, 'atualizar_niveis': sql_atualizar_niveis_reservatorios,
         'atualizar_bloqueio': sql_atualizar_bloqueio_reservatorios}
    ]

    def conectar(self):
        """Abrir uma conexão no banco de dados"""
        try:
            self.conn = sqlite3.connect(self.name_banco, timeout=15)
            self.cursor = self.conn.cursor()
        except Error as error:
            bd_registrar('eventos', 'inserir_base',
                         [(get_now(), 'Null', "FALHAS", f"Erro com o banco de dados: FUNÇÃO: {self.conectar.__name__} - ERRO: {error}")])

    def fechar(self):
        """Fechar a conexão com o banco de dados"""
        try:
            self.conn.close()
        except Error as error:
            bd_registrar('eventos', 'inserir_base',
                         [(get_now(), 'Null', "FALHAS", f"Erro com o banco de dados: FUNÇÃO: {self.fechar.__name__} - ERRO: {error}")])


def verificar_existencia_tabela(consulta):
    """Consulta a existencia de uma tabela no banco de dados"""
    bd = BD()
    bd.conectar()
    try:
        return bd.cursor.execute(consulta).fetchone()
    except Error:
        tk.messagebox.showerror(title="Erro", message="Erro com o banco de dados, reinicie o sistema!")
    finally:
        bd.fechar()


def criar_tabela(consulta):
    """Cria a tabela no banco de dados"""
    bd = BD()
    bd.conectar()
    try:
        bd.cursor.execute(consulta)
        return True
    except Error:
        return False
    finally:
        bd.fechar()


def verificar_banco(splash, incrementar_contador):
    """Verificar se existem as tabelas no banco de dados"""
    resultado = True
    try:
        # Percorre por toda a lista de tabelas as criam e as populam caso necessário
        bd = BD()
        bd.conectar()
        lista_tabelas = bd.lista_tabelas
        bd.fechar()
        x = 1
        texto = ''
        for tabela in lista_tabelas:
            # Verifica a existencia da tabela, caso contrario cria a tabela
            if not verificar_existencia_tabela(tabela['verificar']):
                if criar_tabela(tabela['criar']):
                    texto = f"Tabela {tabela['nome']} foi criada com sucesso no Banco de Dados"
                    bd_registrar('eventos', 'inserir_base', [(get_now(), "Null", "INICIALIZAÇÃO", texto)])
                else:
                    # Impossibilidade do sistema subir devido ao erro em alguma tabela
                    texto = f"Erro na Tabela {tabela['nome']} ao tentar ser criada no Banco de Dados"
                    resultado = False
                if tabela['inserir_valores']:
                    for valores in tabela['inserir_valores']:
                        bd_registrar(tabela['nome'], 'inserir_base', valores)
                    texto = f"Tabela {tabela['nome']} foi populada no Banco de Dados"
                    bd_registrar('eventos', 'inserir_base', [(get_now(), "Null", "INICIALIZAÇÃO", texto)])
            else:
                texto = f"Tabela {tabela['nome']} já existe no Banco de Dados"
                bd_registrar('eventos', 'inserir_base', [(get_now(), 'Null', "INICIALIZAÇÃO", texto)])
            # atualiza o progressbar do splash
            incrementar_contador(splash, int(x * 100 / len(lista_tabelas)), texto)
            x += 1
    except Error as error:
        bd_registrar('eventos', 'inserir_base',
                     [(get_now(), 'Null', "FALHAS",
                       f"Erro com o banco de dados - FUNÇÃO: {verificar_banco.__name__} - ERRO: {error}")])
    return resultado


def bd_registrar(tabela, tipo, valores):
    """Insere/Atualiza os valores na tabela no banco de dados"""
    bd = BD()
    tabela_nome = ""
    try:
        bd.conectar()
        erro = True

        # Percorre pela lista de tabelas
        for tab in bd.lista_tabelas:
            # Caso encontre a tabela monte o sql
            if tab['nome'] == tabela:
                # Verifica se a tabela existe no BD
                if verificar_existencia_tabela(verificar_basico(tabela)):
                    tabela_nome = tabela
                    bd.cursor.executemany(tab[tipo], valores)
                    erro = False

        # Caso não exista erro no sql
        if not erro:
            bd.conn.commit()
    except Error as error:
        bd_registrar('eventos', 'inserir_base',
                     [(get_now(), 'Null', "FALHAS",
                       f"Erro com o banco de dados: FUNÇÃO: {bd_registrar.__name__} - "
                       f"TIPO: {tipo} - TABELA: {tabela_nome} - VALOR: {valores} - ERRO: {error}")])
    finally:
        # Fechar a conexão com o BD
        bd.fechar()


def bd_consultar_config_area(area):
    """Consulta as informações dos horários de uma subarea"""
    bd = BD()
    lista = ()
    try:
        bd.conectar()
        lista = bd.cursor.execute(sql_consultar_config_area(area)).fetchall()

    except Error as error:
        bd_registrar('eventos', 'inserir_base',
                     [(get_now(), 'Null', "FALHAS",
                       f"Erro com o banco de dados: FUNÇÃO: {sql_consultar_config_area.__name__} - TABELA: {area} ERRO: {error}")])
    finally:
        bd.fechar()
    return lista


def bd_consultar_operacao_area(area):
    """Consulta a situação (ligado/desligado) de uma subarea"""
    bd = BD()
    operacao = 0
    try:
        bd.conectar()
        operacao = bd.cursor.execute(sql_consultar_operacao_area(area)).fetchone()
    except Error as error:
        bd_registrar('eventos', 'inserir_base',
                     [(get_now(), 'Null', "FALHAS",
                       f"Erro com o banco de dados: FUNÇÃO: {bd_consultar_operacao_area.__name__} TABELA: {area} ERRO: {error}")])
    finally:
        bd.fechar()
    return operacao


def bd_consultar(tabela):
    """Consulta simples de uma tabela"""
    bd = BD()
    lista = ()
    try:
        bd.conectar()
        lista = bd.cursor.execute(f"SELECT * from {tabela}").fetchall()
    except Error as error:
        bd_registrar('eventos', 'inserir_base',
                     [(get_now(), 'Null', "FALHAS",
                       f"Erro com o banco de dados: FUNÇÃO: {bd_consultar.__name__} TABELA: {tabela} ERRO: {error}")])
    finally:
        bd.fechar()
    return lista


def bd_consulta_generica(sql_consulta):
    """Consulta as informações gerais de um sql já definido"""
    bd = BD()
    lista = ()
    try:
        bd.conectar()
        lista = bd.cursor.execute(sql_consulta).fetchall()
    except Error as error:
        bd_registrar('eventos', 'inserir_base',
                     [(get_now(), 'Null', "FALHAS",
                       f"Erro com o banco de dados: FUNÇÃO: {bd_consulta_generica.__name__} ERRO: {error}")])
    finally:
        bd.fechar()
    return lista


def bd_consultar_atualizacao():
    """Consulta as informações gerais de atualização"""
    bd = BD()
    lista = ()
    try:
        bd.conectar()
        lista = bd.cursor.execute(sql_consultar_atualizacao).fetchall()
    except Error as error:
        bd_registrar('eventos', 'inserir_base',
                     [(get_now(), 'Null', "FALHAS",
                       f"Erro com o banco de dados: FUNÇÃO: {bd_consultar_atualizacao.__name__} ERRO: {error}")])
    finally:
        bd.fechar()
    return lista


def bd_consultar_ferramentas_telas(area):
    """Consulta as informações para a criação das telas"""
    bd = BD()
    lista = []
    try:
        bd.conectar()
        lista = bd.cursor.execute(sql_consultar_ferramentas_telas(area)).fetchall()
    except Error as error:
        bd_registrar('eventos', 'inserir_base',
                     [(get_now(), 'Null', "FALHAS",
                       f"Erro com o banco de dados: FUNÇÃO: {bd_consultar_ferramentas_telas.__name__} - TABELA: {area} - ERRO: {error}")])
    finally:
        bd.fechar()
    return lista


def bd_consulta_lista_usuario():
    """Consulta as informações de usuarios cadastrados"""
    bd = BD()
    lista = []
    try:
        bd.conectar()
        lista = bd.cursor.execute(sql_consulta_lista_usuario).fetchall()
    except Error as error:
        bd_registrar('eventos', 'inserir_base',
                     [(get_now(), 'Null', "FALHAS",
                       f"Erro com o banco de dados: FUNÇÃO: {bd_consulta_lista_usuario.__name__} - ERRO: {error}")])
    finally:
        bd.fechar()
    return lista


def bd_excluir_item(tabela, valor):
    """Excluir usuario"""
    bd = BD()
    lista = ()
    try:
        bd.conectar()
        bd.cursor.execute(sql_delete_item(tabela, valor)).fetchall()
        bd.conn.commit()
    except Error as error:
        bd_registrar('eventos', 'inserir_base',
                     [(get_now(), 'Null', "FALHAS",
                       f"Erro com o banco de dados: FUNÇÃO: {bd_excluir_item.__name__} - TABELA: {tabela} - VALOR: {valor} - ERRO: {error}")])
    finally:
        bd.fechar()
    return lista


def bd_consulta_valor_tabela(tabela, campo, valor, tipovalor="texto"):
    """Consulta as informações de uma tupla de uma tabela"""
    bd = BD()
    lista = []
    try:
        bd.conectar()
        if tipovalor == "texto":
            lista = bd.cursor.execute(f"SELECT * FROM {tabela} WHERE {campo} = '{valor}'").fetchall()
        else:
            lista = bd.cursor.execute(f"SELECT * FROM {tabela} WHERE {campo} = {valor}").fetchall()

    except Error as error:
        bd_registrar('eventos', 'inserir_base',
                     [(get_now(), 'Null', "FALHAS",
                       f"Erro com o banco de dados: FUNÇÃO: {bd_consulta_valor_tabela.__name__} - "
                       f"TABELA: {tabela} - CAMPO: {campo}-  VALOR: {valor} - ERRO: {error}")])
    finally:
        bd.fechar()
    return lista
