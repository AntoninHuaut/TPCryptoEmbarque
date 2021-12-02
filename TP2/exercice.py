# FONTAINE Quentin, HUAUT Antonin
# -*- coding: utf-8 -*-

from Crypto.Util import number


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


def inverse_point(P, p):
    if est_point_infini(P):
        return P

    return (P[0], (-P[1]) % p, P[2])


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
        lamb = (Yq - Yp) * number.inverse(Xq - Xp, p) % p
        x = (lamb**2 - Xp - Xq) % p
        y = (lamb * (Xp - x) - Yp) % p
        return (x, y, 1)

    if est_le_meme_point(P, Q) and Yp == 0:
        return (0, 0, 0)

    if est_le_meme_point(P, Q) and Yp != 0:
        lamb = (3 * (Xp ** 2) + A) * number.inverse(2 * Yp, p) % p
        x = ((lamb ** 2) - (2 * Xp)) % p
        y = (lamb * (Xp - x) - Yp) % p
        return (x, y, 1)


def groupe_des_points(A, B, p):
    list = [(0, 0, 0)]

    for X in range(0, p, 1):
        for Y in range(0, p, 1):
            P = (X, Y, 1)
            if (verifie_point(A, B, p, P)):
                list.append(P)

    return list


def ordre_point(A, B, p, P):
    X = P
    c = 1

    while not est_point_infini(X):
        X = addition_points(A, B, p, X, P)
        c += 1

    return c


def generateurs(A, B, p):
    list = []
    pointsList = groupe_des_points(A, B, p)
    tailleGroupe = len(pointsList)

    for P in pointsList:
        if ordre_point(A, B, p, P) == tailleGroupe:
            list.append(P)

    return list


def double_and_add(A, B, p, P, k):
    return


# Test verifie des points
print("\nPoints sur la courbe")
print("0∞ sur E1:", verifie_point(3, 2, 5, (0, 0, 0)))
print("(2,1,1) sur E1:", verifie_point(3, 2, 5, (2, 1, 1)))
print("(2,2,1) sur E1:", verifie_point(3, 2, 5, (2, 2, 1)))

# Test addition des points
print("\nAddition des points")
res = str(addition_points(3, 2, 5, (2, 1, 1), (2, 4, 1)))
print("(2, 1, 1) + (2, 4, 1) doit donner 0∞ : " + res)

res = str(addition_points(3, 2, 5, (2, 1, 1), (2, 1, 1)))
print("(2, 1, 1) + (2, 1, 1) doit donner (1, 4, 1) : " + res)

res = str(addition_points(3, 2, 5, (2, 1, 1), (0, 0, 0)))
print("(2, 1, 1) + 0∞ doit donner (2, 1, 1) : " + res)

res = str(addition_points(3, 2, 5, (2, 1, 1), (1, 1, 1)))
print("(2, 1, 1) + (1, 1, 1) doit donner (2, 4, 1) : " + res)

res = str(addition_points(3, 2, 5, (2, 1, 1), (1, 4, 1)))
print("(2, 1, 1) + (1, 4, 1) doit donner (1, 1, 1) : " + res)

res = str(addition_points(3, 2, 5, (1, 4, 1), (1, 4, 1)))
print("(1, 4, 1) + (1, 4, 1) doit donner (2, 4, 1) : " + res)

# Test groupe des points
print("\nGroupe des points")
print("(= 5) :", len(groupe_des_points(3, 2, 5)))
print("(= 16) :", len(groupe_des_points(1, 2, 11)))

# Test ordre des points
print("\nOrdre des points")
print(ordre_point(3, 1, 5, (2, 1, 1)))

# Test générateurs
print("\nGénérateurs")
print("E1 :", generateurs(3, 2, 5))
print("E2 :", generateurs(1, 2, 11))
