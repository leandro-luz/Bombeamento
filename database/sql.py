def verificar_basico(nome_tabela):
    return f"SELECT name FROM sqlite_master WHERE type='table' AND name='{nome_tabela}'"


def sql_delete_item(tabela, valor):
    if tabela == 'eventos':
        return f"DELETE FROM {tabela} as x WHERE x.acao = '{valor}';"
    else:
        return f"DELETE FROM {tabela} as x WHERE x.nome = '{valor}';"


""" --------------------------------------------------------------------------- """
# TABELA BOOLEANA
sql_verificar_booleanos = verificar_basico('booleanos')
sql_criar_booleanos = """
        CREATE TABLE booleanos (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        booleano_id INTEGER NOT NULL,
        nome TEXT NOT NULL
        );"""
sql_inserir_base_booleanos = 'INSERT INTO booleanos (booleano_id, nome) VALUES (?,?)'
sql_inserir_valores_booleanos = (
    [(0, 'NÃO')],
    [(1, 'SIM')],
)

""" --------------------------------------------------------------------------- """
# TABELA TIPO DE EVENTOS
sql_verificar_tipos_eventos = verificar_basico('tipos_evento')
sql_criar_tipos_eventos = """
        CREATE TABLE tipos_evento (
        tipo_evento_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
        );"""
sql_inserir_base_tipos_eventos = 'INSERT INTO tipos_evento (nome) VALUES (?)'
sql_inserir_valores_tipos_eventos = [(
    ['ACESSO'],
    ['CADASTRO'],
    ['CONFIGURAÇÃO_AREA'],
    ['INICIALIZAÇÃO'],
    ['FALHAS'],
    ['OPERAÇÃO'],
    ['STARTUP'],
    ['SETUP'],
)]

""" --------------------------------------------------------------------------- """
# TABELA EVENTOS
sql_verificar_eventos = verificar_basico('eventos')
sql_criar_eventos = """
        CREATE TABLE eventos (
        evento_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        data DATE NOT NULL,
        usuario TEXT,
        acao TEXT,
        descricao TEXT NOT NULL
        );"""
sql_inserir_base_eventos = 'INSERT INTO eventos (data, usuario, acao, descricao) VALUES (?,?,?,?)'
sql_inserir_valores_eventos = []

sql_excluir_falhas = """
DELETE FROM eventos WHERE acao = 'FALHAS';
"""


def sql_consultar_eventos_acao(acao):
    return f"SELECT data ||'  -  '|| usuario ||'  -  '|| descricao as valor FROM eventos WHERE acao = '{acao}' ORDER BY data DESC"


""" --------------------------------------------------------------------------- """
# TABELA PERFIL
sql_verificar_perfis = verificar_basico('perfis')
sql_criar_perfis = """
        CREATE TABLE perfis (
        perfil_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
        );"""
sql_inserir_base_perfis = 'INSERT INTO perfis (nome) VALUES (?)'
sql_inserir_valores_perfis = [(
    ['MANUTENÇÃO'],
    ['OPERAÇÃO']
)]

""" --------------------------------------------------------------------------- """
# TABELA USUARIO
sql_verificar_usuarios = verificar_basico('usuarios')
sql_criar_usuarios = """
        CREATE TABLE usuarios (
        usuario_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        booleano_id INTEGER NOT NULL,
        senha TEXT NOT NULL,
        perfil_id INTEGER NOT NULL,
        FOREIGN KEY(perfil_id) REFERENCES perfis(perfil_id)
        FOREIGN KEY(booleano_id) REFERENCES booleanos(booleano_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
        );"""
sql_inserir_base_usuarios = 'INSERT INTO usuarios (nome, booleano_id, perfil_id, senha) VALUES (?,?,?,?)'
sql_inserir_valores_usuarios = (
    [('OPERADOR', 1, 3, '$2b$12$jNngFwYq2Ttm33xR6a0DZ.IYdsblz4XuejzpGYGTg923U/2/6UFpS')],
    [('ADMINISTRADOR', 1, 1, '$2b$12$lF4y1dalv7sQe6jXfMlgm.uNr/Fd1SoIRHBJIGGHfWlDrowUOhwtK')],
)

