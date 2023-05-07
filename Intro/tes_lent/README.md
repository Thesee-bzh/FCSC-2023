# Intro / T'es lent

## Challenge
Vous avez très envie de rejoindre l'organisation du FCSC 2024 et vos skills d'OSINT vous ont permis de trouver ce site en construction. Prouvez à l'équipe organisatrice que vous êtes un crack en trouvant un flag !

## Inputs
- website at https://tes-lent.france-cybersecurity-challenge.fr/


## Solution
Viewing the source code of the main page gives us a commented section with another page: `href="/stage-generateur-de-nom-de-challenges.html`

Heading to that page and viewing the source code gives us another comment:
```
Ne pas oublier d'ajouter cette annonce sur l'interface d'administration secrète : /admin-zithothiu8Yeng8iumeil5oFaeReezae.html
```

Heading to that hidden page gives us the flag.

## Flag
FCSC{237dc3b2389f224f5f94ee2d6e44abbeff0cb88852562b97291d8e171c69b9e5} 
