# RÄKNEGOLF 
pwn
medium

## Beskrivning
* pwn/rev/shellcode

Haralds assistent, Torsten Tvehågsen, har hoppat av till motståndsrörelsen. För att bli bättre mottagen har han stulit med sig en konstig manick från Haralds lab, men han vet inte vad den gör. Harriet har undersökt den och tycker att det verkar vara en väldigt simpel spelkonsol för programmeringsövningar. Kanske kan du få konsolen att köra andra program än bara övningar? Det skulle kanske kunna ge Harriet nya uppslag på hur hon ska kunna hacka sig tillbaka till framtiden.

download: `download/raeknegolf`

## Köra binären 
`./download/raeknegolf`

## Servera och köra utmaningen lokalt över netcat
Notera! Detta startar och serverar en medvetet sårbar tjänst. Håll tungan rätt i mun och exponera ej mot internet.

```
docker build -t 'raeknegolf' .
docker run -p3000:3000 -d raeknegolf
nc localhost 3000
```
