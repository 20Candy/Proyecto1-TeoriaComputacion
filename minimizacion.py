import copy
import graphviz

class Minimizacion:
    def __init__(self, transiciones, estados, alfabeto, estado_inicial, estados_aceptacion):
        self.transiciones = transiciones
        self.estados = estados
        self.alfabeto = alfabeto
        self.estado_inicial = estado_inicial
        self.estados_aceptacion = estados_aceptacion

        self.transiciones2 = []
        self.estados2 = []
        self.alfabeto2 = []
        self.estado_inicial2 = []
        self.estados_aceptacion2 = []

    def minimizar(self):
        # Se crea un diccionario con