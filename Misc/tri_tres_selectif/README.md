# Misc / Tri très sélectif 

## Challenge
Comme l'épreuve Tri Sélectif, vous devez trier le tableau, mais cette fois vous devez être efficace !

## Inputs
- client: [client.py](./client.py)
- application: [tri-tres-selectif.py](./tri-tres-selectif.py)


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

Let's implement an optimized sort, operating in place, like the `Quick sort` (https://fr.wikipedia.org/wiki/Tri_rapide).

Here's the code to add in client's `trier()` function to implement that `Quick sort`:
```python
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
```

Here's the execution output and the flag:
```console
$ python3 client_modified.py
[+] Opening connection to challenges.france-cybersecurity-challenge.fr on port 2052: Done
Le flag est : FCSC{6d275607ccfba86daddaa2df6115af5f5623f1f8f2dbb62606e543fc3244e33a}
[*] Closed connection to challenges.france-cybersecurity-challenge.fr port 2052
```

## Python code
Complete solution in [client_modified.py](./client_modified.py)

## Flag
FCSC{6d275607ccfba86daddaa2df6115af5f5623f1f8f2dbb62606e543fc3244e33a}
