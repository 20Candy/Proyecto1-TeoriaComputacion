from subconjuntos import subconjuntos
from simulacion import simulacion_AFD, simulacion_AFN
from thompson import Thompson
from postfix import InfixToPostfix, readExp

x = True
r = "(b|b)*abb(a|b)*"
w = "babbbaaaaab"  #pertenece
#w = "ab"          #no pertenece
sub_afd_transiciones = {}
alfabeto_exp = []
dic_transiciones = {}
acpEstados = []

while x:
    menu = input("1. Postfix \n2. AFN con Thomson \n3. AFN a AFD \n4. AFD directo \n5. Minimizació AFD \n6. Simulación AFN y AFD\n7.Salir \n" )

    if menu == "1":
        print("Postfix")

    elif menu == "2":
        print("AFN con Thomson")
        t = Thompson('(b|b)*abb(a|b)*')
    
    elif menu == "3":
        print("AFN a AFD")

        #Viene de Thompson
        alfabeto_exp= ['a', 'b', 'E']
        dic_transiciones= {'S0': {'a': [], 'b': [], 'E': ['S7']}, 'S1': {'a': [], 'b': ['S2'], 'E': []}, 'S2': {'a': [], 'b': [], 'E': ['S6']}, 'S3': {'a': [], 'b': ['S4'], 'E': []}, 'S4': {'a': [], 'b': [], 'E': ['S6']}, 'S5': {'a': [], 'b': [], 'E': ['S1', 'S3']}, 'S6': {'a': [], 'b': [], 'E': ['S8', 'S5']}, 'S7': {'a': [], 'b': [], 'E': ['S5', 'S8']}, 'S8': {'a': ['S10'], 'b': [], 'E': []}, 'S9': {'a': [], 'b': [], 'E': []}, 'S10': {'a': [], 'b': ['S12'], 'E': []}, 'S11': {'a': [], 'b': [], 'E': []}, 'S12': {'a': [], 'b': ['S14'], 'E': []}, 'S13': {'a': [], 'b': [], 'E': []}, 'S14': {'a': [], 'b': [], 'E': ['S19', 'S22']}, 'S15': {'a': ['S16'], 'b': [], 'E': []}, 'S16': {'a': [], 'b': [], 'E': ['S20']}, 'S17': {'a': [], 'b': ['S18'], 'E': []}, 'S18': {'a': [], 'b': [], 'E': ['S20']}, 'S19': {'a': [], 'b': [], 'E': ['S15', 'S17']}, 'S20': {'a': [], 'b': [], 'E': ['S22', 'S19']}, 'S21': {'a': [], 'b': [], 'E': []}, 'S22': {'a': [], 'b': [], 'E': []}} 
        acpEstados = 23  #lestado de aceptacion de thomson

        sub_afd_transiciones = subconjuntos(r,w, alfabeto_exp, dic_transiciones, acpEstados)
    
    elif menu == "4":
        print("AFD directo")
    
    elif menu == "5":
        print("Minimizació AFD")

    elif menu == "6":
        print("Simulación AFN y AFD")

        #Llamar data necesearia para la simulacion
        
        if(alfabeto_exp == []):
            #llamar a thomson primero
            alfabeto_exp= ['a', 'b', 'E']
            dic_transiciones= {'S0': {'a': [], 'b': [], 'E': ['S7']}, 'S1': {'a': [], 'b': ['S2'], 'E': []}, 'S2': {'a': [], 'b': [], 'E': ['S6']}, 'S3': {'a': [], 'b': ['S4'], 'E': []}, 'S4': {'a': [], 'b': [], 'E': ['S6']}, 'S5': {'a': [], 'b': [], 'E': ['S1', 'S3']}, 'S6': {'a': [], 'b': [], 'E': ['S8', 'S5']}, 'S7': {'a': [], 'b': [], 'E': ['S5', 'S8']}, 'S8': {'a': ['S10'], 'b': [], 'E': []}, 'S9': {'a': [], 'b': [], 'E': []}, 'S10': {'a': [], 'b': ['S12'], 'E': []}, 'S11': {'a': [], 'b': [], 'E': []}, 'S12': {'a': [], 'b': ['S14'], 'E': []}, 'S13': {'a': [], 'b': [], 'E': []}, 'S14': {'a': [], 'b': [], 'E': ['S19', 'S22']}, 'S15': {'a': ['S16'], 'b': [], 'E': []}, 'S16': {'a': [], 'b': [], 'E': ['S20']}, 'S17': {'a': [], 'b': ['S18'], 'E': []}, 'S18': {'a': [], 'b': [], 'E': ['S20']}, 'S19': {'a': [], 'b': [], 'E': ['S15', 'S17']}, 'S20': {'a': [], 'b': [], 'E': ['S22', 'S19']}, 'S21': {'a': [], 'b': [], 'E': []}, 'S22': {'a': [], 'b': [], 'E': []}} 
            acpEstados = 23 

        if(len(sub_afd_transiciones.keys()) == 0):
            sub_afd_transiciones = subconjuntos(r,w, alfabeto_exp, dic_transiciones, acpEstados)  
                

        #Simulacion AFD con subconjuntos
        print("cadena a verificar: ", w)
        simulacionSub = simulacion_AFD(sub_afd_transiciones, w, str("S"+str(acpEstados-1)))
        print("\nAFD (subconjuntos): La cadena pertenece") if simulacionSub else print("\nAFD (subconjuntos): La cadena no pertenece")
    
        #Simulacion con AFN
        simulacion_afn = simulacion_AFN(w, dic_transiciones, "S"+str(acpEstados-1))
        print("AFN: la cadena pertenece\n") if simulacion_afn else print("AFN: la cadena no pertenece\n")


    elif menu == "7":
        print("Salir")
        x = False

    else:
        print("Opción no válida")
        x = False