from conection import conectar_banco
from operacoes_sensor import menu_sensor
from operacoes_leituras import menu_leitura
from operacoes_produto import menu_produto
from operacoes_cip import aplicar_produto

import os


# Função principal para executar o CRUD
def main():
    
    conexao,conectado = conectar_banco()
    while conectado:
        os.system('clear')
        print('-----------Controle Integrado Doencas e Pragas-----------------')
        print("""
        1 - Sensores
        2 - Leituras
        3 - Produtos
        4 - Aplicar Produtos        
        5 - Sair
        """)
        escolha = input('Escolha -> ')

        if escolha.isdigit():
            escolha = int(escolha)
        else:
            escolha = 5
            print('Digite um numero.\nReinicie a Aplicação!')
        os.system('clear')
        match escolha:
            case 1:
                menu_sensor(conexao,conectado)
            case 2:
                menu_leitura(conexao,conectado)
            case 3:
                menu_produto(conexao,conectado)
            case 4:
                aplicar_produto(conexao)
            case 5:
                conexao.close()
                conectado = False
            case _:
                input('Digite um numero entre 1 e 5.')
    else:
        print('Obrigado, por utilizar a nossa Aplicação! :)')
       
 
   

if __name__ == "__main__":
    main()
