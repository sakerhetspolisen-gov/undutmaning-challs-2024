# Haralds Filserver
pwn
medel

## Beskrivning
* pwn/rev/linux

Genom att ha lyckats gissa Kung Haralds wifi-lösenord har motsråndsrörelsens cyberkommando fått tillgång till hans hemmanätverk och därigenom hans privata filserver. Nu vill de äga upp även den. Tur att kommandots ledare, Procesia F. Sakkunnig, gått kursen i Allmän Universell Xploit Vetenskap. Kan du hjälpa henne att ta sig in i servern?

ingen download (blackbox)

HINT: För att denna utmaningen ska vara lösbar serverar vi utmaningen med en pipe från `cat`, e.g. `cat|./chall.elf`

## Köra binären 
`./run/allmant_underligt_extraordinart_verktyg`

## Servera och köra utmaningen lokalt över netcat
Notera! Detta startar och serverar en medvetet sårbar tjänst. Håll tungan rätt i mun och exponera ej mot internet.

```
docker build -t 'haralds_filserver' .
docker run -p3001:3001 -d haralds_filserver
nc localhost 3001
```
