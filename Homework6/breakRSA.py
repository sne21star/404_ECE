"""
Homework Number: 6
Name: Sneha Mahapatra
ECN Login: mahapat0
Due Date: 03/03/2020
"""
# !/usr/bin/env python
# !/usr/bin/env python -W ignore:tostring:DeprecationWarning
# python breakRSA.py -e message.txt enc1.txt enc2.txt enc3.txt n_1_2_3.txt #Steps 1 and 2
# python breakRSA.py -c enc1.txt enc2.txt enc3.txt n_1_2_3.txt cracked.txt #Step 3
from sys import *
from BitVector import *
import random
import numpy as np

e = 3
eBit = BitVector(intVal=65537)
SIZE_128 = 128
SIZE_256 = 256

def solve_pRoot(p, x):  # O(lgn) solution
    # Upper bound u is set to as follows:
    # We start with the 2**0 and keep increasing the power so that u is 2**1, 2**2, ...
    # Until we hit a u such that u**p is > x
    u = 1
    while u ** p <= x: u *= 2

    # Lower bound set to half of upper bound
    l = u // 2

    # Keep the search going until upper u becomes less than lower l
    while l < u:
        mid = (l + u) // 2
        mid_pth = mid ** p
        if l < mid and mid_pth < x:
            l = mid
        elif u > mid and mid_pth > x:
            u = mid
        else:
            # Found perfect pth root.
            return mid
    return mid + 1


class PrimeGenerator(object):  # (A1)

    def __init__(self, **kwargs):  # (A2)
        bits = debug = None  # (A3)
        if 'bits' in kwargs:     bits = kwargs.pop('bits')  # (A4)
        if 'debug' in kwargs:     debug = kwargs.pop('debug')  # (A5)
        self.bits = bits  # (A6)
        self.debug = debug  # (A7)
        self._largest = (1 << bits) - 1  # (A8)

    def set_initial_candidate(self):  # (B1)
        candidate = random.getrandbits(self.bits)  # (B2)
        if candidate & 1 == 0: candidate += 1  # (B3)
        candidate |= (1 << self.bits - 1)  # (B4)
        candidate |= (2 << self.bits - 3)  # (B5)
        self.candidate = candidate  # (B6)

    def set_probes(self):  # (C1)
        self.probes = [2, 3, 5, 7, 11, 13, 17]  # (C2)

    # This is the same primality testing function as shown earlier
    # in Section 11.5.6 of Lecture 11:
    def test_candidate_for_prime(self):  # (D1)
        'returns the probability if candidate is prime with high probability'
        p = self.candidate  # (D2)
        if p == 1: return 0  # (D3)
        if p in self.probes:  # (D4)
            self.probability_of_prime = 1  # (D5)
            return 1  # (D6)
        if any([p % a == 0 for a in self.probes]): return 0  # (D7)
        k, q = 0, self.candidate - 1  # (D8)
        while not q & 1:  # (D9)
            q >>= 1  # (D10)
            k += 1  # (D11)
        if self.debug: print("q = %d  k = %d" % (q, k))  # (D12)
        for a in self.probes:  # (D13)
            a_raised_to_q = pow(a, q, p)  # (D14)
            if a_raised_to_q == 1 or a_raised_to_q == p - 1: continue  # (D15)
            a_raised_to_jq = a_raised_to_q  # (D16)
            primeflag = 0  # (D17)
            for j in range(k - 1):  # (D18)
                a_raised_to_jq = pow(a_raised_to_jq, 2, p)  # (D19)
                if a_raised_to_jq == p - 1:  # (D20)
                    primeflag = 1  # (D21)
                    break  # (D22)
            if not primeflag: return 0  # (D23)
        self.probability_of_prime = 1 - 1.0 / (4 ** len(self.probes))  # (D24)
        return self.probability_of_prime  # (D25)

    def findPrime(self):  # (E1)
        self.set_initial_candidate()  # (E2)
        if self.debug:  print("    candidate is: %d" % self.candidate)  # (E3)
        self.set_probes()  # (E4)
        if self.debug:  print("    The probes are: %s" % str(self.probes))  # (E5)
        max_reached = 0  # (E6)
        while 1:  # (E7)
            if self.test_candidate_for_prime():  # (E8)
                if self.debug:  # (E9)
                    print("Prime number: %d with probability %f\n" %
                          (self.candidate, self.probability_of_prime))  # (E10)
                break  # (E11)
            else:  # (E12)
                if max_reached:  # (E13)
                    self.candidate -= 2  # (E14)
                elif self.candidate >= self._largest - 2:  # (E15)
                    max_reached = 1  # (E16)
                    self.candidate -= 2  # (E17)
                else:  # (E18)
                    self.candidate += 2  # (E19)
                if self.debug:  # (E20)
                    print("    candidate is: %d" % self.candidate)  # (E21)
        return self.candidate  # (E22)


