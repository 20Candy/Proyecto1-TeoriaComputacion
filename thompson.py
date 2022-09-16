import copy
import graphviz
from postfix import InfixToPostfix, readExp

class Thompson:
    def __init__(self, infix):
        self.infix = infix

        #instrucciones: bb|*a.b.b.ab|*.
        temp1 = readExp(self.infix)
        self.postfix = InfixToPostfix(temp1)

        #eliminacion de #.
        size = len(self.postfix)
        self.postfix = self.postfix[:size - 2]

        self.postfix = [x for x in self.postfix]
        self.postfix2 = copy.deepcopy(self.postfix)

        if True:
            self.simbolos = []
            self.estados = []
            self.states = []
            self.inicio = ["0"]
            self.aceptacion = []
            self.transiciones = []

            self.getSimbolos()
            self.getEstados()
            self.estadosCopy = copy.deepcopy(self.estados)

            self.Thompson(self.postfix2)
            self.simplifyEstados()

            self.Graph()


    ##################### FUNCIONES #######################

    def getSimbolos(self):
        unique = list(set(self.infix))

        for i in unique:
            if i.isalpha():
                self.simbolos.append(i)

        self.simbolos.append("E")

    def getEstados(self):
        list = [x for x in self.postfix]
        contadorEstados = 0

        for i in list:
            if i.isalpha():
                contadorEstados += 2

            elif i == '*':
                contadorEstados += 2
            
            elif i == '|':
                contadorEstados += 2

        for i in range(contadorEstados):
            self.estados.append(str(i))

    def simplifyEstados(self):
        for i in self.transiciones:
            for j in i:
                if(j in self.estados):
                    if(j in self.states):
                        pass
                    else:
                        self.states.append(j)

        entrada = []
        salida = []

        for i in self.transiciones:
            entrada.append(i[0])
            salida.append(i[2])
        
        s = set(entrada)
        self.aceptacion = [x for x in salida if x not in s]
        self.aceptacion = list(set(self.aceptacion))

    def Thompson(self, postfix):
        #ab.c|
        tempTransicion = []
        tempTransicion2 = []
        i = ""

        try:
            i = postfix[-1]
        except:
            return

        if i.isalpha():
            if len(postfix) > 1:
                postfix.pop()
                self.Thompson(postfix)

            temp = self.estadosCopy.pop(0)

            tempTransicion.append(temp)
            tempTransicion.append(i)
            tempTransicion.append(self.estadosCopy[0])

            self.transiciones.append(tempTransicion)
            tempTransicion = []

        elif i == '.':
            if(postfix[-2].isalpha() and postfix[-3].isalpha()):
                postfix.pop()
                one = postfix.pop()
                two = postfix.pop()
                three = copy.deepcopy(postfix)

                self.Thompson(three)
                self.Thompson(two)
                self.Thompson(one)

            elif(postfix[-2].isalpha() and (postfix[-3].isalpha() == False)):
                postfix.pop()
                one = postfix.pop()
                two = copy.deepcopy(postfix)

                self.Thompson(two)
                self.Thompson(one)
            
            elif((postfix[-2].isalpha() == False)):
                temp = postfix.pop()
                one = []
                two = []
                three = []
                counterOne = 0
                counterTwo = 0
                boolOne = True
                tempBool = True

                for i in reversed(postfix):
                    if(boolOne and (counterOne > 0 or tempBool)):
                        if i == '.':
                            counterOne += 1
                            counterTwo += 1
                        elif i == '|':
                            counterOne += 1
                            counterTwo += 1
                        elif i == '*':
                            counterOne += 1

                    tempBool = False
                    if counterOne == 0:
                        boolOne = False
                    
                    elif(boolOne==False):
                        if i == '.':
                            counterTwo += 1
                        elif i == '|':
                            counterTwo += 1
                        elif i == '*':
                            counterTwo += 1

                    if(boolOne):
                        if i.isalpha():
                            counterOne -= 1
                            one.append(i)
                        else:
                            one.append(i)
                    else:
                        if i.isalpha():
                            counterTwo -= 1
                            two.append(i)
                        else:
                            two.append(i)

                one.reverse()
                two.reverse()

                self.Thompson(two)
                self.Thompson(one)

        elif i == '*':

            if(postfix[-2].isalpha()):
                postfix.pop()
                one = postfix.pop()
                two = copy.deepcopy(postfix)

                self.Thompson(two) #THOMPSON

                
                temp = self.estadosCopy.pop(0)
                tempTransicion.append(temp)
                tempTransicion.append("E")
                inicio = self.estadosCopy[0]
                tempTransicion.append(inicio)
                self.transiciones.append(tempTransicion) #[['2', 'E', '3'],]
                tempTransicion = []

                tempTransicion.append(self.estadosCopy[1]) 
                tempTransicion.append("E")
                self.Thompson(one) #THOMPSON ['3', 'c', '4']
                tempTransicion.append(inicio)
                self.transiciones.append(tempTransicion) #['4', 'E', '3']
                tempTransicion = []

                tempTransicion2.append(temp)
                tempTransicion2.append("E")
                tempTransicion2.append(self.estadosCopy[1])
                self.transiciones.append(tempTransicion2)
                tempTransicion2 = []


                temp = self.estadosCopy.pop(0)
                tempTransicion2.append(temp)
                tempTransicion2.append("E")
                tempTransicion2.append(self.estadosCopy[0])
                self.transiciones.append(tempTransicion2)   #['4', 'E', '5']
                tempTransicion2 = []

            else:
                postfix.pop()
                one = [postfix.pop()]
                two = []

                flag = False
                for j in reversed(postfix):
                    if(len(one) > 1 and (j == "." or j == "|" or j == "*" or flag)):
                        if((len(one)-1)%2 == 0 or flag):

                            if (len(one) == 3):
                                if (one[1].isalpha() and (one[2].isalpha() == False)):
                                    one.append(postfix.pop())
                            else:
                                flag = True
                                two.append(postfix.pop())
                        else:
                            one.append(postfix.pop())
                    else:
                        one.append(postfix.pop())

                    if(one[0] == "." or one[0] == "|"):
                        if (len(one) == 3):
                            if (one[1].isalpha() and one[2].isalpha()):
                                flag = True
                    
                    if(one[0] == "*"):
                        if (len(one) == 2):
                            if (one[1].isalpha()):
                                flag = True

                two.reverse()
                one.reverse()

                three = copy.deepcopy(postfix)
                self.Thompson(three)

                temp = self.estadosCopy.pop(0)
                tempTransicion.append(temp)
                tempTransicion.append("E")
                inicio = self.estadosCopy[0]
                tempTransicion.append(inicio)
                self.transiciones.append(tempTransicion) #[['2', 'E', '3'],]
                tempTransicion = []

                
                self.Thompson(one) #THOMPSON ['3', 'c', '4']
                tempTransicion.append(self.estadosCopy[0]) 
                tempTransicion.append("E")
                tempTransicion.append(inicio)
                self.transiciones.append(tempTransicion) #['4', 'E', '3']
                tempTransicion = []

                tempTransicion2.append(temp)
                tempTransicion2.append("E")
                tempTransicion2.append(self.estadosCopy[1])
                self.transiciones.append(tempTransicion2)
                tempTransicion2 = []


                temp = self.estadosCopy.pop(0)
                tempTransicion2.append(temp)
                tempTransicion2.append("E")
                tempTransicion2.append(self.estadosCopy[0])
                self.transiciones.append(tempTransicion2)   #['4', 'E', '5']
                tempTransicion2 = []
   
        elif i == '|':
            if(postfix[-2].isalpha() and postfix[-3].isalpha()):
                postfix.pop()
                one = postfix.pop()
                two = postfix.pop()
                three = copy.deepcopy(postfix)

                self.Thompson(three)

                inicial = self.estadosCopy.pop(0)
                tempTransicion.append(inicial)
                tempTransicion.append("E")
                route1 = self.estadosCopy[0]
                tempTransicion.append(route1)
                self.transiciones.append(tempTransicion) #[['0', 'E', '1'],]
                tempTransicion = []

                self.Thompson(two) #THOMPSON #[['1', 'A', '2'],]
                finalOne = self.estadosCopy.pop(0)

                tempTransicion.append(inicial)
                tempTransicion.append("E")
                route1 = self.estadosCopy[0]
                tempTransicion.append(route1)
                self.transiciones.append(tempTransicion) #[['', 'E', '3'],]
                tempTransicion = []

                self.Thompson(one) #THOMPSON #[['3', 'A', '4'],]
                finalTwo = self.estadosCopy.pop(0)

                tempTransicion.append(finalOne)
                tempTransicion.append("E")
                route1 = self.estadosCopy[0]
                tempTransicion.append(route1)
                self.transiciones.append(tempTransicion)
                tempTransicion = []

                tempTransicion.append(finalTwo)
                tempTransicion.append("E")
                route1 = self.estadosCopy[0]
                tempTransicion.append(route1)
                self.transiciones.append(tempTransicion)
                tempTransicion = []
            
            elif(postfix[-2].isalpha()):
                postfix.pop()
                zero = [postfix.pop()]
                one = []
                two = []

                flag = False
                for j in reversed(postfix):
                    if(len(one) > 1 and (j == "." or j == "|" or j == "*" or flag)):
                        if((len(one))%2 == 0 or flag):
                            flag = True
                            two.append(postfix.pop())
                        else:
                            one.append(postfix.pop())
                    else:
                        one.append(postfix.pop())

                    if(one[0] == "." or one[0] == "|"):
                        if (len(one) == 3):
                            if (one[1].isalpha() and one[2].isalpha()):
                                flag = True
                    
                    if(one[0] == "*"):
                        if (len(one) == 2):
                            if (one[1].isalpha()):
                                flag = True

                two.reverse()
                one.reverse()

                self.Thompson(two)

                inicial = self.estadosCopy.pop(0)
                tempTransicion.append(inicial)
                tempTransicion.append("E")
                route1 = self.estadosCopy[0]
                tempTransicion.append(route1)
                self.transiciones.append(tempTransicion) #[['0', 'E', '1'],]
                tempTransicion = []

                self.Thompson(one) #THOMPSON #[['1', 'A', '2'],]
                finalOne = self.estadosCopy.pop(0)

                tempTransicion.append(inicial)
                tempTransicion.append("E")
                route1 = self.estadosCopy[0]
                tempTransicion.append(route1)
                self.transiciones.append(tempTransicion) #[['', 'E', '3'],]
                tempTransicion = []

                self.Thompson(zero) #THOMPSON #[['3', 'A', '4'],]
                finalTwo = self.estadosCopy.pop(0)

                tempTransicion.append(finalOne)
                tempTransicion.append("E")
                route1 = self.estadosCopy[0]
                tempTransicion.append(route1)
                self.transiciones.append(tempTransicion)
                tempTransicion = []

                tempTransicion.append(finalTwo)
                tempTransicion.append("E")
                route1 = self.estadosCopy[0]
                tempTransicion.append(route1)
                self.transiciones.append(tempTransicion)
                tempTransicion = []

            else:
                temp = postfix.pop()
                one = [postfix.pop()]
                two = []
                three = []

                counterOne = 2 if one[0] == "." else 1
                counterTwo = 1
                boolOne = True
                tempBool = True

                for i in reversed(postfix):
                    if(boolOne and (counterOne > 0 or tempBool)):
                        if i == '.':
                            counterOne += 1
                            counterTwo += 1
                        elif i == '|':
                            counterOne += 1
                            counterTwo += 1

                    tempBool = False
                    if counterOne == 0:
                        boolOne = False
                    
                    elif(boolOne==False):
                        if i == '.':
                            counterTwo += 1
                        elif i == '|':
                            counterTwo += 1

                    if(boolOne):
                        if i.isalpha():
                            counterOne -= 1
                            one.append(postfix.pop())
                        else:
                            one.append(postfix.pop())
                    else:
                        if i.isalpha():
                            counterTwo -= 1
                            two.append(postfix.pop())
                        else:
                            two.append(postfix.pop())

                one.reverse()
                two.reverse()

                three = copy.deepcopy(postfix)
                self.Thompson(three) 

                inicial = self.estadosCopy.pop(0)
                tempTransicion.append(inicial)
                tempTransicion.append("E")
                route1 = self.estadosCopy[0]
                tempTransicion.append(route1)
                self.transiciones.append(tempTransicion) #[['0', 'E', '1'],]
                tempTransicion = []

                self.Thompson(two) #THOMPSON #[['1', 'A', '2'],]
                finalOne = self.estadosCopy.pop(0)

                tempTransicion.append(inicial)
                tempTransicion.append("E")
                route1 = self.estadosCopy[0]
                tempTransicion.append(route1)
                self.transiciones.append(tempTransicion) #[['', 'E', '3'],]
                tempTransicion = []

                self.Thompson(one) #THOMPSON #[['3', 'A', '4'],]
                finalTwo = self.estadosCopy.pop(0)

                tempTransicion.append(finalOne)
                tempTransicion.append("E")
                route1 = self.estadosCopy[0]
                tempTransicion.append(route1)
                self.transiciones.append(tempTransicion)
                tempTransicion = []

                tempTransicion.append(finalTwo)
                tempTransicion.append("E")
                route1 = self.estadosCopy[0]
                tempTransicion.append(route1)
                self.transiciones.append(tempTransicion)
                tempTransicion = []

    def Graph(self):
        q0 = self.inicio[0]
        F = set(self.aceptacion)

        dot_subconjuntos = graphviz.Digraph(comment="Thompson")
        dot_subconjuntos.attr(rankdir='LR', size='15')
        tempStr = str("\AFN: Thompson ["+self.infix+"]")
        dot_subconjuntos.attr(label=tempStr)
        dot_subconjuntos.attr(fontsize='20')
        dot_subconjuntos.attr('node', shape='circle')

        dot_subconjuntos.node("", shape='none',height='0',width='0')

        for i in self.states:
            if(i in F):
                dot_subconjuntos.node(i,i, shape='doublecircle')
            if(i in q0):
                dot_subconjuntos.node(i,i)
                dot_subconjuntos.edge("", i)
            else:
                dot_subconjuntos.node(i,i)

        for i in self.transiciones:
            dot_subconjuntos.edge(i[0], i[2], i[1])
    
        self.finalInfo = {}
        for j in self.states:
            self.finalInfo[j] = {}
        
            for k in self.simbolos:
                self.finalInfo[j][k] = []

                for l in self.transiciones:
                    if(l[0] == j and l[1] == k):
                        self.finalInfo[j][k].append(l[2])
        
        dot_subconjuntos.render(directory='output', filename='Thompson')

        expresion = "\nEXPRESION REGULAR: "+self.infix
        estados = "\nESTADOS: ["+', '.join(self.states)+"]"
        simbolos = "\nSIMBOLOS: ["+', '.join(self.simbolos)+"]"
        inicio = "\nINICIO: ["+', '.join(self.inicio)+"]"
        aceptacion = "\nACEPTACION: ["+', '.join(self.aceptacion)+"]"

        #make self.transiciones more readable
        temp = ""
        for i in self.transiciones:
            if(i == self.transiciones[-1]):
                temp = temp + '('+', '.join(i)+')'
            else:
                temp = temp + '('+', '.join(i)+') - '
        
        transiciones = "\nTRANSICIONES: "+temp
        
        #open text file
        text_file = open("output/Thompson.txt", "w")
        #write string to file
        n = text_file.write(expresion+estados+simbolos+inicio+aceptacion+transiciones)
        #close file
        text_file.close()

        print(expresion+estados+simbolos+inicio+aceptacion+transiciones)
        print("\n")

#instrucciones:(b|b)*abb(a|b)* 
t = Thompson('a(bb)*')

"""
_________________
ab.b.a*.ab.*b.a.|
(abba*|(ab)*ba)
_________________
ab.b.a.*
(abba)*
_________________
ab|*
(a|b)*
_________________
aa*.bb*.|
(aa*)|(bb*)
_________________
a*b*.
a*b*
_________________
bb|*a.b.b.
(b|b)*abb
_________________
bb|*a.b.b.ab|*
(b|b)*abb(a|b)*
_________________
abb.*.
a(bb)*
_________________
bb.*a.
(bb)*a
"""