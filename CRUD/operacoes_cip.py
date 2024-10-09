import cx_Oracle
import pandas as pd
import os

# Função para criar uma aplicação de produto (pesticida/fungicida)
def aplicar_produto(conexao):
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM leituras")
        #Captura os registros e armazena no obj leituras
        leituras = cursor.fetchall()
        for leitura in leituras:
            id_leitura = leitura[0]
            id_sensor = leitura[1]
            valor = leitura[2]
            
        cursor.execute(f""" SELECT * FROM sensores WHERE id_sensor = {id_sensor}""")
        sensores = cursor.fetchall()
        for sensor in sensores:
            tipo = sensor[1]
            area = sensor[3]
            
        
        
        cursor.execute("SELECT * FROM produtos")
        produtos = cursor.fetchall()
        for produto in produtos:
            if tipo == produto[2]:
                id_produto = produto[0]
                dosagem_min = produto[3]
                dosagem_max = produto[4]
                if valor > 30:
                    quantidade_aplicacao = dosagem_max * area
                else:
                    quantidade_aplicacao = dosagem_min * area
                cursor.execute(
                    f"""
                    INSERT INTO aplicacao_produtos (id_aplicacao, id_sensor,id_leitura,id_produto,
                    vl_leitura,quantidade_aplicacao,data_aplicacao) 
                    VALUES (seq_aplicacao_produtos.NEXTVAL, {id_sensor},{id_leitura},{id_produto},{valor},
                    {quantidade_aplicacao},SYSDATE )
                    """
                )
                conexao.commit()
                cursor.close()
        listar_aplicacoes(conexao)
        #print("Ação de controle registrada com sucesso.")
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao criar ação de controle: {e}")


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
        print(f"Erro ao ler leituras: {e}")
    input(' Pressione enter para continuar')
