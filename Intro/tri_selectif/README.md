# Intro / Tri sélectif

## Challenge
Vous devez trier un tableau dont vous ne voyez pas les valeurs !

## Inputs
- client: [client.py](./client.py)
- application: [tri-selectif.py](./tri-selectif.py)


## Solution
The client handles the interaction with the remote application, which implements following API:
```python
def usage():
	print('Actions possibles:')
	print('  - "comparer X Y": compare les valeurs du tableau aux cases X et Y, et retourne 1 si la valeur en X est inférieure ou égale à celle en Y, 0 sinon.')
	print('  - "echanger X Y": échange les valeurs du tableau aux cases X et Y, et affiche le taleau modifié.')
	print('  - "longueur:      retourne la longueur du tableau.')
	print('  - "verifier:      retourne le flag si le tableau est trié.')
```

So we can only compare and exchange values.

Let's implement a simple bubble sort.

Here's the code to add in client's `trier()` function. It implements a very simple, non-optimised Bubble sort:
```python
def trier(N):
        l = longueur()
        for i in range(l-1, 1, -1):
                for j in range(0, i):
                        if comparer(j+1, j):
                                echanger(j+1, j)
```

Here's the execution output and the flag:
```console
$ python3 client_modified.py
[+] Opening connection to challenges.france-cybersecurity-challenge.fr on port 2051: Done
Le flag est : FCSC{e687c4749f175489512777c26c06f40801f66b8cf9da3d97bfaff4261f121459}
[*] Closed connection to challenges.france-cybersecurity-challenge.fr port 2051
```

## Python code
Complete solution in [client_modified.py](./client_modified.py)

## Flag
FCSC{e687c4749f175489512777c26c06f40801f66b8cf9da3d97bfaff4261f121459}
