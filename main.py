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
s_q =  

#---------------------------------------- Variables ----------------------------------------#

# Si el dron d ∈ {1, ..., D} se est ́a cargando en cargador c ∈ {1, ..., C} en hora h ∈ {1, ..., H} del d ́ıa t ∈ {t, ..., T}.
DC_dcht = model.addVars(D, C, H, T, vtype=GRB.BINARY, name="DC_dcht")

# Si el dron d ∈ D lleva el paquete p ∈ P del producto q ∈ Q en la hora h ∈ H a la ubicaci ́on f ∈ F en el d ́ıa t ∈ T
XE_dqhft = model.addVars(D, Q, H, F, T, vtype=GRB.BINARY, name="XE_dqhft")

# Porcentaje de batería restante del dron d en la hora del día t.
PB_dht = model.addVars(D, H, T, vtype=GRB.CONTINUOUS, name="PB_dht")

# Inventario del producto q ∈ {1, ..., Q} en el d ́ıa t ∈ {1, ..., T }.
I_qt = model.addVars(Q, T, vtype=GRB.CONTINUOUS, name="I_qt")

# Unidades del producto q que llegan a la bodega en cierto d ́ıa t
E_qt = model.addVars(Q, T, vtype=GRB.CONTINUOUS, name="DY_pqf")

model.update()

#---------------------------------------- Restricciones ----------------------------------------#

# Restricción 1
model.addConstrs((quicksum(XE_dqhft[d,q,h,f,t] for t in T for f in F for d in D for h in H)for q in Q), name = "R1")

# Restricción 2
model.addConstrs((I_qt[q,t] == I_qt[q, t-1] + E_qt[q, t] - quicksum(XE_dqhft[d,q,h,f,t] for d in D for f in F for h in H) for q in Q for t in T), name = "R2")
model.addConstrs((I_qt[q, 1] == S_q[q] for q in Q), name = "R2.2")

# Restricción 3
model.addConstrs((me_h[h] <= quicksum(DC_dcht[d,c,h,t]*ed_h for d in D for c in C) for h in H for t in T), name = "R3")

# Restricción 4
model.addConstrs((quicksum(DC_dcht[d,c,h,t] for d in D for c in C) <= C for h in H for t in T), name = "R4")

# Restricción 5
model.addConstrs((quicksum(XE_dqhft[d,q,h,f,t] for q in Q for f in F) + quicksum(DC_dcht[d,c,h,t] for c in C) <= 1 for d in D for h in H for t in T), name = "R5")

# Restricción 6
model.addConstrs((DC_dcht[d,c,h,t] + PB_dht[d,h,t] < 101 for d in D for c in C for h in H for t in T), name = "R6")

# Restricción 7
model.addConstrs((PB_dht[d,h,t] == PB_dht[d,h-1,t] + 20*quicksum(DC_dcht[d,c,h,t] for c in C) - 20*quicksum(XE_dqhft[d,q,h,f,t] for q in Q for f in F) for d in D for h in H for t in T), name = "R7")

# Restricción 8
model.addConstrs((PB_dht[d,1,1] == 1 for d in D), name = "R8")
# Restricción 9
model.addConstrs((PB_dht[d,h,t] == PB_dht[d,12,t-1] for d in D for h in H for t in range(2,14)), name = "R9")
# Restricción 10
model.addConstrs((PB_dht[d,h,t] <= 100 for d in D for h in H for t in T), name = "R10")

# Restricción 11
model.addConstrs((quicksum(XE_dqhft[d,q,h,f,t] for q in Q for f in F) >= 100 - PB_dht for d in D for h in H for t in T), name = "R11")

# Restricción 12
model.addConstrs((quicksum(DC_dcht[d,c,h,t] for c in C) >= 1 - (10**3)*(1 - quicksum(DC_dcht[d,c,H,t-1] for c in C)) for d in D for h in H for t in T), name = "R12")

# Restricción 13
model.addConstrs((quicksum(DC_dcht[d,c,h,t] for c in C) <= 100 - PB_dht[d,h,t] for d in D for h in H for t in T), name = "R13")

# Restricción 14
model.addConstrs((quicksum(DC_dcht[d,c,h,t] for c in C) <= 1 for d in D for h in H for t in T), name = "R14")

# Restricción 15
model.addConstrs((quicksum(XE_dqhft[d,q,h,f,t] for h in H for d in D for f in F) >= U_qt for q in Q for t in T), name = "R15")

# Restricción 16
model.addConstrs((quicksum(I_qt[q,t] for q in Q) <= V for t in T), name = "R16")

# Restricción 17
model.addConstrs((I_qt >= U_qt for q in Q for t in T), name = "R17")

# Restricción 18
model.addConstrs((quicksum(DC_dcht[d,c,h,t] for c in C) >= 1 - (10**3)*PB_dht[d,h,t] for d in D for h in H for t in T), name = "R18")

# Restricción 19
model.addConstrs((quicksum(XE_dqhft[d,q,h,f,t] for q in Q for f in F) <= 1 for d in D for h in H for t in T), name = "R19")

# Restricción 20
model.addConstrs((quicksum(XE_dqhft[d,q,h,f,t] for h in H for d in D for f in F) >= I_qt for q in Q for t in T), name = "R20")

# Restricción 21
model.addConstrs((quicksum(XE_dqhft[d,q,h,f,t] for q in Q for f in F for d in D) + quicksum(DC_dcht[d,c,h,t] for c in C for d in D) <= D for h in H for t in T), name = "R21")

model.update()