def GCD(a, b):
    return a.gcd(b)


def generate_key():
    primeP = 0
    primeQ = 0
    num_of_bits_desired = SIZE_128
    while (primeP == primeQ):
        generatorP = PrimeGenerator(bits=num_of_bits_desired)
        generatorQ = PrimeGenerator(bits=num_of_bits_desired)
        primeP = generatorP.findPrime()
        primeQ = generatorQ.findPrime()
        primePBit = BitVector(intVal=primeP - 1, size=SIZE_128)
        primeQBit = BitVector(intVal=primeP - 1, size=SIZE_128)
        primePString = str(primePBit)
        primeQString = str(primeQBit)
        PGCD = GCD(primePBit, eBit).int_val()
        QGCD = GCD(primeQBit, eBit).int_val()
        if (PGCD != 1 or QGCD != 1):
            primeP = 0
            primeQ = 0
            continue
        if (primePString[0:2] != '11' or primeQString[0:2] != '11'):
            primeP = 0
            primeQ = 0
            continue
    return primeP * primeQ


def encrypt():
    # Read N1, N2, N3
    readP = open(sys.argv[6], 'r')
    nList = readP.readlines()
    # Open File for Encrypted Text
    index = 3
    for n in nList:
        # Get specific modulus n
        n = int(n)
        encryptedText = open(sys.argv[index], "w")

        # Read Message convert into long bit vector
        messageBV = BitVector(filename=sys.argv[2])

        while (messageBV.more_to_read):
            # Get 128 Bit for Plain Text
            bitvec = messageBV.read_bits_from_file(SIZE_128)
            # If block is < 128, pad zeroes
            if (bitvec.length() % SIZE_128 != 0):
                bitvec.pad_from_right(128 - bitvec.length())

            # Prepend it with 128 zeros to the left, now 256 Bit in Length
            bitvec.pad_from_left(SIZE_128)

            # M ^ e % n
            messageInt = bitvec.int_val()
            num = pow(messageInt, e, n)
            cipherText = BitVector(intVal=num, size=SIZE_256)
            # Write to File in hex
            encryptedText.write(cipherText.get_bitvector_in_hex())
        # close
        encryptedText.close()
        index += 1


