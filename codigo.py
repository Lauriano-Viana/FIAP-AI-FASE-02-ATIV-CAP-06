import json
import cx_Oracle
import os

# Função para ler dados dos sensores de pragas e doenças
def monitoramento_constante(arquivo_sensores):
    sensores_data = []
    try:
        with open(arquivo_sensores, 'r') as file:
            for line in file:
                # Lê os dados de sensores (formato: id_sensor, tipo, valor)
                id_sensor, tipo, valor = line.strip().split(',')
                sensores_data.append((id_sensor, tipo, float(valor)))
    except Exception as e:
        print(f"Erro ao ler arquivo de sensores: {e}")
    return sensores_data

# Procedimento para registrar uma ação de controle integrado de pragas (CIP)
def controle_integrado(conexao, sensor_data, metodo='quimico'):
    cursor = conexao.cursor()
    # Simula o controle aplicado com base nos dados do sensor
    for id_sensor, tipo, valor in sensor_data:
        if valor > 10:  # Exemplo de critério para acionar o controle
            # Inserir no banco de dados a ação tomada
            cursor.execute(
                """
                INSERT INTO acoes_controle (id_sensor, tipo, valor, metodo)
                VALUES (:1, :2, :3, :4)
                """, (id_sensor, tipo, valor, metodo)
            )
            print(f"Controle {metodo} aplicado no sensor {id_sensor}.")
    conexao.commit()

# Função para ajustar a aplicação de pesticidas e fungicidas com base nos dados
def aplicacao_precisa_produtos(sensor_data, arquivo_aplicacao):
    aplicacao = {}
    for id_sensor, tipo, valor in sensor_data:
        if tipo == 'praga' and valor > 5:
            aplicacao[id_sensor] = 'pesticida'
        elif tipo == 'doenca' and valor > 5:
            aplicacao[id_sensor] = 'fungicida'
    
    # Salva os ajustes em um arquivo JSON
    try:
        with open(arquivo_aplicacao, 'w') as file:
            json.dump(aplicacao, file, indent=4)
        print(f"Ajustes de aplicação salvos em {arquivo_aplicacao}.")
    except Exception as e:
        print(f"Erro ao salvar arquivo JSON: {e}")

# Função para conectar ao banco de dados Oracle
def conectar_banco():
    try:
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='orcl')
        conexao = cx_Oracle.connect(user='seu_usuario', password='sua_senha', dsn=dsn_tns)
        print("Conectado ao banco de dados Oracle")
        return conexao
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def main():
    # Caminhos dos arquivos
    arquivo_sensores = os.path.join('data', 'sensores.txt')
    arquivo_aplicacao = os.path.join('data', 'aplicacao.json')

    # Conectar ao banco de dados Oracle
    conexao = conectar_banco()
    if not conexao:
        return

    # 1. Monitoramento constante (ler dados de sensores)
    sensores_data = monitoramento_constante(arquivo_sensores)
    print(f"Sensores monitorados: {sensores_data}")

    # 2. Controle Integrado de Pragas (CIP)
    controle_integrado(conexao, sensores_data, metodo='quimico')

    # 3. Aplicação precisa de produtos
    aplicacao_precisa_produtos(sensores_data, arquivo_aplicacao)

    # Fechar conexão com o banco
    conexao.close()

if __name__ == '__main__':
    main()
