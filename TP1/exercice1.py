# FONTAINE Quentin, HUAUT Antonin
# -*- coding: utf-8 -*-

from Crypto.Hash import SHA256
import time


def nbFirstname(firstname, strToFound):
    bFirstname = bytes(firstname, encoding='ascii')
    lolHex = ''.join(str(format(ord(c), 'x')) for c in strToFound)

    m = SHA256.new()
    count = 0

    while (not m.hexdigest().endswith(lolHex)):
        m.update(bFirstname)
        count += 1

    return count, m.hexdigest()


t0 = time.perf_counter()

firstname = "Antonin"
strToFound = "LOL"
countTry, hexHash = nbFirstname(firstname, strToFound)
print("Trouvé pour", firstname, "en", countTry, "essais", " hexHash: ", hexHash)

t1 = time.perf_counter()
print("Il a fallut", t1-t0, "secondes")

print("Nombre d'essais moyen :", 2**(len(strToFound)*8),
      "(" + str(2)+"^("+str(len(strToFound)) + "*" + str(8) + "))")

hashVerif = SHA256.new(data=bytes(countTry*firstname, "ascii"))
print("Hash de vérification :", hashVerif.hexdigest())
print("Même hash :", hexHash == hashVerif.hexdigest())
