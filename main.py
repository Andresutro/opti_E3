from gurobipy import GRB, Model, quicksum
from random import randint, seed, uniform
import pandas as pd
from os import path
from crear_parametros import *
model = Model()
model.setParam("TimeLimit", 1800)  # Establece el tiempo m´aximo en segundos

# SETS
# Conjuntos
T = 14  # Horizonte de decisión: 2 semanas
H = 12  # Horas laborales por día
D = 100 # Total de drones
C = 10 # Total de cargadores para drones 
F = 50 # Total de ubicaciones que solicitan entrega por dron 
Q = 5000 # Total de productos a entregar 

cqt = c_qt()
ca_qt = ca_qt()
u_qt = u_qt()
cc_h = cc_h()
ed_h = ed_h()
me_h = me_h()
cv = CV()
v = V()
# VARIABLES
