from subconjuntos import subconjuntos
from simulacion import simulacion_AFD, simulacion_AFN
from thompson import Thompson
from minimizacion import Minimizacion
from postfix import InfixToPostfix, readExp

#PRUEBAS
#verificar esstados de acpetacion
r = "(abba*|(ab)*ba)" 
# r = "(abba)*"   
# r = "(a|b)*" 
#r = "(aa*)|(bb*)" 
#r = "a*b*"
# r = "(b|b)*abb"
# r = "(b|b)*abb(a|b)*"
# r = "a(bb)*"
# r = "(bb)*a"

#r = "(b|b)*abb(a|b)*"
#w = "babbbaaaaab"  #pertenece
w = "ab"          #no pertenece


x = True
sub_afd_transiciones = {}
alfabeto_exp = []
dic_transiciones = {}
acpEstados = []

while x:
    menu = input("1. Postfix \n2. AFN con Thomson \n3. AFN a AFD \n4. AFD directo \n5. Minimizació AFD \n6. Simulación AFN y AFD\n7.Salir \n" )

    if menu == "1":
        print("\nPostfix")
        temp1 = readExp(r)
        postfix = InfixToPostfix(temp1)

        #eliminacion de #.
        size = len(postfix)
        postfix = postfix[:size - 2]

        print(postfix, "\n")

    elif menu == "2":
        print("\nAFN con Thomson")
        t = Thompson(r)

        #instancear variables necesarias para subconjuntos
        alfabeto_exp= t.simbolos
        dic_transiciones = t.finalInfo
        acpEstados = int(t.aceptacion[0])

    elif menu == "3":
        print("\nAFN a AFD")

        #si no se habia creado thomson primero
        if alfabeto_exp == []:
            t = Thompson(r)
            alfabeto_exp= t.simbolos
            dic_transiciones = t.finalInfo
            acpEstados = int(t.aceptacion[0])

        sub_afd_transiciones, info = subconjuntos(r,w, alfabeto_exp, dic_transiciones, acpEstados)
    
    elif menu == "4":
        print("\nAFD directo")
    
    elif menu == "5":
        print("\nMinimización AFD")

        #si no se habia creado thomson primero
        if alfabeto_exp == []:
            t = Thompson(r)
            alfabeto_exp= t.simbolos
            dic_transiciones = t.finalInfo
            acpEstados = int(t.aceptacion[0])

        sub_afd_transiciones, info = subconjuntos(r,w, alfabeto_exp, dic_transiciones, acpEstados)
        m = Minimizacion(info, r)

    elif menu == "6":
        print("\nSimulación AFN y AFD")

        #si no se ha habia creado thomson primero
        if(alfabeto_exp == []):
            #llamar a thomson primero
            t = Thompson(r)
            alfabeto_exp= t.simbolos
            dic_transiciones = t.finalInfo
            acpEstados = int(t.aceptacion[0])

        #si no se ha creado subconjuntos primero
        if(len(sub_afd_transiciones.keys()) == 0):
            sub_afd_transiciones = subconjuntos(r,w, alfabeto_exp, dic_transiciones, acpEstados)  
                

        #Simulacion AFD con subconjuntos
        print("cadena a verificar: ", w)
        simulacionSub = simulacion_AFD(sub_afd_transiciones, w, str(str(acpEstados-1)))
        print("\nAFD (subconjuntos): La cadena pertenece") if simulacionSub else print("\nAFD (subconjuntos): La cadena no pertenece")
    
        #Simulacion con AFN
        simulacion_afn = simulacion_AFN(w, dic_transiciones, str(acpEstados-1))
        print("AFN: la cadena pertenece\n") if simulacion_afn else print("AFN: la cadena no pertenece\n")


    elif menu == "7":
        print("\nSalir")
        x = False

    else:
        print("\nOpción no válida")
        x = False