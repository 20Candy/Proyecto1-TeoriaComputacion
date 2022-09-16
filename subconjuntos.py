import graphviz
import ast
from utils import *

def subconjuntos(r,w,alfabeto_exp,dic_transiciones, acpEstados):

    #inicializacion variables
    sub_afd_transiciones = {}
    final = []
    estadosA = []
    transiciones = []
    contador2 = 0

    # Se quita epsilon ya que no existe transiciones con cadena vacia en AFD
    alfabeto_exp.remove("E")

    # Cerradura epsilon de estado inicial de afn
    cerradura_epsilon = cerraduraEpsilon("S0", dic_transiciones, [])
    cerradura_epsilon.sort()

    # Diccionario de transiciones de AFD, la llave son los conjuntos de estados
    sub_afd_transiciones[str(cerradura_epsilon)] = {
        "Estado del AFD": str(contador2),
    }

    # Transiciones con cada uno si existe
    for i in alfabeto_exp:
        sub_afd_transiciones[str(cerradura_epsilon)][i] = None

    contador2 += 1
    continuar = True
    while(continuar):
        sub_afd_long = len(sub_afd_transiciones)
        estados_afd = list(sub_afd_transiciones.keys())
        # Se recorre el diccionario
        for j in estados_afd:
            # Se recorre cada uno de los elementos
            for i in alfabeto_exp:
                if sub_afd_transiciones[j][i] == None:
                    nuevo_estado = []
                    split = ast.literal_eval(j)
                    nuevo_estado = cerraduraEpsilon_s(mover(split, i, dic_transiciones), dic_transiciones)

                    # Si el conjunto no es llave de diccionario, se agrega como nueva llave y se actualiza las transiciones
                    if len(nuevo_estado) > 0:
                        if str(nuevo_estado) not in sub_afd_transiciones:
                            sub_afd_transiciones[str(nuevo_estado)] = {
                                "Estado del AFD": str(contador2)
                            }
                            for letter in alfabeto_exp:
                                sub_afd_transiciones[str(nuevo_estado)][letter] = None
                            contador2 +=1
                            sub_afd_transiciones[j][i] = sub_afd_transiciones[str(nuevo_estado)]["Estado del AFD"]
                        # Si ya estaba en la lista, se agrega el estado nuevo a la transicion evaluada 
                        else:
                            sub_afd_transiciones[j][i] = sub_afd_transiciones[str(nuevo_estado)]["Estado del AFD"]
        final_size = len(sub_afd_transiciones)
        if sub_afd_long == final_size:
            continuar = not all(sub_afd_transiciones.values())


    # Dibujo AFD por subconjuntos  con graphiz
    dot_subconjuntos = graphviz.Digraph(comment="AFD")
    dot_subconjuntos.attr(rankdir='LR', size='15')
    dot_subconjuntos.attr(label="\nAFD: Subconjuntos")
    dot_subconjuntos.attr(fontsize='20')
    dot_subconjuntos.attr('node', shape='circle')

    # Se dibujan los nodos de afd por subconjuntos
    for i in sub_afd_transiciones.keys():
        estados = ast.literal_eval(i)
        if ("S"+str(acpEstados-1)) in estados:
            final.append(sub_afd_transiciones[i]["Estado del AFD"])
            dot_subconjuntos.node(sub_afd_transiciones[i]["Estado del AFD"], sub_afd_transiciones[i]["Estado del AFD"], shape='doublecircle')
        else:
            dot_subconjuntos.node(sub_afd_transiciones[i]["Estado del AFD"], sub_afd_transiciones[i]["Estado del AFD"])
            

    for llave, valor in sub_afd_transiciones.items():
        for j in alfabeto_exp:
            if valor["Estado del AFD"] != None and valor[j] != None:
                estados = ast.literal_eval(llave)

                # Estado final
                if ("S"+str(acpEstados-1)) in estados:
                    dot_subconjuntos.node(valor["Estado del AFD"], valor["Estado del AFD"],  shape='doublecircle')
                else:
                    dot_subconjuntos.node(valor["Estado del AFD"], valor["Estado del AFD"])
                dot_subconjuntos.node(valor[j], valor[j])
                dot_subconjuntos.edge(valor["Estado del AFD"], valor[j], j)

                transiciones.append([valor["Estado del AFD"], j, valor[j]])

    dot_subconjuntos.render(directory='output', filename='Subconjuntos')


    #generacion de txt con datos de AFD por subconjuntos
    for i in range (contador2):
        estadosA.append(str(i))
    estructura = {

        "estados": estadosA,
        "alfabeto": alfabeto_exp,
        "inicio": [0],
        "final": final,
        "transiciones": transiciones
    }

    with open("output/subconjutnos.txt", 'w') as f: 
        for key, value in estructura.items(): 
            f.write('%s:%s\n' % (key, value))

    return sub_afd_transiciones