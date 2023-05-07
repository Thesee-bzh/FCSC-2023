# Crypto / Elliptic Addventure

## Challenge
Vous devez retrouver le flag caché dans les coordonnées des points donnés.

## Inputs
- SAGE script: [elliptic-addventure.sage](./elliptic-addventure.sage)
- output:  [output.txt](./output.txt)

## Solution
The script defines an elliptic curve on a Finite field, defines two points A and B on that curve, based on the flag. Then it dumps the coordinates of points (A+B) and (A-B):

```python
from Crypto.Util.number import bytes_to_long

flag = open("flag.txt", "rb").read().strip()
assert len(flag) == 64

p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
a = -3
b = 41058363725152142129326129780047268409114441015993725554835256314039467401291

K = GF(p)
E = EllipticCurve([K(a), K(b)])

mid = len(flag) // 2
Ax = K(bytes_to_long(flag[:mid]))
Bx = K(bytes_to_long(flag[mid:]))

A = E.lift_x(Ax)
B = E.lift_x(Bx)

print(f"{A + B = }")
print(f"{A - B = }")
```

Here's the given coordinates for (A+B) and (A-B)
```python
A + B = (65355407912556110148433442581541116153096561277895556722873533689053268966181 : 105815222725531774810979264207056456440531378690488283731984033593201027022521 : 1)
A - B = (103762781993230069010083485164887172361256204634523864861966420595029658052179 : 76878428888684998206116229633819067250185142636730603625369142867437006615111 : 1)
```

We need to recover points A and B, then get back to the flag.

Let's note: P1 = A + B, P2 = A - B. Then we have: 2A = P1+P2, 2B = P1-P2.

Fortunately, `sagemath` has the nice function `division_points()` which exactly resolves `mQ = P` given `(m, P)`.

So let's implement it:
```python
from Crypto.Util.number import bytes_to_long

p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
a = -3
b = 41058363725152142129326129780047268409114441015993725554835256314039467401291

K = GF(p)
E = EllipticCurve([K(a), K(b)])

# P1 = A + B; P2 = A - B
P1 = E(65355407912556110148433442581541116153096561277895556722873533689053268966181, 105815222725531774810979264207056456440531378690488283731984033593201027022521)
P2 = E(103762781993230069010083485164887172361256204634523864861966420595029658052179, 76878428888684998206116229633819067250185142636730603625369142867437006615111)

# 2A = P1+P2; 2B = P1-P2
AA = P1 + P2; A = AA.division_points(2)
BB = P1 - P2; B = BB.division_points(2)

flag = long_to_bytes(A[0][0]) + long_to_bytes(B[0][0])
print(flag.decode())
```

Let's run this in `sage`:
```console
$ sage sol.sage
FCSC{a0c43dbbfaac7a84b5ce7feb81d492431a69a214d768aa4383aabfd241}
```

## Python code
Complete solution in [sol.sage](./sol.sage)

## Flag
FCSC{a0c43dbbfaac7a84b5ce7feb81d492431a69a214d768aa4383aabfd241}
