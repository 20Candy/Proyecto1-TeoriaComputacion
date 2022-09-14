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

        self.postfix = "ab.c*."
        self.postfix = [x for x in self.postfix]
        self.Thompson(self.postfix)
    
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

            elif i == '?':
                contadorEstados += 4
            
            last = i

        for i in range(contadorEstados):
            self.estados.append(str(i))

    def Thompson(self, postfix):
        #ab.c|
        tempTransicion = []
        temp2Transicion = []
        i = ""

        try:
            i = postfix[-1]
        except:
            return

        if i.isalpha():
            temp = self.estadosCopy.pop(0)
            self.aceptacion.append(temp)

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
                two = []
                three = []

                flag = False
                for i in reversed(postfix):
                    if(flag):
                        three.append(postfix[i])
                    else:
                        three.append(postfix[i])

                self.Thompson(two)
                self.Thompson(one)
            
            elif((postfix[-2].isalpha() == False)):
                postfix.pop()
                if("." in postfix):
                    self.Thompson(postfix)

                else:
                    one = postfix.pop()
                    two = copy.deepcopy(postfix)

                    self.Thompson(two)
                    self.Thompson(one)


        elif i == '*':
            postfix.pop()
            one = postfix.pop()
            two = copy.deepcopy(postfix)

            

            self.Thompson(two)
            self.Thompson(one)
        
        elif i == '|':
            pass

        elif i == '?':
            pass


t = Thompson('ab.c.')
print("\nEXPRESION REGULAR:", t.infix)
print("\nSIMBOLOS: [",', '.join(t.simbolos),"]")
print("ESTADOS: [",', '.join(t.estados),"]")
print("INICIO: [",', '.join(t.inicio),"]")
print("TRANSICIONES:", t.transiciones)
print("\n")