def decrypt():
    # Turn File into BitVector Encrypted 1
    HEXFILE = open(sys.argv[2], 'r')
    hexString = HEXFILE.read()
    bv = BitVector(hexstring=hexString)
    BITVECTORTEXT = open("bitVector1.txt", "wb")
    bv.write_to_file(BITVECTORTEXT)
    BITVECTORTEXT.close()
    encrypted1 = BitVector(filename="bitVector1.txt")

    # Turn File into BitVector Encrypted 2
    HEXFILE = open(sys.argv[3], 'r')
    hexString = HEXFILE.read()
    bv = BitVector(hexstring=hexString)
    BITVECTORTEXT = open("bitVector2.txt", "wb")
    bv.write_to_file(BITVECTORTEXT)
    BITVECTORTEXT.close()
    encrypted2 = BitVector(filename="bitVector2.txt")

    # Turn File into BitVector Encrypted 3
    HEXFILE = open(sys.argv[4], 'r')
    hexString = HEXFILE.read()
    bv = BitVector(hexstring=hexString)
    BITVECTORTEXT = open("bitVector3.txt", "wb")
    bv.write_to_file(BITVECTORTEXT)
    BITVECTORTEXT.close()
    encrypted3 = BitVector(filename="bitVector3.txt")

    # Read N elements in the List
    readP = open(sys.argv[5], 'r')
    nList = readP.readlines()
    N = int(nList[0]) * int(nList[1]) * int(nList[2])
    M1 = int(nList[1]) * int(nList[2])
    M2 = int(nList[0]) * int(nList[2])
    M3 = int(nList[0]) * int(nList[1])

    M1Bit = BitVector(intVal=int(M1))
    M2Bit = BitVector(intVal=int(M2))
    M3Bit = BitVector(intVal=int(M3))

    key1Bit = BitVector(intVal=int(nList[0]))
    key2Bit = BitVector(intVal=int(nList[1]))
    key3Bit = BitVector(intVal=int(nList[2]))

    C1 = int(M1) * (M1Bit.multiplicative_inverse(key1Bit)).int_val()
    C2 = int(M2) * (M2Bit.multiplicative_inverse(key2Bit)).int_val()
    C3 = int(M3) * (M3Bit.multiplicative_inverse(key3Bit)).int_val()

    crackedText = open(sys.argv[6], "w")
    bitTotal = BitVector(size=0)
    while (encrypted1.more_to_read):
        bitvec1 = encrypted1.read_bits_from_file(SIZE_256)
        bitvec2 = encrypted2.read_bits_from_file(SIZE_256)
        bitvec3 = encrypted3.read_bits_from_file(SIZE_256)
        c1 = bitvec1.int_val()
        c2 = bitvec2.int_val()
        c3 = bitvec3.int_val()
        decryptedInt = (c1 * int(C1) + c2 * int(C2) + c3 * int(C3)) % int(N)
        intX = solve_pRoot(e, int(decryptedInt))
        bitInt = BitVector(intVal=intX, size=SIZE_128)
        bitTotal += bitInt
        pass

    crackedText.write(bitTotal.get_bitvector_in_ascii())
    # close decrypted File
    crackedText.close()


def CRT(C, p, q, d, n):
    p = int(p)
    q = int(q)
    pBit = BitVector(intVal=p, size=SIZE_256)
    qBit = BitVector(intVal=q, size=SIZE_256)
    Vp = pow(C, d, p)
    Vq = pow(C, d, q)
    # eBit.multiplicative_inverse(totientBit)
    Xp = q * (qBit.multiplicative_inverse(pBit)).int_val()
    Xq = p * (pBit.multiplicative_inverse(qBit)).int_val()
    return (Vp * Xp + Vq * Xq) % n


def main():
    # python breakRSA.py -e message.txt enc1.txt enc2.txt enc3.txt n_1_2_3.txt #Steps 1 and 2
    # python breakRSA.py -c enc1.txt enc2.txt enc3.txt n_1_2_3.txt cracked.txt #Step

    charInput = sys.argv[1]
    if (charInput == '-e'):
        # test of can write 3 generated keys
        n1 = generate_key()
        n2 = generate_key()
        n3 = generate_key()

        n123 = open(sys.argv[6], "w")
        n123.write(str(n1))
        n123.write("\n")
        n123.write(str(n2))
        n123.write("\n")
        n123.write(str(n3))
        n123.close()
        encrypt()
    elif (charInput == '-c'):
        decrypt()
    else:
        print("Either -e or -d")
    pass


if __name__ == "__main__":
    main()
