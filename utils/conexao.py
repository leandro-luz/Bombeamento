from pymodbus.client.sync import ModbusTcpClient

base_entradas = 8264
base_saidas = 8192
base_alarmes = 0


def ler_clp(host, port, tipo, endereco=0):
    """ Função para ler as informações do CLP  """
    try:
        lista = []
        # cria um socket
        client = ModbusTcpClient(host, port, timeout=1)
        # realiza a conexao
        client.connect()
        # realiza a consulta do clp
        if tipo == "saidas":
            lista = client.read_coils(base_saidas, 8, units=1).bits
        if tipo == "alarmes":
            lista = client.read_discrete_inputs(endereco, 8, units=1).bits
        if tipo == "remoto":
            lista = client.read_coils(base_entradas, 8, units=1).bits
        # fecha a conexao
        client.close()
        return True, lista
    except:
        return False, None


def escrever_clp(host, port, endereco):
    """ Função para escrever um bit no endereço do CLP """
    try:
        # cria um socket
        client = ModbusTcpClient(host, port, timeout=1)
        # realiza a conexao
        client.connect()
        # gera um pulso no endereco informado
        client.write_coil(base_entradas + endereco, 1)
        client.write_coil(base_entradas + endereco, 0)
        # fecha a conexao
        client.close()
        return True
    except:
        return False
