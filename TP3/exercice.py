# FONTAINE Quentin, HUAUT Antonin
# -*- coding: utf-8 -*-

from Crypto.Util import number
from Crypto.Hash import SHA256
import random
import math


def est_point_infini(P):
    return P[2] == 0


def verifie_point(A, B, p, P):
    if est_point_infini(P):
        return True

    X = P[0]
    Y = P[1]
    calcY = (X ** 3 + A * X + B) % p
    testY = (Y ** 2) % p
    return calcY == testY


def est_le_meme_point(P, Q):
    return P[0] == Q[0] and P[1] == Q[1] and P[2] == Q[2]


def addition_points(A, B, p, P, Q):
    Xq = Q[0]
    Xp = P[0]
    Yq = Q[1]
    Yp = P[1]

    if est_point_infini(P):
        return Q

    if est_point_infini(Q):
        return P

    if not est_le_meme_point(P, Q) and Xp == Xq:
        return (0, 0, 0)

    if not est_le_meme_point(P, Q) and Xp != Xq:
        lamb = (Yq - Yp) * (number.inverse(Xq - Xp, p) % p)
        x = (lamb**2 - Xp - Xq) % p
        y = (lamb * (Xp - x) - Yp) % p
        return (x, y, 1)

    if est_le_meme_point(P, Q) and Yp == 0:
        return (0, 0, 0)

    if est_le_meme_point(P, Q) and Yp != 0:
        lamb = (3 * (Xp ** 2) + A) * (number.inverse(2 * Yp, p) % p)
        x = ((lamb ** 2) - (2 * Xp)) % p
        y = (lamb * (Xp - x) - Yp) % p
        return (x, y, 1)


def double_and_add(A, B, p, P, k):
    Q = (0, 0, 0)

    if (k == 0):
        return Q

    n = int(math.log(k, 2)) + 1

    for i in range(n, -1, -1):
        Q = addition_points(A, B, p, Q, Q)

        if (k >> i) & 1 == 1:
            Q = addition_points(A, B, p, Q, P)

    return Q


p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
n = 115792089210356248762697446949407573529996955224135760342422259061068512044369
A = -3
B = int("5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b", 16)
Gx = int("6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296", 16)
Gy = int("4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5", 16)
G = (Gx, Gy, 1)


def test_Hasse(n, p):
    pSqrt = math.sqrt(p)
    pPlus = p + 1
    inf = pPlus - pSqrt
    sup = pPlus + pSqrt
    return inf <= n and n <= sup


def ecdh(A, B, p, P):
    a = random.randint(1, n)
    b = random.randint(1, n)

    bG = double_and_add(A, B, p, P, b)
    aG = double_and_add(A, B, p, P, a)

    abG = double_and_add(A, B, p, bG, a)
    baG = double_and_add(A, B, p, aG, b)

    if not est_le_meme_point(abG, baG):
        return False

    x = SHA256.new()
    x.update(number.long_to_bytes(P[0]))
    return x.hexdigest()


# https://fr.wikipedia.org/wiki/Elliptic_curve_digital_signature_algorithm
def ecdsa(A, B, p, P, n, m, a, kConstantTestAttaque=None):
    s = a
    Q = double_and_add(A, B, p, P, s)

    if kConstantTestAttaque == None:
        k = random.randint(1, n - 1)
    else:
        k = kConstantTestAttaque

    iJ = double_and_add(A, B, p, P, k)
    x = iJ[0] % n

    sha = SHA256.new()
    sha.update(m.encode('UTF-8'))

    hexSha = number.bytes_to_long(sha.digest()) + s*x
    y = number.inverse(k, n) * hexSha % n

    return (x, y, 1)


def ecdsa_verif(A, B, p, P, n, m, A1, sign):
    t = sign[0]
    s = sign[1]

    if 1 > t or t > n - 1 or 1 > s or s > n - 1:
        return None

    sha = SHA256.new(m.encode('UTF-8'))
    Hm = number.bytes_to_long(sha.digest())

    sInverse = number.inverse(s, n)
    tmpA = double_and_add(A, B, p, P, Hm * sInverse)
    tmpB = double_and_add(A, B, p, A1, t * sInverse)
    (i, j, k) = addition_points(A, B, p, tmpA, tmpB)

    return t == i % n


def ecdsa_attack(s1, s2, kConstant):
    if s1[0] != s2[0]:
        return False

    t = s1[0]
    s1 = s1[1]
    s2 = s2[1]

    hm1 = number.bytes_to_long(SHA256.new(m1.encode('UTF-8')).digest())
    hm2 = number.bytes_to_long(SHA256.new(m2.encode('UTF-8')).digest())

    kHack = (hm1 - hm2) * number.inverse((s1 - s2), n) % n
    iHack = (hm1 * s2 - hm2 * s1) * number.inverse(t*(s1 - s2), n) % n

    return (kHack, iHack)


print("\nTEST DE HASSE")
print(test_Hasse(n, p))
# Essayer de comprendre le resultat obtenu
print("  => La pr??cision est trop faible et donc ne permet pas de d??duire le bon r??sultat")


print("\nTEST ECDH")
print(ecdh(A, B, p, G))


privateKey = random.randint(1, n - 1)
publicKey = double_and_add(A, B, p, G, privateKey)
m = "J'aime la crypto"
sign = ecdsa(A, B, p, G, n, m, privateKey)
signVerif = ecdsa_verif(A, B, p, G, n, m, publicKey, sign)
print("\nTEST ECDSA ET ECDSA_VERIF")
print("  Message :", m)
print("  Cl?? priv??e: ", privateKey)
print("  Cl?? publique :", publicKey)
print("  Signature :", sign)
print("  V??rification, signature valide :", signVerif)


print("\nTest Attack")
kConstant = 5

privateKey = random.randint(1, n - 1)
m1 = "J'aime la crypto"
m2 = "Je d??teste la crypto"  # C'est bien s??r juste pour les tests
s1 = ecdsa(A, B, p, G, n, m1, privateKey, kConstant)
s2 = ecdsa(A, B, p, G, n, m2, privateKey, kConstant)

print("  ?? Avec k =", kConstant)
(kHack, iHack) = ecdsa_attack(s1, s2, kConstant)
print(" kHack == k :", kHack == kConstant)
print(" privateKeyHack == privateKey :", iHack == privateKey)
if kHack == kConstant and iHack == privateKey:
    print("  => L'attaque a r??ussi, on a retrouv?? la cl?? priv??e !")
