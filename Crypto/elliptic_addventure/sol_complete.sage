from binascii import unhexlify

def bytes_to_long(x):
    return int.from_bytes(x)

def long_to_bytes(val):
    # one (1) hex digit per four (4) bits
    width = len(bin(a)[2:])

    # unhexlify wants an even multiple of eight (8) bits, but we don't
    # want more digits than we need (hence the ternary-ish 'or')
    width += 8 - ((width % 8) or 8)

    # format width specifier: four (4) bits per hex digit
    fmt = '%%0%dx' % (width // 4)

    # prepend zero (0) to the width, to zero-pad the output
    return unhexlify(fmt % val)

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
