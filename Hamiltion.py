from dimod import dimod
from dimod.reference.samplers import ExactSolver
import neal

def createDigPart(letter: str, count :int, value: int):
    tmpDig = dict()
    for i in range(1, count+1):
        tmpDig[letter+str(i)] = value
    return tmpDig

def createDig(nodes: list, count: int, value: int):
    tmpDig = dict()
    for i in nodes:
        tmpDig.update(createDigPart(i, count, value))
    return tmpDig

def fillMatrixC1Part(letter: str, count: int, value: int):
    tmpMat = dict()
    for i in range(1, count+1):
        for j in range(i, count):
            tmpMat[letter+str(i), letter+str(j+1)] = value
    return tmpMat

def fillMatrixC1(nodes: list, count: int, value: int):
    tmpMat = dict()
    for i in nodes:
        tmpMat.update(fillMatrixC1Part(i, count, value))
    return tmpMat

def fillMatrixC2Part(letter1: str, letter2: str, count: int, value: int):
    tmpMat = dict()
    for i in range(1, count+1):
        tmpMat[letter1+str(i), letter2+str(i)] = value
    return tmpMat

def fillMatrixC2(nodes: list, count: int, value: int):
    tmpMat = dict()
    for i in range(0, len(nodes)):
        for j in range(i, len(nodes)-1):
            tmpMat.update(fillMatrixC2Part(nodes[i], nodes[j+1], count, value))
    return tmpMat

def fillMatrixC3(node1: str, node2: str, count: int, value: int):
    tmpMat = dict()
    for i in range(1, count+1):
        a = i+1
        if a == count+1:
            a = 1
            #tmpa = a
            #a = i
            #i = tmpa
        tmpMat[node1+str(i), node2+str(a)] = value
        tmpMat[node1+str(a), node2+str(i)] = value # damit die kante in beide richtungen nicht existiert
    return tmpMat

def printMatrix(dig: dict, mat: dict, nodes:list, count: int):
    headerRow = ","
    for i in nodes:
        for j in range(1, count+1):
            headerRow += i+str(j)+","
    headerRow = headerRow[:-1]
    headerRow += '\n'
    rows = ""

    for i in nodes:
        for j in range(1, count+1):
            row = i+str(j)+","
            for k in nodes:
                for l in range(1, count+1):
                    if(j == l) and (i == k):
                        if i+str(j) in dig:
                            row += str(dig[i+str(j)])+","
                    else:
                        if (i+str(j), k+str(l)) in mat:
                            row += str(mat[i+str(j), k+str(l)])+","
                        else:
                            row += "0,"
            row = row[:-1]
            row += '\n'
            rows += row
    
    print(headerRow+rows)

    
#nodes = ['a', 'b', 'c', 'd']

#testDig = dict()
#testDig = createDig(nodes, 4, -2)
#print(testDig)

#testMat = dict()
#testMat = fillMatrixC1(nodes, 4, 2)
#print(testMat)

#testMat = fillMatrixC2(nodes, 4, 2)
#print(testMat)
#exit()

nodes = ['a', 'b', 'c', 'd']
length = len(nodes)

A = 7
B = 1

diagonal = createDig(nodes, length, -2*A)
matrix = fillMatrixC1(nodes, length, 2*A)
matrix.update(fillMatrixC2(nodes, length, 2*A))

# no edge
matrix.update(fillMatrixC3('b', 'd', length, 2*A))

# weigth the edges that exists
matrix.update(fillMatrixC3('a', 'b', length, 3*B))
matrix.update(fillMatrixC3('b', 'c', length, 4*B))
matrix.update(fillMatrixC3('c', 'd', length, 5*B))
matrix.update(fillMatrixC3('a', 'c', length, 6*B))
matrix.update(fillMatrixC3('a', 'd', length, 7*B))


printMatrix(diagonal, matrix, nodes, length)


# qubo matrix
qubo = dimod.BinaryQuadraticModel(
                                diagonal, 
                                matrix
                                , 2*length, 'BINARY')

print(qubo)

sampler = ExactSolver()
response = sampler.sample(qubo)
print("\nQUBO")
print(response.lowest())