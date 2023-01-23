import pandas as pd
import openpyxl
import os


def search_with_name(search_supply_cod):
    data_loc = r'Data\fnd_gfm1.tsv'
    serv_data = pd.read_csv(data_loc, sep='\t', header=0, encoding="ISO-8859-1")
    serv_data = serv_data[['Item','Fornecedor', 'Descrição','Categoria', 'Número', 'Local']]
    
    serv_data = serv_data[serv_data['Item'].astype(str).str[:2] == '25']
    serv_data['Item'] = serv_data['Item'].astype('int64')

    search_supply_cod = search_supply_cod.upper()
    search_data = serv_data[serv_data['Fornecedor'].str.find(search_supply_cod)  != -1]

    search_data = search_data.drop_duplicates(subset=['Item'])
    return search_data


def search_with_cnpj(search_cnpj):
    data_loc = r'Data\fnd_gfm1.tsv'
    serv_data = pd.read_csv(data_loc, sep='\t', header=0, encoding="ISO-8859-1")
    serv_data = serv_data[['Item','Fornecedor', 'Descrição','Categoria', 'Número', 'Local']]

    serv_data = serv_data[serv_data['Item'].astype(str).str[:2] == '25']
    serv_data['Item'] = serv_data['Item'].astype('int64')

    search_data = serv_data[serv_data['Local'].astype(str).str.find(search_cnpj)  != -1]
    search_data = search_data.drop_duplicates(subset=['Item'])

    search_data = search_data.drop_duplicates(subset=['Item'])
    return search_data
