from binaryTree import Node
from postfix import InfixToPostfix, readExp
import graphviz

operators = ['*', '|', '.']

#Funcion para determinar si el arreglo a está dentro del arreglo b
def ArrayInArray(a, b):
    r = True
    for e in a:
        if e not in b:
            r = False
    return r

def buildTree(e, exp):
    if e == '*':
        #return Node(e, buildTree(exp[:-1]), None)
        return Node(e, None, buildTree(exp.pop(len(exp)-1), exp))
    elif e == '.' or e == '|':
        #
        return Node(e, buildTree(exp.pop(len(exp)-1), exp), buildTree(exp.pop(len(exp)-1), exp))
    else:
        #
        return Node(e, None, None, len(exp)+1)


#(a|b)*abb
#(a|b)*(a|(bb))*



#Funcion para determinar el AFD directo
def direct_AFD(exp1):

    exp = InfixToPostfix(readExp(exp1))
    exp = list(exp)
    
    tree2 = buildTree(exp.pop(),exp)
    tree2.traversePostOrder()
    print('\n')
    tree2.determineFollowPos()
    i = []
    follow_i = []
    tree2.findi(i)
    for e in i:
        follow_i.append(tree2.searchPos(e).follow_pos)

    j = 0
    follow_pos = {}
    while j < len(i):
        follow_pos[i[j]] = follow_i[j]
        j += 1
    #print(follow_pos)

    unique = [list(x) for x in set(tuple(x) for x in follow_i)]
    
    #order unique
    unique.sort()

    for element in unique:
        if element == []:
            unique.remove(element)

    d = 0
    dstates = {}
    dstates2 = []

    for m in range (len(unique)):
        dstates[m] = unique[m]
        dstates2.append(unique[m])

    """d = 0
    dstates = {}
    dstates[d] = tree2.first_pos
    dstates2 = []
    dstates2.append(tree2.first_pos)"""

    transitions = []
    for e in i:
        temp = tree2.searchPos(e).val
        if temp not in transitions and temp != '#':
            transitions.append(temp)

    StateTransitions = {}
    for e in transitions:
        StateTransitions[e] = {}

    #print(dstates)
    #print(StateTransitions)

    states = []
    while not ArrayInArray(dstates.keys(), states):
        for e in dstates.copy():
            if e not in states:
                states.append(e)
                for t in transitions:
                    temp = []
                    for g in dstates[e]:
                        if tree2.searchPos(g).val == t:
                            for h in tree2.searchPos(g).follow_pos:
                                if h not in temp:
                                    temp.append(h)
                    #print (temp)
                    if temp != []:
                        if temp in dstates.values():
                            StateTransitions[t][e] = list(dstates.keys())[list(dstates.values()).index(temp)]
                        
                        if temp not in follow_i and temp not in dstates2:                            
                            d += 1
                            dstates[d] = temp
                            dstates2.append(temp)
                            #print(e, list(dstates.keys())[list(dstates.values()).index(temp)])
                            StateTransitions[t][e] = list(dstates.keys())[list(dstates.values()).index(temp)]            
    #print(StateTransitions)
    #print(dstates)
    acceptance = []
    for e in dstates:
        for g in dstates[e]:
            if tree2.searchPos(g).val == '#':
                acceptance.append(e)
    estados = []
    estadosTemp = []
    for e in dstates:
        estados.append(e)
    transiciones = []
    for e in StateTransitions:
        for g in StateTransitions[e]:
            if(StateTransitions[e][g] in estados):
                estadosTemp.append(StateTransitions[e][g])
            transiciones.append([g, e, StateTransitions[e][g]])

    estadosTemp = list(set(estadosTemp))
    estados = estadosTemp

    finalInfo = {}
    for j in estados:
        finalInfo[j] = {}
    
        for k in transitions:
            finalInfo[j][k] = []

            for l in transiciones:
                if(l[0] == j and l[1] == k):
                    finalInfo[j][k].append(l[2])

    print('Estados: ', estados)
    print('Alfabeto: ', transitions)
    print('Estado(s) de aceptación: ', acceptance)
    print('Estado inicial: ', 0)
    print('Transiciones: ', transiciones)

    estructura = {
        'estados': estados,
        'alfabeto': transitions,
        "inicio": ['0'],
        'transiciones': transiciones,
        'final': acceptance,
        'transiciones_structura':finalInfo
    }

    with open('output/Directo.txt', 'w') as outfile:
        for key, value in estructura.items():
            outfile.write(key + ': ' + str(value) + '\n')

    dot_subconjuntos = graphviz.Digraph(comment="AFD_Directo")
    dot_subconjuntos.attr(rankdir='LR', size='15')
    tempStr = str("\AFD: Directo ["+exp1+"]")
    dot_subconjuntos.attr(label=tempStr)
    dot_subconjuntos.attr(fontsize='20')
    dot_subconjuntos.attr('node', shape='circle')

    dot_subconjuntos.node("", shape='none',height='0',width='0')

    for i in estados:
        if(i in acceptance):
            if(i == 0):
                dot_subconjuntos.node(str(i),str(i), shape='doublecircle')
                dot_subconjuntos.edge("", str(i))
            else:
                dot_subconjuntos.node(str(i),str(i), shape='doublecircle')
        elif(i == 0):
            dot_subconjuntos.node(str(i),str(i))
            dot_subconjuntos.edge("", str(i))
        else:
            dot_subconjuntos.node(str(i),str(i))

    for i in transiciones:
        dot_subconjuntos.edge(str(i[0]), str(i[2]), str(i[1]))
    
    dot_subconjuntos.render(directory='output', filename='AFD_Directo')

    return estructura
    
#direct_AFD('(a|b)*(a|(bb))*')
#direct_AFD('(a|b)*abb')
