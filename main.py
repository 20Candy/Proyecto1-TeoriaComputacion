from subconjuntos import subconjuntos
from simulacion import simulacion_AFD, simulacion_AFN
from thompson import Thompson
from minimizacion import Minimizacion
from postfix import InfixToPostfix, readExp
import copy
from timeit import default_timer as timer

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
w = "abba"          #no pertenece


x = True
sub_afd_transiciones = {}
alfabeto_exp = []
dic_transiciones = {}
acpEstados = []

while x:
    menu = input("\n1. Postfix \n2. AFN con Thomson \n3. AFN a AFD \n4. AFD directo \n\n5. Minimización AFD (subconjuntos) \n6. Minimización AFD (directo) \n\n7. Simulación AFN \n8. Simulación AFD (subconjuntos) \n9. Simulación AFD (directo) \n10. Simulación AFD minimizado (subconjuntos) \n11. Simulación AFD minimizado (directo) \n\n12. Salir \n" )

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

        sub_afd_transiciones, info = subconjuntos(r,w, copy.deepcopy(alfabeto_exp), copy.deepcopy(dic_transiciones), acpEstados)

    elif menu == "4":               #todo @perdomo
        print("\nAFD directo")
    
    elif menu == "5":
        print("\nMinimización AFD (subconjuntos)")

        #si no se habia creado thomson primero
        if alfabeto_exp == []:
            t = Thompson(r)
            alfabeto_exp= t.simbolos
            dic_transiciones = t.finalInfo
            acpEstados = int(t.aceptacion[0])

        sub_afd_transiciones, info = subconjuntos(r,w, copy.deepcopy(alfabeto_exp), copy.deepcopy(dic_transiciones), acpEstados)
        m = Minimizacion(info, r)
    
    elif menu == "6":              #todo @stefano cuando termine perdomo
        print("\nMinimización AFD (directo)")

    elif menu == "7":
        print("\nSimulación AFN")

        #si no se ha habia creado thomson primero
        if(alfabeto_exp == []):
            #llamar a thomson primero
            t = Thompson(r)
            alfabeto_exp= t.simbolos
            dic_transiciones = t.finalInfo
            acpEstados = int(t.aceptacion[0])

        #Simulacion con AFN
        start = timer()
        simulacion_afn = simulacion_AFN(w, copy.deepcopy(dic_transiciones), str(acpEstados-1))
        end = timer()
        print("cadena a verificar: ", w)
        print("\nAFN: la cadena pertenece.") if simulacion_afn else print("\nAFN: la cadena no pertenece.")
        print("Tiempo de simulación:",end - start)

    elif menu == "8":
        print("\nSimulación AFD (subconjuntos)")

        #si no se ha habia creado thomson primero
        if(alfabeto_exp == []):
            #llamar a thomson primero
            t = Thompson(r)
            alfabeto_exp= t.simbolos
            dic_transiciones = t.finalInfo
            acpEstados = int(t.aceptacion[0])

        #si no se ha creado subconjuntos primero
        if(len(sub_afd_transiciones.keys()) == 0):
            sub_afd_transiciones, info = subconjuntos(r,w, copy.deepcopy(alfabeto_exp), copy.deepcopy(dic_transiciones), acpEstados)
                
        #Simulacion AFD con subconjuntos
        print("cadena a verificar: ", w)
        start = timer()
        simulacionSub = simulacion_AFD(sub_afd_transiciones, w, str(str(acpEstados-1)))
        end = timer()
        print("\nAFD (subconjuntos): La cadena pertenece") if simulacionSub else print("\nAFD (subconjuntos): La cadena no pertenece")
        print("Tiempo de simulación:",end - start)

    elif menu == "9":   #todo @carol cuando termine perdomo
        print("\nSimulación AFD (directo)")

    elif menu == "10":  #todo @carol
        print("\nSimulación AFD (minimizado subconjuntos)")

    elif menu == "11":  #todo @carol cuando termine perdomo y stefano
        print("\nSimulación AFD (minimizado directo)")

    elif menu == "12":
        print("\nSalir")
        x = False

    else:
        print("\nOpción no válida\n")