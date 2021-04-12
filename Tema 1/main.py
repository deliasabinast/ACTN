import numpy as np
import random
import os

print("Give a value for m: ")
m = int(input())
print("Give a value for p: ")
p = int(input())

def computeModulo(nr,p):   #computes the modulo of a number nr by division with p
    return nr % p

def convertToBaseP(nr,p):   #de pe net
    base_num = ""
    while nr > 0:
        dig = int(nr % p)
        if dig < 10:
            base_num += str(dig)
        else:
            base_num += chr(ord('A') + dig - 10)  # Using uppercase letters
        nr //= p
    base_num = base_num[::-1]  # To reverse the string
    return base_num

print("This is m in base p: ")
print(convertToBaseP(m,p))

def computeLength(nr):
    converted = convertToBaseP(m,p)
    lgt = len(converted)
    return lgt

print("Length is: ", computeLength(m))

def turnIntoArray(nr,p):
    converted = convertToBaseP(m,p)
    lgt = len(converted)
    #print("This is the LENGTH of the number: ", lgt)
    converted = int(converted)
    #print("This is converted number as INT: ", converted, " and this is its TYPE: ", type(converted))
    m_array = []
    for digit in range(lgt):
        m_array.append(converted % 10)
        converted = converted // 10
    return m_array

print("This is m converted to an array: ", turnIntoArray(m,p))


def horner(nr, value, k, base):
    result = 0
    arr = turnIntoArray(nr, base)
    for index in range(0, k - 1):
        result = result * value + arr[index]
    return result % base

def computeSolution(nr, base):
    arr = turnIntoArray(nr, base)
    lgt = computeLength(nr)
    n = lgt + 1 + 2   #this is k + 2s; since k-1 = lgt, then k = lgt + 1; s is considered to be 1
    y = np.array([])
    y = [0 for i in range(n + 1)]
    i = 1; j = 0
    while i <= (n):
        putere = 1
        for j in range(lgt):
            y[i] += (i ** putere) * arr[j]
            putere += 1
        i += 1
    for i in range(n + 1):
        y[i] = y[i] % base
    y.pop(0)
    return y

print("The encoding is: ", computeSolution(m, p))

print("------------ DECODING ------------")

y = computeSolution(m,p)

def copyVectY(array):
    new_array = [None] * len(array)
    for i in range(0, len(array)):
        new_array[i] = array[i]
    return new_array

z = copyVectY(y)
print("Z is: ", z)
print(os.linesep)

def generateRandomPosition(array):
    random_position = random.randint(0,len(array))
    return random_position

def generateRandomNumber(base):
    random_value = random.randint(0,base)
    return random_value

def arrayWithErrors(array, random_position, random_value):
    array[random_position] = random_value
    return array

random_position = generateRandomPosition(z)
print("Random POSITION chosen is: ", random_position)

random_value = generateRandomNumber(p)
print("Random VALUE in interval is: ", random_value)

print(os.linesep)

z_errors = arrayWithErrors(z, random_position, random_value)
print("Z with errors is: ", z_errors)
print(os.linesep)

def computeA(array, random_position):
    A = [None] * len(array)
    for i in range(0, len(array)):
        A[i] = i             #added +1 cause the initial arrays start from index 0, but the example from the lab starts from 1
    A.pop(random_position)
    return A

A = computeA(z_errors, random_position)
print("A computed is: ", A)
print(os.linesep)

example_array = [9, 2, 6, 5, 8]
B = [0, 2, 3, 4]  #1,3,4,5
print("JUST TO VERIFY THE EXAMPLE : ")
print("A from example is", B, "because z with errors is (9, 2, 6, 5, 8)")

print(os.linesep)


def computeFreeCoeficient(indexes, array, base):   #array has to be z with errors   #indexes = A, array = z
    fc = 0
    for i in indexes:
        produs = 1
        for j in indexes:
            if(i != j):
                produs *= ((j+1) * pow((j % p - i % p), -1, p)) % p
        fc += produs * array[i]
    return fc % base

# print("This is len of B: ",len(B))
# print("This is len of example: ",len(example_array))

# freecoef = computeFreeCoeficient(B, example_array, p)
# print("Free coeficient is: ", freecoef)

freecoef = computeFreeCoeficient(A, z_errors, p)
print("Free coeficient is: ", freecoef)

def computePoly(fc, A, z, base):
    if(fc == 0):
        value = 0
        for i in A:
            produs = 1
            for j in A:
                if i != j:
                    produs *= ((x % base - (j+1) % base) * pow((i % base - j % base), -1, base)) % base
            value += (z[i] * produs) % base
        return value % base

#print("Poly is: ", computePoly(freecoef, A, z_errors, p))