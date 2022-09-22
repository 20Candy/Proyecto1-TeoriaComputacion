import copy
import graphviz
import itertools

class Minimizacion:
    def __init__(self, info, r):
        self.infix = r
        self.transicionesOriginales = list(info["transiciones"])
        self.transiciones = copy.deepcopy(self.transicionesOriginales)

        self.estados = list(info["estados"])
        self.alfabeto = list(info["alfabeto"])
        self.inicio = list(info["inicio"])
        self.estados_aceptacion = list(info["final"])

        self.transiciones2 = [[]]
        self.estados2 = []
        self.inicio2 = []
        self.estados_aceptacion2 = []

        self.states = []
        self.conjuntos = [] # Conjuntos de estados equivalentes

        self.minimizar()
        self.simplifyEstados()
        self.Graph()

    def simplifyEstados(self):
        for i in self.transiciones2:
            for j in i:
                if(j in self.estados2):
                    if(j in self.states):
                        pass
                    else:
                        self.states.append(j)
        

    def minimizar(self):
        #reference https://en.wikipedia.org/wiki/DFA_minimization
        s = set(self.estados_aceptacion)
        temp3 = [x for x in self.estados if x not in s]

        P = [set(self.estados_aceptacion),set(temp3)]
        W = [set(self.estados_aceptacion),set(temp3)]

        while len(W) != 0:
            A = W[0]
            W.remove(A)

            
            for c in self.alfabeto:
                X = set()
                for i in self.transiciones:
                    from_state,transition,to_state = i[0], i[1], i[2]
                    if c == transition and to_state in A:
                        X.update(set([from_state]))

                for Y in P:
                    if (len(X.intersection(Y)) != 0 and len(Y.difference(X)) != 0):
                        P.remove(Y)
                        P.append(X.intersection(Y))
                        P.append(Y.difference(X))

                        if Y in W:
                            W.remove(Y)
                            W.append(X.intersection(Y))
                            W.append(Y.difference(X))
                        else :
                            if len(X.intersection(Y)) <= len (Y.difference(X)):
                                W.append(X.intersection(Y))
                            else :
                                W.append(Y.difference(X))

        self.conjuntos = P
        self.conjuntos = sorted(self.conjuntos, key=len, reverse=True)
        self.conjuntos = sorted(self.conjuntos, key=lambda x: list(x))
        
        transicionesTemp = []

        for i in self.conjuntos:
            index = str(self.conjuntos.index(i))
            self.estados2.append(index)

        for conjunto in self.conjuntos:
            
            for estado in conjunto:

                #estados aceptacion
                if estado in self.estados_aceptacion:
                    index = self.conjuntos.index(conjunto)
                    index = str(index)
                    if index not in self.estados_aceptacion2:
                        self.estados_aceptacion2.append(index)

                #estados inicio
                if estado in self.inicio:
                    index = self.conjuntos.index(conjunto)
                    index = str(index)
                    if index not in self.inicio2:
                        self.inicio2.append(index)

                #transiciones
                for transicion in self.transiciones:
                    if estado == transicion[0]:
                        index = self.conjuntos.index(conjunto)
                        index = str(index)

                        index2 = self.conjuntos.index(
                            [x for x in self.conjuntos if transicion[2] in x][0]
                        )
                        index2 = str(index2)
                        
                        transicionesTemp.append([index, transicion[1], index2])

        transicionesTemp.sort()
        self.transiciones2 = list(transicionesTemp for transicionesTemp,_ in itertools.groupby(transicionesTemp))
                
    def Graph(self):
        try:
            q0 = self.inicio2[0]
        except:
            self.inicio2.append("0")
            q0 = "0"

        F = set(self.estados_aceptacion2)

        dot_subconjuntos = graphviz.Digraph(comment="Minimizacion")
        dot_subconjuntos.attr(rankdir='LR', size='15')
        tempStr = str("\AFD: Minimizacion ["+self.infix+"]")
        dot_subconjuntos.attr(label=tempStr)
        dot_subconjuntos.attr(fontsize='20')
        dot_subconjuntos.attr('node', shape='circle')

        dot_subconjuntos.node("", shape='none',height='0',width='0')

        for i in self.states:
            if(i in F):
                if(i == q0):
                    dot_subconjuntos.node(i,i, shape='doublecircle')
                    dot_subconjuntos.edge("", i)
                else:
                    dot_subconjuntos.node(i,i, shape='doublecircle')
            elif(i in q0):
                dot_subconjuntos.node(i,i)
                dot_subconjuntos.edge("", i)
            else:
                dot_subconjuntos.node(i,i)

        for i in self.transiciones2:
            dot_subconjuntos.edge(i[0], i[2], i[1])
    
        self.finalInfo = {}
        for j in self.states:
            self.finalInfo[j] = {}
        
            for k in self.alfabeto:
                self.finalInfo[j][k] = []

                for l in self.transiciones2:
                    if(l[0] == j and l[1] == k):
                        self.finalInfo[j][k].append(l[2])
        
        dot_subconjuntos.render(directory='output', filename='Minimizado')

        expresion = "\nEXPRESION REGULAR: "+self.infix
        estados = "\nESTADOS: ["+', '.join(self.states)+"]"
        simbolos = "\nSIMBOLOS: ["+', '.join(self.alfabeto)+"]"
        inicio = "\nINICIO: ["+', '.join(self.inicio2)+"]"
        aceptacion = "\nACEPTACION: ["+', '.join(self.estados_aceptacion2)+"]"

        #make self.transiciones more readable
        temp = ""
        for i in self.transiciones2:
            if(i == self.transiciones2[-1]):
                temp = temp + '('+', '.join(i)+')'
            else:
                temp = temp + '('+', '.join(i)+') - '
        
        transiciones = "\nTRANSICIONES: "+temp
        
        #open text file
        text_file = open("output/Minimizado.txt", "w")
        #write string to file
        n = text_file.write(expresion+estados+simbolos+inicio+aceptacion+transiciones)
        #close file
        text_file.close()

        print(expresion+estados+simbolos+inicio+aceptacion+transiciones)
        print("\n")
        
