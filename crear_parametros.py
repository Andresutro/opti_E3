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
    cc_h = read_excel_column('CC_h.xlsx', 'costo')
    cch_dict = dict()
    n = 0
    for i in cc_h:
        n += 1
        cch_dict[n] = i
    return cch_dict

def ed_h():
    ed_h = read_excel_column('ED_h.xlsx', 'emisiones')
    edh_dict = dict()
    n = 0
    for i in ed_h:
        n += 1
        edh_dict[n] = i
    return edh_dict

def me_h():
    me_h = read_excel_column('ME_h.xlsx', 'maximo')
    meh_dict = dict()
    n = 0
    for i in me_h:
        n += 1
        meh_dict[n] = i
    return meh_dict

def CV():
    return read_excel_column('otros_parametros.xlsx', 'costo fijo bodega')[0]

def V():
    return read_excel_column('otros_parametros.xlsx', 'capacidad maxima de inventario')[0]

def ca_qt():
    ca_qt = read_and_remove_first_element('CA_qt.xlsx')
    ca_qt_dict = dict()
    n = 0
    for i in ca_qt:
        for j in i:
            n += 1
            ca_qt_dict[(n, ca_qt.index(i) + 1)] = j
    return ca_qt_dict

def u_qt():
    u_qt = read_and_remove_first_element('U_qt.xlsx')
    uqt_dict = dict()
    n = 0
    for i in u_qt:
        for j in i:
            n += 1
            uqt_dict[(n, u_qt.index(i) + 1)] = j
    return uqt_dict

def c_qt():
    c_qt = read_and_remove_first_element('C_qt.xlsx')
    c_qt_dict = dict()
    n = 0
    for i in c_qt:
        for j in i:
            n += 1
            c_qt_dict[(n, c_qt.index(i) + 1)] = j
    return c_qt_dict