sql_consultar_usuario = """SELECT nome, booleano_id, perfil_id, senha WHERE nome = ?"""

sql_consulta_lista_usuario = """
SELECT u.nome, u.nome || '  -  ' || p.nome AS valor
FROM usuarios AS u INNER JOIN perfis as p ON u.perfil_id = p.perfil_id;"""

sql_atualizar_valores_usuario = """UPDATE usuarios set booleano_id = ?, perfil_id = ?, senha = ? WHERE nome = ?"""

""" --------------------------------------------------------------------------- """
# TABELA AREAS
sql_verificar_areas = verificar_basico('areas')
sql_criar_areas = """
        CREATE TABLE areas (
        area_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        tipo_operacao TEXT NOT NULL,
        ligado INTEGER NOT NULL,
        alarme INTEGER NOT NULL,
        conexao INTEGER NOT NULL,
        local INTEGER NOT NULL
        );"""

sql_inserir_base_areas = 'INSERT INTO areas (nome, tipo_operacao, ligado, alarme, conexao, local) VALUES (?,?,?,?,?,?)'

sql_inserir_valores_areas = (
    [('poco_cut', 'MANUAL', 0, 0, 1, 1)],
    [('poco_a1', 'MANUAL', 0, 0, 1, 1)],
    [('poco_sci', 'MANUAL', 0, 0, 1, 1)],
    [('bomba_sci_1', 'MANUAL', 0, 0, 1, 1)],
    [('bomba_sci_2', 'MANUAL', 0, 0, 1, 1)],
    [('bomba_sci_3', 'MANUAL', 0, 0, 1, 1)],
)

sql_atualizar_operacao_areas = """UPDATE areas set ligado = ? WHERE nome = ?"""
sql_atualizar_conexao_areas = """UPDATE areas set conexao = ? WHERE nome = ?"""
sql_atualizar_local_areas = """UPDATE areas set local = ? WHERE nome = ?"""
sql_atualizar_alarme_areas = """UPDATE areas set alarme = ? WHERE nome = ?"""
sql_atualizar_modo_areas = """UPDATE areas set tipo_operacao = ? WHERE nome = ?"""

sql_atualizar_operacao_geral = """UPDATE areas set tipo_operacao = ?, ligado = ?, alarme = ?, conexao = ?, local = ? WHERE nome = ?"""


def sql_consultar_operacao_area(area):
    return f"SELECT a.ligado FROM areas as a WHERE a.nome = '{area}'"


def sql_consultar_config_area(area):
    return f"SELECT * FROM areas as a WHERE a.nome = '{area}'"


def sql_consultar_clp_areas(area, tipo):
    return f"SELECT DISTINCT a.nome, c.ip, c.porta, e.endereco, c.nome FROM areas as a " \
           f" INNER JOIN entradas_saidas as e ON e.area_id = a.area_id" \
           f" INNER JOIN tipos_io as t ON e.tipo_io_id = t.tipo_io_id" \
           f" INNER JOIN clps as c ON e.clp_id = c.clp_id WHERE t.nome = '{tipo}' and a.nome = '{area}'"


sql_consultar_atualizacao = """SELECT a.nome as nome, 
count(a.nome) as total, 
count(CASE	WHEN a.ligado = 1 THEN 1 END) as ligado,
count(CASE	WHEN a.alarme = 1 THEN 1 END) as alarme,
count(CASE	WHEN a.conexao = 1 THEN 1 END) as conexao
FROM areas as a
GROUP BY a.nome;"""

""" --------------------------------------------------------------------------- """
# TABELA IMAGENS
sql_verificar_imagens = verificar_basico('imagens')
sql_criar_imagens = """
        CREATE TABLE imagens (
        imagem_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        local TEXT NOT NULL
        );"""
