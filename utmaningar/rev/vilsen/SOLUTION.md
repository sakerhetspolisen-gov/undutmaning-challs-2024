## Stegen i utmaningen
* Världen renderas på klientsidan, så koden är tillgänglig i webbläsaren.
* Deltagarna får även tillgång till server-koden (se files/server.tar.gz).
* Då man inte hittar någon flagga i koden, kan man inse att den måste finnas i
  det som servern skickar.
* Servern skickar kartan, samt spelarnas positioner.
* Flaggan finns i kartan: svamparnas positioner.

## Tips/ledtrådar
* Ibland när man kör fast kan det vara bra att anlägga ett
  helikopterperspektiv.

## Lösning
1. Leta upp funktionen _populateMap_ och sätt en stoppunkt där.
2. Skriv ut svamparnas koordinater i konsollen:
```
for (let m of e.filter(r=>r.objtype == 1)){
  console.log(m.x, m.z)
}
```
3. Spara koordinaterna i en local fil.
3. Gör ett diagram med svamparnas koordinater, så framgår flaggan.

## Flagga

`undut{episk_dunk}`
