from binaryTree import Node
from postfix import InfixToPostfix, readExp

operators = ['*', '|', '.']

def ArrayInArray(a, b):
    r = True
    for e in a:
        if e not in b:
            r = False
    return r

#(a|b)*abb
#(a|b)*(a|(bb))*

exp1 = InfixToPostfix(readExp(input()))
exp = list(exp1)
def buildTree(e, exp):
    if e == '*':
        #return Node(e, buildTree(exp[:-1]), None)
        return Node(e, None, buildTree(exp.pop(len(exp)-1), exp))
    elif e == '.' or e == '|':
        #
        return Node(e, buildTree(exp.pop(len(exp)-1), exp), buildTree(exp.pop(len(exp)-1), exp))
    else:
        #
        return Node(e, None, None, len(exp)+1)

tree2 = buildTree(exp.pop(),exp)
tree2.traversePostOrder()
#tree2.determineFollowPos(follows)
print('\n')
#tree2.post2()
tree2.determineFollowPos()
print('\n')
#tree2.post3()
tree2.post2()
print('\n')
i = []
follow_i = []
tree2.findi(i)
for e in i:
    follow_i.append(tree2.searchPos(e).follow_pos)

d = 0
dstates = {}
dstates[d] = tree2.first_pos

transitions = []
for e in i:
    temp = tree2.searchPos(e).val
    if temp not in transitions and temp != '#':
        transitions.append(temp)

#print(transitions)

StateTransitions = {}
for e in transitions:
    StateTransitions[e] = {}

print(dstates)
print(StateTransitions)


def determineStates(dstates, StateTransitions, transitions, follow_i, i):
    for e in dstates:
        for t in transitions:
            temp = []
            for f in dstates[e]:
                if t in follow_i[i.index(f)]:
                    temp.append(f)
            if len(temp) > 0:
                if temp not in dstates.values():
                    dstates[len(dstates)] = temp
                StateTransitions[t][e] = list(dstates.keys())[list(dstates.values()).index(temp)]


#d = 1
#for e in list(dstates):
#    for t in transitions:
#        temp = []
#        for f in dstates[e]:
#            if tree2.searchPos(f).val == t:
#                temp += tree2.searchPos(f).follow_pos
#        if temp != []:
#            if temp not in dstates.values():
#                dstates[d] = temp
#                d += 1
#            StateTransitions[t][e] = list(dstates.keys())[list(dstates.values()).index(temp)]

print('\n')
print(dstates)
print(StateTransitions)
print('\n')
n = 0
while n < len(i):
    print(i[n], tree2.searchPos(i[n]).val, follow_i[n])
    n += 1