sql_inserir_base_imagens = 'INSERT INTO imagens (nome, local) VALUES (?,?)'
sql_inserir_valores_imagens = (
    [('modo_automatico', 'img/modo_automatico.png')],
    [('modo_manual', 'img/modo_manual.png')],
    [('controle_local', 'img/controle_local.png')],
    [('controle_remoto', 'img/controle_remoto.png')],
    [('reservatorio_alarme', 'img/reservatorio_alarme.png')],
    [('reservatorio_bloqueado', 'img/reservatorio_bloqueado.png')],
    [('bomba_ligada', 'img/bomba_ligada.png')],
    [('bomba_desligada', 'img/bomba_desligada.png')],
    [('bomba_alarme', 'img/bomba_alarme.png')],
    [('poco_alarme', 'img/poco_alarme.png')],
    [('poco_ligado', 'img/poco_ligado.png')],
    [('poco_desligado', 'img/poco_desligado.png')],
    [('desconectado', 'img/desconectado.png')],
    [('configuracao', 'img/configuracao.png')],
)


def sql_consultar_ferramentas_telas(area):
    return f"SELECT s.nome, s.funcao, s.ferramenta, s.kwargs" \
           f" FROM areas AS a INNER JOIN telas as s ON a.area_id = s.area_id WHERE a.nome = '{area}'"


""" --------------------------------------------------------------------------- """
# TABELA CLP
sql_verificar_clps = verificar_basico('clps')
sql_criar_clps = """
        CREATE TABLE clps (
        clp_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        ip TEXT NOT NULL,
        porta INTEGER NOT NULL,
        id INTEGER NOT NULL,
        ativo INTEGER NOT NULL,
        FOREIGN KEY(ativo) REFERENCES booleanos(booleano_id)
        );"""
sql_inserir_base_clps = 'INSERT INTO clps (nome, ip, porta, id, ativo) VALUES (?,?,?,?,?)'

sql_inserir_valores_clps = (
    [('CLP01_PC_CUT', '10.22.217.51', 510, 1, 0)],
    [('CLP02_PC_A1', '10.22.217.52', 510, 2, 0)],
    [('CLP03_PC_SCI', '10.22.217.53', 510, 3, 0)],
    [('CLP04_SCI', '10.22.217.54', 510, 4, 0)],
)

sql_consultar_clps_concatenada = """
SELECT c.nome || ' - ' || c.ip || ' - ' || c.porta || ' - ' || c.id || ' - ' || b.nome as valor
FROM clps as c INNER JOIN booleanos as b ON c.ativo = b.booleano_id ;"""

sql_atualizar_clp = """UPDATE clps set nome = ?, ip = ?, porta = ?, id = ? WHERE nome = ?"""

sql_atualizar_clp_ativo = """UPDATE clps set ativo = ? WHERE nome = ?"""

""" --------------------------------------------------------------------------- """
# TABELA TIPOS DE ENTRADAS/SAIDAS
sql_verificar_tipos_io = verificar_basico('tipos_io')
sql_criar_tipos_io = """
        CREATE TABLE tipos_io (
        tipo_io_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
        );"""
sql_inserir_base_tipos_io = 'INSERT INTO tipos_io (nome) VALUES (?)'
sql_inserir_valores_tipos_io = [(
    ['LIGAR'],
    ['DESLIGAR'],
    ['SAIDA'],
    ['FALHA'],
)]

""" --------------------------------------------------------------------------- """
# TABELA TIPOS DE ENTRADAS/SAIDAS
sql_verificar_entradas_saidas = verificar_basico('entradas_saidas')
sql_criar_entradas_saidas = """
        CREATE TABLE entradas_saidas (
        io_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        endereco INTEGER NOT NULL,
        clp_id INTEGER NOT NULL,
        tipo_io_id INTEGER NOT NULL,
        area_id INTEGER NOT NULL,
        FOREIGN KEY(clp_id) REFERENCES clps(clp_id),
        FOREIGN KEY(tipo_io_id) REFERENCES tipos_io(tipo_io_id),
        FOREIGN KEY(area_id) REFERENCES areas(area_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
        );"""

sql_inserir_base_entradas_saidas = """
INSERT INTO entradas_saidas (nome, endereco, tipo_io_id, clp_id, area_id) VALUES (?,?,?,?,?)"""

