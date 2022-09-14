class Thompson:
    def __init__(self, infix):
        self.infix = infix
        self.postfix = ''

        self.simbolos = []
        self.estados = []
        self.inicio = []
        self.aceptacion = []
        self.transiciones = []

        self.getSimbolos()
        self.getEstados()
    
    ##################### FUNCIONES #######################

    def getSimbolos(self):
        unique = list(set(self.infix))

        for i in unique:
            if i.isalpha():
                self.simbolos.append(i)

    def getEstados(self):
        pass

