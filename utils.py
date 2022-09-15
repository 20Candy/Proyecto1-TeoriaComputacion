def cerraduraEpsilon(estado, transiciones, estados = []):
    if estado not in estados:
        estados.append(estado)
    # /si hay transiciones con E, se recorre y para cada una vuelve a hacer la cerradura
    if (len(transiciones[estado]["E"]) > 0):
        for i in transiciones[estado]["E"]:
            if i not in estados:
                estados.append(i)
            cerraduraEpsilon(i, transiciones, estados)
    return estados


def cerraduraEpsilon_s(estados, transiciones):
    estados_finales = []
    # se recorre cada estado
    for i in estados:
        estado_ = []
        estado_ = cerraduraEpsilon(i, transiciones, [])
        estados_finales.append(estado_)


    estados_finales_ = []
    for j in estados_finales:
        for k in j:
            estados_finales_.append(k)

    # Se eliminan duplicados
    estados_finales_ = list(set(estados_finales_))
    estados_finales_.sort()

    return estados_finales_

# Hasta donde se puede llegar con un caracter segun un conjunto de estados
def mover(estados, caracter, transiciones):
    estados_movidos = []
    for i in estados:
        for llave, valor in transiciones.items():
            if llave == i:
                # si hay transicion para la letra, entonces agrega ese estado
                if len(valor[caracter]) > 0:
                    for st in valor[caracter]:
                        if st not in estados_movidos:
                            estados_movidos.append(st)
    return estados_movidos
