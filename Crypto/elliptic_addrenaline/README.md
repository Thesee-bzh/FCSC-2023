# Crypto / Elliptic Addrenaline

## Challenge
Vous devez à nouveau retrouver le flag caché dans les coordonnées des points donnés.

## Inputs
- SAGE script: [elliptic-addrenaline.sage](./elliptic-addvrenaline.sage)
- output:  [output.txt](./output.txt)

## Solution
It's the same thing as for the previous challenge, except the curve is different:

```python
p = 2**255 - 19
a = 19298681539552699237261830834781317975544997444273427339909597334573241639236
b = 55751746669818908907645289078257140818241103727901012315294400837956729358436
```

Here's the given coordinates for (A+B) and (A-B)
```python
A + B = (36383477447355227427363222958872178861271407378911499344076860614964920782192 : 26621351750863883655273158873320913584591963316330338897549941610801666281894 : 1)
A - B = (35017143636654127615837925410012912090234292410137109973033835965781971515338 : 55888666729705323990488128732989325970476008697224551268788692630541877244410 : 1)
```

Only difference with the previous challenge is that `sagemath` function `division_points()` returns two points for A and for B (reminder: it solves `mQ = P` given `(m, P)`).

So we just have to check both points for A and B. It turns out that the correct solution is the 2nd point returned for A and the first point returned for B.

Here's the code:
```python
from Crypto.Util.number import bytes_to_long

p = 2**255 - 19
a = 19298681539552699237261830834781317975544997444273427339909597334573241639236
b = 55751746669818908907645289078257140818241103727901012315294400837956729358436

K = GF(p)
E = EllipticCurve([K(a), K(b)])

# P1 = A + B; P2 = A - B
P1 = E(36383477447355227427363222958872178861271407378911499344076860614964920782192, 26621351750863883655273158873320913584591963316330338897549941610801666281894)
P2 = E(35017143636654127615837925410012912090234292410137109973033835965781971515338, 55888666729705323990488128732989325970476008697224551268788692630541877244410)

# 2A = P1+P2; 2B = P1-P2
AA = P1 + P2; A = AA.division_points(2)
BB = P1 - P2; B = BB.division_points(2)

print(long_to_bytes(A[0][0]), long_to_bytes(A[1][0]))
print(long_to_bytes(B[0][0]), long_to_bytes(B[1][0]))

flag = long_to_bytes(A[1][0]) + long_to_bytes(B[0][0])
print(flag.decode())
```

Let's run this in `sage`:
```console
$ sage sol.sage
b'=st*\xf3nB\xdf\x8aj{\xdfd\x8f\xb7*`~\x1f\x9b\xd0\x17\xa5i\xdd26\x82\xb1\xc9\xba\xc6' b'FCSC{1f0b8b8d4ff304004126f245ee5'
b'f46d8961b60dff4b187ef6fe4f09e34}' b"px$\xfd$\xe8Q\xce\xcb\x08'4\x0e'\x95$\xfeP\xf5\x0e\xe9\x82R\xd0t\x89\x1c\xdf\xe7~\xeel"
FCSC{1f0b8b8d4ff304004126f245ee5f46d8961b60dff4b187ef6fe4f09e34}
```

## Python code
Complete solution in [sol.sage](./sol.sage)

## Flag
FCSC{1f0b8b8d4ff304004126f245ee5f46d8961b60dff4b187ef6fe4f09e34}
