# Heist

Misc
Enkel

## Publik beskrivning

Du har fått hjälp av motståndsrörelsen och lyckats smyga in i ett av Haralds tillhåll.

Framför dig ligger en låda, och din hjälpreda Styrbjörn Sidekick har hört talas om de här enheterna.

Han berättar att de ofta innehåller värdefull information som användaren vill skydda. Men det ska vara bristfälliga skyddsmekanismer. Dock ofta under tidspress.

Ni hör hur Haralds hejdukar är utanför. Det gäller att vara absolut tyst och det måste gå snabbt att hämta informationen.

Styrbjörn ger dig viktig information innan han smyger iväg för att avleda uppmärksamheten och köpa dig lite tid:

ENHETEN VISAR INTE USER INPUT

BACKSPACE FUNKAR INTE, MAN MÅSTE SKRIVA KORREKT FRÅN BÖRJAN

OM ENHETEN INTE HAR KONFIGURERATS HAR MAN FLER CHANSER, DOCK SKA DEN GE IFRÅN SIG ETT LARM

# Köra utmaningen

### Starting

```
Build:
podman build -t "time-ctf-container" .
Run:
podman run -it -d -p 3000:3000 time-ctf-container
``` 

GLHF

### Development
```
podman run --rm -it -e COLUMNS="$(tput cols)" -e LINES="$(tput lines)" --name linux-ctf -d -it linux-ctf-container:latest 
podman exec -it --user ctf linux-ctf /bin/bash
```
