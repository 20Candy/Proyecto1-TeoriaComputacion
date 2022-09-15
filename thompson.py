import copy
from turtle import pos

class Thompson:
    def __init__(self, infix):
        self.infix = infix
        self.postfix = ''

        self.simbolos = []
        self.estados = []
        self.inicio = ["0"]
        self.aceptacion = []
        self.transiciones = []

        self.getSimbolos()
        self.getEstados()

        self.estadosCopy = copy.deepcopy(self.estados)

        self.postfix = "a*c*."
        self.postfix = [x for x in self.postfix]
        self.postfix2 = copy.deepcopy(self.postfix)
        self.Thompson(self.postfix2)
    
    ##################### FUNCIONES #######################

    def getSimbolos(self):
        unique = list(set(self.infix))

        for i in unique:
            if i.isalpha():
                self.simbolos.append(i)

    def getEstados(self):
        list = [x for x in self.infix]
        contadorEstados = 0
        last = ''

        for i in list:
            if i.isalpha():
                contadorEstados += 2

                if last.isalpha():
                    contadorEstados -= 1

            elif i == '*':
                contadorEstados += 2
            
            elif i == '|':
                contadorEstados += 2
            
            last = i

        for i in range(contadorEstados):
            self.estados.append(str(i))

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
                
                if("." in postfix):
                    one = []
                    two = []

                    flag = False
                    for j in reversed(postfix):
                        if(j == "." or flag):
                            flag = True
                            two.append(j)
                        else:
                            one.append(j)

                    two.reverse()
                    one.reverse()

                    self.Thompson(two)
                    self.Thompson(one)

                else:
                    one = [postfix.pop()]
                    two = []

                    flag = False
                    for j in reversed(postfix):
                        if(j == "*" or flag):
                            flag = True
                            two.append(j)
                        else:
                            one.append(j)

                    two.reverse()
                    one.reverse()

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
                tempTransicion.append("ϵ")
                inicio = self.estadosCopy[0]
                tempTransicion.append(inicio)
                self.transiciones.append(tempTransicion) #[['2', 'ϵ', '3'],]
                tempTransicion = []

                tempTransicion.append(self.estadosCopy[1]) 
                tempTransicion.append("ϵ")
                self.Thompson(one) #THOMPSON ['3', 'c', '4']
                tempTransicion.append(inicio)
                self.transiciones.append(tempTransicion) #['4', 'ϵ', '3']
                tempTransicion = []

                tempTransicion2.append(temp)
                tempTransicion2.append("ϵ")
                tempTransicion2.append(self.estadosCopy[1])
                self.transiciones.append(tempTransicion2)
                tempTransicion2 = []


                temp = self.estadosCopy.pop(0)
                tempTransicion2.append(temp)
                tempTransicion2.append("ϵ")
                tempTransicion2.append(self.estadosCopy[0])
                self.transiciones.append(tempTransicion2)   #['4', 'ϵ', '5']
                tempTransicion2 = []



  
        
        elif i == '|':
            pass


t = Thompson('a*c*.')
print("\nEXPRESION REGULAR:", t.postfix)
print("\nSIMBOLOS: [",', '.join(t.simbolos),"]")
print("ESTADOS: [",', '.join(t.estados),"]")
print("INICIO: [",', '.join(t.inicio),"]")
print("TRANSICIONES:", t.transiciones)
print("\n")