# sql_inserir_valores_entradas_saidas = ()
sql_inserir_valores_entradas_saidas = (
    # POÇO CUT
    [('CLP01_SAIDA01', 1, 3, 1, 3)],
    [('CLP01_SAIDA02', 2, 3, 1, 5)],
    [('CLP01_LIGAR_01', 1, 1, 1, 3)],
    [('CLP01_DESLIGAR_01', 2, 2, 1, 3)],
    [('CLP01_LIGAR_02', 3, 1, 1, 5)],
    [('CLP01_DESLIGAR_02', 4, 2, 1, 5)],
    [('CLP01_FALHA_01', 1, 4, 1, 3)],
    [('CLP01_FALHA_02', 2, 4, 1, 5)],

    # POÇO A1
    [('CLP02_SAIDA01', 1, 3, 2, 5)],
    [('CLP02_SAIDA02', 2, 3, 2, 4)],
    [('CLP02_SAIDA03', 3, 3, 2, 8)],
    [('CLP02_SAIDA04', 4, 3, 2, 10)],
    [('CLP02_LIGAR_01', 1, 1, 2, 5)],
    [('CLP02_DESLIGAR_01', 2, 2, 2, 5)],
    [('CLP02_LIGAR_02', 3, 1, 2, 4)],
    [('CLP02_DESLIGAR_02', 4, 2, 2, 4)],
    [('CLP02_LIGAR_03', 5, 1, 2, 8)],
    [('CLP02_DESLIGAR_03', 6, 2, 2, 8)],
    [('CLP02_LIGAR_04', 7, 1, 2, 10)],
    [('CLP02_DESLIGAR_04', 8, 2, 2, 10)],
    [('CLP02_FALHA_01', 1, 4, 2, 5)],
    [('CLP02_FALHA_02', 2, 4, 2, 4)],
    [('CLP02_FALHA_03', 3, 4, 2, 8)],
    [('CLP02_FALHA_04', 4, 4, 2, 10)],

    # POÇO SCI
    [('CLP03_SAIDA01', 1, 3, 3, 4)],
    [('CLP03_SAIDA02', 2, 3, 3, 8)],
    [('CLP03_SAIDA03', 3, 3, 3, 10)],
    [('CLP03_LIGAR_01', 1, 1, 3, 4)],
    [('CLP03_DESLIGAR_01', 2, 2, 3, 4)],
    [('CLP03_LIGAR_02', 3, 1, 3, 8)],
    [('CLP03_DESLIGAR_02', 4, 2, 3, 8)],
    [('CLP03_LIGAR_03', 5, 1, 3, 10)],
    [('CLP03_DESLIGAR_03', 6, 2, 3, 10)],
    [('CLP03_FALHA_01', 1, 4, 3, 4)],
    [('CLP03_FALHA_02', 2, 4, 3, 8)],
    [('CLP03_FALHA_03', 3, 4, 3, 10)],

    # CASTELO SCI
    [('CLP04_SAIDA01', 1, 3, 4, 4)],
    [('CLP04_SAIDA02', 2, 3, 4, 3)],
    [('CLP04_LIGAR_01', 1, 1, 4, 4)],
    [('CLP04_DESLIGAR_01', 2, 2, 4, 4)],
    [('CLP04_LIGAR_02', 3, 1, 4, 3)],
    [('CLP04_DESLIGAR_02', 4, 2, 4, 3)],
    [('CLP04_FALHA_01', 1, 4, 4, 4)],
    [('CLP04_FALHA_02', 2, 4, 4, 3)],

)

sql_consultar_entradas_saidas_concatenada = """
SELECT e.nome, e.nome || ' - ' || e.endereco || ' - ' || c.nome || ' - ' || t.nome || ' - ' || a.nome as valor 
FROM entradas_saidas as e 
INNER JOIN clps as c ON e.clp_id = c.clp_id 
INNER JOIN tipos_io as t ON e.tipo_io_id = t.tipo_io_id
INNER JOIN areas as a ON e.area_id = a.area_id
ORDER BY valor
;"""

sql_consultar_entradas_saidas = """
SELECT e.io_id as id, e.nome, e.endereco as endereco, c.nome as clp, t.nome as tipo, a.nome as area
FROM entradas_saidas as e 
INNER JOIN clps as c ON e.clp_id = c.clp_id 
INNER JOIN tipos_io as t ON e.tipo_io_id = t.tipo_io_id
INNER JOIN areas as a ON e.area_id = a.area_id
;"""

