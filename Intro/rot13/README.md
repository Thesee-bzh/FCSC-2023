# Intro / ROT13

## Challenge
Un de vos collègues ne jure que par cette méthode de chiffrage révolutionnaire appelée rot13.

Il l'a utilisée pour dissimuler un flag dans ce texte. Démontrez-lui qu'il a tort de supposer que cet algorithme apporte une quelconque notion de confidentialité !

## Inputs
Encrypted text below:
```
GBQB yvfgr :
- Cnva (2 onthrggrf)
- Ynvg (1 yvger)
- Pbevnaqer (fhegbhg cnf, p'rfg cnf oba)
- 4 onanarf, 4 cbzzrf, 4 benatrf
- Cbhyrg (4 svyrgf qr cbhyrg)
- 1 synt : SPFP{rq24p7sq86p2s0515366}
- Câgrf (1xt)
- Evm (fnp qr 18xt)
- Abheve zba qvabfnher
```

## Solution
Throwing this into `CyberChef` and bake `ROT13` with default settings gives us the decrypted text and the flag:
```
TODO liste :
- Pain (2 baguettes)
- Lait (1 litre)
- Coriandre (surtout pas, c'est pas bon)
- 4 bananes, 4 pommes, 4 oranges
- Poulet (4 filets de poulet)
- 1 flag : FCSC{ed24c7fd86c2f0515366}
- Pâtes (1kg)
- Riz (sac de 18kg)
- Nourir mon dinosaure
```

## Flag
FCSC{ed24c7fd86c2f0515366}
