#!/usr/bin/env python3

# python3 -m pip install pwntools
from pwn import *

# Paramètres de connexion
HOST, PORT = "challenges.france-cybersecurity-challenge.fr", 2052

def comparer(x, y):
        io.sendlineafter(b">>> ", f"comparer {x} {y}".encode())
        return int(io.recvline().strip().decode())

def echanger(x, y):
	io.sendlineafter(b">>> ", f"echanger {x} {y}".encode())

def longueur():
	io.sendlineafter(b">>> ", b"longueur")
	return int(io.recvline().strip().decode())

def verifier():
	io.sendlineafter(b">>> ", b"verifier")
	r = io.recvline().strip().decode()
	if "flag" in r:
		print(r)
	else:
		print(io.recvline().strip().decode())
		print(io.recvline().strip().decode())

def partitionner(first, last, pivot):
        echanger(pivot, last)
        j = first
        for i in range(first, last):
            if comparer(i, last):
                echanger(i, j)
                j = j + 1
        echanger(last, j)
        return j

def tri_rapide(first, last):
        if first < last:
                pivot = (first + last) // 2
                pivot = partitionner(first, last, pivot)
                tri_rapide(first, pivot-1)
                tri_rapide(pivot+1, last)

def trier(N):
        tri_rapide(0, N-1)


# Ouvre la connexion au serveur
io = remote(HOST, PORT)

# Récupère la longueur du tableau
N = longueur()

# Appel de la fonction de tri que vous devez écrire
trier(N)

# Verification
verifier()

# Fermeture de la connexion
io.close()
