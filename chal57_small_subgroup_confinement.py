import gmpy
import operator
import functools
import random
import hashlib
from utils import *
import math

p = 7199773997391911030609999317773941274322764333428698921736339643928346453700085358802973900485592910475480089726140708102474957429903531369589969318716771
g = 4565356397095740655436854503483826832136106141639563487732438195343690437606117828318042418238184896212352329118608100083187535033402010599512641674644143
q = 236234353446506858198510045061214171961


j = 30477252323177606811760882179058908038824640750610513771646768011063128035873508507547741559514324673960576895059570

bob_secret_key = random.randint(1, q)
msg = b"crazy flamboyant for the rap enjoyment"


def factor(num):
    factors = set()
    i = 2
    while i*i <= num:
        if num % i:
            i += 1
        else:
            # Is a factor
            num //= i
            factors.add(i)

        if functools.reduce(operator.mul, factors, 1) > q:
            print("Found enough factors!")
            return factors

    exit("Didn't find enough factors!")

def find_elem(order):
    while True:
        cand = pow(random.randint(1, p), (p-1)//order, p)
        if cand == 1:
            continue
        else:
            return cand

def solve_crt(eqns):
    b1, mod1 = eqns[0][0], eqns[0][1]
    for i in range(1, len(eqns)):
        b2, mod2 = eqns[i][0], eqns[i][1]

        mod_prod = mod1* mod2
        y1 = b1 * mod2 * modinv(mod1, mod2)
        y2 = b2 * mod1 * modinv(mod2, mod1)
        y = (y1 + y2) % mod_prod

        b1, mod1 = y, mod_prod

    return y

# def pohlig_hellman():

def compute_bob_mac(h, msg):
    shared_secret_K = pow(h, bob_secret_key, p)
    shared_secret_K = int2bytes(shared_secret_K)
    return hashlib.md5(shared_secret_K+msg).digest()

# def baby_step_giant_step():

def bruteforce_dlp(h, order, true_mac):
    for i in range(order):
        guess_K = pow(h, i, p)
        guess_K = int2bytes(guess_K)
        guess_mac = hashlib.md5(guess_K+msg).digest()

        if guess_mac == true_mac:
            print("Found DL by bruteforce!")
            return i


factors = factor(j)

crt_eqns = []
for order in factors:
    h = find_elem(order)

    t = compute_bob_mac(h, msg)

    x = bruteforce_dlp(h, order, t)

    crt_eqns.append((x, order))

print("crt coeffs", crt_eqns)
assert solve_crt(crt_eqns) == bob_secret_key











