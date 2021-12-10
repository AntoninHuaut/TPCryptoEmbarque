# FONTAINE Quentin, HUAUT Antonin
# -*- coding: utf-8 -*-

from Crypto.Util import number
from Crypto.Hash import SHA256
import math
import random


class SecretKey:
    def __init__(self, p, q, d, dP, dQ, iP, iQ):
        self.p = p
        self.q = q
        self.d = d
        self.dP = dP
        self.dQ = dQ
        self.iP = iP
        self.iQ = iQ


class PublicKey:
    def __init__(self, N, e):
        self.N = N
        self.e = e


def square_and_multiply(a, k, n):
    n = abs(n)
    p = k
    sumRes = a
    res = 1
    while p >= 1:
        resMod = p % 2

        # Si le bit est à 0, il ne compte pas pour le résultat final
        if resMod == 1:
            res *= sumRes
            res %= n

        p = p // 2
        sumRes = sumRes ** 2 % n

    return res


def generer_cle_RSA(n):
    p = number.getStrongPrime(n)
    q = number.getStrongPrime(n)

    N = p*q
    phiN = (p - 1) * (q - 1)
    e = None

    while e == None or math.gcd(e, phiN) != 1:
        e = number.getRandomInteger(n)

    d = number.inverse(e, phiN)

    dP = d % (p - 1)
    dQ = d % (q - 1)
    iP = number.inverse(p, q)
    iQ = number.inverse(q, p)

    sK = SecretKey(p, q, d, dP, dQ, iP, iQ)
    pK = PublicKey(N, e)
    return sK, pK


def signature_RSA_CRT(m, sK, pK):
    sha = SHA256.new(m.encode('utf-8'))
    mLong = number.bytes_to_long(sha.digest())

    if mLong >= pK.N:
        return False

    sP = square_and_multiply(mLong, sK.dP, sK.p)
    sQ = square_and_multiply(mLong, sK.dQ, sK.q)

    s1 = number.inverse(sK.q, sK.p) * sK.q * sP
    s2 = number.inverse(sK.p, sK.q) * sK.p * sQ
    s = (s1 + s2) % pK.N

    return s


def signature_RSA_CRT_faute(m, sK, pK):
    sha = SHA256.new(m.encode('utf-8'))
    mLong = number.bytes_to_long(sha.digest())

    if mLong >= pK.N:
        return False

    sP = square_and_multiply(mLong, sK.dP, sK.p)
    sQ = square_and_multiply(mLong + 1, sK.dQ, sK.q)

    s1 = number.inverse(sK.q, sK.p) * sK.q * sP
    s2 = number.inverse(sK.p, sK.q) * sK.p * sQ
    s = (s1 + s2) % pK.N

    return s


def RSA_CRT_Bellcore(m, sK, pK):
    signValid = signature_RSA_CRT(m, sK, pK)
    signError = signature_RSA_CRT_faute(m, sK, pK)

    pHack = math.gcd(signError - signValid, pK.N)
    qHack = pK.N // pHack

    return (pHack, qHack)


n = 1024
m = "La crytographie, c'est ma passion ! (It's a joke)"
(sK, pK) = generer_cle_RSA(n)
s = signature_RSA_CRT(m, sK, pK)
print("\nAvec une signature RSA CRT classique : fonction pow sans square and multiply, le calcul est trop long !")

sCheck = signature_RSA_CRT(m, sK, pK)
print("\nTest signature message identique :", s == sCheck)
sCheck = signature_RSA_CRT(m + "l", sK, pK)
print("Test signature message différent :", s == sCheck)

(pHack, qHack) = RSA_CRT_Bellcore(m, sK, pK)
print("\npHack == p :", pHack == sK.p)
print("qHack == q :", qHack == sK.q)
if pHack == sK.p and qHack == sK.q:
    print("  => L'attaque a réussi, on a retrouvé la clé privée !")
