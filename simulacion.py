import ast
from utils import *

def simulacion_AFD(transiciones, w, final):
    current_state = "0"
    in_estado = False
    for i in w:
        llave = ""
        for key, v in transiciones.items():
            if v["Estado del AFD"] == current_state and v[i] != None:
                llave = key
            elif v["Estado del AFD"] == current_state and v[i] == None:
                return False
        current_state = transiciones[llave][i]
    for llave, valor in transiciones.items():
        if valor["Estado del AFD"] == current_state:
            estado = ast.literal_eval(llave)
            for i in final:
                if i in estado:
                    in_estado = True

    return in_estado


def simulacion_AFN(w, transiciones, estado_final):
    estados = cerraduraEpsilon("0", transiciones, [])
    contador = 1
    w += "·"
    inicio = w[0]
    while inicio != "·":
        estados = cerraduraEpsilon_s(mover(estados, inicio, transiciones), transiciones)
        inicio = w[contador]
        contador += 1
    if estado_final in estados:
        return True
    else:
        return False