sql_atualizar_entradas_saidas = """UPDATE entradas_saidas set nome = ?, endereco = ?, clp_id = ?, tipo_io_id = ?, area_id = ? WHERE nome = ?"""

""" --------------------------------------------------------------------------- """
# TABELA PARAMETROS DO SISTEMA
sql_verificar_sistema = verificar_basico('sistema')
sql_criar_sistema = """
        CREATE TABLE sistema (
        sistema_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        tela_aberta INTEGER NOT NULL,
        login INTEGER NOT NULL,
        atualizacao INTEGER NOT NULL,
        operacao INTEGER NOT NULL
        );"""
sql_inserir_base_sistema = 'INSERT INTO sistema (tela_aberta, login, atualizacao, operacao) VALUES (?,?,?,?)'
sql_inserir_valores_sistema = [(
    [5, 10, 1, 1],
)]
sql_atualizar_valores_sistema = """UPDATE sistema set tela_aberta = ?, login = ?, atualizacao = ?, operacao = ? WHERE sistema_id = 1"""

""" --------------------------------------------------------------------------- """
# TABELA MAC ADDRESS PC CLIENTE
sql_verificar_mac_address = verificar_basico('mac_address')

sql_criar_mac_address = """
        CREATE TABLE mac_address (
        mac_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        mac_nome TEXT NOT NULL
        );"""
sql_inserir_base_mac_address = 'INSERT INTO mac_address (mac_nome) VALUES (?)'

sql_inserir_valores_mac_address = []

""" --------------------------------------------------------------------------- """
# TABELA DIAS DA SEMANA
sql_verificar_dias_semana = verificar_basico('dias_semana')

sql_criar_dias_semana = """
        CREATE TABLE dias_semana (
        dia_semana_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
        );"""
sql_inserir_base_dias_semana = 'INSERT INTO dias_semana (nome) VALUES (?)'

sql_inserir_valores_dias_semana = [(
    ['TODOS DIAS'],
    ['DIAS ÚTEIS'],
    ['FIM DE SEMANA'],
)]

""" --------------------------------------------------------------------------- """
# TABELA RESERVATORIOS
sql_verificar_reservatorios = verificar_basico('reservatorios')
sql_criar_reservatorios = """
        CREATE TABLE reservatorios (
        reservatorio_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        nivel_minimo INTEGER NOT NULL,
        nivel_maximo INTEGER NOT NULL,
        nivel_atual INTEGER NOT NULL,
        alarme_minimo INTEGER NOT NULL,
        alarme_maximo INTEGER NOT NULL,
        offset_minimo INTEGER NOT NULL,
        offset_maximo INTEGER NOT NULL,
        x_ref INTEGER NOT NULL,
        bloqueado INTEGER NOT NULL
        );"""

sql_inserir_base_reservatorios = \
    'INSERT INTO reservatorios (nome, nivel_minimo, nivel_maximo, nivel_atual, alarme_minimo, alarme_maximo, offset_minimo, offset_maximo, x_ref, bloqueado) ' \
    'VALUES (?,?,?,?,?,?,?,?,?,?)'

sql_inserir_valores_reservatorios = (
    [('reservatorio_1', 40, 90, 50, 15, 95, 0, 0, 145, 0)],
    [('reservatorio_2', 40, 90, 50, 15, 95, 0, 0, 355, 0)],
    [('reservatorio_3', 40, 90, 50, 15, 95, 0, 0, 370, 0)],
    [('reservatorio_4', 40, 90, 50, 15, 95, 0, 0, 580, 0)],
    [('reservatorio_5', 40, 90, 50, 15, 95, 0, 0, 920, 0)],
    [('reservatorio_6', 40, 90, 50, 15, 95, 0, 0, 645, 0)],
)

sql_atualizar_nivel_atual_reservatorios = """UPDATE reservatorios set nivel_atual = ? WHERE nome = ?"""
sql_atualizar_bloqueio_reservatorios = """UPDATE reservatorios set bloqueado = ? WHERE nome = ?"""
sql_atualizar_niveis_reservatorios = \
    """UPDATE reservatorios set nivel_minimo = ?, 
    nivel_maximo = ?, alarme_minimo = ?, alarme_maximo = ?, offset_minimo = ?, offset_maximo = ? WHERE nome = ?"""
