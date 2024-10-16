import cx_Oracle
import pandas as pd
import os


def calcular_quantidade_aplicacao(vl_leitura, dosagem_min, dosagem_max):
    # Exemplo de regra de aplicação: a quantidade é proporcional à leitura
    quantidade = dosagem_min + (vl_leitura / 100) * (dosagem_max - dosagem_min)
    return quantidade


# Função para listar aplicacoes
def listar_aplicacoes(conexao):
    try:
        lista_dados = [] #lista para captura de dados 
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM aplicacao_produtos ")
        #Captura os registros e armazena no obj aplicacoes
        aplicacoes = cursor.fetchall()
        for aplicacao in aplicacoes:
            lista_dados.append(aplicacao)
        lista_dados = sorted(lista_dados)
        # Gera um Dataframe com os dados da lista usando o Pandas
        dados_df = pd.DataFrame.from_records(lista_dados, columns = ['Id','Id_Sensor','Id_leitura','Id_produto','Leitura','dose_aplicada','data'], 
                                             index ='Id')
        if dados_df.empty:
            print(f'Não há aplicacoes cadastradas!!')
        else:
            print(dados_df)
        cursor.close()
    except cx_Oracle.DatabaseError as e:
        print(f"listar aplic---Erro ao criar aplicacao: {e}")
    except:
        print('Erro desconhecido ---listar aplicacaoes')
        input('Digite enter para continuar')
    else:
        input('Digite enter para continuar')

# Procedimento para criar aplicação de produtos com base na leitura
def aplicar_produto(conexao, id_leitura, id_sensor, valor_leitura):
    cursor = conexao.cursor()
    cursor.execute(f"SELECT tipo FROM sensores WHERE id_sensor = '{id_sensor}'")
    tipo = cursor.fetchone()[0]
    cursor.execute(f"SELECT id_produto, dosagem_min, dosagem_max FROM produtos WHERE tipo = '{tipo}'")
    produto = cursor.fetchone()
    
    if produto:
        id_produto, dosagem_min, dosagem_max = produto
        quantidade_aplicacao = calcular_quantidade_aplicacao(valor_leitura, dosagem_min, dosagem_max)
        # Inserir aplicação de produto
        cursor.execute("""
            INSERT INTO aplicacao_produtos 
            (id_aplicacao, id_sensor, id_leitura, id_produto, vl_leitura, quantidade_aplicacao, data_aplicacao) 
            VALUES (seq_aplicacao_produtos.NEXTVAL, :1, :2, :3, :4, :5, SYSDATE)
        """, (id_sensor, id_leitura, id_produto, valor_leitura, quantidade_aplicacao))
        conexao.commit()
    cursor.close()

def criar_aplicacao(conexao):
    
        cursor = conexao.cursor()
        consulta = f"""SELECT id_leitura, id_sensor, valor FROM leituras """
        cursor.execute(consulta)
        #Captura os registros e armazena no obj leituras
        leituras = cursor.fetchall()
       
        for leitura in leituras:
            id_leitura, id_sensor, valor = leitura            
            aplicar_produto(conexao, id_leitura, id_sensor, valor)
        
        listar_aplicacoes(conexao)
        cursor.close()