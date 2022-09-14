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
        self.Thompson()
    
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

    def Thompson(self):
        self.postfix = "ab.c|#."

        for i in self.postfix:
            if i.isalpha():
                pass

t = Thompson('(ab)|c')
print("SIMBOLOS:",t.simbolos)
print("ESTADOS:",t.estados)
print("INICIO:",t.inicio)
