import sympy
import random
from time import perf_counter



print("----------------MULTI-PRIME-------------------")

# print("Give value for p: ")
# p = int(input())
# print("Give value for q: ")
# q = int(input())
# print("Give value for r: ")
# r = int(input())

p = sympy.prime(1123453534365465)
q = sympy.prime(1107543564365464583)
r = sympy.prime(54664365546465463737)

print("p, q, r are: ", p, ", ", q, ", ", r)

def check_if_prime_and_distinct(number1, number2, number3):
    if number1 != number2 != number3:
        if sympy.isprime(number1) == True and sympy.isprime(number2) == True and sympy.isprime(number3) == True:
            return 1
    return 0

primality = check_if_prime_and_distinct(p,q,r)
print("Numbers are prime and distinct or not: ", primality)

def compute_n(primality, p, q, r):
    n = 1
    if primality == 1:
        n = p * q * r
    else:
        raise Exception("Cannot compute n because not all of the arguments are prime")
    return n

n = compute_n(primality, p, q, r)
print("This is n MULTI-PRIME: ", n)


def compute_phi_function(p, q, r):
    phi = (p-1) * (q-1) * (r-1)
    return phi

phi = compute_phi_function(p, q, r)
print("-----------------------------")
print("This is MULTI-PRIME phi(n): ", phi)

def generate_e():
    """
    The fact that we're generating a random PRIME number ensures the fact that (e,phi(n)) = 1
    :return: e
    """
    prime = 0
    e = 0
    while prime == 0:
        e = random.randint(2, 2147483647)
        if sympy.isprime(e) == True:
            prime = 1
    return e

print("____________________________")
new_e = generate_e()
print("E is: ", new_e)

def compute_d(e, phi):
    d = sympy.mod_inverse(e, phi)
    return d

d = compute_d(new_e, phi)
print("____________________________")
print("D is: ", d)

def encrypt(x, e, n):
    enc = (x ** e) % n
    return enc

print("Give value for x (encryption): ")
x = int(input())

y = encrypt(x, 11, n)    #change e -> daca e prea mare, dureaza prea mult calculul
print("x ENCRYPTED is: ", y)
print("__________________________")


def compute_xs(y, d, p, q, r):
   """
   We compute these 3 using Fermat
   :return: x_p, x_q, x_r
   """
   x_p = ((y % p) ** (d % (p - 1))) % p
   x_q = ((y % q) ** (d % (q - 1))) % q
   x_r = ((y % r) ** (d % (r - 1))) % r
   return x_p, x_q, x_r

x_p, x_q, x_r = compute_xs(y, d, p, q, r)
print("The 3 x's are: ", x_p, " ", x_q, " ", x_r)

def CRT(x_p, x_q, x_r):
    """
    Solves the system:
    x = x_p mod p
    x = x_q mod q
    x = x_r mod r
    using CRT
    :return: x, time for CRT
    """
    begin = perf_counter()
    N1 = q * r
    N2 = p * r
    N3 = p * q
    N = p * q * r

    x1 = sympy.mod_inverse(N1, p)
    x2 = sympy.mod_inverse(N2, q)
    x3 = sympy.mod_inverse(N3, r)

    x = x_p * N1 * x1 + x_q * N2 * x2 + x_r * N3 * x3
    end = perf_counter()
    time = end - begin
    return x, time

print("___________________________________________________")
x_multiprime, time = CRT(x_p, x_q, x_r)
print("X computed with multi-prime RSA is: ", x_multiprime)
print("Time with CRT is: ", time)

print("-------------------MULTI-POWER-----------------------")

def compute_n_mpower(p, q):
    n = p * p * q
    return n

n2 = compute_n_mpower(p, q)
print("This is MULTI-POWER n: ", n2)

def compute_phi_mpower(p, q):    #same specs as before
    phi = p * (p-1) * (q-1)
    return phi

phi2 = compute_phi_mpower(p,q)
print("This is MULTI-POWER phi(n): ", phi2)

def compute_xs_Hensel(y, d, p, q):
    x_0 = ((y % p) ** (d % (p - 1))) % p
    x_q = ((y % q) ** (d % (q - 1))) % q
    return x_0, x_q

x0, x_q_mpower = compute_xs_Hensel(y, d, p, q)
print("x0 si x_q for MULTI-POWER are: ", x0, " ", x_q_mpower)

def compute_x1_mpower(y, e, x0):
    x1 = ((y - (x0 ** e) % (p * p)) / p) * (pow(((e*(x0 **(e-1)) % (p * p)) % p), -1)) % p
    return x1

x1_mpower = compute_x1_mpower(y, new_e, x0)
print("This is x1: ", x1_mpower)


def compute_x_p2_mpower(x1, p, x0):
    x2 = x1 * p + x0
    return x2

x_p2_mpower = compute_x_p2_mpower(x1_mpower, p, x0)
print("This is x_p2: ", x_p2_mpower)

def CRT_MULTIPOWER(x_p2, x_q, p, q):
    begin = perf_counter()
    N1 = q
    N2 = p * p

    x1 = sympy.mod_inverse(N1,p * p)
    x2 = sympy.mod_inverse(N2,q)

    x = x_p2 * N1 * x1 + x_q * N2 * x2
    end = perf_counter()
    time = end - begin
    return x, time

x_solution_mpower, time_mpower = CRT_MULTIPOWER(x_p2_mpower, x_q_mpower, p, q)
print("This is MULTI-POWER x: ", x_solution_mpower)
print("This is time with MULTI-PRIME: ", time_mpower)


def classic_method(y, d, n):
    start = perf_counter()
    x = (y ** d) % n
    end = perf_counter()
    time = end- start
    return x, time

x_classic, time_classic = classic_method(y,d,n)
print("x with the standard method is: ", x_classic)
print("Time with standard method is: ", time_classic)

