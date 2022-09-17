exp = []
operators = ['*', '|', '.', '(', ')']
ops = {'*': 3, '.': 2, '|': 1}


#Función necesaria para leer la expresión regular y agregar los operadores de concatenación
def readExp(exp):
    infix = []
    abc = [] 
    symbols = ['*', '|', '(', ')']
    #exp = input('Ingrese la expresion regular: \n')
    exp2 = ''
    for e in exp:
        infix.append(e)
        if e not in symbols and e not in abc:
            abc.append(e)
    size = len(infix)
    kleene = False
    waiting  = 0
    while size > 0:
        if size > 1:
            v1 = infix[size-1]
            v2 = infix[size-2]
            if kleene:
                if waiting > 0:
                    waiting -= 1
                    kleene = False                    
                    waiting = 0
            elif v1 == '*' and not kleene:
                kleene = True
                waiting = 1
            if (v1 == '(' and v2 in abc and not kleene) or (v1 in abc and v2 == ')' and not kleene) or (v1 in abc and v2 in abc and not kleene) or (v1 == '(' and v2 == ')' and not kleene) or (v1 in abc and v2 == '*' and not kleene) or (v1 == '(' and v2 == '*' and not kleene):
                exp2 = '.' + v1 + exp2
            else:
                exp2 = v1 + exp2
            size -= 1
        else:
            v1 = infix[size-1]
            exp2 = v1 + exp2
            size -= 1
    #exp2 = exp2 + '.#'
    return exp2

#Basado en el algortimo de Shunting-yard
def InfixToPostfix(exp):
    OpStack = []
    postfix = []
    for e in exp:
        #If the input symbol is a letter… append it directly to the output queue
        if e not in operators:
            postfix.append(e)
        else:
            if e == '(':
                OpStack.append(e)
            elif e == ')' and OpStack[-1] != '(' and len(OpStack) > 0:
                while OpStack[-1] != '(':
                    postfix.append(OpStack.pop())
                OpStack.pop()
            else:
                if len(OpStack) > 0:
                    while len(OpStack) > 0 and OpStack[-1] != '(' and ops[e] <= ops[OpStack[-1]]:
                        postfix.append(OpStack.pop())
                OpStack.append(e)
    while len(OpStack) > 0:
        postfix.append(OpStack.pop())
    postfix.append('#')
    postfix.append('.')
    exp_postfix = ''.join(postfix)
    return exp_postfix