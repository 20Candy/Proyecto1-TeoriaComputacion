from subconjuntos import subconjuntos

x = True
while x:
    menu = input("1. Postfix \n2. AFN con Thomson \n3. AFN a AFD \n4. AFD directo\n 5. Minimizació AFD\n 6. Simulación AFN y AFD\n" )

    if menu == "1":
        print("Postfix")

    elif menu == "2":
        print("AFN con Thomson")
    
    elif menu == "3":
        print("AFN a AFD")

        r = "(b|b)*abb(a|b)*"
        w = "babbbaaaaab"  #pertenece
        #w = "ab"          #no pertenece

        #Viene de Thompson
        alfabeto_exp= ['a', 'b', 'E']
        dic_transiciones= {'S0': {'a': [], 'b': [], 'E': ['S7']}, 'S1': {'a': [], 'b': ['S2'], 'E': []}, 'S2': {'a': [], 'b': [], 'E': ['S6']}, 'S3': {'a': [], 'b': ['S4'], 'E': []}, 'S4': {'a': [], 'b': [], 'E': ['S6']}, 'S5': {'a': [], 'b': [], 'E': ['S1', 'S3']}, 'S6': {'a': [], 'b': [], 'E': ['S8', 'S5']}, 'S7': {'a': [], 'b': [], 'E': ['S5', 'S8']}, 'S8': {'a': ['S10'], 'b': [], 'E': []}, 'S9': {'a': [], 'b': [], 'E': []}, 'S10': {'a': [], 'b': ['S12'], 'E': []}, 'S11': {'a': [], 'b': [], 'E': []}, 'S12': {'a': [], 'b': ['S14'], 'E': []}, 'S13': {'a': [], 'b': [], 'E': []}, 'S14': {'a': [], 'b': [], 'E': ['S19', 'S22']}, 'S15': {'a': ['S16'], 'b': [], 'E': []}, 'S16': {'a': [], 'b': [], 'E': ['S20']}, 'S17': {'a': [], 'b': ['S18'], 'E': []}, 'S18': {'a': [], 'b': [], 'E': ['S20']}, 'S19': {'a': [], 'b': [], 'E': ['S15', 'S17']}, 'S20': {'a': [], 'b': [], 'E': ['S22', 'S19']}, 'S21': {'a': [], 'b': [], 'E': []}, 'S22': {'a': [], 'b': [], 'E': []}} 
        acpEstados = 23  #lestado de aceptacion de thomson

        subconjuntos(r,w, alfabeto_exp, dic_transiciones, acpEstados)
    
    elif menu == "4":
        print("AFD directo")
    
    elif menu == "5":
        print("Minimizació AFD")

    elif menu == "6":
        print("Simulación AFN y AFD")
    
    else:
        print("Opción incorrecta")
        x = False