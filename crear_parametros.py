import pandas as pd
from os import path

FOLDER_PATH = './/archivos'

def read_excel_column(file_name, column_name):
    path_to_file = path.join(FOLDER_PATH, file_name)
    data = pd.read_excel(path_to_file)
    return data[column_name].tolist()

def read_and_remove_first_element(file_name):
    path_to_file = path.join(FOLDER_PATH, file_name)
    data = pd.read_excel(path_to_file)
    lista_excel = data.values.tolist()

    for fila in lista_excel:
        fila.pop(0)

    return lista_excel

def cc_h():
    return read_excel_column('CC_h.xlsx', 'costo')

def ed_h():
    return read_excel_column('ED_h.xlsx', 'emisiones')

def me_h():
    return read_excel_column('ME_h.xlsx', 'maximo')

def CV():
    return read_excel_column('otros_parametros.xlsx', 'costo fijo bodega')[0]

def V():
    return read_excel_column('otros_parametros.xlsx', 'capacidad maxima de inventario')[0]

def ca_qt():
    return read_and_remove_first_element('CA_qt.xlsx')

def u_qt():
    return read_and_remove_first_element('U_qt.xlsx')

def c_qt():
    return read_and_remove_first_element('C_qt.xlsx')
